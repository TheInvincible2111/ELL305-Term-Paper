# Fifth review of initial-draft-2 (8 November 2026)

Brief followed: `research/review-prompt-initial-draft-2-v4.md`, applied to the draft as it now stands (169 pages, after the fourth review, its rerun and the 5600X measurements). Findings continue the series as K1, K2, ….
Only local files were used; nothing on the web. No other project file was changed; all reruns went to a temporary folder.
Page references are **PDF viewer pages** of `build/pdf/ELL305-initial-draft-2.pdf` (the printed page number is one lower). Line references are to `initial-draft-2/` unless a full path is given; `part5:498` means `sections/part5-case-study.tex`, line 498.

**Build currency.** The PDF was built on 8 Nov 2026 at 13:47; the newest source is 13:46, so the PDF matches the sources. Build log (`tmp/linux-build/main-initial-draft-2.log`): no errors, no undefined references or citations, **0 overfull boxes**, 30 underfull boxes.

**What this review did not do.**
- `test/crosscheck.js` (C++ against JavaScript) could not be run: Node.js is not installed in Windows, MSYS2 or WSL here. The earlier responses' claim that it passes is unverified by this review.
- Mittal and Vetter's 90%, 8× and 8–15× figures (`part4:30`, `part2:335`) could not be located by text search in the extracted PDF and were not read by eye. They are marked "not rechecked", not wrong.
- The simulator's warm-up code and its GUI were not re-read. The warm-up statement rests on the fourth review's reading and on the byte-identical rerun.
- The textbook was checked only for the items listed in §5.

---

## 1. Overall assessment

The paper is strong for an undergraduate term paper, and the fourth review's corrections are real: almost every I and J finding is fixed, the simulation reproduces exactly, the worked examples recompute, and the source values sampled match. I would place it provisionally at A−. The new risk is concentrated in one place. The 5600X measurements are valuable, but the paper describes them as an independent test passed, and the headline result ("within 5% and 1%") comes after two inputs were set to that machine's own values. An examiner who opens `compare_5600x.py` will see this at once, and it sits in the abstract, the Findings, the summary of Part V and the evidence table. Left as it is, that moves the paper towards B+, because it undoes the care that makes the rest credible. The second weakness is a set of small contradictions in the parts an examiner reads first: Contributions, RQ2 and RQ4.

**The two changes that would improve the paper most:**
1. Restate what the 5600X shows (K1, K2, K6). Report the unfitted comparison as the test, call the refit what it is, and limit the "real gain is larger" claim to latency sweeps. An accurate and still positive sentence is available: *with nothing fitted, the model's L1 and L2 agree with the 5600X and its L3 and memory latencies are within about 20%*.
2. Clear the contradictions in Part I and the Conclusions (K3, K4, K5).

---

## 2. Findings (most severe first)

