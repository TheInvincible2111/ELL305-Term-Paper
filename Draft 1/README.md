# Draft 1

This folder contains the source modules for the independent milestone report dated 24 August 2026. The active build entry point remains `paper/main.tex`, which imports these files.

## Editing map

- `metadata.tex` - title, author, date, and provisional topic
- `front-matter.tex` - title block, milestone note, and contents
- `sections/00-work-done.tex` - required milestone heading and status framing
- `sections/01-topic-and-scope.tex` - chosen topic and research question
- `sections/02-textbook-mapping.tex` - mapping to ELL305 Chapters 9--12
- `sections/03-preliminary-survey.tex` - initial primary literature
- `sections/04-research-directions.tex` - questions and technical themes
- `sections/05-work-packages.tex` - progress table and interpretation
- `sections/06-semester-schedule.tex` - schedule and Gantt chart
- `sections/07-sources.tex` - source-status explanation and bibliography
- `sections/08-next-steps.tex` - immediate actions
- `figures/gantt-chart.tex` - editable programmatic Gantt chart

The professor-facing report intentionally contains no tooling/workflow section.

Institutional typography, cover conventions, headers, captions, and bibliography styling are shared through `paper/styles/ell305-format.tex` so later drafts use the same format.

For later milestones, create sibling folders named `Draft 2`, `Draft 3`, and `Draft 4`, then change only the input paths in `paper/main.tex`.
