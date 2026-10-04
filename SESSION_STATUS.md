# Intro Data Science project status and handoff

This file is a handoff for a new coding session. It describes the two related
repositories, the decisions already made, and the conventions to preserve.

The dated updates below are snapshots, not a live status feed. Read the latest
update first; it supersedes earlier status statements where they differ. Check
the repositories directly before acting because branch and worktree state can
change after this file is updated.

## Project purpose and repository boundaries

The project is an introductory data-science book for STAT 3255/5255 at UConn.
The canonical book is instructor-authored and semester-independent.  A separate
semester repository contains class-specific material and student contributions.
Do not duplicate substantial instructor exposition in the semester repository.

- Book: <https://github.com/statds/ids-book>
- Fall 2026 notes: <https://github.com/statds/ids-f26>
- Reusable homework starter: <https://github.com/statds/hw-template>

The working directory is `/home/junyan/work/teaching/ids-book`.  In this
checkout, `ids-f26` is a symlink to
`/home/junyan/work/teaching/ids-f26/ids-f26`; `ids-f25` and `ids-s26` are other
semester/research links.  These symlinks are intentionally untracked.

## `ids-book`

Important source files include `index.qmd`, `01-intro.qmd`, `02-git.qmd`,
`03-quarto.qmd`, `_quarto.yml`, `Makefile`, `requirements.txt`,
`references.bib`, `apa.csl`, `README.md`, `PLAN.md`, `codex.md`,
`COPYRIGHT.md`, and `LICENSE`.

The book is licensed CC BY-NC 4.0 for its original written and visual content,
unless a source says otherwise.  Source code, data, and third-party material
can have separate terms.

### Writing and teaching style

- Give every paragraph a strong, representative topic sentence.
- Avoid fragmented or unnecessarily short paragraphs.
- Begin sentences with words, not symbols, variables, function names, or code.
- Edit prose in place and preserve existing line wrapping unless a changed
  sentence requires different wrapping, so diffs show only substantive changes.
- Preserve concrete, specific user tips; do not replace them with vague
  recommendations or omit useful original links.
- Support factual claims with citations. Use Google-Scholar-style BibTeX keys:
  lowercase author name, publication year, and first significant title word;
  use `nd` for undated sources. Chapter-level references use
  `## References {.unnumbered}`.
- Insert each new BibTeX entry in alphabetical key order and match the existing
  field formatting, so `references.bib` remains sorted and consistent.
- Explain basic computer literacy explicitly: Downloads, files, folders,
  paths, and command-line navigation matter for portability and literacy.
- On Windows recommend Git Bash (or Cygwin/WSL), whose commands match macOS and
  Linux.  PowerShell has a different, awkward command vocabulary and is not the
  shell used for course examples (except for software-installation guidance).
- Explain absolute versus relative paths and reproducibility.  Recommend short,
  readable, lowercase names without spaces or punctuation that requires shell
  quoting.  Explain why locations such as `Program Files` are inconvenient in
  shell-based, portable workflows.

### Chapters currently in the book

**Chapter 1, Introduction.**  Computing foundations cover operating systems,
files and paths, the command line, and Python.  The tools section introduces
Git and Quarto, including installation.  Git Bash and tab completion are
recommended.  The minimal `hello.qmd` example is deliberately Markdown-only:
headings, paragraphs, emphasis, lists, and a link, followed by
`quarto render hello.qmd`; it does not contain code chunks.  Exercises are
large numbered problems with subquestions, all answered in one `.qmd` file.

**Chapter 2, Project Management.**  The chapter teaches a practical Git
sequence: fork/clone, configure and inspect remotes, pull safely, branch, edit,
review diffs, stage named files, commit, push, open/revise a pull request,
review, and resolve conflicts.  It explicitly warns beginners that `git add .`
can stage unintended files.  Students should track source/docs/small example
data and environment specifications, but not credentials, private data, huge
raw data, generated output, caches, virtual environments, or `_book`.  Commit
messages should be short, informative, imperative, and describe one logical
change.  Evidence in the homework `.qmd` should include links, branch name,
commit hashes/messages, and concise command results—not an unfiltered terminal
transcript.