| ID | Severity | Location | What the draft says | What the source, CSV, code or rule says | Suggested correction |
|---|---|---|---|---|---|
| K1 | Overstated (regression of I10) | Abstract (`front-matter.tex:49`, p. 4); `part1:155, 171, 183` (p. 33, "holds up on real hardware"); `part5:467` (p. 120, "One test is independent … reproduces its cache hierarchy closely"); `part5:498` (p. 121–122, "The model's structure therefore carries over"); `part5:609` (p. 135, "show that it is a sound one"); `part5:612`; `part6:151` (p. 145, "structure is confirmed on real hardware"); `part6:194` (p. 147); caption `figures/m5600x-latency.tex` | The 5600X is "a machine the model was never fitted to", and "with two machine-specific latencies set" the model matches the plateau within 5% and memory within 1%. | `tools/cachesim/study/compare_5600x.py:11–12`: L3 = 54 cycles is "the measured 2 MB-page plateau", memory = 90 ns is set "so that the 1 GB value matches". So the 5% and 1% are fits, by the logic `part5:494` itself applies to Milan ("Neither match is a test"). L1 and L2 are inputs from another Zen 3 chip, so their agreement compares two chips. What is out of sample (`research/measurements/5600X/model-comparison.csv`, measured ÷ model): default inputs give L1 1.00, L2 1.08–1.10 at 250–500 KB, L3 plateau 1.19–1.20, 1 GB 1.20; 2.39 at 32 MB. After the refit the mismatch remains 1.22–2.08 from 19 to 38 MB and 1.12–1.31 from 45 to 108 MB. | Make the unfitted comparison the test, and label the refit as a calibration: "With nothing fitted, the model's L1 and L2 agree with the 5600X and its L3 and memory latencies are about 20% low; near the capacity edges it is further off, up to 2.4× at 32 MB. Setting two latencies to this machine's values aligns the plateaus by construction; it does not remove the edge differences." Replace "holds up", "confirmed", "sound", "carries over". |
| K2 | Overstated | `part5:504` (p. 122, "they strengthen the main result"; "the real gain … is, if anything, larger"); `part5:609` (p. 135, "understates rather than overstates"); `part5:604` says the opposite ("optimistic near each capacity edge") | Both mismatches make the small cache worse "in reality", so the model is conservative from half the small cache's capacity to about 64 MB. | (a) The first mismatch is, by the paper's own account, a property of the pointer chase's fixed cycle, not of programs. Random and cyclic order are two synthetic extremes, and real programs need not resemble either. (b) It is only a partial explanation, stated flatly in the text though the caption says "probably": at 64 MB the 5600X measures 66.9 ns, between the random model (56.6) and an all-miss chase (about 99), so about a third of accesses still hit. Milan is similar (240 against 195 and 342 cycles). (c) The second mismatch has causes the paper says it cannot separate (`part5:502`), including WSL2. `ANALYSIS.md` notes a guest 2 MB page need not be a 2 MB host page, and App. G records huge pages probably only partly granted in one run. At 32 MB the three runs give 24.1, 23.9 and 73.8 ns. | Limit the claim: "For a latency sweep, the measured gain is larger than the model's from about 20 to 64 MB. How far this applies to real programs depends on their access order, and the early L3 slowdown may partly reflect the virtual machine." Remove "strengthen", and align `part5:604` and `:609`. |
| K3 | Error (contradiction) | `part1:163` against `:155, :171` (p. 32–33); caption `figures/evidence-method.tex:13` (p. 103) | "This paper contributes no new hardware measurements", and two bullets later lists the 5600X measurements as a contribution. Fig. 42: "no new hardware measurement". | App. G records a set of hardware measurements. `part1:153` is correctly scoped ("for these processors"). | "This paper makes no new measurements of chiplet or stacked-cache processors, and one set on a planar Ryzen 5 5600X; its contributions are otherwise analytical and, in one part, computational." In the caption: "published research and benchmarks; the 5600X measurements are in App. G". |
| K4 | Inconsistent (and a response file misreports it) | `part6:87` (p. 140), `part6:223` (p. 151) against Abstract, `part1:182`; `review-initial-draft-2-v4-rerun-response.md`, row J6 | Part VI and RQ4: "from about 0.12 to about 0.35". Abstract and Findings: "from about 0.1 to about 0.35". | The response to J6 says RQ4 and the Part VI summary were changed; they were not. 0.12 is the 4.2 GHz value and 0.35 uses 4.8/5.15 GHz (`part5:463`), the mixed baseline I14 and J6 flagged. Also not carried to any headline: the simulation's equal-clock value is 0.04, so its factor is about 9, not 3 (`s3_breakeven.csv`). | Use "about 0.1" in `part6:87` and `:223`, or state both clocks. Correct the J6 row of the response file. |
| K5 | Error | `part3:355` (p. 73), `:401` (p. 76), `part6:219` (p. 149) | Zen 4 servers span "16 to 96 cores", "4 to 48 MB of L3 per core", "with only two variants of the compute die". | `AMD-EPYC-9004-Datasheet.pdf`, p. 2: EPYC 9224 has 24 cores and 64 MB, 2.7 MB per core, and `part3:327` itself cites it. The same table lists 128-core and 112-core parts (9754, 9734; 256 MB, 2 MB per core at 128 cores) built on the Zen 4c die (`AMD-4th-Gen-EPYC-Architecture-White-Paper.pdf`), which the claim leaves out without saying so. | "In the products of `tab:product-matrix`, 16 to 96 cores and 4 to 48 MB per core (the datasheet's EPYC 9224 is lower, at 2.7 MB; the 112- and 128-core 97xx parts use a different, Zen 4c, die)." |
| K6 | Inconsistent (a comparison not made) | `part5:557`, `figures/sim-pingpong.tex` (p. 129) against `part3:185`, App. G (`appendix-g-5600x.tex:59`, p. 167) | The model's same-CCD ping-pong is "49 ns". The 5600X hand-over is "about 49 ns". | These are different things. The model's 49 ns is a full round trip with two transfers and two write upgrades at 4 GHz (`s4_pingpong.csv`; `cachesim.cpp` ping-pong). The 5600X's round trip is 98.5 ns. Like for like, the model is about half the measured value, and this is the one out-of-sample check of coherence timing the group has. The caveats are real (WSL2; 66–72 ns on some pairs; a different test), but a reader will take the two 49s as agreement. | State the comparison: "the model's same-CCD round trip is 49 ns at 4 GHz, against about 98.5 ns measured under WSL2 (66–72 ns on the fastest pairs), so its sharing latencies should be read as lower estimates." |
| K7 | Inconsistent (notation) | `part2:316–324` (p. 49) against `appendices/appendix-e-simulation.tex:14, :46` (p. 162–163); App. G | Part II: $h$ is the *hidden* fraction; $h = 0$ means no overlap and $h$ tends to $1 - 1/n$. Appendix E: $h$ is the overlap factor, the fraction *not* hidden; 1 means no overlap. | Same symbol, opposite meaning: Part II's $h$ is one minus Appendix E's. The name "overlap factor" also runs against its value (more overlap gives a smaller factor). | Use a different symbol in Appendix E (for example $\omega$, the exposed fraction) and state $\omega = 1 - h$ once. Consider "exposed fraction" as the name. |
| K8 | Inconsistent (terminology) | `part5:557` (p. 129); `figures/sim-pingpong.tex` caption; `part5:596`; `part1:183` | "the model's exchange between CCDs takes 2.2 times as long", then "One exchange between two different CCDs crosses the CCD–IOD link four times". | The first "exchange" is a full ping-pong round trip, which contains four hops (`s4_pingpong.csv`: 4 ns per ns of hop; `cachesim.cpp:364–365, :293`). The second is one hop. | Use "round trip" for the first and "one transfer between CCDs (a request and its reply)" for the second, in all four places. |
| K9 | Overstated (minor) | `part5:547` (p. 128) | "The whole difference, a factor of about 2.4, comes from one assumption." | If the simulation charged the four cycles in full, its break-even at 5.15 GHz would be about 15.1/(0.335 × 377) ≈ 0.12, past the analytical 0.10. Hiding the cycles accounts for a factor of 3, partly offset by the model's smaller saving per miss (126 against 159 cycles). | "Most of the difference". |
| K10 | Overstated | `part5:510` (p. 123), `:609`, `part1:183` | "the measured overlap of misses covers the range the model was fitted to", presented as support for the model. | The test can barely fail: the measured fractions run from 0.07 to 1, so nearly any fitted factor falls inside. It shows that a Zen 3 core *can* sustain the implied overlap, not that the fitted values are overlap: the paper itself says they may reflect prefetch counting (`part4:178`). The heading "plausibility check" is right; the summaries are stronger. | Keep the paragraph. In `:609` and `part1:183` use "the implied overlap is within what the core can sustain, which does not show that overlap is the explanation". |
| K11 | Inconsistent | `part4:226` (p. 93) against `part4:218–222`, `part6:172, :234`, `part6:127` and others | "This paper therefore names designs by product rather than by generation." | The sections use "first-generation" 17 times and "first two generations" 4 times. `part4:222` calls the Zen 4 7800X3D "first-generation", which is the very usage the sentence says is ambiguous, since AMD's 2024 talk calls Zen 4 the second generation. | Define once: "first-generation arrangement = cache die on top (Zen 3, Zen 4)", or replace by "Zen 3 and Zen 4 stacks". |
| K12 | Overstated (minor; I28 partly fixed) | `part4:222` (p. 93) | "more than half of the gap therefore remained." | The arithmetic holds (5.5/10, 5.5/7), but this is the same claim I28 asked to drop, restated from the other side. The caveat that it mixes rated maxima with measured averages comes only at the end of the paragraph. | "…a deficit of similar size remained" and keep the caveat. |
| K13 | Inconsistent (minor; J17 partly fixed) | `tab:evidence-strength`, `part6:156` (p. 145) against `part4:194`, `part6:63` | "about 0.6 TB/s". | `part4:194` gives 0.62 at 4.2 GHz and about 0.71 at 4.8 GHz; Lam's multithreaded chart reads 701.67 GB/s (`ChipsAndCheese-7950X3D-2023.pdf`, p. 18). | "about 0.6–0.7 TB/s". |
| K14 | Minor | `appendices/appendix-g-5600x.tex:50` (`tab:m5600x-levels`, p. 167) | Model input: "L3 + 74 ns, about 82 ns at this clock". | L3 + 74 ns at 4.614 GHz is 84.2 ns. 81.9 ns is the model's *output* at 1 GB, where a few per cent of accesses still hit the L3. | "L3 + 74 ns (84 ns); the model gives 82 ns at 1 GB". |
| K15 | Minor | `part5:516`, caption of `fig:sim-working-set` (p. 125) | Random: "every access reaches the L3 or memory". | At 2 MB the 512 KB L2 serves about a quarter of accesses; this is why the speed-up starts at 0.956 rather than 0.949 (`s1_working_set.csv`). | "almost every access, once the working set is well above the L2". |
| K16 | Minor | `appendix-g-5600x.tex:59`, `part3:185` | Core-to-core median 98.6 ns. | Median of the 132 rows of `c2c.csv` is 98.5 ns. No conclusion changes. | Recheck, or state how the figure was formed. |
| K17 | Minor (stale tools text) | `tools/cachesim/README.md:9`; `appendix-e:75`; `sims.py:8` | README lists "victim-cache behaviour" among AMD features the model omits. Run time "about an hour" and "about 40 minutes" on two cores. | J4 removed the claim that Zen's L3 is a victim cache, and the README line still implies it. The two run times disagree (the full study took 7 minutes here on 16 threads). | Reword the README and use one run-time statement. |
| K18 | Figure and format | `tab:m5600x-conditions` (p. 166); PDF pp. 53, 56, 108, 128, 133 | The table is never referenced. Five pages are about half empty because a figure and a table float separately. | It is the only figure or table of 106 with no reference. | Add a reference in App. G; adjust float placement before any submission. |
| K19 | Writing | `part5:536` (eDRAM); `part3:241` (TSV); `front-matter.tex:49` | eDRAM appears before its expansion ("embedded-DRAM", `part6:63`). TSVs appear in Part III before the glossary-linked first use in Part IV. The abstract has "7 %" where the text has "7%". | — | Expand at first use: "embedded DRAM (eDRAM)", "through-silicon vias (TSVs)". |
| K20 | Structure | Part V order, p. 99–103 | `sec:evidence-method` comes third, after two sections that already compare products. | A reader meets comparisons before the rules for reading them. | Move `sec:evidence-method` to the start of Part V. |
| K21 | Structure (half-page rule; judgement) | `sec:dies-per-wafer` (p. 69), TLB reach in `sec:virtual-memory` (pp. 47–48), `sec:cache-clock-model` (pp. 118–120), S0's "Where the shapes differ" (pp. 122–123) | Self-contained explanations of more than about half a page in the main text. | The rule applies at submission. The simulation's length is Ishan's decision (I43) and is not re-raised. | Before any submission, move the working of these to appendices and leave the result. |

