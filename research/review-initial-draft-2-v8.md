# Eighth review of initial-draft-2 (9 November 2026)

No v8 brief exists, so this pass repeats `research/review-prompt-initial-draft-2-v7.md` on the current 164-page draft. Findings are numbered N1, N2, …, and the regression list is M1–M29 from `review-initial-draft-2-v7.md`.
Only local files were used; nothing on the web. No project file other than this report was changed, and all reruns went to a temporary folder.
Page references are **PDF viewer pages** of `build/pdf/ELL305-initial-draft-2.pdf`. Line references are to `initial-draft-2/` unless a full path is given.

**Build currency.** The PDF was built on 9 Nov 2026 at 03:30:23. No file under `initial-draft-2/`, `paper/` or `references/` is newer. Build log: no errors, no undefined references or citations, **0 overfull boxes**, 35 underfull boxes. `pdfinfo` gives 164 pages, A4.

**How this pass differs from a cold review, and what it did not do.**
- The same reviewer wrote the seventh review, so this is not a fresh pair of eyes. One finding (N2) comes from wording that review suggested.
- A word-level comparison of the old and new PDF text listed every change (about 400 edits, most of them caption full stops, reflow or the listed fixes). Each change was read. Unchanged text was re-examined for new problems, and N3–N5 and N8 come from that, but it was not all re-verified line by line.
- `test/crosscheck.js` was not run because Node.js is not installed here. `check_golden.py` was run instead.
- `sims.py` was rerun only for `s0 s4 policy`. S1–S3, S5 and S6 were not rerun, but all their figures and tables were regenerated from the stored CSV files.
- Of the 61 figure pages, 26 are pixel-identical to the pages read in the seventh review (headers and page numbers excluded) and were not read again. Five more differ only by a caption full stop or a single pixel. The other 30, including Fig. 55's new page, were rendered at 125 dpi and read.
- `Gem5/` is out of scope.

---

## 1. Overall assessment

The paper remains strong for an undergraduate term paper, and I hold it provisionally at A−, close to A. The M fixes are nearly all present and correct: the 37 ns hop is now described honestly, the 5600X status is right, the simulated 0.38 carries its limit, and the terminology for generations and hops is consistent. Every rerun is identical to the stored files, and all fresh spot-checks against the sources passed. One fix went wrong: to remove four lines from Appendix C, the edit deleted the worked example's limit, including the bonding-yield break-even that L3 and J2 had corrected, and the response file says the cut was made elsewhere (N1). The new RQ3 sentence claims that no thermal measurement of a V-Cache part was found, while Part IV reports one (N2). A fresh look at unchanged text found two overstated engineering conclusions (N3, N8), one inconsistent explanation (N4) and a small factual slip (N5). None of these changes a main conclusion, and each is a one-sentence edit.

**The two changes that would improve the paper most:**
1. Restore the limit in Appendix C (N1).
2. Correct the claim about thermal measurements in RQ3 and in Threats (N2).

---

## 2. Findings (most severe first)