**Chapter 3, Reproducible Data Science.**  It introduces Quarto Markdown,
properly punctuated and dynamically numbered equations, citations and
cross-references, tables, executable Python chunks, and captioned/numbered
figures.  Line diagrams should be vector graphics (SVG/PDF); raster graphics
are appropriate for photographs or inherently pixel-based images.  It explains
why the software environment matters and uses Python 3.12 virtual environments.
It also explains why Excel, Word, and PowerPoint are office tools rather than
the primary authoring system for data science: opaque diffs, weak automation,
manual synchronization, limited provenance, and poor reproducibility.  Git and
Quarto provide reviewable history, executable documents, generated tables and
figures, and polished homework that students can reuse professionally—not just
for this course.

Chapter 3 exercises cover Python 3.12 environment setup, Markdown syntax
(equation/table/figure/citation/reference), executable Python with generated
results, and reproducibility/collaboration readiness.  Students check unresolved
references by rendering, searching the log for warnings/undefined references,
and checking the rendered document for `??` and missing labels or bibliography
entries.

The chapter exercises are problems only.  They do not prescribe how homework
is collected or require students to render/print; those mechanics belong in the
semester-specific repository.  The single starter at `statds/hw-template` is
the intended template, not one repository per assignment.

## `ids-f26` (Fall 2026)

This repository contains the Fall 2026 syllabus, schedule, student-contributed
class notes, presentations, roster, and semester-specific instructions.  Its
`codex.md` and `PLAN.md` distinguish it from the canonical book.  Students add
worked examples, explanations, Python demonstrations, visualizations, debugging
notes, extensions, and useful links through topic branches and pull requests.

The LMS enrollment file currently has 25 students, and `roster.txt` plus the
wishlist in `index.qmd` were synchronized in commit `524ec4d`.  Broken UConn
Library links were corrected in commit `275ae90`.

### Current Fall 2026 working-tree state

At the time this handoff was written, the external repository has these relevant
uncommitted changes:

- `.gitignore` ignores LaTeX auxiliary files and generated `/syllabus.pdf` and
  `/syllabus.tex`; keep `syllabus-f26.tex` as the source.
- `syllabus-f26.tex` has tagged PDF metadata (`lang`, title, author, subject),
  corrected Library URLs, and the original visual layout/margins/list settings
  restored at the user’s request.  It compiles to a three-page PDF.  The PDF is
  tagged, but the reported accessibility score is about 49%; improving it to
  80% may require layout tradeoffs, especially around columns and lists.
- `lms.csv` and `syllabus-f26.pdf` are currently untracked.  Numerous LaTeX
  build products may also be present; do not accidentally add them.

Do not alter or commit these files without checking the user’s intended grouping.

## Build and environment conventions

Use Python **3.12**.  The Makefile checks the selected interpreter’s major and
minor version, creates/checks the virtual environment, installs requirements,
and checks Quarto.  It supports a user’s already-active environment and detects
`uv` when available; students are not required to use `uv`.  The environment
directory used in this project is `.ids` (and must be ignored), not a committed
artifact.  `make check-tools` validates Python and Quarto; `make install` must
not silently use a different default Python (for example, Python 3.14 on macOS).

Useful checks:

```bash
git status --short
make check-tools
quarto render
```

Render into a temporary directory when testing if you want to avoid touching
generated `_book`; never edit `_book` directly.  Expected generated directories
and caches are ignored.

## Git and handoff rules

Follow the commit style in `README.md`: `type: concise imperative summary`, no
period, at most 72 characters.  Types include `content`, `feat`, `fix`,
`build`, `style`, `refactor`, `docs`, and `chore`.  Group related changes into
sensible commits, inspect `git diff` before staging, and use explicit
`git add path/to/file` for beginners’ instructions.