**Writing: suggested rewrites (in addition to K19).**

| Location | Problem | Rewrite |
|---|---|---|
| `part6:87` | Double "and" joins three results | "…to about 0.35 per thousand instructions, and the simulation gives 0.38. A program that gains nothing from the cache loses about 7% on the V-Cache CCD." |
| `part6:168` | Semicolon chain with a run-on ("…(`tab:core-to-core`); for most others…") | Start a new sentence at "For most other workloads". |
| `part6:219` | Three sentences of 88, 63 and 77 words in one paragraph | Split at "; in Rome and Matisse" and at "On power the evidence is thin". |
| `part2:89` | 78-word sentence on $ED^2$ | Split after "$E \propto V^2$". |
| `part6:127` | 79-word sentence on Black's simulation | Split after "and raise performance by 15%". |
| `part6:125` | 74-word sentence on AMD's directions | Split after "rather than only cache". |
| `part5:53` | 71-word sentence on latency steps | Split after "added 7 to 8 cycles of L3 latency". |
| `part5:498` | "Its other two inputs are close" (they differ by 8–17% and 20%) | "Its other two inputs differ by about 20% or less." |

No sentence attributes work to an individual, and no gendered pronouns for authors or sources remain (searched all sections, appendices, figures and the glossary).

---

## 3. Regression check

