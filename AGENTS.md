# Repository guidance

## Scope and project boundaries

- This repository is the semester-independent, instructor-authored book for
  introductory data science. Keep semester-specific policies, schedules,
  student work, and course administration in the appropriate semester
  repository (for example, `ids-f26`). Avoid duplicating substantial book
  exposition there.
- Before editing, read `codex.md` and inspect `git status --short` and
  `git log -5 --oneline`. If work touches a linked repository, inspect its
  status and read its local instructions before editing it.
- `SESSION_STATUS.md` contains project background and dated handoff snapshots.
  Use its newest update for context, but verify live branch and worktree state
  directly before acting.
- Do not stage, commit, or overwrite user files unless the user asks. Review
  `git diff` before staging, and stage named paths rather than using `git add .`.

## Editing the book

- At the start of each task involving book content, load both the installed
  `technical-writing` and `book-writing` skills. If Codex does not offer them
  as skills, read their `SKILL.md` files from `~/.codex/skills/` or the
  neighboring `wit-skills` clone.
- Write for general readers, including college and advanced high-school
  readers. Keep explanations accessible and technically precise.
- Give each paragraph a clear topic sentence. Start sentences with words,
  rather than symbols, variables, function names, or code. Preserve useful
  specifics, examples, and links when revising.
- Edit prose in place and preserve existing line wrapping unless a substantive
  edit requires a change. Keep diffs focused.
- Support factual claims with citations. Follow the existing BibTeX format
  and alphabetical key order; keys use lowercase author, year (or `nd`), and
  the first significant title word. Chapter reference sections use
  `## References {.unnumbered}`.
- Use Python 3.12 for the book environment and follow the existing Quarto and
  Makefile workflows. Keep generated output, caches, virtual environments,
  credentials, private data, and large raw data out of version control.
- Respect `COPYRIGHT.md`, `LICENSE`, and any source-specific terms when
  adding or reusing material.

## Verification and commits

- Do not run tests or builds unless the user asks for verification or the task
  requires it. When verification is requested, use the repository's existing
  checks and avoid editing generated `_book` output.
- Make each commit a coherent change. Follow `README.md`: use
  `type: concise imperative summary`, with no trailing period and preferably
  no more than 72 characters. Do not commit unless asked.
