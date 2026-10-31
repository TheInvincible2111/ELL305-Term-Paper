---
draft: 1
verified: 2026-08-24
status: final-audited
tags: [draft-1, build, format]
---

# Build and format status

## Current output

- PDF: `../../../build/pdf/ELL305-Draft-1.pdf`
- Format: A4
- Length: 19 pages
- Bibliography: 6 entries exported from Zotero/Better BibTeX
- Cover: IIT Delhi identity, Department of Electrical Engineering, three group members, and no faculty-consultation block
- Main milestone heading: **Work Done as of 24 August 2026**
- Gantt chart: generated in LaTeX and placed on a landscape page
- Textbook-to-topic mapping: generated in TikZ, introduced with the mapping overview, and placed as a top-of-page figure before the remaining chapter details

## Verification completed

- The active LaTeX project compiled successfully through the normal project build script.
- MiKTeX is installed system-wide under `C:\Program Files\MiKTeX-25.12`; the build scripts prefer that installation explicitly, refresh its font maps, and use the same project script as the default VS Code build task.
- The bibliography processor completed without warnings or errors.
- No LaTeX errors, package warnings, overfull or underfull boxes, undefined citations, or undefined references are present in the final log.
- All 19 pages of the final PDF were rendered and visually inspected, including the mandated front matter, generated lists and glossary, mapping diagram, tables, bibliography, landscape Gantt chart, both appendices, and index.

## Format decision

The supplied `Term Paper Overleaf Template.zip` was reviewed as a reference. Its useful institutional report sequence informed the reusable templates, but its CLL110 sample text, bundled class, sample images, `natbib` setup, and `jfm.bst` do not replace the ELL305 milestone instructions, the modular project structure, or the Zotero-generated bibliography workflow.

The verified PDF and submission package were published to the private GitHub repository in commit `89a4c69` (confirmed against GitHub on 28 October 2026).