**I1–I43 (fourth review).** Checked in the sources, the code or the CSVs.

| ID | Status | Note |
|---|---|---|
| I1 | Fixed | Metrics are named. S1's "about 5%" (time, with other work) against S2's 5.6% (exposed latency) is correct and explained by the S1 caption. The response's "5.6% in both" no longer describes S1. |
| I2 | Fixed | `cachesim.cpp:334`; `twoccd` preset sets `dram_hop`; 1.20×, 1.39×, 1.08× match. |
| I3 | Fixed, but see K2 | "Upper bounds" is gone. |
| I4, I5 | Fixed | `cachesim.cpp:420` has 10⁻⁶ resolution. |
| I6 | Fixed | `part4:178`. |
| I7 | Fixed | Related error remains (K5). "Eight links" is derived from AMD's stated one link per CCD above four CCDs. |
| I8 | Fixed | Small leftover K13. Mind map reads "AMD: over 2 TB/s peak". |
| I9 | Fixed | |
| I10 | **Regressed** | Fixed for S0–S6; the 5600X text brings the problem back (K1). |
| I11–I16 | Fixed | |
| I17 | Fixed | Now one of several candidates (`part5:502`). |
| I18 | Fixed | |
| I19 | Fixed | Related error K5. |
| I20–I27 | Fixed | |
| I28 | Partly fixed | K12. |
| I29–I38 | Fixed | |
| I39 | Fixed | Figs 16, 40, 57 rendered and clear. |
| I40 | Fixed | ECC at App. D; K19 lists three others. |
| I41, I42 | Fixed | K8 is a new terminology problem. |
| I43 | Declined by Ishan | Not re-raised. |

