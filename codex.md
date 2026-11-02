# Instructions for Codex

This repo `ids-book` is for classnotes of STAT 3255/5255, targeting
for a future book on Intro Data Science.

Do not use 42 as a random seed in generated examples. Choose and document
a fixed seed for reproducibility; do not search for a seed to obtain a
desired result.

The past two semesters' notes are in linked folders `ids-f25` and `ids-s26`.

This semester I separate my parts from student-contributed part for the
first time. My plan is in PLAN.md.

## Writing skills

Install the WIT skills once on each computer. From the `ids-book` root, run
the installer in the neighboring `wit-skills` clone. The first command shows
the destinations without writing files; the second installs or updates the
skills in `~/.codex/skills`:

```sh
python ../wit-skills/installers/codex/install.py
python ../wit-skills/installers/codex/install.py --apply
```

After installation, start a new Codex session. For work on this book,
activate both `$technical-writing` and `$book-writing`; repository guidance
also asks Codex to load both at the start of each book-content task. The
technical skill covers shared academic and revision conventions. The book
skill covers chapter structure, explanations, examples, code, and exercises.
If the skills are not available to Codex, read their `SKILL.md` files from
`~/.codex/skills/` or the neighboring `wit-skills` clone. Skills can be
invoked again if a long session no longer has their instructions in context.

## Quarto structure and verification

Preserve blank lines before headings. Quarto uses Pandoc Markdown, whose
[heading rules](https://pandoc.org/MANUAL.html#extension-blank_before_header)
require that separation from a preceding paragraph. A heading that looks
correct in the source can otherwise render as ordinary text without an error.
Preserve code fences, div boundaries, and list indentation when editing layout.

After rendering changed chapters, run `make check-book` and inspect the
affected headings, exercise numbers, tables, and figures in the rendered
pages. Do not treat a successful render command as sufficient verification.

Use quoted YAML strings with escaped line continuations for multiline
`fig-alt` cell options. A minimal test with the current Quarto/Jupyter
pipeline showed that folded strings can corrupt image attributes. Verify
figure IDs and captions along with alternative text in the rendered HTML.
