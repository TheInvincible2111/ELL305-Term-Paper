# Fourth-brief review of initial-draft-2, re-run on the corrected draft (8 November 2026)

Brief: `research/review-prompt-initial-draft-2-v4.md`. Only local files were used; nothing on the web.

**Why this file has this name.** The brief says to write `research/review-initial-draft-2-v4.md`, but that file already exists: it is the earlier fourth review (I1–I43), dated 8 Nov 02:57, and `-v4-response.md` answers it. Overwriting it would destroy that record, so this pass is saved here and its findings are numbered **J1, J2, …** so they cannot be confused with the I-series. No other file was changed.

**The brief describes an older draft.** It gives 155 pages, an overlap factor of 0.42, break-evens of 0.04/0.29, `work_cycles` = 0.31 and a `verbatim` block in Appendix E. All of those were superseded when I1–I43 were applied (now 160 pages; overlap 0.335; break-evens 0.04/0.38; 0.48; `lstlisting`). I checked the paper as it stands and say so where a value in the brief no longer applies. Because of that, §3 also gives the status of the I-series.

Page references are **PDF viewer pages** of `build/pdf/ELL305-initial-draft-2.pdf` (the printed number is one lower). `part5:433` means `initial-draft-2/sections/part5-case-study.tex`, line 433.

**Build currency.** The PDF was built on 8 Nov 2026 at 03:44 (`pdfinfo`). The newest file under `initial-draft-2/` or `paper/` is `part5-case-study.tex`, 03:43, so the PDF matches the sources. Build log (`tmp/linux-build/main-initial-draft-2.log`): no errors, no undefined references or citations, 0 overfull boxes, 26 underfull boxes.

---

## 1. Overall assessment

This is strong undergraduate work, and the corrected draft is clearly better than the one the earlier fourth review saw. I would place it in the A− band: the argument is coherent, almost every number I re-derived is right, and the paper is unusually honest about vendor claims and confounds. The simulator is reproducible: a full rerun matched all 16 stored CSV files byte for byte. What holds the grade below a clean A is a small group of interpretive errors around the model and one worked example. The replacement-policy "sensitivity test" was run on a workload where the policy cannot matter. The product-line silicon example contradicts the paper's own bonding-yield formula. The fitted 37 ns hop is compared with the wrong physical quantity. The headline "roughly triples" is not what the simulation shows. None of these overturns a conclusion, but an examiner who reads the code would find the first and third. The two weakest parts of the argument remain that the model has never been tested on anything it was not fitted to, and that stacking economics rest on silicon area alone.

**The two changes that would improve the paper most:**
1. Fix the model's interpretation (J1, J3, J5, J6, J7), and give it one out-of-sample test, either the 5600X kit or a pointer-chase workload plus randomised page placement.
2. Correct the product-line example (J2) and bring the headline claims in the Abstract, Findings and Conclusions into line with what the evidence shows (J6, J8, J9, J10).

---

## 2. Findings (most severe first)