**J1–J33 (rerun).** All applied except as noted.

| ID | Status | Note |
|---|---|---|
| J4 | Fixed in the paper | README line remains (K17). |
| J6 | **Partly fixed; response inaccurate** | K4. |
| J17 | Partly fixed | K13. |
| J18 | Fixed as asked; then extended | "but the model's structure is confirmed on real hardware" was added later (K1). |
| J1–J3, J5, J7–J16, J19–J33 | Fixed | J3's numbers are right; its wording leads to K8. |

**H1–H24.**

| ID | Status | Note |
|---|---|---|
| H1–H9 | Fixed | |
| H10 | Fixed | Geometric mean labelled as the authors' (I29). |
| H11 | Fixed | |
| H12–H16 | Fixed | |
| H17 | Partly applied | Ishan's decision. |
| H18 | Decision taken | All 13 mind maps rendered and legible; I found no node that adds a claim the text lacks. |
| H19 | Partly applied | Cezanne kept by decision. |
| H20 | Fixed | |
| H21 | Partly fixed | Abstract and date done; `\partbudget` lines and App. A/B `\todo` remain. |
| H22–H24 | Fixed | |

**W1–W18.** All fixed. W4 (TDP) and W5 (NUMA) are defined at first prose use; W10 is at `part5:202`; W18 is settled by the glossary entry `l3d` ("stacked die" now appears once, "stacked CCD" not at all).

**F1–F23 and G1–G20 (spot-check).** Rechecked with no regression: F2 (NUMA labels), F7, F8 (three times, a thirteenth), F19 (bins 150/91), F20, F21, F22; G3, G7, G8, G9 (limited to the 7950X3D in RQ4), G10, G12, G14, G15, G16 (arrow in `fig:stack-process`), G17, G18, G19.

---

## 4. Simulation check

### 4.1 Model description (Appendix E against `tools/cachesim/src/cachesim.cpp`)

| Appendix E statement | Code | Verdict |
|---|---|---|
| L2 contains L1 | `l2Fill` invalidates the L1 copy on an L2 eviction (`:265`) | Correct |
| L3 filled on every miss | `fetch` → `l3Insert` (`:333`, also `:292`, `:308`, `:317`) | Correct |
| L4 inclusive or victim, looked up after L3 | `:322–332` | Correct |
| Remote = 2 × L3 + hop | `:293`, `:309`, `:318` | Correct |
| L4 hit = L3 + L4; DRAM = L3 + ns, plus hop in two-die | `:328`, `:334` | Correct |
| Write hit with other holders: one L3 latency, plus hop if remote | `:364–365` | Correct |
| Write miss: fetch plus a further hop | `:365` after `:347` | Correct |
| L3-only copies invalidated at no cost | `:368` | Correct |
| Overlap scales the part beyond an L2 hit | `:373` | Correct |
| Raw and exposed averages both reported | `:564`, `:566` | Correct |
| Time = max of three limits; link off | `:579`; `link_gbs` not set in `sims.py` | Correct |
| Hand-typed values limited to Milan points and Reguly's ratio | `make_figures.py` docstring | Correct for `make_figures.py`. `compare_5600x.py` also holds the two refit values, which K1 asks to label. |
| Presets | `:659–665` | Match `tab:sim-parameters` |

### 4.2 Reproduction

- Built with MSYS2 UCRT64 `g++ -O2 -std=c++17`. `--selftest`: **8 passed, 0 failures**.
- Reran `sims.py` for s0, s1, s2, s3, s3sens, s4, s5, s6, sens and policy (7 min, 16 threads): **all 16 CSVs byte-identical** to `research/measurements/cachesim/`. `seed_spread.csv` was not regenerated.
- `make_figures.py` on the rerun: **all 15 `figures/sim-*.tex` identical** to the paper's.
- `compare_5600x.py`: **`model-comparison.csv`, `m5600x-latency.tex` and `m5600x-table-mlp.tex` identical**.
- `crosscheck.js`: not run (no Node.js).

### 4.3 Numbers checked against the CSVs (all match)