Before making edits in a new session, inspect both repositories:

```bash
cd /home/junyan/work/teaching/ids-book
git status --short
git log -5 --oneline
git -C ids-f26 status --short
git -C ids-f26 log -5 --oneline
```

Read `codex.md` in the repository being changed before modifying content.  Keep
semester-specific changes in `ids-f26`; keep reusable exposition and chapter
exercises in `ids-book`.  Ask before making a materially different design
choice, and do not overwrite user edits or generated output.

## Latest session update (2026-09-16)

### User writing preferences confirmed

- The book is written for general readers, including college students and
  advanced high-school readers; do not address readers as students entering
  “this course” or assume a particular class.
- Keep language accessible while preserving precise technical definitions.
- Give every paragraph a strong topic sentence.
- Do not begin a sentence with a symbol, variable, function name, or code.
- Edit prose in place and preserve existing line wrapping unless a changed
  sentence requires different wrapping; avoid noisy rewrapping in diffs.
- Do not impose an arbitrary limit of four exercise subquestions. Preserve the
  complete sequence of requested subquestions when adapting older material.
- Use the exact name **Game 24**, and preserve the definitions of `\(\square\)`
  as a card value and `\(\bigcirc\)` as an operation when describing it.
- Preserve user-provided references and detailed descriptions when revising
  exercises; improve clarity without silently dropping material.

### ids-book latest state

Commits through the latest completed work include:

- `7530072 content: improve Quarto workflow guidance` (Chapter 3)
- `3711c75 content: clarify data science notation` (Chapter 1)
- `bc2f063 style: lead prose with words` (Chapters 2 and 4)
- `5a0a340 docs: simplify local build setup` (index)
- `8f541ef content: expand Python practice exercises` (Chapter 4 titles and
  Exercises 4.4–4.7)
- `ae1556f content: clarify Python ecosystem` (Chapter 4 definitions and the
  official Python import-system reference)

Chapter 4 is titled **Python Practice** and uses short section titles:
**Python Ecosystem**, **Imports**, **Functions**, **Names and Objects**, **Data
Structures**, **Number Representation**, **Simulation**, and **Debugging**.
Exercises 4.4–4.7 adapt the Fall 2025 Chapter 14 exercises: generalized Monty
Hall, Monte Carlo \(\pi\), the Google Billboard Ad search in the digits of \(e\),
and Game 24. Monty Hall retains all requested stages, including one-game
simulation, repeated simulation, both parameter settings, theoretical
comparison, and reproducibility. Game 24 uses brute force, not recursion, and
has a separate duplicate-removal subquestion.

The Chapter 3 Matplotlib example simulates 30 students in three subjects with
`numpy.random.default_rng(2026)`, then plots subject means with standard-error
bars. Section 3.6 explains why local rendering matters, assumes an activated
environment, clones the book, and makes the optional dedicated-environment path
explicit. It also encourages readers to inspect the Makefile and use AI to
explain targets, variables, and commands while checking the explanation against
the source.

`references.bib` was cleaned to remove the unused `python2026modules` entry,
alphabetize entries by key, and use consistent `urldate` fields for undated web
sources. Keys follow the Google-Scholar-style pattern: lowercase author name,
year (or `nd`), and first significant title word. The source bibliography
cleanup is currently uncommitted if `git status` reports it as modified.

The complete book has rendered successfully to `_book/index.html` after the
latest Chapter 4 and bibliography changes.

### ids-f26 latest design and working state

Student presentations have two distinct categories:

1. Topic presentations live under `topic/<last-name-topic>/index.qmd` and are
   linked from the relevant topical chapter.
2. Final-project presentations live under `final/<project-name>/index.qmd` and
   are linked from the dedicated `chapters/final-project-presentations.qmd`
   chapter.

