ELL305 Draft 1 submission package
=================================

Submit-ready file:
- ELL305-Draft-1.pdf

Reproducible source:
- ELL305-Draft-1.tex      Single consolidated LaTeX source. All Draft 1 modules,
                          TikZ figures, and Zotero-exported bibliography data are inlined.

Required image assets:
- iit-delhi-logo.png      Institutional image used on the cover
- grammarly-plagiarism-report-2026-08-24.png
                          Evidence image reproduced in Appendix A
- readability-indices-2026-08-24.png
                          Evidence image reproduced in Appendix B

Build sequence (MiKTeX or TeX Live):
1. pdflatex ELL305-Draft-1.tex
2. biber ELL305-Draft-1
3. makeindex -s ELL305-Draft-1.ist -t ELL305-Draft-1.glg -o ELL305-Draft-1.gls ELL305-Draft-1.glo
4. makeindex ELL305-Draft-1.idx -o ELL305-Draft-1.ind
5. pdflatex ELL305-Draft-1.tex
6. pdflatex ELL305-Draft-1.tex

Research PDFs, Obsidian notes, source templates, SVG originals, and generated auxiliary files are intentionally excluded because they are not required to compile or submit Draft 1.