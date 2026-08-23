# Modular project structure

The project is deliberately divided so that content, formatting, bibliography data, figures, and milestone history can be edited independently.

## Active LaTeX assembly

- `../../paper/main.tex` is the small active entry point. It assembles the selected milestone and should not contain substantive chapter prose.
- `../../paper/styles/ell305-format.tex` contains the shared institutional appearance, typography, page layout, heading styles, caption rules, hyperlinks, and bibliography configuration.
- `../../paper/assets/` contains reusable publication assets such as the IIT Delhi logo.
- `../../Draft 1/metadata.tex` contains Draft 1 names, entry numbers, emails, title, and date.
- `../../Draft 1/front-matter.tex` contains the cover, abstract, keywords, and contents page.
- `../../Draft 1/preamble.tex` contains packages needed specifically by Draft 1 rather than by every future paper.
- `../../Draft 1/sections/` contains one independently editable file per substantive section.
- `../../Draft 1/figures/` contains the programmatic figure sources used by Draft 1.

## Reusable templates

- `../../paper/templates/ell305-milestone-main.tex` is the entry-point pattern for future independently preserved milestone drafts.
- `../../paper/templates/ell305-final-paper-main.tex` is the entry-point pattern for the long final paper.
- The final-paper template combines the approved seven-part research plan with the useful report sequence in the supplied Overleaf archive: introduction, background/theory, method and evidence, results and discussion, conclusions, appendices, and bibliography.

## Notes, references, and generated output

- `../Drafts/` mirrors the LaTeX draft modules in editable Obsidian notes.
- `../Papers/` stores one structured reading note per source; preliminary identification is not recorded as completed reading.
- `../Textbook/` stores the course-text mapping and chapter-specific foundations.
- `../../references/references.bib` remains the canonical Zotero/Better BibTeX export used by LaTeX.
- `../../diagrams/` is reserved for text-based diagram sources; WaveDrom is used exclusively for waveforms and timing diagrams.
- `../../build/aux/` contains generated intermediates, while `../../build/pdf/` contains the compiled deliverable.

## Version rule

Drafts 1--4 must remain separate directories. Starting a new milestone means creating a new draft module and switching the small active entry point; it does not mean overwriting an earlier milestone submission.