The former `presentations/` source tree was reorganized accordingly. The former
example now lives at `topic/example-quarto-presentations/index.qmd`. The
repository-level `_quarto-presentations.yml` profile renders both trees into
`_book/topic/` and `_book/final/`; the Makefile's `presentations` target and
`render-one` target use that profile. `render-one` accepts paths such as
`topic/last-name-topic/index.qmd` or `final/project-name/index.qmd`.

The Fall 2026 book configuration includes the new final-project chapter. The
main index and README describe the two source trees, link the example topic
presentation, and explain where final-project links belong. A complete
`make render` from the real repository directory
`/home/junyan/work/teaching/ids-f26/ids-f26` successfully rendered the notes and
the topic example. The `final/` tree currently contains no student decks.

The ids-f26 reorganization and presentation examples are committed in the
focused commits listed in the latest session update below. Do not add the
unrelated untracked `lms.csv` or `syllabus-f26.pdf` files.

The `ids-f26` symlink in the ids-book checkout points to the real repository;
some editing tools require the real path for nested files:
`/home/junyan/work/teaching/ids-f26/ids-f26`.

## Latest session update (2026-09-21)

### ids-book status

The bibliography cleanup is now committed as `bb5f942 chore: alphabetize
bibliography entries`. The only untracked items in this checkout are the
session handoff file and the intentionally untracked semester/research
symlinks: `SESSION_CONTEXT.md`, `ids-f25`, `ids-f26`, and `ids-s26`.

### ids-f26 completed changes

The presentation reorganization and examples are committed in focused batches:

- `d4b176a refactor: split topic and final presentations`
- `cff24ea docs: explain presentation contribution workflow`
- `10aaa27 content: add presentation examples`
- `39b46c8 docs: clarify fork synchronization`

Later documentation and content commits are:

- `5c9322c docs: require assignment development history`
- `f3ac4f9 docs: streamline assignment workflow`
- `21a55f5 docs: link contribution guide`
- `0c4e89b docs: explain topic branch creation`
- `ea00886 docs: explain contribution commands`
- `87dd342 fix: refresh presentation roster`
- `2369535 docs: add presentation evaluation rubrics`

The public class notes now link to `CONTRIBUTING.md` and explain topic and
final-project presentation contributions, branch creation, Git commands,
pull-request review, maintainer acceptance, fork synchronization, and branch
cleanup. The assignment section links to the canonical book's Git workflow and
retains only Fall 2026-specific policy, including at least ten meaningful
commits for every assignment and preservation of the complete history.

The class notes now include a 20-point topic-presentation rubric: approval and
preview (4 points), oral presentation (10 points), and pull request and
revision (6 points). They also include a peer-evaluation rubric for final
presentations. Each student evaluates every other presenter on domain, methods,
and presentation using a 5--1 scale, with evidence-based comments and anchors
for each score.

The roster was reduced to 22 presenters after removing three names. The
presentation-order code reads `roster.txt` dynamically, uses the current class
seed, and has document-level `execute: freeze: false` metadata so future roster
changes invalidate the cached result. A fresh book render confirmed 22 names.

At that historical point, the complete Fall 2026 book and all presentation
trees rendered successfully with `make render`. The worktree status has since
changed; see the 2026-09-27 update below for the current state.

The current Fall 2026 branch is not clean: inspect the worktree before making
changes, and do not add the untracked administrative or environment files
without checking the user's intended grouping.

## Latest session update (2026-09-27)

### ids-book status

The latest committed ids-book change is `388993b content: enhance Python
practice chapter`. The checkout contains the intentionally untracked session
handoff file, notebook, and semester/research symlinks:
`SESSION_CONTEXT.md`, `Untitled.ipynb`, `ids-f25`, `ids-f26`, and `ids-s26`.

### ids-f26 presentation changes

The relevant presentation commits are:

- `0199953 build: fix presentation project output paths`
- `7b0fe8c content: split presentation examples`