| ID | Severity | Location | What the draft says | What the source, CSV, code or rule says | Suggested correction |
|---|---|---|---|---|---|
| J1 | Error (invalid test) | `part5:433`, `:509`; `appendices/appendix-e-simulation.tex:49`; `figures/sim-table-sensitivity.tex`; PDF pp. 119, 128, 158 | "The replacement policy is not the cause, since changing it alters the results by less than 0.05%." "The replacement policy changes nothing measurable." The random workload is "like the pointer-chasing test of a latency sweep". | The sensitivity runs use only `kind=random` (`sims.py:296`), and that workload draws each line independently and uniformly (`cachesim.cpp:434`). Under independent uniform access every evicted line is equally likely to return, so no policy can matter. The result is built in. A pointer chase is different: it visits each line once per pass. Reviewer's runs, 64 MB, 32 MB L3: `hotcold` gives 60.83 (LRU), 62.84 (random), 59.65 (PLRU) cycles; `sequential` (cyclic) gives 343.0 (LRU), 305.8 (random), 343.0 (PLRU). Against that, the model's i.i.d. value is 195 and Milan's measured value is about 240, so the measurement lies between the two model access patterns. | Delete both claims and the "like the pointer-chasing test" clause. Say: "The random workload is insensitive to replacement by construction, so this comparison says nothing about policy." Name i.i.d. access as a further reason the model and the sweep differ. Add a cyclic-permutation workload and re-run S0. |
| J2 | Error | `part4:269`, `:273`, `tab:product-line-silicon` (`:287`), `:292`; Part IV summary `:329`; PDF pp. 94–96 | Strategy (C) adds "$44.5/0.95 \approx 46.8$" mm² to the CCD's 94.8. (C) = 99/107/118 mm². "The saving in silicon is small, 1–6%." (C) loses to (A) "only if the bonding yield falls below about 75%". | `eq:d2w-cost` and `tab:stack-yield` divide the **whole stack** by $Y_{bonding}$ (139 mm² ÷ $Y$), because a failed bond scraps the CCD too. The paper says so at `:267`: "as long as bonding loses fewer than about 10% of stacks ($139/154$)". That contradicts the 75%. Corrected at 95%: a stacked part costs 146.6 mm²; (C) = **100/108/121** mm²; saving against (B) **0.7–3%**; break-even against (A) **about 90%**. Even with the draft's own figures the upper saving is 5%, not 6% (124.4 → 118.2). The clause "at 99% the stacked figures fall by less than 1 mm²" also fails (146.6 → 140.7). | Use $(1-p)\,94.8 + p\cdot139.3/Y_{bonding}$ and redo the table, the percentages and the 75%. The conclusion, flexibility rather than silicon, gets stronger. If the intent is that a failed bond spares the CCD, say so and justify it. |
| J3 | Overstated (wrong comparison) | `part5:482`, caption `figures/sim-pingpong.tex:18`, `part5:520`; `part3:185`; Findings `part1:181`; PDF pp. 31, 65, 125, 128 | "That hop must be about four times AMD's 9 ns." "More than twenty times AMD's figure of under 9 ns for one round trip." | AMD's 9 ns is one CCD → IOD → CCD round trip (Naffziger p. 1). A request-and-reply between two **different** CCDs crosses the link four times, which is **two** such round trips, 18 ns. The model charges one "hop" for each such exchange (`cachesim.cpp:293`; the slope in `s4_pingpong.csv` is exactly 4 hops per round trip). Reviewer's run at hop = 18 ns: 144.5 ns, ratio 2.95×. So 9 ns understates even the bare link. | "If the extra cost is modelled as a hop per request–reply, it must be about 37 ns, about twice the 18 ns of the two link round trips that exchange involves." Part III: "about eleven times two link round trips". The direction of the argument stands. |
| J4 | Unsupported | `appendix-e:10`, `part5:529`, `tools/cachesim/README.md`; PDF pp. 129, 157 | "Real Zen L3s are filled by evictions from the L2s." | No local AMD, Chips and Cheese or 7-cpu source says this (the word "victim" does not occur in any of them). It also conflicts with `part2:261`: "The sources used in this paper do not state which inclusion policy Zen 3's L3 follows". Cannot verify against a local file. | Cite a local source, or write "the model fills the L3 on every miss; real L3 fill policies may differ, and the sources used here do not state Zen's". |
| J5 | Overstated | `part5:461`, `:518`; PDF pp. 122, 128 | "The side die never matches the stacked L3." "A side die looked up after the L3 cannot match a stacked L3 even at 5 ns." | Only 48 and 80 MB were compared (`s2_side_die.csv`). For data that fits in 32 MB the side die is **faster**: 5.88 against 6.21 ns (`s2_designs.csv`, 32 MB, 5.6%), because it does not pay the four cycles. The claim also follows from the design chosen (L4 is looked up after an L3 miss). | "For working sets beyond 32 MB, a side die looked up after the L3 cannot match…; below 32 MB it is the faster of the two, because it adds nothing to the L3 hit." |
| J6 | Inconsistent | Abstract (`front-matter`, PDF p. 4); Findings `part1:180`–`181`; `part5:472`; `part6:145`, `:282`; PDF pp. 4, 31, 123, 138, 147 | "A 7% clock gap roughly triples the number of misses…", set beside "the model … reproduces … the weight of the clock gap". S3 is "consistent with the main result". | The simulated break-even goes from 0.041 to 0.376 (`s3_breakeven.csv`): a factor of **9.2**, not 3. The analytical factor is 2.9 (or 3.6 at 5.15 GHz). The two agree at the 7.3% gap (0.38 / 0.35) and disagree at equal clocks, which `part5:472` explains, but the headline does not carry this. | Abstract and Findings: "raises it from about 0.1 to about 0.35–0.4, roughly threefold in the analytical model and more in the simulation, which also hides part of the four cycles". |
| J7 | Error (wrong explanation) | `part5:474`; PDF p. 124 | At equal clocks the break-even "hardly moves, 0.03 to 0.05, because a removed miss is worth so much more than four cycles". | The cause is algebraic. The overlap factor multiplies both sides, so it cancels: break-even ≈ $4A/(L3 + t_{mem} - L3_s)$ = 15.1/377 = 0.040 (CSV 0.041). The table confirms it: 0.041–0.042 across overlap 0.105–1.0; only memory latency moves it (0.034–0.051). The robustness is a property of the model's construction. | "At equal clocks the overlap factor cancels, since it scales both the saving and the four extra cycles, so the break-even depends only on memory latency in the model." |
| J8 | Overstated | `part5:327`, `part6:259`, `figures/stacking-decision.tex`; PDF pp. 115, 136, 145 | "The useful predictor is … its L3 miss rate." "The deciding question … is the L3 miss rate." | The paper's own third class has a high miss rate and no gain (working set far beyond 96 MB, streaming; `part4:311`). In `tab:lam-detail` 7-Zip has the highest miss rate (54.2%) and gains 9.75%; Call of Duty at 53.5% gains 19.7%; GHPC gains less than Cyberpunk despite the higher MPKI. MPKI is known for only four of six workloads. | "A first screen, not the deciding question: a low miss rate rules the cache out; a high one still leaves open whether the working set fits in 96 MB." Keeps the figure, which already asks that second question. |
| J9 | Unsupported | `part1:176`, `part3:319`, `:400`, `part6:278`; PDF pp. 31, 71, 76, 147 | Link power "roughly 1–2% of the power budget". | Only Genoa has a denominator (7.4 W of 360 W = 2.1%). Rome's 3.3 W has none in the text, so the "1%" end is not derived. | Give a sourced Rome TDP, or say "about 2% on Genoa (memory traffic only)". |
| J10 | Overstated | `part1:169`, `tab:sim-plan` (`part5:416–422`); PDF pp. 31, 118 | "Seven controlled simulations, each changing one factor, five of them set beside a published measurement." | S0 and S3 are compared with measurements they are fitted to; S4 with the ratio it was fitted to. S1 is compared in shape only ("heights are not comparable"). S5's "AMD's 19% IPC claim" is never compared numerically. S2 changes arrangement and latency; S0 size and overlap. | "…most changing one factor; three set beside the measurements they are fitted to and one compared in shape". Change S5's column entry to "—". |
| J11 | Inconsistent | `part5:309` against `:311`; PDF p. 113 | "The two most memory-bound tests gained most" and, two sentences later, 523.xalancbmk is "the most memory-bound SPEC test". | Cozma p. 11 says the first only of the **floating-point** subtests; p. 9 is about the integer suite. Also 1.075/0.912 = 1.18, so the range is 18–26%, not 17–26%. | "In the floating-point suite the two most memory-bound tests…". "18–26%". |
| J12 | Overstated (attribution) | `part6:278`; PDF p. 147 | AMD "connects them through the organic substrate because that reach lets eight CCDs surround one IOD". | This is Naffziger's (AMD's) stated reason, p. 1. Part III attributes it; the Conclusions do not. | "…because, by AMD's account, that reach…". |
| J13 | Overstated (minor) | `part5:474`, `:519`; PDF pp. 124, 128 | "Across the range of Lam's own workloads it changes about threefold." | Only the overlap factor changes. The mix stays libx264's: 3.78 L3 accesses per 1000 instructions, against 9.3 (Cyberpunk) and 13.3 (GHPC). `part1:181` and `part6:282` word this correctly. | "Across the overlap factors fitted to Lam's workloads, with the libx264 mix held fixed". |
| J14 | Inconsistent (label) | `figures/sim-table-calibration.tex`; `part5:435`; `README.md`; PDF p. 120 | Column "Gross saving per removed miss": 101 and 303; README says "about 103 cycles net". | `s0_calibration.csv` holds both: the model value 101.46 / 302.86 is **net** of the four cycles on that workload's hits; the gross value is 102.8 / 306.8. README has the two reversed. | Head the column "Saving per removed miss, net of four extra cycles on hits", or print 103/307. Align the README. |
| J15 | Inconsistent (description) | `appendix-e:12`; README; PDF p. 157 | "If other cores held the line, the write is charged one extra L3 latency, plus the hop." | `cachesim.cpp:364` adds the L3 latency only for a write that hit privately. A write miss to a remote line pays the fetch and a further hop (`:293` + `:365`). Remote L3 copies held by no core are invalidated at no cost (`:368`). | Add those two conditions in one clause each. |
| J16 | Overstated (minor) | `part5:488`; PDF p. 125 | "The 37 ns hop was fitted to sharing, so the second figure is an upper bound." | The stated reason does not give an upper bound. What makes 1.39× high is that 37 ns is also charged to memory accesses. Removing that gives about 1.35× (22 per 1000 × 28 ns × 0.335). A hop above 37 ns also remains possible (Reguly measured one cloud VM). | "It also charges memory accesses at 37 ns; at 9 ns for those it would be about 1.35×." |
| J17 | Inconsistent (minor) | `part4:194`, `tab:evidence-strength` against `part6:63`; PDF pp. 88, 134, 142 | "About 0.6 TB/s" (computed at 4.2 GHz) and "702 GB/s" (Lam's multithreaded test). | The paper gives no clock for the 702. 18.45 B/cycle × 8 × 4.2 GHz is 620 GB/s, so 702 GB/s implies about 4.75 GHz, near Lam's sustained 4.8 GHz (Lam p. 9), which suggests a stock-clock run. I did not re-read the chart. | State the clock of the 702 GB/s test, so the reader can reconcile the two figures. |
| J18 | Inconsistent (minor) | `tab:evidence-strength` row "The controlled simulations"; PDF p. 142 | Strength: "Illustrative". | The caption defines only strong/moderate/weak, and places "modelled with illustrative inputs" under weak. | "Weak (by this table's definition): illustrative model outputs". |
| J19 | Structure | `part5:419`, `:472` against `part6:112`; PDF pp. 118, 123, 137 | S3 and the Part V summary compare with an analytical model not defined until Part VI. | The reader meets `tab:cache-clock-model` about 14 pages after it is used; the model is analysis of Lam's data, which is Part V's job. | Move "Refining the rule" and its table before `sec:sim-study`. Part VI keeps a reference and the decision figure. This adds about a page to Part V, which is already over target; if that is unwanted, keep the model in Part VI and give its one-line definition at the start of S3. |
| J20 | Structure (repetition) | `part5:269` and `:280`; apparent-saving caveat in `part4:178`, `part5:248`, `:435`, `part6:282`, App. E; PDF pp. 87, 108, 111, 120, 147, 158 | Genoa-X "0.98× to 1.60×" is stated in full twice within one page; the prefetch caveat is restated in full five times. The 130-cycle derivation itself now appears once. | Brief item 11. | Drop the Genoa-X sentence at `:269`. State the caveat in full once (`sec:tradeoff-example`) and cross-refer elsewhere. |
| J21 | Structure (half-page rule) | Directory example (`part2:413–437`, about 1 p., p. 52); product-line example (`part4:269–292`, about 1 p., pp. 94–95); analytical model (`part6:113–145`, over 1 p., p. 137) | Self-contained derivations in the main text. | Format rule: over about half a page goes in a numbered appendix. | Move the directory example and the product-line working to appendices, leaving the conclusion. The analytical model is central, so keep it but shorten the calibration. |
| J22 | Writing | `part5:427–428`; PDF p. 119 | Heading "How close is the model to the hardware?"; label `sec:sim-validation`. | The text says "Neither match is a test". Brief item 3 warns about fitted agreement presented as validation. | "S0: What the calibration fixes, and where the model differs". Rename the label. |
| J23 | Format (figure) | `figures/sim-zen2-zen3.tex`, Fig. 55; PDF p. 127 | Legends sit at top left in both panels. | Rendered at 100 dpi: both legends cover the 2 × 16 MB curves over about 20–36 MB, the range the figure exists to show. The I39 fix did not clear this. | `legend pos=south east` or a shared legend below. |
| J24 | Structure (figures) | `fig:numa-latency` (p. 63), `fig:bandwidth-balance` (p. 66), `fig:clock-correction` (p. 118) | The text says the chart shows "the same numbers". | Each duplicates its table with no new reading. No figure or table is unreferenced (all 101 labels are cited). | Keep one of each pair, or use the caption to say what the chart adds. |
| J25 | Writing | `part5:288`, `:307`; caption `figures/sim-pingpong.tex:18`; `appendix-c:23` | "corrected his results", "his correction", "his test", "He regarded". | The sources do not state these authors' pronouns. W1 and W2 removed the same usage elsewhere. | Use the name or "the author's": "corrected those results", "Cozma's correction", "Reguly's test", "Murphy regarded". |
| J26 | Writing | First uses | "IPC" (`part1:178`, in Findings), "EFB" (`part3:262`), "UCIe" (`part6:184`) are not expanded in prose; "DIMMs" (`part3:80`). | TLB, MMU, SMT, DVFS, KGD, FVOPS, NUMA, TDP are all defined at first use. | Write "instructions per cycle (IPC)" at `part1:178`. Expand EFB and UCIe only if a local source gives the expansion; otherwise keep the descriptive phrase already there. "Memory modules (DIMMs)" at `part3:80`. |
| J27 | Writing | Terminology (all parts) | "stacked die" (10 uses), "stacked CCD", "plain part/die/CCD" (34 uses across three forms). | W18's convention was not applied. "Hop" is now consistent. | Glossary rule: "cache die (L3D)" for the SRAM die; "V-Cache CCD" for the assembled unit; "plain CCD" throughout. |
| J28 | Writing | `part5:497`; PDF p. 126 | "…about 12% higher … entirely because of its lower latency". | "Its" reads as the unified L3, which has the higher latency. | "…entirely because the split L3 has the lower latency". |
| J29 | Writing | `part5:503`; PDF p. 127 | "With 20 MB per thread, both caches overflow and both meet the same limit." | The 96 MB L3 holds four such threads and reaches 1.07 G/s (`s6_streaming.csv`). | "…both overflow by six threads and then meet the same limit". |
| J30 | Format (draft state) | `metadata.tex:7`; six `\partbudget` lines | Draft date 5 November; build 8 November. Part V's status line omits the model; Part II's says "expand worked examples and figures"; Part III's says estimates "need checking". | H21's residue. | Update or remove before any submission. |
| J31 | Minor (transcription) | `tab:topologies`, `part2:459`; PDF p. 54 | Butterfly diameter $\log N$. | Sarangi Table 12 (PDF p. 634): $\log(N)+1$. | Correct the entry. |
| J32 | Minor (count) | `part6:69`; PDF p. 135 | "Three interactions stand out." | Four follow. | "Four". |
| J33 | Minor (arithmetic, wording) | `part3:185`; `part4:294`; `tab:sim-breakeven` | "$265 - 59 \approx 207$" (it is 206). SRAM "barely shrinks" from 7 to 5 nm. Analytical row blank at 2, 4, 6 and 10%. | Slide 6's SRAM line still falls visibly. The analytical values are 0.17, 0.24, 0.31, 0.45 (reviewer, from `eq:cache-clock-model`), against simulated 0.13, 0.22, 0.32, 0.50. | "≈ 206". "shrinks less than logic". Fill the row: the agreement away from 0 is worth showing. |

---

## 3. Regression

### H1–H24 and W1–W18

| ID | Status | Note |
|---|---|---|
| H1 | Fixed | RQ1 and evidence row say cost per good die; cites Murphy and Dong–Xie. |
| H2 | Fixed | `part5:196`: 1.2–2.8 points. |
| H3 | Fixed | Part IV summary: "the reason AMD gives". |
| H4 | Fixed | RQ4, Part V summary and evidence paragraph separate latency (strong) from IPC (moderate). |
| H5 | Fixed | "No visible hop, without showing how large"; caption and evidence row match. |
| H6 | Fixed | `part6:148` "suggest". |
| H7 | Fixed | Bandwidth weak; yield/cost moderate. |
| H8 | Fixed | All four mind-map and caption items checked. |
| H9 | Fixed | Fig. 58 box names only MiniFE. |
| H10 | Fixed | Now computed and labelled (`sec:lam-detail`). |
| H11 | Fixed | "No processor with stacked cache"; open question added. |
| H12 | Fixed | "By AMD's account…". |
| H13 | Fixed | Footnote present. |
| H14 | Fixed | Caveat at `part5:53`. |
| H15 | Fixed | "Up to about 8%". |
| H16 | Fixed | One statement of 1.24× (1.22× in Fig. 4). |
| H17 | Fixed | Architectural reason given first. |
| H18 | Decided | All 13 maps kept. Text now about 7.6–9 pt (computed from the layout; see §5.3). |
| H19 | Partly fixed | App. D added; Cezanne stays (decided). See J21 for new long examples. |
| H20 | Fixed | Fig. 16 clean at 100 dpi. |
| H21 | Partly fixed | Abstract and caption done; draft date stale and status lines remain (J30). |
| H22 | Fixed | Power and flexibility in RQ2. |
| H23 | Fixed | "Probably explains much of why". |
| H24 | Fixed | `tab:three-way` note. |
| W1, W2 | Fixed where raised | The same usage appears elsewhere (J25). |
| W3–W9 | Fixed | SerDes, TDP, NUMA, HBM, SoIC, RTL, OPIO. |
| W10 | Fixed | GHPC described at `part5:202`. |
| W11–W17 | Fixed | As suggested; W12 at `part2:89`. |
| W18 | Not fixed | No convention applied (J27). |

### F1–F23 and G1–G20 (spot-check)
Sampled, none regressed: F2 (NUMA1–3 labels), F3, F9, F12, F19, F21, G1, G2, G4, G5, G7, G9, G10, G11, G12, G14, G16, G19.

### I1–I43 (added, because this draft is the one those fixes produced)
| IDs | Status | Note |
|---|---|---|
| I1–I5, I13–I15, I18–I23, I25–I33, I35–I38, I42 | Fixed | Checked against the code, CSVs or text. |
| I6, I7, I9 | Fixed | Caveats present at every location listed. |
| I8 | Fixed | J17 is a small residue. |
| I10, I11 | Mostly fixed | Residue in J10, J22. |
| I12 | Fixed | Column label in J14. |
| I16 | Fixed | Claim now over-general (J5). |
| I17 | By explanation only | The stated cause is still untested (J1). |
| I24 | Fixed in the paper | the project guidelines §3 still says published data only. |
| I34 | Fixed | App. E uses `listings`. |
| I39 | Partly fixed | Fig. 55 legends (J23). |
| I40, I41 | Mostly fixed | IPC and terminology (J26, J27). |
| I43 | Declined | Decision by Ishan; not re-raised. |

---

## 4. Simulation check

### 4.1 Model description (Appendix E against `cachesim.cpp`)
| Item | Result |
|---|---|
| Latency formula | Matches: L1/L2/L3; remote 2 × L3 + hop (`:293`, `:309`); L4 hit L3 + L4 (`:328`); DRAM L3 + mem, + hop if `dram_hop` (`:334`). |
| Overlap | Matches: only the part beyond an L2 hit is scaled (`:373`). |
| L3 fill | Matches: filled on every miss (`:333`). The claim about real Zen is unsupported (J4). |
| L4 fill | Matches: inclusive fills on every miss, victim takes evictions. I tested the "only 64 MB distinct" claim: at 80 MB, 198.7 DRAM accesses per 1000, i.e. 64.1 MB held. Correct. |
| Warm-up | Matches: pre-touch then warm then statistics reset (`:606–623`); ping-pong skips 40 accesses (`:634`). |
| Coherence | Simplified; two conditions unstated (J15). |
| Time model | Matches: largest of latency, DRAM and L3 limits; link limit off (`:579`). |
| Pointer-chase description | Wrong (J1). |
| Calibration equations | Reproduce: 0.335, 0.202, 0.105. |

### 4.2 Reproduction
Built with `g++ -O2 -std=c++17`; `--selftest`: 8 passes, 0 failures. Ran **the full study** (not only S0 and S4): 8 m 48 s on 16 cores. Compared with the stored CSVs: **16 of 16 files identical, 3,859 cells, 0 differences.**

### 4.3 Numbers against the CSVs (48 rows checked, all correct)
| Claim | Text | CSV | | Claim | Text | CSV |
|---|---|---|---|---|---|---|
| S0 plateau, 32 MB | 46.4 | 46.45 | | S3 equal clock | 0.04 | 0.041 |
| S0 plateau, 96 MB | 50.8 | 50.79 | | S3 7.3% gap | 0.38 | 0.376 |
| 1 GB, 32 MB | 334 | 333.7 | | S3 sens. Cyberpunk | 0.58 | 0.578 |
| 1 GB, 96 MB | 319 | 319.1 | | S3 sens. GHPC | 1.05 | 1.047 |
| Model at 64 MB | 195 | 194.6 | | S3 sens. no overlap | 0.17 | 0.171 |
| Saved per miss | 101 | 101.46 | | Memory 60 / 90 ns | 0.46 / 0.31 | 0.463 / 0.309 |
| S1 fit range | 0.949–0.956 | 0.949–0.9557 | | Check: L3 accesses | 3.78 | 3.778 |
| S1 40 MB | 1.71 | 1.7137 | | Check: misses | 1.44 | 1.436 |
| S1 96 MB | 3.49 | 3.4913 | | Check: cycles | 729 | 729.0 |
| S1 128 MB | 1.95 | 1.9503 | | Check: gain | 5.2% | 5.19 |
| S1 256 MB | 1.27 | 1.2666 | | Stacked MPKI | 1.04 | 1.04 |
| Hot/cold range | 1.03–1.28 | 1.0328–1.2752 | | S4 same CCD | 49 ns | 49 |
| Hot/cold fit | 1–5% slower | 0.8–4.8% | | S4 9 ns | 108.5; 2.2× | 108.5; 2.214 |
| S2 stacked | 6.21 | 6.213 | | S4 37 ns ratio | 4.5 | 4.5 |
| S2 planar | 6.87 | 6.873 | | Crossings | 66 | 66.36 |
| S2 baseline | 5.88 | 5.884 | | DRAM, shared | 22 | 22.02 |
| Planar +17%, stacked +5.6% | yes | 1.168; 1.056 | | Shared ratios | 1.20; 1.39 | 1.2021; 1.389 |
| Planar break-even 40 / 96 | 107 / 245 | 106.9 / 245.3 | | Private ratio | 1.08 | 1.0831 |
| Side die 22 ns, 80 MB | 10.34 / 13.81 | 10.3438 / 13.8115 | | S5 raw at 32 MB | 4.0× | 4.02 |
| Side die 5 ns, 48 MB | 6.46 / 6.23 | 6.4572 / 6.2307 | | S5 exposed | 12% | 11.8–12.5% |
| S6 before/after | 1.08 → 0.68 | 1.0847, 0.6768 | | S5 1.7–3.0× | yes | 1.74–3.00 |
| S6 limit | 0.8 | 0.8 | | S5 8 threads | 1.3–2.3× | 1.29–2.33 |
| S6 96 MB; ratio | 2.1; 2.7× | 2.1405; 2.68 | | Sensitivity loss | 2.4–9.6% | 2.4; 9.64 |
| Sensitivity gain | 1.89–3.78 | 1.8857–3.7838 | | ±34/32% | yes | 0.66; 1.324 |

Every number above matches its CSV. The findings on this section (J1, J3, J5–J7, J13, J14, J16, J29) concern what the numbers are said to mean, not their values.

### 4.4 Calibration against validation, and overreach
- Fitted agreement is labelled as such throughout `sec:sim-study`, `sec:sim-limits` and threats to validity. Remaining soft spots: J10, J22.
- Assumed inputs (59 cycles, L4 22 ns, 1 access per 3 instructions, `l1_lat` = 1, `work_cycles` = 0.48) are labelled where used.
- Model outputs are labelled; memory-system speed-ups are kept separate from program speed-ups; the old "upper bounds" claim is gone (J16 is the one remaining use).

### 4.5 Comparison with Part VI
Now fair: `tab:sim-breakeven` uses 5.15 GHz for both, and gives the 4.2 GHz value in the caption. "Factor of about 2.4" is right (0.097/0.041 = 2.4), and attributing it to the overlap of the four cycles is right, because the calibration difference (130 against 101 cycles) comes from the same assumption. See J33 for the blank cells.

### 4.6 Design and fit
One factor at a time, five seeds and two sensitivity tables suit the purpose. **Missing, and would matter:** a cyclic pointer-chase workload (J1); randomised page placement, which would test S0's stated "main reason"; and an S3 mix fitted to a second workload, so that the threefold range is not only an overlap effect (J13). **Adds least:** S6, whose result follows from taking the largest of three limits. Length is decided (I43); placement after the confounds is right.

---

## 5. Spot-checked numbers

### 5.1 Sources (44 checked, 2 wrong)
| Claim | Draft | Source and page | OK? |
|---|---|---|---|
| Core-to-core, same CCD | 58.6 ns | Reguly Fig. 2, p. 3 | Yes |
| Cross-CCD | 265.2–266.2 | Reguly Fig. 2 ("different chiplet", p. 2) | Yes |
| Other socket | 396.9–415.3 | Reguly Fig. 2 | Yes |
| Xeon 8360Y; Max 9480 | 106.1–109.5; 83.6–84.4 | Reguly Fig. 2 | Yes |
| STREAM 310; 1446 GB/s; ratios 14×/6×/3.8× | as stated | Reguly pp. 2–3 | Yes |
| 9124: 16 c, 64 MB, 200 W, 3.00 GHz | yes | EPYC 9004 datasheet p. 2 | Yes |
| 9174F: 16 c, 256 MB, 320 W, 4.10 GHz | yes | Datasheet p. 2 | Yes |
| 9184X; 9684X | 768, 320 W; 1152, 400 W | Datasheet p. 2 | Yes |
| 9224 counter-example | 24 c, 64 MB | Datasheet p. 2 | Yes |
| 9654 / 9684X all-core | 3.55 / 3.42 | Datasheet p. 2 | Yes |
| 9334; 9354; 9554 | 128/210; 256/280; 256/360 | Datasheet p. 2 | Yes |
| 460.8 GB/s; 4.8 per core | yes | Datasheet p. 2; 460.8/96 | Yes |
| 9174F eight dies × 2 | yes | White paper p. 5 | Yes |
| 4, 8 or 12 CCDs | yes | White paper p. 9 | Yes |
| 7–8 cycles from unification | yes | Cozma 2022b p. 4 | Yes |
| 24–28 cycles vs mesh | yes | Cozma 2022b p. 6 | Yes |
| 25% / −12.5% bytes per cycle | yes | Cozma 2022b pp. 7–8 | Yes |
| 3.15 vs 3.3 GHz | yes | Cozma 2022b p. 12 | Yes |
| 20 µm; 1.2 V; 1.4 V; 1.28–1.31 V | yes | Cozma 2024 pp. 1–2 | Yes |
| 300 MHz; 10 / 70 MHz | yes | Cozma 2024 p. 3 | Yes |
| fotonik3d +7.5%; roms +15% | yes | Cozma 2024 p. 11 | Yes (J11 on scope) |
| 5.2 vs 5.7 → 17–26% | 17–26% | recomputed 18–26% | **No (J11)** |
| 4.8 vs 5.15 GHz; 7% | yes | Lam pp. 5, 9 | Yes |
| 18.45 B/cycle | yes | Lam p. 10 | Yes |
| CoD 46.5→68.7; IPC 0.71→0.85 | yes | Lam chart, p. 15 | Yes |
| Pipeline slots 29.7→24.2 | yes | Lam chart, p. 15 | Yes |
| Cyberpunk IPC 1.26→1.43 | yes | Lam p. 13 | Yes |
| DCS 0.35→0.28; GHPC 9.67% | yes | Lam pp. 13–14 | Yes |
| Prefetch counting | yes | Lam p. 10 | Yes |
| eDRAM over 30 ns; 50 GB/s; 64 GB/s | yes | Lam pp. 17–19 | Yes |
| 47 cycles + 74 ns; 40 + up to 20 | yes | 7-cpu p. 1 | Yes |
| TLB 7 / 1.7 and 24 / 5 cycles | yes | 7-cpu p. 1 | Yes |
| 13 FCLK under 9 ns; 55 GB/s; 2 pJ/bit; 19% | yes | Naffziger p. 1 | Yes |
| Cost chart ≈2× at 48/32, 1.8× at 16 | yes | Naffziger Fig. 2.2.2, read | Yes |
| 7→5 nm cost up about a third | 3.7 → 4.95 | ISSCC slide 6, read | Yes |
| Table 5 row labels misprinted | yes; 3.4–3.5 / 3.2–3.4 | Lawenda p. 6, rendered | Yes (inference labelled) |
| 0.81–1.54×; 0.98–1.60×; 1.24–1.70×; 2.67× | yes | Lawenda pp. 6–7 | Yes |
| 15k–100k; 10k–200k cells per core | yes | Lawenda p. 7 | Yes |
| 3.4×; 9.56× | yes | Domke pp. 1–3 | Yes |
| 88.35→92.85 °C; 0.08 °C; 13%; 66% | yes | Black pp. 1, 7 | Yes |
| 1 access in 3 instructions | yes | Sarangi 11.1.1, PDF p. 510 | Yes |
| CPI = ideal + f(AMAT−1) | yes | Sarangi Eq. 11.1, p. 536 | Yes |
| Exclusive = not strictly inclusive | yes | Sarangi Def. 100, p. 517 | Yes |
| Butterfly diameter | $\log N$ | Sarangi p. 634: $\log N + 1$ | **No (J31)** |

Not re-read in this pass: the 702 and 53 GB/s chart labels in Lam (earlier reviews read them).

### 5.2 Worked examples recomputed (all correct unless noted)
Geometric mean 1.114 and 1.094; `tab:lam-per-miss` (all three rows); stock-clock nets; libx264 chain 3.85 → 0.40 → 36 + 15 → 130; DCS 3.2 vs 3.7 and 0.24; `tab:clock-correction`; `tab:cache-clock-model` (0, 0.4; break-evens 0.12/0.35); 26% and 30%; MiniFE 245–310 and 275–330 bytes; yields, 139/154, W2W 78.8%; address fields; TLB reach; directory total 18 and 35/315; write-through 1/10 and 1/80; inclusion 12.5% and 4.2%; Amdahl; overlap calibration 0.335/0.202/0.105. **`tab:product-line-silicon` is arithmetically correct as drawn but rests on the wrong formula (J2).**

### 5.3 Internal consistency (brief item 5)
| Quantity | Result |
|---|---|
| 4 extra cycles; 96 MB | Consistent everywhere (3–4 measured on Milan-X is stated as such). |
| 7% / 1.073; 4.8 vs 5.15 GHz | Consistent. |
| 130; 50/80/130; +11.4% | Consistent, labelled apparent and authors' calculation. |
| Under 9 ns; 37 ns; 58.6 vs about 265 ns | Consistent (brief's "37 calibrated" still current). See J3 on meaning. |
| 204.8; 3.2/4.8 GB/s; 12 MB per core | Consistent. |
| 47 vs 39 cycles | Consistent. |
| Break-evens | Analytical 0.12/0.35/0.50 consistent. Simulated are now 0.04/**0.38** (brief's 0.29 is stale) and consistent. Overlap is now **0.335** (brief's 0.42 is stale) and consistent. J6 for the headline. |
| Mind maps | All 13 legible (level-2 text `\scriptsize`, 8 pt, scaled about 0.95–1.14: about 7.6–9 pt, computed from the layout geometry). None adds a claim, number or term the text lacks. |
| Citations | All 36 keys used are in `references.bib` and listed present in `research/pdfs/README.md`. The one unused key is the missing Swaminathan 2022 PDF, correctly not cited. |

---

## 6. RQ-by-RQ assessment

| RQ | Answered in Conclusions? | Supported? | Strength consistent with `tab:evidence-strength`? |
|---|---|---|---|
| RQ1 | Yes | Yes. Mechanism robust; quantities illustrative. | Yes (moderate). |
| RQ2 | Yes, all four aspects | Latency, bandwidth and flexibility well supported. Power honestly stated as qualitative, but see J9. Sharing cost rests on one VM, said so. | Yes. |
| RQ2a | Yes, briefly | Rests on AMD's stated reason alone (J12), and only for Rome and Matisse, as stated. | Not separately graded; would be vendor-only. Add a row. |
| RQ3 | Yes | Yes, with the voltage caveat. | Yes. Stacking cost correctly weak (J2 makes it weaker, not stronger). |
| RQ4 | Yes | Direction and latency strong; size moderate. The simulations illustrate only. | Yes, except the "roughly triples" headline (J6). |

**Overreach (brief item 8).** Causal claims from uncontrolled comparisons are now hedged. Model outputs and chart readings are labelled. CCD counts and Lawenda's misprint are presented as inferences. Conclusions stay within the threats section, apart from J6, J8 and J9.

**The three weakest links.**
1. *The apparent saving per miss.* Everything quantitative about clock against cache rests on one processor's counters, which include prefetches, and on 130 cycles from one program. Fix: state the break-evens as ranges (0.17–1.05 is already in the paper), and use the 5600X kit's overlap test to give one independent value.
2. *The model has no out-of-sample test.* Every agreement it shows is with something it was fitted to or built from. Fix: compare one result it was not fitted to, such as a measured 5600X latency curve, or say plainly in the Abstract that it has not been tested independently.
3. *The economics of stacking.* The case rests on silicon area, with no bonding, thinning or test cost, and J2 removes most of the margin over two planar dies. Fix: keep the claim to flexibility and to where silicon is spent, as `part6:235` already does, and correct J2.

**Missing at undergraduate level.** Only one point matters: prefetching is named as a candidate explanation for the per-miss result but is never explained beyond a table row. A short paragraph in `sec:mlp` would serve the argument.

---

## 7. Per-part page counts (PDF pages)

| Part | Pages | Count | Target | Difference | What it needs |
|---|---|---|---|---|---|
| I | 24–33 | 10 | 10 | 0 | Nothing. |
| II | 34–55 | 22 | 25 | −3 | A paragraph on prefetching; otherwise complete. |
| III | 56–76 | 21 | 25 | −4 | Would gain from a non-AMD chiplet example if a local PDF becomes available. |
| IV | 77–98 | 22 | 25 | −3 | Fine; J21 would move a page out. |
| V | 99–130 | 32 | 25 | +7 | The simulation section's length is decided (I43). The overrun is otherwise acceptable; moving the evidence ledger table to an appendix would save about a page. |
| VI | 131–148 | 18 | 20 | −2 | Fine. J19 would move about a page to Part V. |
| **Body** | | **125** | **130** | **−5** | |

References 149–151, Appendices 152–159, Index 160.

---

## 8. Course format and leftovers

| Item | State |
|---|---|
| A4, 12 pt, single spacing, 1-inch margins | Set centrally (`main-initial-draft-2.tex`, `ell305-format.tex:9, 82`); page size confirmed by `pdfinfo`. |
| Page order | Cover 1, copyright and IP 2, acknowledgements 3, abstract 4, contents 5–10. Correct. |
| Generated lists | List of Tables p. 11, List of Figures p. 15, Glossary p. 22, Index p. 160. |
| Appendix A, B | Placeholders, as expected; wording is limited to what a tool displayed. Not counted as an error. |
| Diagrams | TikZ and pgfplots; the only `\includegraphics` is in the front matter. |
| Code | Appendix E now uses `lstlisting`, which meets the rule. |
| `\todo` | 2 (Appendices A, B). |
| `\verify`, `??`, undefined references or citations, overfull boxes | 0. |
| "placeholder" | 1, `part5:531`, a true statement about the energy model. |
| `\partbudget` | 6 status lines (J30). |

---

## 9. What I checked and found correct

- The whole of `sec:sim-study` and Appendix E against the code and CSVs, apart from the points in §2; 48 rows of numbers, and a byte-identical rerun of the full study.
- `tab:product-matrix`: every row against the datasheet; inferences labelled; the arithmetic is right.
- `tab:core-to-core`, read directly from Reguly's Fig. 2.
- `sec:lam-detail`: both tables and the geometric mean; `sec:genoax`, including the row-label inference, which I rendered and agree with.
- Directory example: arithmetic right, assumptions labelled as the authors' own.
- Part IV: the node-cost reading from slide 6; the Zen 5 residual (5.45%, "more than half" holds against 7% and 10%).
- The S3 comparison with Part VI is now fair and explained.
- All 59 figure pages rendered. Apart from J23 and the duplicates in J24, no overlapping labels or unreadable text. All 101 figure and table labels are referenced.
- No text assigns group work to an individual.
