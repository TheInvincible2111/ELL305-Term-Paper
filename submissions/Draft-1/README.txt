ELL305 Draft 1 submission package
=================================

Submit-ready file:
- ELL305-Draft-1.pdf

Reproducible source:
- ELL305-Draft-1.tex      Consolidated LaTeX source (all Draft 1 modules and TikZ figures inlined)
- references.bib          Zotero/Better BibTeX bibliography export
- iit-delhi-logo.png      Only external image required by the LaTeX source

Build sequence (MiKTeX or TeX Live):
1. pdflatex ELL305-Draft-1.tex
2. biber ELL305-Draft-1
3. pdflatex ELL305-Draft-1.tex
4. pdflatex ELL305-Draft-1.tex

Research PDFs, Obsidian notes, source templates, SVG originals, and generated auxiliary files are intentionally excluded because they are not required to compile or submit Draft 1.