The presentation builds no longer use nested `topic/_quarto.yml` or
`final/_quarto.yml` projects. `_quarto-presentations.yml` defines a
repository-level `presentations` profile, and the Makefile uses it for both
`make presentations` and `make render-one`. This removes Quarto warnings caused
by output directories configured outside a nested project.

The example material is split into two topic decks:

1. `topic/example-quarto-presentations/index.qmd` explains Quarto, RevealJS,
   executable Python, figures, and the presentation workflow.
2. `topic/presentation-skills/index.qmd` covers storytelling, visual design,
   delivery, practice review, and evidence-proportionate claims.

Both decks use a 1280-by-720 RevealJS canvas for a 16:9 display. The duplicate
title slide was removed from the presentation-skills deck. The malformed
literal Jupyter cell-output example was removed; the executable Python slide
now displays the actual code and result. The two decks are linked from
`index.qmd` and `chapters/data-wrangling-visualization.qmd`.

The repository ignores Quarto-generated `index_files/` directories through
`.gitignore`. Both decks have rendered successfully with:

```bash
make render-one FILE=topic/example-quarto-presentations/index.qmd
make render-one FILE=topic/presentation-skills/index.qmd
```

The current `ids-f26` worktree has these untracked items; do not add them
without checking the user's intent:

- `.ids`, a symlink to the ids-book environment;
- `lms.csv`, semester administration data;
- `references.bib`, a local bibliography file; and
- `syllabus-f26.pdf`, generated syllabus output.

The current branch also contains later student contributions and merges after
the presentation work, including commits `10dc5cc`, `07f17f8`, `0e66806`,
`1284f8b`, and `1826e9d`. Inspect the latest status and log before editing or
committing further changes.

## Latest session update (2026-09-30)

### VDS references and book positioning

The closest related book discussed with the user is *Veridical Data Science*
by Bin Yu and Rebecca L. Barter (2024). Keep these links in view:

- Open-access book: <https://vdsbook.com/>
- MIT Press edition: <https://mitpress.mit.edu/9780262049191/veridical-data-science/>

The book is cited as `@yu2024veridical` in `references.bib`. Chapter 1 now has
the section **This Book's Emphasis**, which positions this text as an
implementation-focused introduction with four computing foundations chapters,
a sustained NYC 311 example, and explicit problem-to-data/data-to-question
reasoning. It distinguishes this scope from VDS's PCS framework and cites VDS.
The Introduction also cites VDS when describing the nonlinear data-science
life cycle. Chapter 5 cites VDS while discussing the data-to-question route;
Chapter 6 cites it on contextual, iterative data preparation.

The relevant ids-book commits are `78a6873 content: refine problem formulation
chapter`, `cdd01a4 content: link later chapters to problem formulation`, and
`a3c012e content: position book alongside VDS`. The Python dictionary
formatting update is committed as `58c08a9 style: compact Python dictionary
examples`. Chapter 1, Chapter 5, Chapter 6, and the full book rendered
successfully after the relevant updates. The user's latest ids-book status
reports that `main` was up to date with `origin/main` at that time; see the
2026-09-30 status snapshot below for the latest checked branch state.

### Homework workflow

Chapter 5 Exercises 5.1 and 5.2 are the recommended core homework; Exercise
5.3 is optional. Students download the linked NYC 311 archive into a local
`data/` folder in their homework clone and do not track either the archive or
the generated Feather data. The grader stages the source archive at the
expected path before rendering.

The homework template commit is `99770e4 Clarify local homework data
workflow`; it updates the README and ignores the source ZIP and derived
Feather file. The IDS-F26 reproducibility instructions are in
`cc6c0af docs: clarify homework reproducibility check`; students use the same
Python environment as the notes, submit `.qmd` source rather than PDF, and the
grader renders the source.