| Experiment | Values |
|---|---|
| S0 | 46.4, 50.8; 334, 319; 195 at 64 MB; 51 at 96 MB; gross 103 and net 101 cycles per removed miss |
| S1 | 0.949–0.956; 1–5% hot/cold; 1.71 at 40 MB; 3.49 at 96 MB; 1.03–1.28; 1.95; 1.27 |
| S2 | 6.21, 6.87, 5.88 ns; about 10% (9.4–9.6%); 17%; 5.6%; 107…245 cycles; side die 6.46 vs 6.23, 10.34 vs 13.81 |
| S3 | 0.04/0.13/0.22/0.32/0.38/0.50; analytic within 0.05 from 2 to 10%; 0.58, 1.05, 0.17; 0.46, 0.31; 3.78, 1.44, 729, 5.2% |
| S4 | 49, 72.5, 108.5, 144.5, 220.5 ns; 2.2, 2.9, 4.5; 66, 22; 1.20, 1.39, 1.08; 1.35 by the stated estimate |
| S5 | 12% / 20%; 1.7–3.0; 4.0 raw; 1.3–2.3 |
| S6 | 1.08 → 0.68; 0.8; 2.1; 2.7× |
| Sensitivity | 2.4–9.6%; 1.89–3.78; −34% / +32%; 5.1 → 9.6%; policy 1.15–1.19 and 4.27–4.75 |
| 5600X raw files | 0.87, 2.61–2.69, 11.1–12.0, 98.6, 115.3 ns; 66.9 at 64 MB; all MLP fractions; 108, 30, 280–296, 41 GB/s; clock 4.614 GHz |

### 4.4 Calibration against validation

Labelling of fitted values is good throughout S0–S6, and the tables and captions say what is fitted. The exception is the 5600X refit (K1). The genuinely independent results are the default-input comparison and the core-to-core round trip, the second of which is not reported as a comparison (K6).

---

## 5. Spot-checked numbers (43 groups, re-verified in this review)

"Rendered" means the page or image was viewed; "text" means found by search in the extracted PDF.

