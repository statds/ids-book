"""Check Quarto source structure and the corresponding rendered book pages."""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


def walk(value):
    """Yield dictionaries from a Pandoc syntax tree."""
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def check_spacing(source, text):
    """Catch headings absorbed into paragraphs, excluding fenced examples."""
    errors = []
    lines = text.splitlines()
    fence = None
    for index, line in enumerate(lines):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            run, rest = marker.groups()
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence) and not rest.strip():
                fence = None
            continue
        if fence or not re.match(r"^#{1,6} ", line) or index == 0:
            continue
        previous = lines[index - 1]
        opens_div = re.match(r"^\s*:{3,}\s+\S", previous)
        if previous.strip() and not opens_div:
            errors.append(f"{source}:{index + 1}: missing blank before heading")
    if fence:
        errors.append(f"{source}: unclosed code fence")
    return errors


def parsed_structure(text):
    """Parse headings while treating executable Quarto cells as code blocks."""
    markdown = re.sub(
        r"^(`{3,})\{(python|r|julia|ojs|mermaid|dot)\}\s*$",
        r"\1{.\2 .audit-executable}", text,
        flags=re.MULTILINE,
    )
    result = subprocess.run(
        ["quarto", "pandoc", "-f", "markdown", "-t", "json"],
        input=markdown, text=True, capture_output=True, check=True,
    )
    tree = json.loads(result.stdout)
    headers = [node["c"] for node in walk(tree) if node.get("t") == "Header"]
    figures = []
    for node in walk(tree):
        if node.get("t") == "CodeBlock" and "audit-executable" in node["c"][0][1]:
            figures.extend(re.findall(
                r"^#\| label:\s*(fig-[\w-]+)", node["c"][1], re.MULTILINE
            ))
        elif node.get("t") in ("Div", "Image"):
            identifier = node["c"][0][0]
            if identifier.startswith("fig-"):
                figures.append(identifier)
    return headers, figures


def chapter_files(items):
    """Collect chapter paths, including chapters nested inside book parts."""
    for item in items:
        if isinstance(item, str) and item.endswith(".qmd"):
            yield Path(item)
        elif isinstance(item, dict):
            if "href" in item:
                yield from chapter_files([item["href"]])
            yield from chapter_files(item.get("chapters", []))


def inspect_page(source, text, soup, output):
    """Check headings, numbered exercises, citations, and figure resources."""
    errors = []
    identifiers = Counter(node["id"] for node in soup.find_all(id=True))
    for identifier, count in identifiers.items():
        if count > 1:
            errors.append(f"{source}: duplicate HTML identifier {identifier}")
    headers, figure_ids = parsed_structure(text)
    callouts = soup.select(".callout-title-container")
    for _, attributes, content in headers:
        identifier = attributes[0]
        if not identifier or identifier in identifiers:
            continue
        title = " ".join(
            node["c"] for node in walk(content) if node.get("t") == "Str"
        )
        # Quarto converts callout headings into accessible title containers.
        if not any(node.get_text(" ", strip=True).endswith(title) for node in callouts):
            errors.append(f"{source}: heading missing from HTML: {identifier}")
    main = soup.find("main") or soup
    for paragraph in main.find_all("p"):
        if re.search(r"(^|\s)#{2,6}\s+\S", paragraph.get_text()):
            errors.append(f"{source}: literal heading markup inside a paragraph")
    for node in main.select(".quarto-unresolved-ref,.cell-output-error"):
        errors.append(f"{source}: unresolved reference or code error: {node.get_text()[:100]}")
    for citation in main.select("[data-cites]"):
        for key in citation["data-cites"].split():
            if not soup.find(id="ref-" + key):
                errors.append(f"{source}: unresolved citation {key}")
    exercises = re.findall(r"\{#(exr-[\w-]+)", text)
    chapter_number = soup.select_one("h1 .chapter-number")
    chapter = chapter_number.get_text(strip=True) if chapter_number else None
    for number, identifier in enumerate(exercises, start=1):
        exercise = soup.find(id=identifier)
        title = exercise.select_one(".theorem-title") if exercise else None
        if title is None:
            errors.append(f"{source}: missing or unnumbered exercise {identifier}")
        elif chapter and title.get_text(strip=True) != f"{chapter}.{number}":
            errors.append(f"{source}: incorrect exercise number for {identifier}")
    if exercises:
        section = soup.find(id="exercises")
        title = section.find("h2") if section else None
        if title is None or title.get_text(strip=True) != "Exercises":
            errors.append(f"{source}: missing unnumbered Exercises heading")
    for identifier in figure_ids:
        figure = soup.find(id=identifier)
        if figure is None or figure.find("figcaption") is None:
            errors.append(f"{source}: figure identifier or caption missing: {identifier}")
    images = main.find_all("img")
    for image in images:
        reference = image.get("src") or image.get("data-src", "")
        if not image.get("alt"):
            errors.append(f"{source}: figure missing alternative text: {reference}")
        parsed = urlsplit(reference)
        if reference and not parsed.scheme:
            if not (output.parent / unquote(parsed.path)).is_file():
                errors.append(f"{source}: missing image file {reference}")
    for resource in soup.select("script[src],link[href]"):
        reference = resource.get("src") or resource.get("href", "")
        parsed = urlsplit(reference)
        if reference and not parsed.scheme and not parsed.netloc:
            if not (output.parent / unquote(parsed.path)).is_file():
                errors.append(f"{source}: missing stylesheet or script {reference}")
    return errors, (len(headers), len(exercises), len(images))


