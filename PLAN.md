# IDS Course Notes Repository Plan

## Objective

Split the IDS course materials into two distinct note systems so that
the instructor-authored material can be tightly controlled and developed
into a future book, while students can collaboratively build a separate
set of crowd-sourced notes.

## 1. Instructor Notes: `ids-book`

`ids-book` is the canonical, instructor-controlled source for the course
content.

### Purpose

-   Serve as the authoritative course notes for Introduction to Data
    Science.
-   Maintain consistent organization, exposition, notation, examples,
    exercises, and references.
-   Remain semester-independent where practical.
-   Be extensible into a future textbook/book project.
-   Avoid mixing student contributions or semester-specific
    administrative material into the core manuscript.

### Technology

-   Quarto book.
-   Python-based examples and computation.
-   Git/GitHub for version control.

### GitHub setup

Suggested repository description:

> Course notes for Introduction to Data Science, with ongoing
> development toward a textbook.

Use the GitHub **Python** `.gitignore` template.

Add Quarto/Jupyter generated files as appropriate:

``` gitignore
# Quarto
_book/
.quarto/

# Jupyter
.ipynb_checkpoints/
```

Commit reproducibility/environment specifications such as
`requirements.txt`, `environment.yml`, `pyproject.toml`, or relevant
lock files rather than ignoring them.

### License

For now, use **no open-source license**. This retains full copyright
while the manuscript is being developed and preserves flexibility for a
future book/publisher arrangement.

A Creative Commons license such as CC BY-NC 4.0 can be considered later
if the material is intentionally released for reuse.

## 2. Student Collaborative Notes: `ids-f26`

Keep the Fall 2026 collaborative notes separate from `ids-book`.

### Purpose

The collaborative notes should supplement, rather than replace or
modify, the instructor notes. They provide students with practice in
explaining data-science concepts and using a real collaborative
Git/GitHub workflow.

Possible student contributions include:

-   worked examples;
-   alternative explanations;
-   Python demonstrations;
-   visualizations;
-   common mistakes and debugging notes;
-   extensions and applications;
-   summaries of useful class discussions;
-   useful external resources with appropriate attribution.

### Contribution workflow

Prefer a structured GitHub workflow rather than unrestricted wiki-style
editing:

``` text
topic/issue
    -> branch
    -> commits
    -> pull request
    -> review
    -> revision
    -> merge
```

This makes Git/GitHub collaboration itself part of the learning
experience.

A student contribution should generally contain:

1.  **What** --- concise explanation of the concept.
2.  **Example** --- preferably an executable demonstration.
3.  **Interpretation** --- explanation of what the output/result means.
4.  **Takeaway** --- one or two key conclusions.
5.  **Sources** --- citations/links when external material is used.

The collaborative notes should link to relevant sections of `ids-book`
rather than duplicate the instructor-authored exposition.

## 3. Assignments: Classroom 50

Keep graded assignments separate from both sets of notes.

Use Classroom 50 repositories for individual or team assignments,
including assignments based on exercises appearing in `ids-book`.

Conceptually:

``` text
                         IDS course
                             |
          +------------------+------------------+
          |                  |                  |
       ids-book            ids-f26          Classroom 50
          |                  |                  |
    instructor notes    student notes        assignments
       canonical        collaborative          graded
       long-term          semester           private
          |
     future textbook
```

## 4. Grading Philosophy for Collaborative Notes

Avoid making publication/merging into the public collaborative notes the
primary grading criterion.

Where collaborative-note work is assessed, emphasize the process:

-   meaningful contribution;
-   correct use of Git/GitHub;
-   clear commits and pull requests;
-   responsiveness to review;
-   revision and improvement;
-   constructive review of other students' work;
-   reproducibility and correctness.

This separates assessment from editorial acceptance.

## 5. Long-Term Relationship Between the Two Note Systems

Treat student collaborative notes as a source of feedback about the
instructor book.

At the end of a semester, review them for:

-   recurring misconceptions;
-   topics needing clearer explanations;
-   useful examples;
-   effective alternative explanations;
-   interesting applications or datasets;
-   gaps in the instructor notes.

