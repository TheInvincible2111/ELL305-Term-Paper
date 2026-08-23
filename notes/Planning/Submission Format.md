# Submission format

## Shared institutional format

- Use the IIT Delhi logo and institute name on the cover.
- Name the Department of Electrical Engineering as the submitting department.
- List all three group members with entry numbers and institutional email addresses.
- Do not place the faculty consultation choice on the cover.
- Use the shared LaTeX format in `../../paper/styles/ell305-format.tex` for all drafts going forward.
- Keep milestone drafts independent from the final paper and preserve each draft separately.

## Draft 1 instruction

The required main heading is **Section 1: Work Done as of 24 August 2026**. It must state the chosen topic, map the topic to the textbook, identify Prof. Sumantra Dutta Roy as the faculty member chosen for consultation, and show collective progress through a LaTeX Gantt chart and work packages.

Textbook-reading percentages must be described as orientation progress unless a complete reading is recorded. Sources identified or examined preliminarily must not be described as fully read.

## Internal workflow requirements

- Consult the current Obsidian notes before drafting or revision.
- Consult `../../sources/archbook.pdf` for relevant course foundations.
- Manage bibliography data through Zotero and its canonical Better BibTeX export.
- Use TikZ, Graphviz, Mermaid, or compatible text-to-diagram tools for diagrams.
- Use WaveDrom exclusively for waveforms and timing diagrams.
- Do not add a professor-facing tooling section unless explicitly required.

## Reusable LaTeX structure

- Shared appearance: `../../paper/styles/ell305-format.tex`.
- Milestone entry-point pattern: `../../paper/templates/ell305-milestone-main.tex`.
- Final-paper entry-point pattern: `../../paper/templates/ell305-final-paper-main.tex`.
- The supplied Overleaf archive is a formatting reference. Its useful report sequence is retained, but its CLL110 sample content and bundled bibliography/class files do not override ELL305 milestone instructions or the Zotero-generated bibliography workflow.