| ID | Severity | Location | What the draft says | What the source, CSV, code or rule says | Suggested correction |
|---|---|---|---|---|---|
| N1 | Error (regression from the M27/M28 fixes) | `appendix-c:66` (p. 152); `research/review-initial-draft-2-v7-response.md`, row M28; also `appendix-f:33` (p. 158) | App. C's closing paragraph now ends at "so the mix can follow demand." | The deleted text held the argument's limit: (C) loses its advantage over (A) for V-Cache parts below about 139.3/154 ≈ 90% bonding yield, and at the same point its lead over (B). That is the point L3 and J2 corrected, and the brief's consistency list requires it. It now appears nowhere; `part4:266` gives only the planar-die version. The response says duplicated sentences were removed "from the main text (`part4:268`, `part2:390`)", but those sentences are still there, and the deletions were from App. C and App. F. | Restore in App. C: "The table also shows the limit of the argument: below a bonding yield of about 139.3/154 ≈ 90%, strategy (C) loses its advantage over (A) for V-Cache parts, and at the same point its small silicon lead over (B), since (A) and (B) both spend 154 mm² on a V-Cache part." To keep the page count, cut the duplicated AMD sentence from `part4:268` as M28 intended. Correct the response. |
| N2 | Inconsistent (new sentence) | `part6:221` (p. 144), `part6:190` (p. 142) against `part4:220` (p. 89) | "No energy or thermal measurement of a V-Cache part was found; the only direct indication is the EPYC 9684X's default power of 400 W against the similar 9654's 360 W". Threats: "no published thermal measurement of a hybrid-bonded stack was found". | Part IV reports one: Cozma's 9800X3D "held its 4.7 GHz base clock while running at 95 °C" (Y-Cruncher, Noctua NH-D15; Cozma 2024). A temperature reading is a thermal measurement, though not one of what the stack adds. The 400 W and 360 W are rated defaults, not measurements, and the two parts also differ in clocks (2.55 against 2.40 GHz base). The sentence came from the seventh review's suggestion, which was too broad. | "No measurement of a V-Cache part's energy use, or of the temperature the stack adds, was found. The one temperature reported is a 9800X3D at 95 °C under load (`sec:thermal-evidence`), and the only power figures are rated defaults (400 W for the EPYC 9684X, 360 W for the 9654, which also differ in clocks)." Use the same wording in Threats. |
| N3 | Overstated | `part4:129` (p. 82); `part4:305` (p. 94) | The calculation "shows why a wide, parallel, cache-speed interface between two dies is practical only with 3D bonding". The 9 µm pitch is "what makes a wide, parallel, cache-speed interface possible and keeps the latency cost to four cycles". | The calculation rules out only C4 bumps (92 mm²). Micro-bumps need 5.3 mm². At the 2.5D pitch of Fig. 31 (625 per mm²) the same 4096 wires need 6.6 mm² of an 81 mm² die, so the arithmetic does not exclude 2.5D. `part4:118` says only that density "helps explain" the four cycles. | "…shows why such an interface is impractical at C4 pitch and costs several mm² at micro-bump or 2.5D pitch." Summary: "which allows a wide, parallel interface in little area and helps keep the latency cost to four cycles". |
| N4 | Inconsistent (unchanged text, new finding) | `part2:52` (p. 37) against `part1:14` (p. 25) | "The same reasoning explains why designers stopped raising clock frequency by deepening pipelines (`sec:intro`), and why a design that reduces the stall rate … is a more durable source of performance than a higher clock." | The section cited gives a different reason: after about 2002 "power and temperature became the limit" (Sarangi sec. 12.1.2). The optimal-depth argument does not explain that. "More durable source of performance" is the paper's own judgement, placed directly after the textbook's conclusions. | "The optimal-depth argument shows that deepening pipelines has limits of its own, besides the power limit of `sec:intro`. In our reading, reducing the stall rate is therefore a useful alternative to a higher clock." |
| N5 | Error (small) | `part2:310` (p. 49) | "one CCX runs up to 16 hardware threads that share its 4 MB of L2 and 32 MB of L3". | The L2 is private to each core, 512 KB (`part2:259`, `tab:zen-progression`, Wuu slide 20). Only the two threads of one core share an L2. | "…16 hardware threads: each core's two threads share its 512 KB L2, and all share the 32 MB L3…". |
| N6 | Inconsistent (from the M14 fix) | `part1:176` (p. 32), bullet title | "Chiplets trade a small latency cost on every access for cost and flexibility." | The same bullet says "Every L3 miss pays". An L1, L2 or L3 hit pays nothing for the die-to-die link. `part3:152` and `part6:166` are safe only because their context is memory accesses. | "a small latency cost on every L3 miss". |
| N7 | Inconsistent (from the M2 fix) | `part5:532`, caption `figures/sim-pingpong.tex:20` (p. 125) | "Only the ratio can be compared", followed five sentences later by an absolute comparison: 25 against 58.6 ns and 110 against 265 ns. The caption says 37 ns "is not the real cost of a transfer, which `sec:cross-ccd` puts at about 206 ns". | The new comparison is right and useful, but it contradicts the sentence introducing it. The 206 ns is also from one cloud virtual machine, and Reguly warns that this may have affected the results (`part3:181`). | "Only the ratio can be fitted; the absolute values can be compared only roughly." In the caption: "…puts at about 206 ns on one cloud instance." |
| N8 | Overstated (inference stated as fact) | `part6:87` (p. 135) | V-Cache keeps SRAM and changes only its placement, "which is why it could ship in a mainstream product with the latency cost held to four cycles". | No source gives this as the reason. The paper's own evidence credits the bond, the short vertical connections and the design of the CCD. | "which is probably one reason why…". |
| N9 | Writing (from the M28 fix) | `part5:587` (p. 130) | "Against the group's Ryzen 5 5600X its inputs are close, and its latency close to each cache's capacity is too low". | "Close" is used in two senses in one clause, and "its" has to be traced back to the model a sentence earlier. | "On the group's Ryzen 5 5600X the model's input latencies are nearly right, but just above each cache's capacity its latency is too low." |
| N10 | Minor (terminology) | Abstract; `part1:180`; `part5:400`; `part6:170` | "in the first two generations". | `part4:216` says AMD's generation labels conflict and that the paper names designs by product. M7 was right to keep the phrase, but it is never tied to products at first use. | Abstract, first use: "in the first two generations (Zen 3 and Zen 4)". |
| N11 | Minor (title) | `part1:182` (p. 33) | "The group's own measurements bound the model." | The text does not give a bound. It gives an agreement on inputs and a one-sided error near capacity. | "The group's own measurements check the model's inputs and expose its limits." |
| N12 | Minor (tool file) | `tools/measurements/ELL305-5600X-kit.zip` | File date 8 Nov 12:05. | The kit's README and `run_all.sh` changed on 9 Nov (M16), so the zip holds the older text. It is gitignored and the paper cites the folder, not the zip. | Rebuild before giving the kit to anyone. |

