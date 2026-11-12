# Drafts and milestones

| Folder | What it is | Status |
|---|---|---|
| `Draft 1/` | Progress report, "Section 1: Work Done as of 24 August 2026" | Submitted; kept unchanged (`build/pdf/ELL305-Draft-1.pdf`, `submissions/Draft-1/`) |
| `draft-initial/` | First working draft of the full paper (from 28 October 2026) | Kept unchanged as the predecessor of `initial-draft-2/` |
| `initial-draft-2/` | **The term paper** (from 30 October 2026) | Final; submitted as `build/submission-final/` |

Entry points: `paper/main.tex` (Draft 1), `paper/main-draft-initial.tex` and `paper/main-initial-draft-2.tex`. Notes for each are in `notes/Drafts/<folder>/`; `notes/Drafts/initial-draft-2/00 Draft Overview.md` records every change to the paper.

The submission is two files: one self-contained `.tex` and the PDF compiled from it. `scripts/flatten-initial-draft-2.py` generates the `.tex` from the modular sources; it is never edited by hand. Earlier milestone folders are never overwritten.
