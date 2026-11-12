# Response to the final pre-submission review (v9)

Date: 10 November 2026. Review: `research/review-initial-draft-2-v9-final.md`.

Ishan's decisions:
- Submit two files only (one `.tex`, one PDF), with no ZIP.
- He will make the repository public for viewing himself.
- Apply all P fixes, the safe cuts, short captions and the cuts of textbook-style worked examples. C7 (Wang), C8 (two-socket), C10 (Findings), C14 (abstract) and R1–R4 were not taken.
- Keep the individual `.tex` files for editing, and generate the submission file from them.

**Result:**
- Modular build: 152 pages, down from 162; the front matter is 17 pages, down from 24.
- 0 overfull boxes, no undefined references, all 117 labelled floats referenced.
- The single-file build compiles alone in an empty folder to text identical to the modular PDF.

## P items

| ID | Status | What was done |
|---|---|---|
| P1 | Fixed | `scripts/flatten-initial-draft-2.py` merges every `\input` and embeds the bibliography (`filecontents*`) into `build/submission-final/ELL305-Term-Paper.tex`. It compiles alone in an empty folder, and its PDF text is identical to the modular build. Compile order (stated in the file header): pdflatex, biber, makeglossaries, pdflatex ×2, makeglossaries, makeindex, pdflatex ×2. The earlier order left the index one page off in a fresh folder. The modular files stay the editing source. |
| P2 | **Open (needs Ishan)** | Appendices A and B still need the plagiarism report and readability indices, run on the final text. They will be entered as text, not images. |
| P3 | Fixed except the date | Cover status line now "Term Paper"; PDF title and author set to the paper's own. **The submission date is still 8 November** (`\draftdate` in `metadata.tex`), waiting for Ishan. |
| P4 | Fixed | the project instructions §5 and `notes/Planning/Submission Format.md` now say two files, no ZIP. |
| P5 | Fixed | Colour syntax for listings, set in `initial-draft-2/preamble.tex` (Draft 1's style unchanged). |
| P6 | Ishan | Repository to be made public by Ishan; links kept. |
| P7 | Fixed | Fig. 28(b) is shape-only, with node labels at the slide's positions and the 2004–2012 trend line; the caption says so. |
| P8 | Fixed | "Chapters 7 and 9–12" in Part I, Part II and the Part II comment. |
| P9 | Fixed | Part I methodology states the chapter mapping (mainly 11 and 12; foundations from 7, 9, 10) and that this makes Prof. Sumantra Dutta Roy the advisor. |
| P10 | Fixed | 4.9% fewer cycles (5.1% IPC gain from chart values; Lam states 4.9%), in Part IV, Part V and App. F. |
| P11 | Fixed | "the 37 ns hop to a measured ratio". |
| P12 | Fixed | "the simulation's overlap factor", "In the simulation the overlap factor"; file comment updated. |
| P13 | Fixed | `\tiny` → `\scriptsize` in the listed figures. The CCD figure shows "L2" in the boxes, with 512 KB moved to the caption. `horizontal-vs-vertical` is scaled up instead, because larger type overlapped. |
| P14 | Fixed | Refresh box now joined to the sense-amplifier row. |
| P15 | Fixed | Fig. 4: Part V branch "Cache against clock; simulation", Part VI "Strength of evidence". |
| P16 | Fixed | "This calculation …" in Apps C and F. The label `app:worked-examples` is kept (no visible effect). |
| P17 | Fixed | The flattener drops every full-line comment outside `filecontents*` blocks. No tool, script or AI names remain in the submitted `.tex`. |
| P19 | Fixed | 14 of 15 long sentences split; the remaining one is the equation-definition sentence pair in Part V. |
| P20 | Fixed | "a 2.5D bridge (labelled EFB on AMD's slide)"; Lambert's slide gives no expansion. |
| P18, P21 | No change needed | — |

## Cuts

| Cut | What was done |
|---|---|
| C1 | Repeated caveats shortened to one full statement plus references:<br>• prefetch caveat in Part V (two places) and App. E;<br>• 5600X details removed from Threats (kept in S0, App. G and the evidence table);<br>• the qualifier on the 4.5× figure dropped from the Part III summary. |
| C2 | The hybrid-bond chemistry is cut to two sentences (no solder, so a fine pitch); the map leaf is changed to match. |
| C3 | The evidence ledger table moved to a new App. H (`app:evidence-ledger`); the summary paragraph stays in Part V. |
| C4 | Cut `tab:op-sequence`, and shortened write buffer / critical word to one sentence. |
| C5 | Cut the two-level page-table example, CR3 and the page-fault detail. |
| C6 | Part II "Beyond SRAM" cut to one sentence pointing to `sec:llc-alternatives`. |
| C9 | `fig:nps-modes` removed (`tab:nps-modes` kept). |
| C12 | Topology tables merged into one (formula plus N = 8 and N = 64 columns). |
| C13 | ED² section removed. |
| F1 | Short captions for all 119 floats (13 maps through `\mapfigure`). |

**Worked-example cuts:**
- **Cut to their conclusions:** the CPI-with-stalls example, the CPI-34 example, the textbook AMAT example, and the AMAT example on the 3700X and 5800X (one sentence, still cited).
- **Reduced to a short paragraph:** the address split (on tag storage and VIPT indexing).
- **Shortened:** the overlap example and the directory bit-vector.
- **Removed:** the Amdahl figure and numbers.
- **Kept, without their headings:** the MSI trace text and table, because App. F needs them.
- **Part III:** the Rome silicon example becomes one sentence (59/41% split), and the shared-counter example becomes one sentence.

Every research calculation was kept.