**Writing: suggested rewrites (in addition to N9).** A script found 30 sentences of 55 words or more; these are worth changing.

| Location | Length | Rewrite |
|---|---|---|
| `part5:584` (p. 130) | 66 words, new | End after "within what the core sustains". Start "Where they exercise the model's own behaviour…". |
| `part1:180` (p. 33) | 61, grew with M4 | End after "per thousand instructions". Start "The controlled simulation, built on the same calibration and so not an independent check, gives 0.38 at that gap". |
| `part6:221` (p. 144) | 62 | End after "no growth in package footprint". Start "Its price is a harder heat path". |
| `part2:83` (p. 39) | 64 | Split at the semicolon. |
| `part3:287` (p. 69) | 63 | End after "through one link or two". |
| `part3:152` (p. 61) | 62 | End after "crosses the IFOP link to the IOD". Start "AMD nevertheless reports…". |
| `part3:376` (p. 73) | 62 | Make the semicolon-separated list a short list of items. |
| `part6:63` (p. 132) | 62 | End after "65 against 463 mW". |
| `part4:295` (p. 93) | 62 | Split at the second colon. |
| `part5:325` (p. 111) | 61 | End after "gained least or lost". |

Abbreviations: eDRAM, TSV, PBO and ω are defined at first use, and WSL2 is now expanded at its first use. No sentence attributes work to an individual, and no gendered pronouns occur (searched).

---

## 3. Regression check

| ID | Status | Note |
|---|---|---|
| M1 | Fixed | 1.25 and 1.35 recomputed. |
| M2 | Fixed | 25, 110, 2.4× and 97 ns recomputed. "Only the ratio" now clashes (N7). |
| M3 | Fixed | Part I, abstract, App. G. |
| M4 | Fixed | All three places. |
| M5 | Fixed | Table 1, Fig. 17 legend, Fig. 14. |
| M6 | Fixed | Row 1 now follows the caption; `part6:160` uses its classes. |
| M7 | Fixed | No "first-generation" remains in the text; see N10. |
| M8 | Fixed | |
| M9, M10 | Fixed | |
| M11, M12, M13 | Fixed | N9 is a side effect in one sentence. |
| M14 | Fixed, with a side effect | N6. |
| M15 | Fixed | Glossary and Fig. 13. |
| M16 | Fixed | README and `ANALYSIS.md` checked; zip is N12. |
| M17 | Fixed | Figs 50 and 63 rendered. |
| M18 | Fixed | Fig. 43 rendered. |
| M19–M25 | Fixed | |
| M26 | Fixed | Legend now below Fig. 56; all 55 table captions end with a full stop. |
| M27 | **Fixed, but regressed content** | The p. 154 overflow is gone because App. C lost its limit (N1). |
| M28 | **Partly fixed; response wrong** | 5600X framing shortened correctly. Duplicates were removed from the appendices, not the main text (N1). |
| M29 | Deferred by decision | Decide at submission. |
| Ten long sentences | Fixed | |
| RQ3 power sentence | Added, too broad | N2. |

