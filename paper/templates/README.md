# ELL305 LaTeX templates

`ell305-milestone-main.tex` is the reusable entry-point pattern for Drafts 2--4 and any later milestone document. It deliberately does not compile in place: first create a new preserved `Draft N` directory from the preceding milestone, then replace the placeholder paths with the new directory name.

`ell305-final-paper-main.tex` is the long-form template. It incorporates the useful report sequence from the supplied `Term Paper Overleaf Template.zip`---cover, abstract, contents, introduction, theory/background, method, results and discussion, conclusions, appendices, and bibliography---while mapping those headings to the approved processor-foundations, cache, monolithic-scaling, chiplet, AMD Zen, and 3D V-Cache parts.

The institutional appearance is centralized in `paper/styles/ell305-format.tex`. Future additions should use that shared style rather than copying formatting commands into individual section files. Each milestone keeps its own metadata, front matter, figures, and modular section files so that an earlier submitted draft is never overwritten. The archive's bundled `report.cls`, `natbib.sty`, sample figures, and `jfm.bst` are reference examples only; this project retains the current Zotero-generated BibTeX and `biblatex` workflow.

Before submitting a new milestone:

1. Update the milestone title, date, and evidence-limited abstract.
2. Use the exact heading and status date specified for that milestone.
3. Record only work actually completed; distinguish identified sources from completed readings.
4. Compile through `scripts/build.ps1`, inspect the log, and visually inspect every PDF page.
5. Publish only after the user explicitly requests it.
