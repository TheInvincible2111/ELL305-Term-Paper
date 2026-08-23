---
draft: 1
verified: 2026-08-24
status: compiled
tags: [draft-1, build, format]
---

# Build and format status

## Current output

- PDF: `../../../build/pdf/ELL305-Draft-1.pdf`
- Format: A4
- Length: 11 pages
- Bibliography: 6 entries exported from Zotero/Better BibTeX
- Cover: IIT Delhi identity, Department of Electrical Engineering, three group members, and no faculty-consultation block
- Main milestone heading: **Work Done as of 24 August 2026**
- Gantt chart: generated in LaTeX and placed on a landscape page
- Textbook-to-topic mapping: generated in TikZ, introduced with the mapping overview, and placed as a top-of-page figure before the remaining chapter details

## Verification completed

- The active LaTeX project compiled successfully through the normal project build script.
- The per-user MiKTeX 25.12 installation was repaired and the same script used by the default VS Code build task was verified end to end.
- The bibliography processor completed without warnings or errors.
- No LaTeX errors, package warnings, overfull boxes, undefined citations, or undefined references were present in the final log. One benign underfull-vbox notice remains from page balancing at a section transition; visual inspection shows no corresponding defect.
- All 11 pages of the final PDF were rendered and visually inspected, including the cover, abstract, contents, mapping diagram, tables, bibliography, and landscape Gantt chart.

## Format decision

The supplied `Term Paper Overleaf Template.zip` was reviewed as a reference. Its useful institutional report sequence informed the reusable templates, but its CLL110 sample text, bundled class, sample images, `natbib` setup, and `jfm.bst` do not replace the ELL305 milestone instructions, the modular project structure, or the Zotero-generated bibliography workflow.

The verified PDF is local. No GitHub publication is recorded by this note.