**Earlier items.** L3 and J2's clause on (B) are **lost** through N1. The numbers 100/108/121 and 0.7–3% and the planar 90% remain. L1, L2, L4–L29 and K1–K21 hold where they touch changed text. J27 is restored in the two figures. J3 and J16 now read correctly with the M2 fix.

---

## 4. Simulation and measurement check

### 4.1 Reproduction

- `g++ -O2 -std=c++17` build succeeded (MSYS2 UCRT64). `--selftest`: **0 failures**.
- `check_golden.py`: **15 of 15 identical** to the stored JavaScript results (Node v22.23.4, 8 Nov). **No warning** that `gui/sim-core.js` changed.
- `sims.py --only s0 s4 policy` (2 min 41 s): five CSV files **byte-identical** to `research/measurements/cachesim/`.
- `compare_5600x.py`: `model-comparison.csv` **byte-identical**; both generated figure files differ only in line endings.
- `make_figures.py` from the stored CSV files: all 15 `sim-*` files differ from the paper's only in line endings.

### 4.2 5600X numbers checked

The raw results have not changed since the seventh review (file dates). The recomputation script was rerun. Medians of three runs unless stated; all match the new text.

| Claim | Raw value |
|---|---|
| L1 4.0 cycles | 0.868 ns × 4.614 |
| L2 12.1 cycles (12.0–12.4 across the level) | 2.614–2.695 ns |
| L3 51–55 cycles | 11.085–11.961 ns |
| 1 GB 98.6 ns; 4 KB pages 115.3 ns; about 17 ns | 98.562; 115.335; 16.77 |
| Model 82 ns; input 84 ns | 81.85; 84.2 |
| Up to 2.4× at 32 MB | 24.096/10.066 = 2.39 |
| 32 MB runs | 24.096, 23.936, 73.761 |
| Refit 1.2–2.1× at 19–38 MB | 1.22–2.08 |
| Refit 1.1–1.3× at 45–108 MB | 1.12–1.31 |
| 64 MB: 66.9 against 56.6 ns | 66.859; 56.593 |
| Overlap 0.349, 0.113, 0.071; L3 0.077 | as stated |
| 105 to 120 ns per step | 104.9 to 119.7 |
| Single L3 108 GB/s; memory 30 GB/s | 108.01; 30.29 |
| Six threads 41 GB/s; 280–296 GB/s for 8–16 MB | 40.95; 279.77, 295.79 |
| c2c 98.5 ns; CPU 0 responder 66–72 ns; fastest of three trials | 98.5; 65.8–72.1; `c2c.c` |
| Clock 4.614 GHz | before and after |

### 4.3 and 4.4 Model and kit descriptions

`cachesim.cpp`, `latency.c`, `bandwidth.c`, `c2c.c` and `clock.c` have file dates earlier than the seventh review, which compared App. E and App. G with them line by line. The only changes to those appendices are the hop row and the three-trials wording (M23, M24), and both are correct. Stated limits match the raw files: WSL2, the slow third 2 MB run, the 12-thread values (0.14–480.61 GB/s), and the CPU 0 pattern, now worded as "probably". No text claims that the model reproduces a cyclic chase.

### 4.5 Calibration against validation

All earlier cases are now labelled. Only N7 remains, as a wording conflict rather than a false claim. The genuinely out-of-sample results are the capacity-edge differences and the 49 against 98.5 ns round trip; both are stated and both are unfavourable.

---

## 5. Spot-checked numbers (34, chosen to differ from the seventh review's list)

