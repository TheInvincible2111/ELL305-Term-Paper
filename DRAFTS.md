# Semester draft structure

The course has four independently evaluated versions. Keep each milestone in its own top-level folder:

```text
Draft 1/
Draft 2/
Draft 3/
Draft 4/
```

The course's second milestone was skipped. The folder numbering stays sequential for convenience, so the next milestone submitted after Draft 1 lives in `Draft 2/` (decision recorded 28 October 2026).

`paper/main.tex` is a thin active-build file. It imports the selected draft's modules, so switching milestones requires changing only the folder name in those input paths. Obsidian planning and source notes are mirrored under `notes/Drafts/Draft N/`.

`draft-initial/` (started 28 October 2026) is a working draft of the full paper, not a milestone; it is built from `paper/main-draft-initial.tex`.