At the time of the 2026-09-30 check, `hw-template` was clean and up to date with
`origin/main`. The IDS-F26 repository was one commit ahead of `origin/main` and
had untracked local files; see the status snapshot below. Do not stage the
untracked session file, notebooks, semester symlinks, or
administrative/environment files unless the user explicitly asks. This
handoff file is untracked and should remain so unless the user asks to add it.

### Python example formatting

The user prefers compact formatting when a dictionary is the first argument
to a function call. Write `pd.Series({` or `pd.DataFrame({` on one line,
indent dictionary entries one level, and close with `})` (or include a short
keyword argument on that closing line) when readable. Do not put the opening
`{` on a separate line merely to apply a hanging indent. Keep standalone
dictionaries and nested structures expanded when that improves clarity. This
formatting was applied to matching examples in Chapters 4–6 and the full book
render passed. These formatting edits are committed in `58c08a9`.

### Repository status checked 2026-09-30

These are the branch and worktree states observed during the latest review.
Recheck before making changes because they can change independently of this
handoff.

- `ids-book`: `main` is one commit ahead of `origin/main` at `58c08a9`. The
  worktree also contains untracked local items, including this handoff file,
  notebooks, symlinks to related repositories, and `acadwriting.md`.
- `ids-f26`: `main` is one commit ahead of `origin/main` at `b464731`. Its
  untracked items are `.ids`, `lms.csv`, `references.bib`, and
  `syllabus-f26.pdf`; do not add them without checking the user's intent.
- `hw-template`: `main` is up to date with `origin/main` at `99770e4`, with a
  clean worktree.

These checks establish local tracking status only; they do not verify that
unpublished commits have been pushed to a remote other than `origin`.

## Latest session update (2026-10-04)

### Visualization and shared preparation

The visualization chapter now develops purpose, the grammar of graphics,
comparisons, common mistakes, static maps, and interactive maps. It uses the
NYPD illegal-parking request extract throughout, with a small simulated
distribution example. The chapter includes Plotnine facets, Matplotlib
comparisons, GeoPandas point and ZCTA maps, a Folium/Leaflet map, an optional
Google Maps example, and exercises that prepare students for an independent
midterm project. The prose follows `acadwriting.md` with integrated paragraphs,
explicit definitions, and qualified interpretations. The corresponding
references and pinned Python dependencies are in `references.bib` and
`requirements.txt`.

The compact `data/nyc_zcta_boundaries.geojson` contains the 221 NYC ZCTAs
used for the maps. Its source and simplification are documented in
`data/nyc_zcta_boundaries.md`; `scripts/build_zcta_boundaries.py` rebuilds it
from NYC Open Data. Chapters on exploration and visualization now call
`scripts/parking_requests.py` for their common screened request table. The
wrangling chapter remains the explanation of those transformations, and both
later chapters render independently.

Book prose now uses Quarto cross-references in place of hard-coded chapter
and numbered-object references. The Quarto teaching example no longer renders
duplicated labels such as “Figure Figure.” A full `quarto render` completed
all 11 book inputs on October 4, 2026. An audit of the rendered HTML found
38 Quarto cross-reference links and no broken destinations. The source scan
found no hard-coded numbered references in the book files. The Google Maps
example is intentionally not executed because it requires an API key.

### Commits and worktree

The work was committed in these stages:

- `d2511fb refactor: share parking request preparation across chapters`
- `6f014e0 content: develop visualization chapter with spatial examples`
- `a07f18a fix: replace hard-coded book references`
- `72b7360 build: ignore generated Quarto support files`

The four work commits leave `ids-book` on `main`, four commits ahead of
`origin/main`; this handoff commit makes it five ahead. The new ignore rules
cover root-level Quarto `*_files/` folders and `site_libs/`; `_book/` was already
ignored. Unrelated local notebooks, semester links, an archive, style notes,
and credential-named files remain untracked and must not be staged as book
content. This dated snapshot supersedes older book-status statements above;
inspect live status and log before the next edit. No linked semester
repository was changed during this work.