| # | Claim (location) | Source | OK? |
|---|---|---|---|
| 1 | 16-way, 32 B/cycle, >2 TB/s, +4 cycles, per-die tag and LRU (`part4:152`) | Wuu slide 20, rendered | ✓ |
| 2 | 512 × 128 KB, 1088 × 6 KB, dual rail (App. D) | Wuu slide 25, rendered | ✓ |
| 3 | 1.36× to a tie, about 15%, 5800X3D vs 5900X (`part4:282`) | Wuu slide 29, rendered | ✓ |
| 4 | 24.4 → 40.6 jobs/h, 66%, Synopsys VCS (`tab:amd-reported`) | Wuu slide 31, rendered | ✓ |
| 5 | 81 mm², 7 nm, 32 MB, "from Day 1" | Wuu slide 10, rendered | ✓ |
| 6 | About 1000 mm², 204.8 GB/s (`part3:70, :156`) | Suggs slide 19, rendered | ✓ |
| 7 | 1.15 × 1.17 × 1.47, 2× (`part3:53`) | Suggs slide 4, rendered | ✓ |
| 8 | 1.04–1.25×, 15%, fixed 4.0 GHz (`part4:280`) | Swaminathan slide 19, rendered | ✓ |
| 9 | 74, 416, 125 mm² | Naffziger Fig. 2.2.1, rendered | ✓ |
| 10 | Cost chart: 1.88, 1.65, 1.39, 1.19 against 0.9, 0.77, 0.72, 0.67 | Naffziger Fig. 2.2.2, rendered | ✓ within stated ±0.05 |
| 11 | 90/141/234/128; 94/104/201; 0.81× | Naffziger Fig. 2.2.6, rendered | ✓ |
| 12 | 55 GB/s, 1.46 GHz, 14.6 GT/s, ≥ 4 CCDs, 13 FCLK < 9 ns, 2 pJ/b, 19% | Naffziger p. 44, text | ✓ |
| 13 | 0.1, 106.1–109.5, 228.3–233.9; 0.7, 83.6–84.4, 241.6–246.6; 58.6, 265.2–266.2, 396.9–415.3 | Reguly Fig. 2, p. 3, rendered | ✓ |
| 14 | 1.6×, VM warning | Reguly p. 3, rendered | ✓ |
| 15 | 310 and 1446 GB/s, 3.8/6/14×, 4.8× | Reguly, text | ✓ |
| 16 | 47.49, 51.14, "boosting better" | Cozma 2022a p. 2, rendered | ✓ |
| 17 | 7–8 cycles and preplanning caveat; 25%; 12.5% lower; 3.3 vs 3.15 GHz; 7.6 → 12.5%; 5 → 10% | Cozma 2022b, text | ✓ |
| 18 | 18.45 B/cycle, 7%, 4.8 and 5.15 GHz, 9.67%, 0.35 → 0.28, 1.48 MPKI | Lam, text | ✓ |
| 19 | 34.18 and 10.65 ns; 701.67 and 53.10 GB/s; about 50 GB/s, a quarter | Lam p. 18, rendered | ✓ |
| 20 | 64 GB/s per CCD | Lam, text | ✓ |
| 21 | 1.4 V; 1.28–1.31 V; 10 vs 70 MHz; 300 MHz; 95 °C at 4.7 GHz; sample from AMD; 20 µm; power distribution | Cozma 2024, text | ✓ |
| 22 | xalancbmk little benefit; fotonik3d and roms most memory-bound | Cozma 2024, text | ✓ |
| 23 | 47, 12 cycles; 47 cycles + 74 ns; 64 and 2048 entries; 7/1.7 and 24/5; "about 800 KB"; 40-cycle base slice | 7-cpu, text | ✓ |
| 24 | AIDA64: 68.8/61.8 ns; 9.9/10.9 ns; 633/631 GB/s; 50.7 GB/s; 0.9/0.8, 2.7/2.5 ns; 4400/4850 MHz; 1800 MHz FCLK | FPS Review screenshots, rendered | ✓ |
| 25 | 9654, 9554, 9354, 9334, 9124, 9224, 9174F, 9684X, 9184X (cores, L3, TDP) | EPYC 9004 datasheet p. 2, text | ✓ (K5 for the range) |
| 26 | 4.10 GHz; "spreads the thermal load"; "specialized processing"; "unit of innovation"; one or two links | 4th-Gen white paper, text | ✓ |
| 27 | 4 TB, 128 lanes, 1600 MHz, 96 and 768 MB | EPYC 7003 overview, text | ✓ |
| 28 | 13%, 55%, 0.08 °C, 66%; 15% and 15%; 34% and 8% | Black 2006, text | ✓ |
| 29 | 11.448/5.024 mm²; 6.589/6.904; 3.274/11.898 ns; 0.182/1.127 nJ; 462.9/64.8 mW; 26% | Kim Table 1, text | ✓ |
| 30 | 9.56×; 280 W; 2.45/2.20 GHz; 256/768 MiB | Domke, text | ✓ |
| 31 | 0.81–1.54×; 0.98–1.60×; 1.24–1.70×; 2.67×; 14 821 and 4715; 30 points; 1.54 → 1.24 | Lawenda Table 6 and text | ✓ |
| 32 | Clock ranges; two rows labelled "64-core Genoa", none "Genoa X" | Lawenda Table 5, p. 6, rendered | ✓ |
| 33 | 420 tests; "small set"; 294.4%; "a couple percent" | Phoronix 5800X3D, text | ✓ |
| 34 | 2.2 and 2.45 GHz, same 3.5 GHz boost | Phoronix 7773X, text | ✓ |
| 35 | 19%, 25 workloads, locked 4 GHz, 3800XT, DDR4-3600 | AMD PR, note 4, text | ✓ |
| 36 | 22/24/19/16/30/26/12/6/14/27/23%; 4.55 GHz | TechSpot 5800X, text | ✓ |
| 37 | 10%, 9%, 11%, 15% | TechSpot 5700G, text | ✓ |
| 38 | 3.22%, 4.5–4.55 GHz, "very similar", ring to fabric | CapFrameX, text | ✓ |
| 39 | 96 MB, 5.2/4.7 GHz, 4 nm, 6 nm | AMD 9800X3D specs, text | ✓ |
| 40 | 7 nm on 5 nm, 9 µm, F2B | Alam IMAPS 2024, text | ✓ |
| 41 | < 9, < 40, < 150 µm | Lambert IMAPS 2025, text | ✓ |
| 42 | Butterfly diameter log N + 1; ring, mesh, torus, hypercube values | Sarangi Table, PDF p. 634 | ✓ |
| 43 | 100–300-cycle stall | Sarangi sec. 12.4.8, text | ✓ |

**Worked examples recomputed by hand (all correct).** Pipeline depth 13; CPI 34; AMAT 3 cycles and 1.60/1.46/1.38 ns; write traffic 160 KB and 20 480 against 256; inclusion 36/100 MB; TLB reach and 24 576 pages; Amdahl 5.9/9.1/15.4; directory 18 and 35/315; sharer overhead 1.6/12.5/25%; 1008 mm²; link power 0.9, 3.3 and 7.4 W; bandwidth crossing 3.7 CCDs; xGMI 128/160 lanes; counter 0.12/0.53/0.80 s; yield 82.4/68.8/86.6/38.3%; 44% and 63%; dies per wafer 878/92/760/35 and factors 1.9/2.7/3.5; Murphy triangular and Poisson values; 0.64 chiplet split; pad densities 772/12 346/44 and 16×, 280×; 4096 wires; L3 slice average 8.25; libx264 3.85/1.08/0.40/130 and 3–14%; DCS 3.2, 3.7, 15%, 0.24; `tab:lam-per-miss`; geometric mean 1.114 and 1.094; stock-clock nets; stack yields 85.4/92.2/79.1% and 5%/10%/14%; product-line 100/108/121, 0.7–3%, 140.7; App. D 51 bits, 26-bit tag, 3 × 2¹⁵ sets; analytical model 5.2%, −2.1/−6.7/−8.7%, 0.12/0.35/0.50, 26% and 30%; S4's 1.35; fitted factors 0.335/0.202/0.105; SPEC 18–26%.