| # | Claim (location) | Source and place | OK? |
|---|---|---|---|
| 1 | 130 nm in 2001 to 22 nm in 2011 (`part1:16`) | Sarangi Table 12.1 | ✓ |
| 2 | 32 or 64 cores in 5–10 years | Sarangi sec. 12.1.2 | ✓ |
| 3 | Pipelines and clocks rose until about 2002 | same | ✓ |
| 4 | 500 MB of page tables for 200 processes | Sarangi sec. 11.4.3 | ✓ |
| 5 | No appreciable difference, 35 and 200 processors | Sarangi sec. 12.2.3 | ✓ |
| 6 | Write buffer of 4–8 entries | Sarangi sec. 11.3.3 | ✓ |
| 7 | 200 °C uncooled; up to 120 °C | Sarangi sec. 10.10.1 | ✓ |
| 8 | DRAM cell 0.005 µm², 50–200 cycles | Sarangi Table 11.1 | ✓ |
| 9 | Exclusive caches "as of 2025"; Definitions 100, 114; Important Point 20 | Sarangi | ✓ |
| 10 | FCLK up to 1600 MHz with DDR4-3200 | EPYC 7003 overview | ✓ |
| 11 | New six-channel interleave mode | same | ✓ |
| 12 | 1 to 16 NUMA domains in two sockets | same (1, 2, 4, 8, 16) | ✓ |
| 13 | Three links: 80 lanes per socket, 160 | same | ✓ |
| 14 | 4, 8 or 12 CCDs "depending on the" requirements | 4th-Gen white paper | ✓ |
| 15 | "unit of innovation"; "swap in and out"; "on top of each CPU die" | same | ✓ |
| 16 | About 14 800 and 4700 cells per core | Lawenda: 14 821, 4715 | ✓ |
| 17 | Genoa, Rome, Milan 256 MB L3 per socket; miss rates to 80% | Lawenda | ✓ |
| 18 | EPYC 58.6, 265.2–266.2, 396.9–415.3 ns | Reguly Fig. 2, rendered | ✓ |
| 19 | 8360Y 0.1, 106.1–109.5, 228.3–233.9 ns | same | ✓ |
| 20 | Xeon Max 0.7, 83.6–84.4, 241.6–246.6 ns | same | ✓ |
| 21 | 16-way, 32 B/cycle, >2 TB/s, +4 cycles, own arrays | Wuu slide 20, rendered | ✓ |
| 22 | 512 × 128 KB, 1088 × 6 KB; VDDM and RVDD | Wuu slide 25, rendered | ✓ |
| 23 | Cost rises about a third from 7 to 5 nm (read) | Wuu slide 6: about 3.7 to 4.9 | ✓ |
| 24 | 416, 125, 74 mm² | Naffziger Fig. 2.2.1, rendered | ✓ |
| 25 | 90/141/234/128 and 94/104/201/0.81× | Naffziger Fig. 2.2.6, rendered | ✓ |
| 26 | Monolithic about twice the cost at 32 and 48 cores (read) | Naffziger Fig. 2.2.2, rendered | ✓ |
| 27 | 95 °C, 4.7 GHz base held | Cozma 2024 text (Y-Cruncher, NH-D15) | ✓ |
| 28 | About 20 µm; AMD-supplied sample; "biggest weakness" | Cozma 2024 text | ✓ |
| 29 | 3950X/5950X, 3900X/5900X, 3800X/5800X, 3700X, 3600/5600X rows | Ryzen datasheet p. 2, rendered | ✓ |
| 30 | Chiplet systems still far from all the benefits; shared design responsibility | Liu sec. on conclusions ("still a long way from") | ✓ |
| 31 | 11% slower; 15% system power; "basically no difference" | TechSpot 5700G | ✓ |
| 32 | 4 GHz, DDR4-3200 CL16 | CapFrameX | ✓ |
| 33 | Eq. 15; W2W "always" dearer | Dong and Xie | ✓ |
| 34 | Rectangular and triangular distributions | Murphy | ✓ |

**Worked examples recomputed (all correct).** New in this draft: 1.25 and 1.35× (S4), 25, 110 and 97 ns (S4). Rechecked: yields; 44% and 63%; dies per wafer and factors 2.7, 1.9, 3.5; `tab:stack-yield`; **App. C product line** 100/108/121, 101/110/124 and 0.7–3%; `tab:cache-clock-model` and break-evens; **App. F** 18 messages, 35 and 315 deliveries, TLB reach and 24 576 pages; `tab:lam-per-miss`; AMAT; Amdahl; pad densities; link powers. N3's 6.6 mm² is 4096/625.

**Internal consistency (brief item 5).** All listed quantities agree, except that "about 90% bonding break-even" now survives only for the planar-die comparison (N1).