Useful insights can inform later revisions of `ids-book`, while the
instructor book remains independently authored and editorially
controlled.

## Guiding Principle

The three components have different functions and should remain
separate:

-   **`ids-book`: what the instructor wants students to learn.**
-   **`ids-f26`: what the class collectively learns and contributes.**
-   **Classroom 50: where students practice and are assessed.**

## 6. Shared `stat-writing-check` Skill

The writing/checking conventions should not belong specifically to
`ids-book`. They are useful across course repositories, student work,
manuscripts, research projects, and future books.

### Source of truth

Keep the human-readable guidelines and the reusable Codex skill in the
`stat-writing` repository.

Suggested structure:

``` text
stat-writing/
├── ...                         # existing Quarto source
└── skills/
    └── stat-writing-check/
        ├── SKILL.md
        ├── references/
        │   ├── latex.md
        │   ├── git.md
        │   └── file-naming.md
        └── scripts/
            └── check_files.py
```

The published `stat-writing` guide remains authoritative. The skill is
an operational, machine-oriented implementation of selected rules from
that guide.

Initial scope should focus on relatively objective conventions:

-   file naming;
-   Git hygiene;
-   LaTeX/source conventions.

Later versions may add Quarto, BibTeX, Python, R, and selected
statistical-writing checks.

### Pre-commit workflow

Conceptually:

``` text
student/user edits
       |
       v
"check before commit"
       |
       v
stat-writing-check
   |           |
   v           v
deterministic  Codex review
checks         requiring judgment
   \           /
    \         /
     v       v
    review report
         |
   problems found?
      /       \
    yes        no
     |          |
     v          v
 revise/fix   git commit
     |
     +------> check again
```

For students, default to review-only behavior. The skill should report
problems and explain the applicable convention rather than silently
rewriting the student's work.

For instructor/Codex use, it should also support requests such as:

> Run `stat-writing-check` and fix all mechanical violations before
> committing.

### How Codex finds the skill from `ids-book`

Codex running in `ids-book` should not depend on searching another Git
repository directly. The reusable skill needs to be installed in a Codex
skills location.

The `stat-writing` repository remains the development/source location:

``` text
~/work/stat-writing/
└── skills/
    └── stat-writing-check/
        └── SKILL.md
```

For local development, avoid maintaining a duplicate copy. Install it
for Codex using a symbolic link from the Codex skills directory to the
source directory. For example:

``` bash
mkdir -p ~/.codex/skills

ln -s ~/work/stat-writing/skills/stat-writing-check \
      ~/.codex/skills/stat-writing-check
```

Then the relationship is:

``` text
~/work/stat-writing/skills/stat-writing-check/
              |
              | symbolic link
              v
~/.codex/skills/stat-writing-check/
              |
              | discovered by Codex
              v
      +-------+--------+-----------+
      |                |           |
   ids-book          ids-f26    manuscripts/
```

This keeps a single editable copy of the skill. Changes made to the
skill in the `stat-writing` repository are immediately visible through
the symbolic link.

Before relying on the exact `~/.codex/skills` location, verify it
against the current Codex CLI skill-discovery documentation because
Codex skill conventions may evolve.

### `ids-book` integration

`ids-book` should not copy the `stat-writing` rules or the skill itself.

Its `AGENTS.md` can contain a small project-specific instruction such
as:

``` markdown
## Pre-commit review

Before committing changes, use the `stat-writing-check` skill
to review the changes against the statistical writing guidelines.
```

A typical local workflow is then:

``` bash
cd ~/work/teaching/ids-book
codex
```

followed by a request such as:

> Run the `stat-writing-check` skill on my current changes.

### Student distribution

The instructor's symbolic-link setup is appropriate for developing and
testing the skill but is not, by itself, a student distribution
mechanism because students will not have the instructor's local
`stat-writing` checkout.

First develop and test version 1 using `ids-book`. Once the skill is
stable, define a simple student installation/distribution process for
use with `ids-f26` and Classroom 50 repositories.
