# ids-book

Course notes for Introduction to Data Science, with ongoing development toward
a textbook.

Copyright © 2026 Jun Yan. Unless otherwise noted, the written and visual
content is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/);
see [COPYRIGHT.md](COPYRIGHT.md) before reusing the material.

## Shared Python Environment

Use Python 3.12 and one course environment for this book, the semester's
student-contributed notes, and coursework. Follow the
[book setup instructions](https://statds.github.io/ids-book/#building-the-book)
to create and activate the environment, then run these commands from
`ids-book`:

```sh
make install
make check-tools
```

The root `requirements.txt` is the single source for course package versions.
Keep `ids-book` and `ids-f26` side by side when cloning them:

```text
course-work/
├── ids-book/
└── ids-f26/
```

The semester's `requirements.txt` includes this file rather than maintaining
another package list. Activate the same environment when switching
repositories; do not create a separate environment inside `ids-f26`.

Propose new dependencies in `ids-book/requirements.txt` for instructor review.
After an approved change, activate the shared environment and run
`make install` from `ids-book` again. The `make req` target is for maintainers:
it overwrites the requirements file with the active environment's packages.

## Checking the Book

After rendering, run `make check-book`. It checks heading spacing in the
chapter sources and verifies headings, exercise numbering, citations,
figure alternative text, local files, and link anchors in the rendered HTML.
A successful Quarto render alone does not establish that these are correct.
For a source-only check, run `python scripts/check_book.py --source-only`
in the shared environment.

The book uses `freeze: auto`, so a whole-book render can reuse computations
from unchanged chapters. Render an individual chapter with
`make render-one FILE=chapter.qmd` to execute its code again. Check the
rendered page as well as the execution log. External URLs and visual layout
need separate review.

## Contributing

Make each commit a coherent change. Use an imperative, concise subject without
a trailing period, preferably no longer than 72 characters. Commit messages
follow this format:

```text
type: concise imperative summary
```

Use these types:

- `content`: add or revise book prose, examples, or exercises
- `feat`: add a structural or reader-facing capability
- `fix`: correct an error or broken behavior
- `build`: change Quarto, Python, dependency, or build configuration
- `style`: make formatting-only changes
- `refactor`: reorganize source without materially changing content
- `docs`: update repository documentation
- `chore`: perform repository maintenance

For example:

```text
content: add preliminary book chapter
build: configure Quarto book output
fix: correct Python environment instructions
```

Add a commit body when the motivation or a non-obvious decision needs further
explanation. Reference a related issue in the body when applicable.