**Citations.** All 36 cited keys are in `references.bib`, each with a README row marked present and the file on disk. The only uncited bib key is `swaminathanNextFrontierEnabling2022`. Vendor attribution is sound in every place checked, including the 19% and "under 9 ns".

---

## 6. Research questions and argument

| RQ | Answered in Conclusions? | Supported? | Consistent with `tab:evidence-strength`? |
|---|---|---|---|
| RQ1 | Yes (`part6:215`) | Yes | Yes, now that row 1 follows the caption |
| RQ2 | Yes (`:217–219`) | Yes; power is an estimate and says so | Yes |
| RQ2a | Yes, inside RQ2 | Yes, with AMD's reasoning attributed | No separate row; adequate |
| RQ3 | Yes (`:221`) | Yes for capacity and latency; thermal indirect; the new sentence overreaches (N2) | Yes |
| RQ4 | Yes (`:223`) | Direction and latency well supported; size moderate; model illustrative | Yes |

**Overreach.** N2, N3, N4, N8. **Over-hedging.** None found.

**The three weakest links.**
1. **How much a stacked cache helps in general.** Fully controlled evidence covers six workloads on one processor. The paper says so; only a broad fixed-clock study would change it.
2. **The break-evens rest on one program and borrowed clocks.** The simulated 0.38 is now correctly marked as not independent. Presenting the headline as "of order 0.1 to 0.4 for this program" would fit best.
3. **Power and heat.** RQ2 rests on one predecessor link figure, and RQ3 on rated power and indirect thermal evidence. The paper now says this, once N2 is corrected.

**Anything important still missing.** Only a measurement of a V-Cache part's energy use, which the group cannot obtain without such a part.

---

## 7. Page counts per part (PDF pages)

| Part | Pages | Count | Target | Comment |
|---|---|---|---|---|
| Front matter | 1–24 | 24 | — | In order |
| I Introduction | 25–34 | 10 | 10 | On target |
| II Foundations | 35–54 | 20 | 25 | Short by 5 |
| III Chiplets | 55–74 | 20 | 25 | Short by 5 |
| IV Stacked cache | 75–95 | 21 | 25 | Short by 4 |
| V Case study | 96–130 | 35 | 25 | Over by decision |
| VI Synthesis | 131–145 | 15 | 20 | Short by 5 |
| **Body** | 25–145 | **121** | 130 | Short by 9; no padding is advised |
| References | 146–148 | 3 | — | |
| Appendices A–G | 149–163 | 15 | — | |
| Index | 164 | 1 | — | |

Each part does one job and hands over cleanly.

---

## 8. What was checked and found correct

**Format.** A4 (595.3 × 841.9 pt); `12pt` class option; `\singlespacing`; one-inch `geometry` margins; order cover, copyright, acknowledgements, abstract, contents confirmed on pp. 1–5; contents, lists of tables and figures, glossary and index generated. All diagrams are TikZ or pgfplots (the only image is the logo). There are no waveforms. Code appears only through `lstlisting`.

**Leftovers.**
- Two `\todo` notes: App. A (p. 149) and App. B (p. 150), known placeholders, not counted as errors.
- Cover line and PDF title still say "working draft", correctly for now.
- The `\partbudget` macro with "Target length" remains defined at `preamble.tex:23–25` but does not print. "(target: about N pages)" remains only in source comments.
- No `\verify` use, no "??", no undefined references or citations, no overfull boxes.

**Float placement.** Of 119 floats, 8 sit exactly two pages from their nearest reference (Figs 2, 15, 34, 41, 62; Tables 22, 26, 44). `tab:llc-alternatives` is on p. 134, three pages after its first citation on p. 131. Appendix tables and forward references from earlier parts lie further away, as intended. Sparse pages are p. 95 (end of Part IV), pp. 149–150 (placeholders) and p. 160 (table at the end of App. F).

**Figures.** Figs 13, 14, 17, 43, 50, 51, 52, 54, 55, 56, 57 and 63 and the mind maps on changed pages were read. No overlaps or unreadable labels were found. Every figure and table is referenced. Mind-map text is unchanged in style and adds no claim the text lacks.

**Correct in the material new since the seventh review.** The S4 rewrite's numbers; the 5600X wording in the abstract, Findings, S0, limits, Threats and evidence row; the cache-on-top terminology; the tool documents; the restated evidence caption.
