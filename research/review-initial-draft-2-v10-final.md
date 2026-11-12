# Final review before submission: initial-draft-2 (v10, 11 November 2026)

Reviewer brief: `research/review-prompt-initial-draft-2-v10-final.md`. No paper source, script, figure or build file was edited. Files written: this review, and (at Ishan's request during the review) the checkpoint note `notes/Drafts/initial-draft-2/CHECKPOINT 2026-11-11 v10 review.md`. Scratch work is outside the project.

**Page convention.** "p." is the printed page number; printed = PDF page − 1 (the cover is PDF page 1).

**Three limits of this review, stated once.**
1. **Pages were not looked at by eye.** The review environment could render pages but had no way to display them. Figure and layout checks were therefore done on the PDF's own text boxes (font size, position and overlap of every word, with `pdfplumber`) and on pixel counts of rendered pages (`pdftoppm`). Findings that rest on this are marked "not viewed". Q8 in particular needs one look at the page before it is acted on.
2. **Unchanged text was sampled, not re-read line by line.** Everything that changed since v9 (the full `git diff` against `f19d19f`) was read, as were Part I, the abstract, the Conclusions, the text around every cut and every consistency anchor. The rest of Parts II–VI was checked by targeted search and by the number sample in section 7, not by a complete re-read.
3. **The single-file compile used the workspace's TeX Live 2022**, which needs the `\IfDocumentMetadata` shim (section 3). It was not repeated on MiKTeX or Overleaf from here.

---

## 1. Verdict

Provisional grade: **A−**. The two files are in good order: the `.tex` compiles alone in an empty folder to 152 pages whose text is identical to both stored PDFs, the log is clean, the file is up to date with the modular sources, and it needs no other file. The simulator rebuilds, passes its tests and reproduces the stored results byte for byte. The v9 fixes are present and the cuts removed nothing the argument needs.

The files are **not yet ready to upload**, for three reasons. Two are the known open items: Appendices A and B still print "[TODO: …]" (pp. 135–136), and the date is still 8 November 2026. The third is new and small: **Q1 (BLOCKER)**, the draft macros `\partbudget` ("Target length … Draft status"), `\verify`, `\plannedcontent` and `\todo` are still defined in the submitted `.tex`.

Beyond that, the last round left six small defects that a reader would notice: two list entries with a hole in them (Q2), two overview maps that still show cut or duplicated topics (Q3, Q4), one sentence whose number changed meaning when its table was cut (Q5), a P10 correction that missed two places (Q6), and one figure still below 7 pt (Q7). None affects a conclusion. Once Q1–Q7 are fixed, A and B are filled, the date is set and the single file is regenerated and recompiled alone, the two files are ready.

---

## 2. Findings

| ID | Severity | Location (modular source; page in the submission PDF) | What the paper says | What the source, data, code or rule says | Safe fix, and everything that must change with it |
|---|---|---|---|---|---|
| Q1 | **BLOCKER** (draft leftovers in the submitted `.tex`) | `initial-draft-2/preamble.tex:42–51` and `:64–68` (generated file, from line 4692 to about line 4711; nothing visible in the PDF) | The submitted `.tex` still defines `\todo`, `\verify`, `\partbudget` ("Target length: about #1 pages. Draft status: #2.") and `\plannedcontent` ("Planned content (not yet written)"), with the colours `todored` and `verifyamber`. | Brief, Part 1.4: no "Target length", `\partbudget` or `\verify` in the submitted file. A search of all sources shows `\verify`, `\partbudget` and `\plannedcontent` are used nowhere; `\todo` is used only in Appendices A and B. | Now: delete `preamble.tex:45` (`verifyamber`), `:47` (`\verify`), `:48–51` (`\partbudget`) and `:64–68` (`\plannedcontent`). When Appendices A and B are filled: delete `:44` (`todored`) and `:46` (`\todo`) as well. Nothing else refers to them. Then regenerate the single file and search it for `todo`, `verify`, `Target length`, `Planned content`: expect no match. |
| Q2 | Format (two list entries with a missing word) | `appendices/appendix-f-directory-example.tex:15`; `figures/libx264-waterfall.tex:23` (List of Tables entry 46, p. 11; List of Figures entry 35, p. 13) | The lists read "The accesses of under a directory protocol" and "The libx264 calculation of as a sequence". | The short captions were written as `[The accesses of  under …]` and `[The libx264 calculation of  as a sequence]`: the `\cref` of the long caption was removed and nothing put in its place. All other 115 short captions read correctly; none contains "??" or a stray reference. | `appendix-f…:15`: `\caption[The five accesses of the MSI trace under a directory protocol]{…}`. `libx264-waterfall.tex:23`: `\caption[The libx264 calculation as a sequence]{…}`. Long captions unchanged. Only the two list pages change. |
| Q3 | Broken by cut (C13) | `figures/mindmap-foundations.tex:16` (Fig. 5, p. 26) | The map leaf reads "Thermal resistance, ED²". | The ED² subsection was removed; "ED²" now occurs nowhere else in the paper. The v9 review listed this leaf as a required change. | Change the leaf to `{Thermal resistance}`. Nothing else changes. (The "Amdahl's law" leaf on the same map is still valid: section 5.2 remains.) |
| Q4 | Broken by cut (C2) | `figures/mindmap-stacked.tex:22` and `:24` (Fig. 27, p. 63) | Two neighbouring leaves under "Hybrid bonding" read "No solder" and "No solder, so a fine pitch". | The C2 fix replaced "Oxide bond, then anneal" at `:24` with a text that repeats `:22`. | Change `:22` to `{Oxide and copper pads}` (which the shortened text at `part4-stacked-cache.tex:137` still describes) and keep `:24`. Nothing else changes. |
| Q5 | Error (introduced by the AMAT cut); also the longest sentence in the paper, 69 words | `sections/part2-foundations.tex:114` (pp. 31–32) | "…with the latencies measured on a Zen 2 and a Zen 3 desktop part and illustrative local miss rates of 5, 30 and 40% for L1, L2 and L3, a 60–70 ns memory latency adds only about half a nanosecond to an average access of about 1.5 ns." | With those miss rates the memory term is 0.05 × 0.30 × 0.40 × (61.8 to 68.8 ns) = **0.37–0.41 ns**. The 0.53–0.56 ns ("about half a nanosecond") of the cut table was the L3 **and** memory terms together. The 1.5 ns (1.46 and 1.60) and the 60–70 ns are right; the sentence is cited (`justiceAMDRyzen72021`) and says the miss rates are illustrative, as the brief requires. | Replace with two sentences: "Because the lower levels are weighted by the miss rates above them, a long memory latency adds little to the average. With the latencies measured on a Zen 2 and a Zen 3 desktop part \cite{justiceAMDRyzen72021} and illustrative local miss rates of 5, 30 and 40% for L1, L2 and L3, the L3 and a 60–70 ns memory together add only about half a nanosecond to an average access of about 1.5 ns." The following sentence ("Each load that does miss still stalls…") stays. No other place quotes this figure. |
| Q6 | Inconsistent (P10 applied in three places, missed in two) | `sections/part5-case-study.tex:507` (p. 110); `appendices/appendix-e-simulation.tex:60` (p. 143) | S3 check: "the V-Cache CCD gains 5.2%, against the 4.9% Lam measured". App. E: "its agreement with Lam's 4.9% gain at equal clocks". | P10 established that a 5.2% speed-up compares with the **5.1%** IPC gain from Lam's chart values (1.36 → 1.43), and that 4.9% is the figure Lam states. Part IV `:167`, Part V `:415` and App. F `:60` now say so. The simulation's own numbers are right: `s3_validation_libx264.csv` gives 3.78 L3 accesses, 1.44 misses, 729 cycles and a 5.19% gain. | `part5…:507`: "…gains 5.2%, against 5.1% from Lam's chart IPCs (Lam states 4.9%)." `appendix-e…:60`: "its agreement with Lam's gain at equal clocks (5.2% against 5.1% from the chart IPCs; \cref{sec:sim-clock})". `tab:lam-detail`, `tab:cache-vs-clock` and Findings keep 4.9% (Lam's own figure, correct there). |
| Q7 | Figure (P13 not complete) | `figures/horizontal-vs-vertical.tex:5, 6, 12, 14, 17, 22, 25, 29` (Fig. 31, p. 67) | All labels inside both panels are set in `\tiny`. | Measured in the PDF: 50 words (255 characters) at **6.1 pt**, below the 7 pt threshold. The v9 response says the figure was "scaled up instead"; the `\resizebox{\textwidth}` scale is only about 1.02. This is the only figure in the paper with running text under 6.9 pt (every page was measured; the only other small glyphs are subscripts). | Without changing any label: draw the two panels one above the other instead of side by side (give the second `scope` `yshift=-5.2cm` and no `xshift`) and change the `\resizebox` width to about `0.6\textwidth`; each panel is then scaled up by roughly a third. Adjust the width until the text measures at least 7 pt. Caption and label unchanged. The figure grows by about 4 cm, so re-check the page break on p. 67. |
| Q8 | Figure (side effect of P13; **not viewed, confirm by eye first**) | `figures/zen-ccd-evolution.tex:54–55` (Fig. 43, p. 85) | In the third panel the white label "structural / silicon / over cores" is drawn on top of two core boxes on each side. | With the label enlarged to `\scriptsize`, its box (x 211–251 pt, y 372–402 pt on the page) covers most, but not all, of the "Core" and "Zen 3" labels beneath (x 230–253 pt): by the text boxes, about 2 pt of the "e" of "Core" and the "3" of "Zen 3" stick out at the right edge of the white box, on both sides of the panel. | If the page confirms it: add `minimum width=1.45cm, inner sep=2pt` to the two label nodes at `:54–55`, so the white box covers the two core labels completely. Nothing else changes. |
| Q9 | Writing (comma splice made by a P19 split) | `sections/part1-introduction.tex:182` (p. 25) | "…the published Zen 3 L1 and L2 latencies the model uses agree with the measured ones, its L3 and memory latencies are within about 20%." | Two main clauses joined by a comma; before the split the sentence continued ", and the core…". | "…agree with the measured ones, and its L3 and memory latencies are within about 20%." |
| Q10 | Layout | Fig. 13 (`figures/topologies.tex`, input from `part2-foundations.tex`), p. 42; Table 48, p. 146 | p. 42, the last page of Part II, holds only Fig. 13 (three small topologies); two thirds of the page is empty. p. 146, the last page of App. F, holds only Table 48. | The brief's example of a page to flag: "a single figure alone at the end of a Part". After the C12 merge the figure no longer fits on p. 41. | Any cut of about 8 lines in section 5.4, or K1–K3 below, pulls Fig. 13 back onto p. 41 and saves a page. If none is taken, leave it: the page is tidy. Table 48 on its own page at the end of an appendix needs no change. |
| Q11 | Minor (orphans left by the cuts; none is in the submitted file's visible output) | `figures/amdahl.tex`, `figures/nps-modes.tex`; `part2-foundations.tex` (`eq:mlp-stall`, `eq:amdahl`); Part IV (`eq:pad-density`, `eq:w2w-cost`); `references/references.bib` | — | The two figure files are no longer `\input` and nothing refers to their labels. Four equation labels have no reference (`eq:mlp-stall` newly so, after the overlap cut; `eq:cpi-stalls` is still referenced). `swaminathanNextFrontierEnabling2022` is in the `.bib` (and so in the embedded bibliography) but uncited, as in v9; its README row says "missing — do not cite". No cited key became unused: all 36 cited keys are in the `.bib` and have a README row. 28 section labels and `app:worked-examples` are unreferenced, which is harmless. | Nothing must change. Optional tidy-up: move the two figure files out of `initial-draft-2/figures/` (they are not in the submission), and leave the labels. |
| Q12 | Minor (process hazard, not in the paper) | `tools/cachesim/study/compare_5600x.py:69, 83`; `make_figures.py:52–237` | — | These scripts write the paper's generated figure files with `\caption{…}` only. The files in `initial-draft-2/figures/` were then given short captions by hand. A rerun into that folder (as App. E's listing shows) would silently undo the short captions of the generated simulation and 5600X floats. A fresh run today differs from the stored `m5600x-latency.tex` and `m5600x-table-mlp.tex` **only** in the caption line. | Do not rerun the two scripts into `initial-draft-2/figures` before submission. If they must be rerun, re-apply the short captions and check the two lists. |
| Q13 | Minor | `initial-draft-2/metadata.tex:4` against `preamble.tex:16` (cover; PDF properties) | Cover subtitle: "Chiplet Architectures, Cache Hierarchies, and 3D-Stacked Cache — A Case Study of AMD Zen Processors". PDF title and the paper's stated title: "…: Chiplet Architectures and 3D-Stacked Cache in AMD Zen Processors". | The two forms differ; the project instructions §3 allows either. | Ishan's choice; no change needed. If one form is wanted, change `\draftsubtitle` or `pdftitle`, not both. |
| Q14 | Minor | Index, p. 151 | The index has 18 entries, none after Part IV except the two appendix entries, and none for the paper's own subjects (chiplet, 3D V-Cache, CCD, I/O die, NUMA, TLB, working set). | The course asks for a generated index; this one is generated and all 18 page numbers are right (section 3). It is thin for a 150-page paper. | Optional: add `\index{…}` at the defining sentence of 10–15 core terms. Each is safe (the index is generated; the page count changes only if the index passes one page, which 15 more entries will not). |
| Q15 | Minor (title after cut C4) | `sections/part2-foundations.tex:176` (section 4.6, p. 33) | "Writes, write buffers and inclusion" | After C4 the write buffer is one sentence (`:184`). | Optional: "Writes and inclusion". The label `sec:writes-inclusion` has no reference, the contents list regenerates, and the "Write buffer" leaf of Fig. 11 stays valid because the sentence and the row of `tab:cache-optimisations` remain. |

**Writing: other sentences near the 55-word threshold** (none over it except Q5): `part3-chiplets.tex:295` (61 words; split at the semicolon: "…is not stated in the datasheets. The table infers it from…"), `part5-case-study.tex:454` (59; split before "and the latency at 1 GB"), `part2-foundations.tex:216` (59; split at the colon), `part4-stacked-cache.tex:14` and `:20` (58 each; split at the semicolons). No gendered pronouns, no undefined abbreviation and no group work attributed to an individual were found in the changed text or in Part I.

**For Ishan, not a finding on the paper.** GitHub `main` is still `f19d19f`, and none of the v9 changes is committed. `appendices/appendix-h-evidence-ledger.tex`, `front-matter/logo-embedded.tex`, `scripts/flatten-initial-draft-2.py` and `build/submission-final/` are untracked. If the repository is made public as it stands, the paper's links will open the earlier 162-page draft, with the "working draft" cover, beside a simulator and data that do match the paper. Every `\ghdir`/`\ghfile` path the paper links exists in that commit.

**State of the known open items (not counted as findings).**
- Appendix A and Appendix B: still `\todo` placeholders (`appendix-a-plagiarism-report.tex:7`, `appendix-b-reading-indices.tex:6`; pp. 135–136). They print "[TODO: … for this draft …]" in red. They must be typed as text or a table.
- Date: `\draftdate` is still "8 November 2026" (`metadata.tex:7`); it appears on the cover and on the copyright page (p. 1).
- Repository: recorded as private in the project notes; access could not be checked (no web).

---

## 3. Single-file check

**Commands** (in a new empty folder holding only a copy of `build/submission-final/ELL305-Term-Paper.tex`; `SHIM` is the string `\providecommand\IfDocumentMetadataTF[2]{#2}\providecommand\IfDocumentMetadataT[1]{}\providecommand\IfDocumentMetadataF[1]{#1}\input{ELL305-Term-Paper.tex}`):

```
pdflatex -no-shell-escape -interaction=nonstopmode -jobname=ELL305-Term-Paper "SHIM"     # pass 1
biber ELL305-Term-Paper
makeglossaries ELL305-Term-Paper
pdflatex … "SHIM"   (twice)                                                              # passes 2, 3
makeglossaries ELL305-Term-Paper
makeindex ELL305-Term-Paper.idx
pdflatex … "SHIM"   (twice)                                                              # passes 4, 5
```

**Results.**

| Check | Result |
|---|---|
| Pages after each pass | 144, 151, 151, 152, 152 |
| Final PDF | 152 pages, A4, 1 305 023 bytes (the stored submission PDF is the same size) |
| `pdftotext -layout` against `build/submission-final/ELL305-Term-Paper.pdf` | identical (`cmp`: no difference) |
| `pdftotext -layout` against `build/pdf/ELL305-initial-draft-2.pdf` | identical |
| Log | 0 errors; 0 overfull boxes; no undefined reference or citation; no "Rerun" request; 25 underfull boxes (float pages); the only LaTeX warnings are the two expected "Writing or overwriting file" lines for the embedded bibliography and logo |
| biber, makeglossaries, makeindex | clean; 45 glossary lines accepted, 0 rejected; index 57 lines, 0 warnings |
| Index | all 18 entries checked against the pages they give (2.5D integration 54, AMAT 31, cache miss 32, dynamic power 28, hybrid bonding 69, Infinity Fabric 49, leakage power 28, memory hierarchy 29, Moore's law 17, Murphy yield model 44, performance equation 27, plagiarism report 135, readability indices 136, reticle limit 43, SRAM 30, thermal resistance 29, yield 44 and 137): every term is on its page |
| Glossary | 26 entries; every term occurs in the body text |
| **Shim** | **Needed here.** Without it this TeX Live 2022 stops twice on `\IfDocumentMetadataT` (biblatex 3.21 with an older LaTeX kernel) and gives 144 pages. A current TeX Live, MiKTeX or Overleaf defines these commands itself. The file was not compiled on one of those from this environment; the project instructions §5 asks for that before upload. |

**Freshness.** `python3 scripts/flatten-initial-draft-2.py <scratch>/regen.tex` gives a file byte-identical to the stored `.tex`. The stored PDF (10 Nov, 17:40 UTC) is newer than the `.tex` (17:39 UTC). No file under `initial-draft-2/`, `paper/` or `references/` is newer than either.

**Nothing external.** The file has one `\includegraphics` (the logo) and one `\addbibresource`; both files are written by `filecontents*` blocks. There is no `\graphicspath`, no other `\input`, and all packages are standard. The only non-ASCII bytes in the `.tex` are eight lines inside the bibliography block (UTF-8 in authors' names and one title, which the `inputenc` line covers); the logo block is ASCII only. On the rendered cover a coloured image occupies the logo position (pixel count; not viewed).

**Leftovers.** Searched the `.tex` (outside the two `filecontents*` blocks) and the PDF text for: working draft, initial-draft, Target length, `\partbudget`, `\verify`, "??", "[TODO", `tmp/`, `scripts/`, and the names of AI tools, Obsidian and Zotero. Matches: the macro definitions of Q1; the two known `\todo` uses in Appendices A and B; and the page-2 "Use of AI Tools" statement. Remaining comments are the three-line header and three two-character labels inside one figure (`% M11`). `pdfinfo` gives the paper's title and the three authors.

**Course rules and format.**
- Diagrams: all TikZ or pgfplots; no timing diagrams.
- Code: only in App. E (`listings`). On the rendered listing page (p. 143) the comments are green and the keywords blue (pixel counts by hue; not viewed); the listing contains no strings, so the string colour does not appear.
- Bibliography: Better BibTeX export, embedded unchanged.
- Chapter mapping: Part I methodology (`part1-introduction.tex:149`) states Chapters 7 and 9–12, mainly 11 and 12, and names Prof. Sumantra Dutta Roy as advisor. Chapters actually cited with a section number: 7 (8 times), 9 (2), 10 (18), 11 (26, plus 2 table citations), 12 (32, plus 1 table citation). They match.
- A4 (595.276 × 841.89 pt), 12 pt, `margin=1in`, single spacing; the text block keeps the one-inch margins on every page. Two things sit outside it by design: the App. E listing's line numbers in the left margin, and `microtype`'s character protrusion at line ends (2 pt on most pages, about 4 pt on two reference pages; the log reports no overfull line).
- Page order: cover, copyright (p. 1), acknowledgements with the AI-use statement (p. 2), abstract (p. 3), contents (pp. 4–9), List of Tables (pp. 10–11), List of Figures (pp. 12–14), glossary (pp. 15–16); then Parts I–VI, references (pp. 132–134), Appendices A–H (pp. 135–150), index last (p. 151).
- Lists: 51 tables and 66 figures; short captions read well except the two of Q2.

---

## 4. v9 regression table

| Item | Status | Note |
|---|---|---|
| P1 single file | correct | Section 3. |
| P2 Appendices A, B | open (known) | Still placeholders. |
| P3 cover, PDF title | correct, except the date (known) | "Term Paper" on the cover; title and authors in the PDF properties. |
| P4 two files, no ZIP | correct | the project instructions §5 now says two files. |
| P5 listing colours | correct | Set in `preamble.tex:18`; Draft 1's style untouched. Pixel check only. |
| P6 repository access | open (known) | See the note for Ishan in section 2. |
| P7 Fig. 28(b) | correct | Marker positions re-measured on Wuu slide 6 at 72 dpi: x = 96.7, 171.7, 246.8, 322.4, 397.6, 510.0, 660.3 (years 2004, 2006, 2008, 2010, 2012, 2015, 2019 on the slide's axis) and y offsets 0, 24.1, 44.7, 63.0, 83.8, 109.8, 137.5. The figure's seven points keep these in a constant ratio (2.07–2.10). The dashed line runs through the 2004 and 2012 points; the 14 nm and 10/7 nm points lie above it, as the caption says. The caption states that the slide has no axis values and that the line continues the 2004–2012 pace. |
| P8 "Chapters 7 and 9–12" | correct | Part I `:149`, Part II `:10`. |
| P9 chapter mapping and advisor | correct | Matches the chapters cited (section 3). |
| P10 4.9 / 5.1 / 5.2% | correct in the three places listed; **two more missed** | Q6. |
| P11 "37 ns … to a measured ratio" | correct | `part5:560`. All seven uses of 37 ns are tied to the ratio. |
| P12 "the simulation" | correct | `part5:501, 503`. |
| P13 figure text size | **incomplete; one side effect** | Every figure page measured: all text is 6.9 pt or larger except Fig. 31 (Q7). The enlarged label in Fig. 43 now sits over core labels (Q8, not viewed). |
| P14 refresh box | correct (source) | `dram-array.tex:39` draws the connector to the sense-amplifier row's edge. |
| P15 Fig. 4 leaves | correct | "Cache against clock; simulation" under Part V, "Strength of evidence" under Part VI. |
| P16 "This calculation…" | correct | Apps C and F. "In the example above" in App. C `:32` refers to App. C's own numbers. |
| P17 comments | correct | No full-line comment outside the header; no tool name. |
| P19 long sentences | correct; **one comma splice created** | Q9. One sentence over 55 words was created by a cut (Q5). |
| P20 EFB | correct | Lambert's slide reads "2.5D EFB" with no expansion. |
| C1(a) prefetch caveat | correct | Stated in full at `sec:tradeoff-example` (`part4:174`); the other places point to it. |
| C1(b) 5600X limits | correct | Still in S0 (`part5:454`), App. G (`:65`) and `tab:evidence-strength` (`part6:149`); Threats (`part6:192`) now points to S0 and App. G and reads naturally. |
| C1(c) 4.5× qualifier | correct | "in the one measurement available" is on the first statement (Findings, `part1:176`) and in the Conclusions (`part6:217`); `part3:182` presents it directly under Reguly's table with the virtual-machine warning. |
| C2 hybrid-bond process | text correct; **map leaf duplicated** | Q4. `alam2ndGeneration3D2024` is still cited. |
| C3 evidence ledger → App. H | correct | `part5:163` points to the table "in Appendix H"; App. H points back; the "Two patterns" paragraph stayed. |
| C4 `tab:op-sequence`, write buffer | correct | No reference to the removed table. Title note: Q15. |
| C5 page-table example | correct | TLB reach and the "low 12 bits" sentence (`part2:212`) that `:218` relies on are still there. |
| C6 "Beyond SRAM" | correct | Points to `sec:llc-alternatives`; Mittal and Kim are still cited. |
| C9 NPS figure | correct | `tab:nps-modes` kept; file orphaned (Q11). |
| C12 merged topology table | correct | All 22 values recomputed: chain 7/1 and 63/1; ring 4/2 and 32/2; fat tree 6/4 and 12/32; mesh 14/8; torus 8/16; hypercube 3/4 and 6/32; butterfly 4/4 and 7/32. |
| C13 ED² | text correct; **map leaf remains** | Q3. |
| F1 short captions | correct, **except two** | Q2. See also Q12. |
| CPI examples | correct | `part2:44` reads as a conclusion; `eq:cpi-stalls` is still referenced. |
| AMAT examples | **one number wrong** | Q5. Cited, and says the miss rates are illustrative. |
| Address split | correct | 27-bit tag = 48 − 6 − 15; `sec:address-example` (`part2:141`) is referenced from the TLB section (`:218`). |
| Overlap example | correct | 50–150 and 25–75 cycles. `eq:mlp-stall` is now unreferenced (Q11). |
| Directory overhead | correct | N/512; 12.5% for 64. |
| Amdahl | correct | Section 5.2 and its equation remain; `part3:188` still refers to it validly. |
| MSI trace | correct | `tab:msi-example` is intact and App. F's directory table repeats its five accesses. |
| Rome silicon | correct | 592/1008 = 59%, 416/1008 = 41%; the derivation of 1008 mm² is still at `part3:13`. |
| Shared counter | correct | 2 × 10⁶ × 58.6 ns = 0.12 s; × 265 ns = 0.53 s; × 400 ns = 0.80 s. |
| Lost context | correct | Every number in Findings, the abstract and the Conclusions that was searched for still appears in the body (section 7, anchors). |

---

## 5. Optional cuts

None re-opens the simulation section, the maps, the Cezanne comparison, the Findings or the abstract. K4 and K5 were offered in v9 (as C7 and C8) and not taken; they are listed again only because they are the largest remaining passages of their kind.

| ID | Location, length | Cut or shorten to | Why the argument does not need it | Everything that must change with it | Pages saved |
|---|---|---|---|---|---|
| K1 | `part2-foundations.tex:178–180` (section 4.6, write-through and write-back; about 0.3 page) | Two sentences: a store first brings in the whole block; a write-back cache writes a block down only on eviction, so writes are cheap and evictions carry the traffic. Keep `:182` (write-backs cross the die-to-die link), which is the point the paper uses. | Textbook explanation the reader knows; only `:182` is used later. | Keep one `\cite[sec.~11.2.3]{sarangi2025basic}`. No label, figure or table is involved. Apply Q15 with it. | about 0.25 |
| K2 | `part2-foundations.tex:284`, last sentence (the (0,1), (1,2), (2,2) example) | Delete the sentence. | Illustrates the order axiom, which the paper does not use again. | Nothing. | about 0.05 |
| K3 | `part2-foundations.tex:212–214` (pages, frames, page table, TLB; about 0.3 page) | Three sentences: addresses are translated page by page; with 4 KB pages the low 12 bits pass through unchanged; recent translations are cached in a small TLB whose misses cost tens of cycles. | Textbook basics. | **Keep the "low 12 bits" sentence**: `:218` and the tag paragraph at `:140` depend on it. Keep one Sarangi 11.4.3 citation. `sec:virtual-memory` (3 references) keeps its heading. | about 0.2 |
| K4 | `part2-foundations.tex:143` (Wang's Z-order L1 cache; about 0.25 page) | Delete. | About L1 layout for matrices and images, away from the central question. | **This is the only citation of `wangDesignImplementationCache2019`**: its reference entry disappears, its README row becomes unused, and its key in the `DeclareSourcemap` at `preamble.tex:76` becomes dead (harmless). Reference numbers after it shift (automatic). | about 0.25 |
| K5 | `part3-chiplets.tex:222` and `fig:two-socket` (Fig. 23, p. 54; about 0.5 page) | One sentence on xGMI links reusing PCIe lanes; drop the figure. | Lane budgeting is product configuration. | Remove the `\Cref{fig:two-socket}` sentence and the figure's `\input`; `amd2022epyc7003` stays cited elsewhere. | about 0.5 |

**Total:** K1–K3 about 0.5 page of text, which should also pull Fig. 13 back from p. 42 (Q10) and so remove one page; with K4 and K5 about 1.25 pages of text.

---

## 6. Fix order and final checklist

1. **Modular fixes**, in this order (later ones do not disturb earlier line numbers): Q6 (`appendix-e:60`, `part5:507`), Q9 (`part1:182`), Q5 (`part2:114`), any of K1–K5 and Q15 from the end of Part II backwards, then the figure files Q2, Q3, Q4, Q7, Q8, then Q1 in `preamble.tex`.
2. **Ishan's items:** type the Appendix A and B results as text or a table, in the "the tool displayed…" wording; remove `\todo` and `todored` (rest of Q1); set `\draftdate` in `metadata.tex:7`.
3. **Rebuild the modular PDF** (`scripts/build-linux.sh all --initial-draft-2 --install`, in steps if it exceeds the time limit). Log: 0 errors, 0 overfull, nothing undefined.
4. **Regenerate** the single file: `python3 scripts/flatten-initial-draft-2.py build/submission-final/ELL305-Term-Paper.tex`.
5. **Compile it alone** in an empty folder with the order in its header, on MiKTeX or another current TeX without the shim, and copy the PDF beside it.
6. **Compare:** same page count; `pdftotext -layout` of the single-file PDF and the modular PDF identical.
7. **Search the regenerated `.tex` and PDF text:** `TODO`, `todo`, `verify`, `Target length`, `Planned content`, `ED$^2$`, "of  under", "of  as", "4.9\% Lam measured" — expect no match; "No solder" — expect one.
8. **Look at these pages:** cover; pp. 11 and 13 (lists, Q2); p. 26 (Fig. 5); p. 63 (Fig. 27); p. 67 (Fig. 31); p. 85 (Fig. 43); pp. 135–136 (Appendices A, B); p. 143 (listing colours); the last page of Part II.
9. **Simulator**, only if anything under `tools/cachesim` changed (nothing has): `--selftest`, `check_golden.py`.
10. Upload exactly the two files in `build/submission-final/`.

---

## 7. Spot-checked numbers

"Recomputed" = arithmetic redone. "Source" = found in the local PDF's text (or, where stated, read from a rendered slide by OCR or pixel measurement). Numbers 1–22 are in text that changed since v9.

| # | Number (location) | Method | Result |
|---|---|---|---|
| 1 | Merged topology table, 22 values (`part2`, Table 7) | Recomputed from the formulas | correct |
| 2 | AMAT: average about 1.5 ns (1.46, 1.60) | Recomputed from the cut table's latencies | correct |
| 3 | AMAT: "memory adds about half a nanosecond" | Recomputed: 0.37–0.41 ns | **Q5** |
| 4 | L3 tag 27 bits (48 − 6 − 15); L1 index + offset = 12 bits | Recomputed | correct |
| 5 | 48-bit physical address on EPYC 7003 | A text search of the SEV guide found no match (the value may sit in a table that does not extract); the README records it at p. 10 | cannot verify here |
| 6 | Overlap: 50–150 and 25–75 cycles | Recomputed | correct |
| 7 | Directory: N/512; 12.5% for 64 | Recomputed | correct |
| 8 | Amdahl limit 20 for 5% sequential | Recomputed | correct |
| 9 | Rome: 592 mm² (59%), 416 mm² (41%) of 1008 mm² | Recomputed | correct |
| 10 | "~1000 mm²" cumulative area (Suggs, slide 19) | Source (OCR of the slide) | correct |
| 11 | 74 mm² CCD; 14.6 GT/s; 1.46 GHz FCLK; about 55 GB/s; 9-2-9 and 5-2-5 packages | Source (Naffziger) | correct |
| 12 | Shared counter 0.12 / 0.53 / 0.80 s | Recomputed | correct |
| 13 | 265/58.6 = 4.5; 265 − 59 = 206 ns; 206/18 ≈ 11; cross-socket ≈ 1.5 × cross-CCD | Recomputed | correct |
| 14 | libx264: 40–120, 15, 25–105 cycles; 735 and 699 cycles; 3–14%; 4.9% fewer cycles; 5.1% IPC gain; ≈130 cycles | Recomputed | correct |
| 15 | DCS: 3.2 and 3.7 accesses; +15%; predicted 0.24 MPKI | Recomputed | correct |
| 16 | Waterfall caption: 735 − 52 + 15 = 698 against 699 | Recomputed | correct |
| 17 | S3 check: 3.78 accesses, 1.44 misses, 729 cycles, 5.2% | `s3_validation_libx264.csv` (37.5 MB row: 3.778, 1.436, 729.0, 5.19) | correct |
| 18 | Simulated break-evens 0.04 (equal clocks) and 0.38 (7.3% gap) | `s3_breakeven.csv` (0.041, 0.376) | correct |
| 19 | S4: 108.5/49 = 2.2; 25 ns and 110 ns per message; "2.4 times too fast" | Recomputed (58.6/24.5 = 2.39; 265/110 = 2.41) | correct |
| 20 | 5600X: L3 51–55 against 47 cycles; 98.6 against 82 ns ("about 20%") | Recomputed (8–17%; 20.2%) | correct |
| 21 | Bonding-yield threshold 139.3/154 ≈ 90% (App. C) | Recomputed (0.905) | correct |
| 22 | Fig. 28(b): seven node positions | Pixel measurement of Wuu slide 6 | correct (section 4, P7) |
| 23 | Domke: 9.56× average for cache-sensitive HPC applications | Source | correct |
| 24 | Domke: up to 3.4× on MiniFE; 280 W TDP; 100³ to 400³ | Source | correct |
| 25 | Lawenda: clocks 2.9–3.2 GHz (Milan) and 2.8–3.0 GHz (Milan-X) | Source (Table 5) | correct |
| 26 | Lawenda: L3 miss rate down by up to 30 percentage points | Source | correct |
| 27 | Lawenda: each test repeated five times (App. H) | Source | correct |
| 28 | Lawenda: 10 000–200 000 and 15 000–100 000 cells per core | In charts only | cannot verify from text |
| 29 | Chips and Cheese (Milan-X): about 25% more bytes per cycle; about 12.5% lower for a whole CCD | Source | correct |
| 30 | Chips and Cheese: AMD's L3 latency 24–28 cycles lower | Source | correct |
| 31 | Chips and Cheese latency article: 342 and 313 cycles; 89 and 106 ns; 47.49 cycles | In chart images; text confirms only "Milan-X is boosting better" | cannot verify from text |
| 32 | Zen 2 efficiency: 1.15× from IPC (Suggs, slide 4) | Source (OCR) | correct; 1.17× and 1.47× not legible by OCR |
| 33 | White paper: "depending on the performance and power requirements"; 9174F, eight dies with two active cores; "spreads the thermal load…"; "on top of each CPU die"; up to 1152 MB | Source | correct |
| 34 | TechSpot 5800X: 16%, 30%, 26%, 27%, 23%; about 4.55 GHz; about 20 W more than the 3700X | Source | correct |
| 35 | Mittal and Vetter: SRAM caches could occupy 90% of chip area | Source | correct |
| 36 | AMD IMAPS 2024: 9 µm minimum pitch; face-to-back; 7 nm cache die; "2nd Generation" | Source | correct |
| 37 | AMD press release: cache "relocated below the processor"; "2nd Gen" | Source | correct |
| 38 | 9800X3D specifications: 96 MB L3; TSMC 4 nm; I/O 6 nm; 5.2 GHz boost | Source | correct |
| 39 | 300/5500 = 5.5% | Recomputed | correct |
| 40 | Phoronix EPYC: 2.45 and 2.2 GHz base, 3.5 GHz boost, 768 MB | Source | correct |
| 41 | Black et al.: 13% average; off-die bandwidth −66%; +0.08 °C; 88.35 °C | Source | correct |
| 42 | EPYC 7003 overview: 512 KB L2 per core, up to 4 MB L2 and 32 MB (96 MB) L3 per CCX | Source | correct |
| 43 | Lambert 2025: "Continued strategic use of 2.5D…"; < 9 µm; < 40 µm; "2.5D EFB" | Source | correct |
| 44 | 7-cpu: L3 47 cycles; memory 47 cycles + 74 ns | Source | correct |
| 45 | 4 and 48 MB of L3 per core (384/96; 768/16) in the Conclusions | Recomputed | correct |
| 46 | Sarangi chapters cited: 7, 9, 10, 11, 12 | Counted in the sources | correct |
| 47 | √2 per two years: 130 nm (2001) → 22 nm (2011) | Recomputed (130/2^2.5 = 23) | correct |
| 48 | 5600X comparison: `model-comparison.csv` | Regenerated; byte-identical | correct |

**Consistency anchors.** Each was searched across all sources and is consistent in value and wording: 4 cycles and 96 MB; 7% (1.073) and 4.8 against 5.15 GHz; 130 apparent cycles and 103 in the simulation; break-evens 0.1 (0.12 at 4.2 GHz), 0.35 and 0.50; simulated 0.04 and 0.38, each time with "not an independent check" or "expected rather than independent"; 9, 18 and 37 ns, the last always tied to a ratio; 58.6, about 265, 49 and 98.5 ns; about 2% link power; the 5600X triple (L1 and L2 agree, L3 and memory within about 20%, up to 2.4 times at 32 MB); 100/108/121 mm², 0.7–3% and about 90%; about 800 mm² and 1008 mm²; 4.9 times cost at 5 nm ("almost five times" in Part I); "first two generations (Zen 3 and Zen 4)"; "cache-on-top"; "the simulation" for model results. The one inconsistency found is Q6.

**Simulation.**
- `g++ -O2 -std=c++17`: builds; `--selftest`: 0 failures.
- `test/check_golden.py`: 15 of 15 identical. `node test/crosscheck.js` (Node 22): "C++ and JavaScript results identical".
- `sims.py --only s0 s4 policy` rerun from nothing (660 simulator runs, in three sessions of under three minutes because of the workspace's time limit, with a wrapper that stores finished runs): `s0_latency_sweep.csv`, `s0_calibration.csv`, `s4_pingpong.csv`, `s4_split.csv` and `s1_policy.csv` are all byte-identical to `research/measurements/cachesim/`.
- `compare_5600x.py`: `model-comparison.csv` byte-identical; the two figure files differ only in the caption line (Q12).

**Citations.** All 36 cited keys exist in `references.bib` and have a PDF row in `research/pdfs/README.md` (the textbook is in `sources/`). In the sample above no source is cited for a claim it does not make, and AMD's figures are attributed to AMD. **Overreach and over-hedging:** none found in the changed text, Part I, the abstract or the Conclusions; model outputs are labelled as such wherever they appear there, and after C1 the caveats are no longer repeated to the point of weakening the results.

---

## 8. Page counts (printed pages)

| Part | Pages | Count |
|---|---|---|
| Front matter: cover, copyright, acknowledgements, abstract, contents (6), List of Tables (2), List of Figures (3), glossary (2) | cover + 1–16 | 17 |
| I Introduction and research framing | 17–25 | 9 |
| II Architectural foundations | 26–42 | 17 |
| III Chiplet-based architecture | 43–62 | 20 |
| IV 3D-stacked cache | 63–82 | 20 |
| V Case study and quantitative analysis | 83–116 | 34 |
| VI Synthesis, limitations, future directions | 117–131 | 15 |
| References | 132–134 | 3 |
| Appendices A–H (A 1, B 1, C 3, D 1, E 3, F 3, G 3, H 1) | 135–150 | 16 |
| Index | 151 | 1 |
| **Body (I–VI)** | 17–131 | **115** |
| **Total** | | **152** |

---

## 9. What was checked and found correct

- **The two files:** compile alone; text identical to the modular build; up to date; self-contained; clean log; correct index and glossary; correct PDF properties (section 3).
- **Format and course rules:** page size, margins, page order, generated lists, programmatic diagrams, code in an appendix with colour, chapter mapping and advisor (section 3).
- **v9 fixes and cuts:** all present; the exceptions are Q2–Q9 (section 4).
- **References between parts:** 231 labels, none duplicated and none undefined; every figure and table label is referenced; no sentence refers to a removed table, figure, equation or example ("example above" occurs once, in App. C, about its own numbers).
- **Floats:** no float is far from its first reference except deliberate forward references from Part I and tables placed in appendices. Mostly empty pages: Part title pages, p. 42 (Q10), the last page of Part VI (p. 131), Appendices A and B (known), p. 146 (Table 48) and the index.
- **Text size and overlap** on all 152 pages, from the PDF's text boxes: Q7 and Q8 are the only cases.
- **Simulation, measurements, citations and anchors:** section 7.
