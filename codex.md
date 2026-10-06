# Instructions for Codex

This repo `ids-book` is for classnotes of STAT 3255/5255, targeting
for a future book on Intro Data Science.

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