def check_links(pages):
    """Check local links and HTML anchors; external URLs require separate review."""
    errors = []
    for output, soup in list(pages.items()):
        for link in soup.find_all("a", href=True):
            reference = link["href"]
            parsed = urlsplit(reference)
            if parsed.scheme or parsed.netloc or parsed.path.startswith("/"):
                continue
            if not parsed.path and not parsed.fragment:
                continue
            target = (output.parent / unquote(parsed.path)).resolve()
            if not parsed.path:
                target = output
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                errors.append(f"{output.name}: broken local link {reference}")
                continue
            if parsed.fragment and target.suffix == ".html":
                if target not in pages:
                    pages[target] = BeautifulSoup(target.read_text(), "html.parser")
                if not pages[target].find(id=unquote(parsed.fragment)):
                    errors.append(f"{output.name}: broken local anchor {reference}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-only", action="store_true")
    args = parser.parse_args()
    result = subprocess.run(
        ["quarto", "inspect", str(ROOT)], check=True, capture_output=True, text=True,
    )
    config = json.loads(result.stdout)["config"]
    chapters = list(chapter_files(config["book"]["chapters"]))
    output_dir = ROOT / config["project"].get("output-dir", "_book")
    errors, pages = [], {}
    totals = [0, 0, 0]
    for source in chapters:
        path = ROOT / source
        if not path.is_file():
            errors.append(f"{source}: chapter source missing")
            continue
        text = path.read_text()
        errors.extend(check_spacing(source, text))
        if args.source_only:
            continue
        output = (output_dir / source.with_suffix(".html")).resolve()
        if not output.is_file():
            errors.append(f"{source}: render the chapter before checking its HTML")
            continue
        soup = BeautifulSoup(output.read_text(), "html.parser")
        pages[output] = soup
        found, counts = inspect_page(source, text, soup, output)
        errors.extend(found)
        totals = [a + b for a, b in zip(totals, counts)]
    if not args.source_only:
        errors.extend(check_links(pages))
    if errors:
        print("Book checks failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"Checked {len(chapters)} chapter sources.")
    if not args.source_only:
        print(f"Verified {totals[0]} headings, {totals[1]} exercises, and {totals[2]} figures.")
        print("Local links, anchors, citations, and figure resources passed.")


if __name__ == "__main__":
    main()