Citations: all 36 cited keys are in `references.bib` and named in `research/pdfs/README.md`; the only uncited bib key is `swaminathanNextFrontierEnabling2022`. Vendor claims are attributed to AMD throughout.

---

## 6. Research questions and argument

| RQ | Answered in Conclusions? | Supported? | Consistent with `tab:evidence-strength`? |
|---|---|---|---|
| RQ1 | Yes (`part6:217`) | Yes: yield and dies-per-wafer models, reticle statement, uneven scaling. | Yes (Moderate). |
| RQ2 | Yes (`part6:219`) | Yes on latency, bandwidth, sharing and flexibility. Power is an estimate and is called qualitative. | Yes, except the range in K5. |
| RQ2a | Yes, inside RQ2 | Yes, with AMD's reasoning attributed. | No separate row; adequate. |
| RQ3 | Yes (`part6:221`) | Yes for capacity, latency and footprint; the thermal side is indirect, as stated. | Yes. |
| RQ4 | Yes (`part6:223`) | Direction and latency strong; size of the IPC gain moderate; the model illustrates only. | Yes, except K1's row wording and K4's baseline. |

**Overreach.** Causal claims from uncontrolled comparisons are well handled; chart readings are labelled; CCD counts and Lawenda's misprint are labelled as inferences. The remaining overreach is the 5600X framing (K1, K2, K10).

**The three weakest links, and what would fix each.**
1. **"The model is tested on real hardware."** Fix: K1, K2 and K6. The honest result is still useful.
2. **The apparent 50–130 cycles per removed miss.** It feeds the break-evens and the calibration, and rests on counters that include prefetches. The paper now says so. Showing the conclusions under ±50% in that value, which the S3 sensitivity largely does, is enough.
3. **Product flexibility as the economic case for stacking.** It rests on AMD's statements and an illustrative silicon model; `tab:product-line-silicon` is sound, and the paper now says the silicon saving against two planar dies is small.

**Anything important still missing.** No. The statement that the sources do not say how Zen's L3 is filled closes the gap the fourth review named.

---

## 7. Page counts per part (PDF pages)

| Part | Pages | Count | Target | Comment |
|---|---|---|---|---|
| Front matter | 1–24 | 24 | — | Cover, copyright, acknowledgements, abstract, contents, lists, glossary, in order |
| I Introduction | 25–34 | 10 | 10 | On target |
| II Foundations | 35–56 | 22 | 25 | Short by 3; acceptable |
| III Chiplets | 57–77 | 21 | 25 | Short by 4; acceptable |
| IV Stacked cache | 78–98 | 21 | 25 | Short by 4; acceptable |
| V Case study | 99–135 | 37 | 25 | Over by 12, by Ishan's decision (I43) |
| VI Synthesis | 136–152 | 17 | 20 | Short by 3 |
| **Body** | 25–152 | **128** | 130 | On target overall |
| References; App. A–G; index | 153–169 | 17 | — | |

Structure otherwise holds: each part does one job and hands over to the next. Repetition is now limited; the 130-cycle argument is derived once and cited back. K20 and K21 are the remaining structural points.

---

## 8. Format, leftovers and what was found correct

**Format.** A4 (595.3 × 841.9 pt); 12-pt class option; single spacing; left and right text margins measured at 70–72 pt on two pages; page order cover → copyright → acknowledgements → abstract → contents; generated contents, lists of tables and figures, glossary and index present; diagrams all TikZ or pgfplots; code through `lstlisting` (the `verbatim` of I34 is gone).

**Leftovers.** Two `\todo` notes (App. A, B: known placeholders, wording "as displayed by the tool"); six `\partbudget` status lines, which print "Target length…" under each Part heading and must go before any submission; no `\verify`, no "??", no undefined references or citations, no overfull boxes.

**Figures and tables.** All 59 pages carrying figures were rendered and inspected, including the 13 mind maps, the seven `fig:sim-*` and `fig:m5600x-latency`. No overlapping labels and no unreadable text. Only K18 remains (one unreferenced table, five half-empty pages), plus the stale caption in K3. `fig:numa-latency`, `fig:bandwidth-balance` and `fig:clock-correction` say what they add (J24).

**Correct in the material new since the fourth review.** The 5600X raw numbers as reported; the description of the kit and its limits in App. G, which is candid (WSL2, pinning, unusable 12-thread values, the slow third run); S0's statement of the mismatches themselves; the product-line correction (J2); the replacement-policy tests (J1); the side-die limits (J5); and the move of the analytical model into Part V (J19).
