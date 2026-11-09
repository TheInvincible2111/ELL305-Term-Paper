# Third independent review: `initial-draft-2` (ELL305 term paper)

Reviewed 5 Nov 2026. I used only project-local files: `research/pdfs/` (index `research/pdfs/README.md`),
`sources/archbook.pdf`, `references/references.bib`, the two earlier reviews and their responses, and
`notes/Planning/Submission Format.md`. No web. `tools/`, `Gem5/` and `research/measurements/` were ignored as instructed.

- **Compiled draft:** `build/pdf/ELL305-initial-draft-2.pdf`, 121 pages, A4, built 3 Nov 2026 15:47. No file under
  `initial-draft-2/` is newer than the PDF, so it is current.
- **Build log:** `tmp/linux-build/main-initial-draft-2.log` (3 Nov 15:47): no errors, no undefined references or
  citations, no multiply-defined labels, **no overfull boxes**; 26 underfull boxes only. Biber ran cleanly. The PDF text
  contains no "??".
- **Page numbers:** "PDF p." is the physical page. The printed page number is one lower.
- **Line numbers** refer to the `.tex` files under `initial-draft-2/`.
- **Files changed:** none, apart from this one.

## 1. Overall assessment

The draft is accurate, carefully hedged and unusually honest about its evidence: every one of the 38 numbers I
spot-checked matches its local source, every worked example recomputes, and all 43 earlier findings (F1–F23, G1–G20)
are fixed at the place they were raised. What remains is mostly a consistency problem between the body and its
summaries: hedges added in Parts IV–VI have not reached the Part IV summary, the Part V summary, the RQ4 answer, two
evidence-strength grades and several of the new mind maps, which in places restate claims the text has since withdrawn
(for example "flat to about 96 MB"). There is one plain error of reasoning that recurs in the Conclusions: the paper says
*yield* falls faster than linearly with die area, when what the model shows is that *cost per good die* rises faster
than linearly (the yield curve itself is convex). Two inferences are still stronger than their evidence: that the Cezanne
comparison "bounds" the cost of the chiplet hop, and that the 313-cycle memory latency means a removed miss saves at
least as much as Part IV assumed, which contradicts Part IV's own 130-cycle result. The body is about 94 pages against a
130-page target for the six parts, and about 11 of those pages are mind maps, so Parts II, III and V are well short.
**Provisional examiner judgement:** a strong undergraduate paper in the upper band on technical accuracy and source
handling, held back to "very good, not yet excellent" by summary-level overstatement and by thin length in Parts II, III
and V. **The two changes that would improve it most:** (1) one consistency pass that brings every summary, conclusion,
mind map and caption into line with the hedged body text and with `tab:evidence-strength` (H1, H3–H9); (2) fill the
short parts with argument rather than diagrams, chiefly the RQ2 power/flexibility evidence and a sharper Cezanne and
chiplet-latency analysis (H5, H22), instead of adding further mind maps.

## 2. Findings (most severe first)

| ID | Severity | Location | What the draft says | What the source or rule says | Suggested correction |
|---|---|---|---|---|---|
| H1 | Error | `sections/part6-synthesis.tex:204` (`tab:evidence-strength`, PDF p. 107); `:271` (RQ1, PDF p. 112) | "Yield falls faster than linearly with die area", graded "Strong (mechanism)", with "Textbook yield models (`sec:yield-cost`)" as the evidence. RQ1: "Because yield falls faster than linearly with area". | The Poisson and Murphy yield functions are convex and decreasing, so yield falls *more slowly* than a straight line. A linear fall at the initial slope (−0.2 per cm² at D₀ = 0.2) would reach zero at 5 cm²; the model gives 38.3% at 5.92 cm² (recomputed). What rises faster than linearly is cost per good die, ∝ A/Y(A). Part III says this correctly (`part3-chiplets.tex:43`: "Cost per good die rises faster than area"), as does App. C (factor 2.40 for doubled area). Also, the textbook contains no yield model: I searched Ch. 9–12 of `archbook.pdf`. The models are Murphy 1964 and Dong & Xie 2009. | "Cost per good die rises faster than linearly with die area (fewer dies per wafer and lower yield)". Change the evidence cell to "Murphy and Dong–Xie yield models; AMD's cost chart". |
| H2 | Inconsistent | `sections/part5-case-study.tex:165`; PDF p. 87 | "The measured memory latency of 313–342 cycles lies just above the 100–300-cycle range … so on these processors a removed miss saves at least as much as that example allowed. With the measured values, `eq:vcache-tradeoff` gives a break-even of 3.65/313 ≈ 1.2 percentage points." | Part IV (`part4-stacked-cache.tex:176`) shows that a removed miss saved only about 130 cycles, because an out-of-order core overlaps misses. Part VI then calibrates its model on that 130 (`part6:119`). Latency is not stall saved. With s ≈ 130 cycles, the break-even is 3.65/130 ≈ 2.8 points, more than twice the stated 1.2. The 313 cycles is also a Milan-X figure, applied to a rule calibrated on a Zen 4 desktop part. | "…lies just above the textbook range. As `sec:tradeoff-example` showed, the stall actually saved per miss is smaller, about 130 cycles, so the break-even lies between 3.65/313 ≈ 1.2 and 3.65/130 ≈ 2.8 points." |
| H3 | Overstated (residual of F5/F6/G10) | `sections/part4-stacked-cache.tex:302` (Summary of Part IV); PDF p. 80 | "And the heat path, which the first generation managed with structural silicon and lower clocks, was important enough for AMD to invert the stack in Zen 5." | Part IV's own body (`:209`, `:222`) now says that the lower clocks are only "consistent with" a thermal choice and that the sources attribute them "at least partly" to voltage tolerance (Lam p. 4; Cozma 9800X3D p. 2). RQ3 was fixed (G10); this summary was not. AMD's stated reason for inverting the stack is to put the CCD "closer to the cooling solution" (`AMD-PR-Ryzen-7-9800X3D-2024.pdf`). That is AMD's motive, not a measured importance. | "And the heat path, which the first generation managed with structural silicon (its lower clocks being attributed partly to voltage tolerance), is the reason AMD gives for inverting the stack in Zen 5." |
| H4 | Inconsistent (residual of G11) | `sections/part6-synthesis.tex:277` (RQ4), `:216`; `sections/part5-case-study.tex:279`; PDF pp. 112, 108, 95 | RQ4: "the best such evidence supports the mechanism strongly". Part V summary: "confidence … high for the direction and mechanism". `:216`: "The claims about mechanism are the best supported", listing the IPC gain. | After G11, `tab:evidence-strength` grades the IPC claim as "Moderate: controlled on one processor, not replicated under equal clocks". Only the four-cycle latency claim is graded "Strong". | RQ4: "…supports the mechanism, but on one processor and a handful of workloads". Part V: "high for the direction and the latency cost; moderate for the mechanism's size…". `:216`: separate the latency claim (strong) from the IPC claim (moderate). |
| H5 | Overstated (residual of G2) | `sections/part3-chiplets.tex:295` (also `:291`, the caption of `figures/mindmap-chiplet-tradeoff.tex`, and `tab:evidence-strength` row 2); PDF pp. 58–60, 107 | "It does, however, bound the cost of the chiplet split for this core. Whatever latency the die-to-die hop adds, it is too small to show up clearly against differences in memory configuration." | The only matched comparison sets Cezanne against a **Zen 2** 3950X: a different IOD generation, so not "this core" on both sides. CapFrameX itself offers a confound that could hide the hop: it asks whether Cezanne's "memory interface and the memory controller itself [were] designed with certain compromises in terms of energy aspects" (`CapFrameX-Cezanne-Memory-Latency-2021.pdf`, pp. 2–3). Its framing is also the opposite of the draft's: it expected the monolithic die to recover the latency that chiplets lose, and calls the result "the first field for criticism of Cezanne's design". The draft reports only CapFrameX's ring-to-fabric explanation. | "The sources do not show the hop: the one matched comparison (against Zen 2) found similar latency, but CapFrameX suggests Cezanne's memory interface may trade latency for power, so the comparison cannot bound the hop's size." Mention CapFrameX's power-compromise remark. Apply the same softening in the mind-map caption and the evidence row. |
| H6 | Unsupported | `sections/part6-synthesis.tex:147`; PDF p. 103 | "The independent evidence of Part V confirms that these alternatives [eDRAM, stacked DRAM, STT-RAM, HBM] differ chiefly in which workloads they serve, not in a single ranking." | Part V contains no measurement of any of these alternatives. The only evidence is in Part VI: Lam's Broadwell figures, and Reguly's HBM study, which has no plain Milan. Black and Kim are simulations. | "The figures in `tab:llc-alternatives` suggest that these alternatives differ chiefly in which workloads they serve…". Or delete the sentence. |
| H7 | Inconsistent | `tab:evidence-strength`, rows "Peak V-Cache bandwidth above 2 TB/s" and "Yield falls…" (`part6-synthesis.tex:210`, `:204`); PDF p. 107 | Bandwidth peak graded "Moderate (peak, not sustained)". Yield graded "Strong". | The caption defines "weak" as "vendor-only, uncontrolled or modelled with illustrative inputs". The paper itself says no independent measurement tests the >2 TB/s peak (`:228`; Cozma measured single-thread bytes per cycle only), so that row is vendor-only. The yield row rests on models with illustrative D₀. | Grade the peak "Weak (vendor figure; the independent per-core test measures something else)". Grade yield "Moderate: robust model mechanism, illustrative inputs; AMD's chart agrees". Or relax the caption to fit the grades. |
| H8 | Inconsistent (mind maps) | (a) `figures/mindmap-case-study.tex:17` (PDF p. 82) and the caption of `figures/milanx-latency.tex:23` (PDF p. 88); (b) `figures/mindmap-synthesis.tex:15–18` (PDF p. 97); (c) `figures/mindmap-stacked.tex:23` (PDF p. 62); (d) `figures/mindmap-stack-costs.tex:6` (PDF p. 74) | (a) "Flat to about 96 MB"; caption: "from 32 MB to about 96 MB, Milan-X still hits in its L3". (b) Remaining bottlenecks: "Cache against clock, Bandwidth per core, Heat from stacks". (c) Part IV map: "Separate L4 (Broadwell)". (d) "CCD thinned to 20 µm" under "Heat path". | (a) After F12 the text says Milan-X "stays flat until beyond about 64 MB and then rises" (`part5:161`). (b) The text names "memory bandwidth per core; the die-to-die hop…; and heat removal" (`part6:147`). (c) Broadwell appears only in Part VI, not in Part IV. (d) The text gives thinning no thermal role (F10 removed causal clauses); the mind map implies one. The brief asked that mind maps add no new claims. | (a) "Flat to beyond 64 MB"; caption "…from 32 MB to beyond about 64 MB". (b) Replace "Cache against clock" with "Die-to-die hop". (c) Remove the node, or point it to Part VI. (d) Move thinning under "Manufacturing". |
| H9 | Inconsistent | `figures/stacking-decision.tex` (`fig:stacking-decision`); PDF p. 101 | The "Far larger, or streaming: little change" box gives as examples "largest OpenFOAM and MiniFE inputs". | Part V reports Milan-X still 1.24× faster (text) or 1.22× faster (Fig. 4) on the largest OpenFOAM mesh (`part5:184`; Lawenda pp. 7–8). That is not "little change". MiniFE settles at about 1.04× (`part5:175`), which fits. | Keep MiniFE (n ≥ 330) as the example and drop OpenFOAM. |
| H10 | Inconsistent (method) | `sections/part5-case-study.tex:109`; PDF p. 85 | "Averages across workloads are formed as geometric means of performance ratios, so that no single workload dominates." | No geometric mean is computed anywhere in the paper (searched all sections). Part V reports ranges, medians (Phoronix) and AMD's own averages. | Delete the sentence, or compute geometric means (for example of Lam's six IPC ratios) and report them. |
| H11 | Inconsistent | `sections/part5-case-study.tex:103` vs `sections/part6-synthesis.tex:248`; PDF pp. 85, 110 | Part V: "the group does not have access to the relevant hardware". Part VI: "Measurements on hardware the group owns, which would test some of the assumptions above, are listed as further work." | These contradict each other, and the open questions (`part6:283–292`) list no such measurement. | Choose one statement. If own measurements are planned, add them to the open questions; otherwise delete the sentence at `:248`. |
| H12 | Overstated | `sections/part1-introduction.tex:59`; PDF p. 21 | B "is far cheaper and the only option that can be built at all". | `tab:thought-experiment` and Naffziger say only the **full 64-core part with I/O** exceeds the reticle. Part III (`:259`) treats a 592 mm² compute-only die as conceivable ("assumes that a 592 mm² die could be made at all"). "Far cheaper" rests on an illustrative model and AMD's chart. | "By AMD's account the full 64-core design could not be built as one die, and the models of Part III make B far cheaper…". |
| H13 | Overstated (minor) | `tab:cache-vs-clock` (`part6-synthesis.tex:102`); PDF p. 101 | Cyberpunk 2077: net +6.1%, "Better CCD: V-Cache". | Lam p. 12: the benchmark run "ends up being GPU bound" and V-Cache gave "only … a 0.5 FPS gain". IPC is not frame rate. | Add a note that the Cyberpunk run was GPU-bound, so the IPC gain did not appear as frame rate. |
| H14 | Overstated (minor) | `sections/part5-case-study.tex:49`; PDF p. 83 | Unifying the two 16 MB caches "added 7 to 8 cycles", which "suggests that enlarging slices is cheaper in latency than merging separate caches into one". | Cozma (`ChipsAndCheese-Zen3-VCache-Deep-Dive-2022.pdf`, p. 3) adds: "how much of that extra latency was due to AMD preplanning for V-Cache, we simply can not know". | Add the caveat: "although Chips and Cheese notes that some of the 7–8 cycles may come from provision for V-Cache". |
| H15 | Minor (arithmetic) | `sections/part3-chiplets.tex:293`; PDF p. 58 | Measured clocks "a gap of up to about 7%". | 4.85/4.50 = 1.078 and 4.85/4.55 = 1.066, so the gap is up to about 8%. | "up to about 8%". |
| H16 | Minor (consistency) | `sections/part4-stacked-cache.tex:292`; `sections/part5-case-study.tex:184`; PDF pp. 80, 89 | Part IV: the advantage "fell to 1.24× for the largest mesh". Part V gives both "1.24× on the largest, 39.4-million-cell mesh" and "1.22× ahead at about 308 000 cells per core (xhigh)". | These are the same mesh: Lawenda's text says 1.24× and Fig. 4 says 1.22×. The figure caption explains this, but the Part V paragraph reads as if they were two results. | "…1.24× on the largest (xhigh) mesh (1.22× in their Fig. 4)". Drop the second mention. |
| H17 | Structure (scope) | `sections/part4-stacked-cache.tex:135–141` (`sec:bond-process`) and `figures/stack-process.tex`; PDF pp. 68–69, 77 | Silanol and siloxane chemistry, with a reaction equation, Cu diffusion and dishing. | Part I's scope (`part1-introduction.tex:133`) excludes "fabrication chemistry and process details beyond what is needed to explain an architectural decision". The architectural point, that there is no solder and so the pitch can be fine, needs one sentence. | Cut to two or three sentences without the equation, or state explicitly why the chemistry is needed. |
| H18 | Structure (figures) | 13 mind maps (`fig:mindmap-*`), PDF pp. 25, 27, 29, 38, 45, 60, 62, 74, 82, 93, 97, 106, 111 | Each part opens with a mind map, and several sections close with one. | Together they fill about 11 pages, around 12% of the 94-page body. Several duplicate the section list or a table (`fig:mindmap-misses` duplicates `tab:cache-optimisations`; `fig:mindmap-confounds` duplicates the bullet list beside it). Some captions say nothing to look for ("Mind map of Part VI."). Leaf labels are about 5–6 pt after `\resizebox` (rendered at 110 dpi). They also inflate the page counts in §6. | Keep three or four that add structure (`mindmap-paper`, `mindmap-rq`, `mindmap-chiplet-tradeoff`, `mindmap-stack-costs`), make those half-page size with ≥ 7 pt leaves, give each caption a "what to see" sentence, and drop the rest. |
| H19 | Structure (half-page rule) | `sec:cache-interface` worked examples (`part4:186–196`, about 1.5 pp, PDF pp. 71–73); `part5:49` (one paragraph of about 0.7 pp, PDF p. 83); `sec:cezanne` (about 3 pp, PDF pp. 57–59) | Long self-contained explanations in the main text. | The format rule: a self-contained explanation longer than about half a page goes in a numbered appendix. The tag-overhead and set-indexing examples, and the Cezanne source-by-source table and discussion, are self-contained. The Zen 2 → Zen 3 paragraph is not self-contained, only too long. | Move "the cost of tags" and "an open detail" to an appendix (Appendix D). Keep a three-sentence Cezanne conclusion in Part III with the table and source discussion in an appendix. Split `part5:49` into three paragraphs (vendor IPC; TechSpot; AIDA64 and Chips and Cheese). |
| H20 | Figure | `figures/monolithic-vs-chiplet.tex`, Fig. 16(a); PDF p. 47 | — | Rendered at 150 dpi: the fourth column of core boxes ("C") is partly hidden under the "Shared L3 cache" box, and the "die-to-die link" label in (b) sits on its arrow. | Narrow the core grid or move the L3 box right. Raise the link label. |
| H21 | Format / draft state | `front-matter.tex:49` (abstract `\todo`, PDF p. 4); App. A and B `\todo` (PDF pp. 117–118); `\partbudget` status lines at the start of every Part; `metadata.tex` `\draftdate` 30 Oct 2026 (cover) against a 3 Nov build; caption of `figures/evidence-method.tex:13`, "Planned evidence-analysis procedure", although Part V is written | — | The abstract still describes intentions only ("the paper asks…") and reports no findings. | Rewrite the abstract with the main findings (four cycles; workload dependence; clock gap triples the break-even; chiplet trade-offs). Remove the status lines and the word "Planned" before any reuse. Update the date. The App. A/B placeholders are known. |
| H22 | Structure (argument) | RQ2 answer, `sections/part6-synthesis.tex:273`; PDF p. 112 | The RQ2 answer lists the hop, link bandwidth and NUMA as costs, and yield and the cheaper node as gains. | RQ2 asks about latency, bandwidth, **power** and **product flexibility**. Power is supported only by an illustrative 0.9 W per link using the predecessor's 2 pJ/bit (`part3:158`). Flexibility (one CCD reused across products; `part3:66`) is not mentioned in the answer. The answer also omits the latency *benefit* the paper reports: Rome's average memory latency is 19% lower than Naples's (`tab:numa-latency`). | Add one sentence each on power (state that the evidence is illustrative only), product flexibility, and the 0.81× average latency. |
| H23 | Overstated (minor) | `sections/part4-stacked-cache.tex:198`; PDF p. 72 | "This difference is the main reason a stacked cache can add only four cycles while a die-to-die hop … costs several nanoseconds." | This is the paper's inference. No source compares the two interfaces in these terms (Wuu slide 26 describes only the simple interface). | "This difference probably explains much of why…". |
| H24 | Minor (consistency) | `tab:three-way`, "Memory latency" row (`part6-synthesis.tex:27`); PDF p. 98 | Monolithic: "Shortest on-die paths". Chiplets: "Extra die-to-die hop to memory". | Correct as mechanism, but the paper's only measured comparison (`sec:cezanne`) found no visible advantage for the single die. | Add "(not visible in the Cezanne comparison, `sec:cezanne`)". |

### Writing (at most 25 key cases)

| # | Location | Problem | Suggested rewrite |
|---|---|---|---|
| W1 | `part3-chiplets.tex:293` (PDF p. 58) | "he also notes": a pronoun for a named reviewer | "the reviewer also notes" |
| W2 | `part6-synthesis.tex:63` (PDF p. 99) | "in his chart", "He also notes" | "in Lam's chart", "Lam also notes" |
| W3 | `part1-introduction.tex:24` (PDF p. 21) | "SerDes" not defined at first use | "serialiser–deserialiser (SerDes) links" |
| W4 | `part3-chiplets.tex:279` (PDF p. 57) | "TDP" not defined (also `part5:45`, `:171`) | "thermal design power (TDP)" at first use, plus a glossary entry |
| W5 | `part1-introduction.tex:112`, `part2-foundations.tex:303` | "NUMA" used before it is defined at `part3:82` | Define it at its first use in Part II: "non-uniform memory access (NUMA)" |
| W6 | `part3-chiplets.tex:214` (PDF p. 53) | "HBM" defined only in Part VI (`part6:171`) | "high-bandwidth memory (HBM)" at `part3:214` |
| W7 | `part4-stacked-cache.tex:106` (PDF p. 67) | "SoIC" used before its expansion at `:143` | Expand at `:106` and drop the later expansion |
| W8 | `part4-stacked-cache.tex:278` (PDF p. 79) | "RTL simulation" not expanded | "register-transfer-level (RTL) simulation, a chip-design workload" |
| W9 | `part6-synthesis.tex:63` | "OPIO" not expanded | "Intel's on-package I/O (OPIO) link" |
| W10 | `part6-synthesis.tex:100` (`tab:cache-vs-clock`) | "GHPC" appears without introduction (the Part IV text never names it) | Name it in `part4:288`: "the tank simulator GHPC (+9.7%)" |
| W11 | `part6-synthesis.tex:144` (PDF p. 103) | "with no misses removed the stacked die loses 6.7%": "stacked die" could mean the L3D | "the V-Cache CCD loses 6.7%" |
| W12 | `part2-foundations.tex:89` (PDF p. 32) | "which raises the power budget and lowers the clock of some products" is unclear | "which on some products comes with a higher default power (EPYC 9684X, 400 against 360 W) and lower clocks" |
| W13 | `part3-chiplets.tex:156` (PDF p. 52) | "so the ratio is only indicative, but it is consistent with…": a stacked "but" | "…so the ratio is only indicative. It is, however, consistent with…" |
| W14 | `figures/mindmap-misses.tex:17` | Caption: "each term of the AMAT equation", but compulsory, capacity and conflict misses are not AMAT terms | "the miss classes and AMAT terms, and the techniques that target each" |
| W15 | `figures/mindmap-synthesis.tex:27` | Caption "Mind map of Part VI." says nothing to look for | Add one sentence on what the map shows (for example, which branch answers which RQ) |
| W16 | `part5-case-study.tex:184` (PDF p. 89) | One 170-word sentence chain on cells per core | Split it: the range claim, then the Fig. 4 value, then best utilisation |
| W17 | `part6-synthesis.tex:279` (PDF p. 112) | "AMD Zen shows that they work best together": "best" is not tested against any alternative | "AMD Zen shows that they work well together" |
| W18 | Terminology | "V-Cache CCD", "stacked CCD", "stacked die", "cache die", "L3D" and "extended L3 die" are used interchangeably. The usage is mostly consistent, but "stacked die" is ambiguous | Fix one convention in the glossary: "L3D/cache die" = SRAM die; "V-Cache CCD" = CCD with an L3D on it |

## 3. Regression check, F1–F23 and G1–G20

| ID | Status | Note |
|---|---|---|
| F1 | Fixed | V-Ray 30% named as the largest gain (`part5:49`). |
| F2 | Fixed | NUMA1/2/3 labels in the table and figure. |
| F3 | Not upheld, correctly | Values stand. Their use at `part5:165` is a separate issue (H2). |
| F4 | Fixed | 21 vs 12 cycles; 4 KB penalty left unstated. Re-checked against 7-cpu. |
| F5 | Fixed in body; **residual** | `part4:222` is hedged. The Part IV summary `:302` is not (H3). |
| F6 | Fixed in body and RQ3; **residual** | Part IV summary (H3). |
| F7 | Fixed | 15% iso-clock figure cited to Swaminathan only. |
| F8 | Fixed | "about three times", "a thirteenth". |
| F9 | Fixed | `part3:220` and RQ2 limited to Rome/Matisse. |
| F10 | Fixed in text; minor residual | No causal clause in the text, but `mindmap-stack-costs` places thinning under "Heat path" (H8d). |
| F11 | Fixed | Slides 12–13 (`part6:183`); slide 13 in `tab:packaging-levels`. |
| F12 | Fixed in text; **residual** | `mindmap-case-study` "Flat to about 96 MB" and the `fig:milanx-latency` caption (H8a). |
| F13 | Fixed | Clock-estimation caveat present (`part4:196`). |
| F14 | Fixed | "which Lam suggests is likely due to". |
| F15 | Fixed | "probably". |
| F16 | Fixed | Base and boost clocks in Part IV and `tab:config-pairs`. |
| F17 | Fixed | "analogous effect for 3D stacking" (`part3:233`). |
| F18 | Fixed | One merged 19% row. |
| F19 | Fixed | "10% or more"; bins 150/91; bin convention in the caption. |
| F20 | Fixed | App. C restricted and the 38.3/34.4 gap stated. |
| F21 | Fixed | 2× power-density assumption (`part6:185`). |
| F22 | Fixed | "64 cores per socket". |
| F23 | Unchanged, as agreed | Not an error. |
| G1 | Fixed | Hop graded Moderate. But the row's "too small to see" wording inherits H5. |
| G2 | Fixed in large part; **residual** | Clocks, tentative reading and 1440p caveat are all present. "Bound the cost" overreaches (H5). The "up to about 7%" should be about 8% (H15). |
| G3 | Fixed | "roughly a tenth of … 60 to 90 ns". |
| G4 | Fixed | Both tiling sentences say the V-Cache share is unknown. |
| G5 | Fixed | 5.2 / 5.1 / 4.9% explained. |
| G6 | Fixed | Column labelled "(both 4.2 GHz)"; 0.10 at 4.8 GHz noted. |
| G7 | Fixed | "about twice as much". |
| G8 | Fixed | 30% / 26%. |
| G9 | Fixed | RQ4 names the Zen 4 7950X3D gap. |
| G10 | Fixed in RQ3; **residual** | Part IV summary (H3). |
| G11 | Fixed in table; **residual** | RQ4, Part V summary and `:216` (H4). |
| G12 | Fixed | "is expected to remain faster … no source … measures this directly". |
| G13 | Fixed | `part6:228`. |
| G14 | Fixed | "about 4.7×", with Reguly's 4.8× explained. |
| G15 | Fixed | Prototype drawn as a 1.04–1.25 bar (rendered p. 87). |
| G16 | Fixed | W2W branch starts at "Finished CCD and cache-die wafers"; brackets moved (rendered p. 77). |
| G17 | Fixed | Range attributed to Lawenda *et al.*; 1.22× at xhigh noted. The wording leaves the 1.24/1.22 duplication (H16). |
| G18 | Fixed | 0.8542 × 0.9223 = 78.8% in the table and figure. |
| G19 | Fixed | "In Rome and Matisse…". |
| G20 | Fixed | Sentence split; "In our reading". |

No fix introduced a new numerical error. The residuals above all come from the same cause: a hedge was added at the
point of the finding, but summaries, mind maps or captions written earlier or later still carry the old wording.

## 4. Numbers spot-checked (38)

| # | Value in draft | Location | Source and page | Result |
|---|---|---|---|---|
| 1 | 5700G clock rise of >10% gives 3.22% in games; 4.5–4.55 GHz | `part3:293` | `CapFrameX-Cezanne-Memory-Latency-2021.pdf` p. 6 | ✓ (4.0 → 4.5 GHz is 12.5%) |
| 2 | "very similar" memory latency, 5700G vs 3950X with 1 CCD, both at 4 GHz, same DDR4-3200 CL16 kit | `tab:cezanne-vermeer` | CapFrameX pp. 3, 9 (test setup) | ✓ (but see H5 for the omitted power-compromise remark) |
| 3 | Ring-to-Infinity-Fabric transition costs cycles; AIDA64 criticised as too low | `part3:291` | CapFrameX p. 2 | ✓ |
| 4 | 5700G vs 5800X: Cinebench about 10%, 7-Zip 9%, games 11%, system power 15% lower; "it appears"; 1440p "basically no difference" | `part3:293`, table | `TechSpot-Ryzen-7-5700G-Review-2021.pdf` pp. 13–15, 37–38 | ✓ |
| 5 | 4.6 vs 4.7 GHz boost; 65 vs 105 W; PCIe 3.0 | table | TechSpot 5700G spec table and p. 6 | ✓ |
| 6 | 5600G 4.45 GHz; DDR4-3000 15-16-16-35; L1 4, L2 12, L3 47 cycles; RAM 47 cycles + 74 ns | `part3`, `part5:163` | `7cpu-Zen3-Cezanne-latency.pdf` p. 1 | ✓ |
| 7 | Slice extras for core 0 (0, 6, 1, 10, 6, 13, 10, 20) and core 2 | `fig:l3-slices` | 7-cpu slice table | ✓, all 16 values |
| 8 | Slice average 8, total 48 vs 47 | `part4:35` | recomputed: 66/8 = 8.25 | ✓ |
| 9 | 47 + 74 ns × 4.45 GHz ≈ 375 cycles; ≈ 85 ns | `part5:163`, table | recomputed: 376; 84.6 ns | ✓ |
| 10 | Milan-X +3 to 4 L3 cycles; Zen → Zen 2 about +5; unification +7 to 8 | `part4:152`, `part5:49` | `ChipsAndCheese-Zen3-VCache-Deep-Dive-2022.pdf` p. 3 | ✓ (caveat omitted, H14) |
| 11 | AMD L3 24–28 cycles lower than Intel mesh server parts | `part2:350` | Deep dive p. 4 | ✓ |
| 12 | About 25% more single-thread bytes per cycle; "doubling that AMD claimed"; clock estimated | `part4:152`, `:196` | Deep dive p. 5 | ✓ |
| 13 | Clocks 3.3 / 3.15 GHz; gem5 +7.6%; libx264 and 7-Zip about +5% | `tab:independent`, `tab:clock-correction` | Deep dive pp. 9–11 | ✓ |
| 14 | "Milan-X was boosting better than Milan" in the latency test | `part5:161` | `ChipsAndCheese-VCache-Latency-2022.pdf` p. 2 | ✓ |
| 15 | Plain CCD about 7% faster; 4.8 vs 5.15 GHz all-core L3 load | `part4:220`, `part6:119` | `ChipsAndCheese-7950X3D-2023.pdf` pp. 5, 9 | ✓ |
| 16 | Cyberpunk IPC 1.26 → 1.43; CoD hit rate +47%, IPC >19%; GHPC 9.67%; 7-Zip 9.75% | `part4:288`, `tab:cache-vs-clock` | Lam pp. 12–17 | ✓ (Cyberpunk run GPU-bound, H13) |
| 17 | libx264 1.48 MPKI, 4.9%, "it'll probably come close"; default policy places apps on the faster CCD | `part4:163`, `part6:77`, `:108` | Lam p. 16–17 | ✓ |
| 18 | eDRAM about 50 GB/s, a quarter of Broadwell's L3; OPIO 64-bit at 6.4 GT/s (Haswell); Zen 4 IF 64 GB/s read per CCD | `part6:63` | Lam pp. 18–19 | ✓ |
| 19 | Lam: 8 MB extension per 4 MB slice; "probably … a subset of the address bits" | `part4:190`, `part6:63` | Lam p. 19 | ✓ |
| 20 | Milan 2.9–3.2 GHz, Milan-X 2.8–3.0 GHz | `part5:189` | `Lawenda-L3-Size-CFD-EPYC-arXiv-2025.pdf` Table 5 | ✓ |
| 21 | 0.81–1.54×; Genoa-X 0.98–1.60×; UAP up to 1.47×; up to 30 points; 10–15% → 80% | `part5:184`, `tab:independent` | Lawenda Table 6, pp. 7–9 | ✓ |
| 22 | Best utilisation 14 800 vs 4700 cells per core; "15k to 100k" | `part5:184` | Lawenda p. 7 (14 821; 4715) | ✓ |
| 23 | DRAM about 8× density; stacked DRAM 8–15× bandwidth at 1/2–1/3 latency; SRAM up to 90% of chip area; hundreds of MB | `part2:226`, `part4:30`, `:286` | `Mittal-Vetter-DRAM-Cache-Survey-TPDS-2016.pdf` sec. 1 | ✓ |
| 24 | Black: 88.35 → 92.85 °C (SRAM), 88.43 °C (DRAM); Core 2 Duo baseline | `part4:207` | `Black-…-MICRO-2006.pdf` Fig. 8, Table 3 | ✓ |
| 25 | Black: 13% and up to 55%, −66% off-die BW and bus power, +0.08 °C; logic+logic 15% / 15%, 1.3×, +14 °C, 26 °C with 2× density, 34% / 8% | `part6:65`, `:185` | Black abstract and sec. 5 | ✓ (the body text gives 50% where the abstract gives 55%; the draft follows the abstract) |
| 26 | Kim Table 1: 5.0/11.4 mm²; 65/463 mW; read 6.9/6.6 ns; write 11.9/3.3 ns; write energy 1.13/0.18 nJ; 26% | `part6:65`, `tab:llc-alternatives` | `Kim-…-Electronics-2022.pdf` Table 1, p. 3 | ✓, all six pairs |
| 27 | Textbook: 100–300 cycles (sec. 12.4.8); leakage 20–40%; 200 °C, 60–100 °C, 120 °C; window 64–128; 0.08/0.005 µm², 1–5 / 50–200 cycles; Ex. 142 = 12.9; 32–64 cores by 2020; 35 vs 200 processors | Parts I, II, IV | `archbook.pdf` Ch. 10–12 | ✓ |
| 28 | 10–20 mm route; 55 GB/s at 1.46 GHz, 14.6 GT/s; ≥ 4 CCDs; 13 FCLK, <9 ns; 2 pJ/b; 9-2-9 / 5-2-5; 74 mm²; 19%; "way beyond maximum reticle size" | Part III | `AMD-Chiplet-Architecture-ISSCC-2020.pdf` pp. 1–2 | ✓ |
| 29 | 4 TB per socket; 768 MB; FCLK 1600 MHz with DDR4-3200; >200× / >15×; IOD labelled 14 nm; central L3 tiles; diagonal quadrants | Parts III, IV | `AMD-EPYC-7003-Microarchitecture-Overview.pdf` | ✓ |
| 30 | 9 µm; micro-bump 50 → 36 µm; >3× energy efficiency; >15× density; lower TSV C and L | `part4:113–116` | Swaminathan slide 17 (rendered) | ✓ |
| 31 | 64 MB cache die on an up-to-8-core CCD, Cu–Cu bond; future schemes (DRAM on CPU, cores on cores, folding) | `part4:100`, `part6:181` | Swaminathan slides 15, 20 (rendered) | ✓ |
| 32 | uHAST 96 h, TC 2500 cycles, HTS 1000 h | `part4:269` | `AMD-IMAPS-2024-2nd-Gen-VCache-Zen4.pdf` slide 14 | ✓ |
| 33 | 7800X3D max 1.2 V; 300 MHz deficit vs 9700X; 95 °C; "biggest weakness"; same 4 cycles; 20 µm | `part4:220–230` | `ChipsAndCheese-9800X3D-2024.pdf` pp. 1–5 | ✓ |
| 34 | 9800X3D 4.7 GHz base, 96 MB, TSMC 4 nm CCD, 6 nm IOD | `part5:77`, `tab:later-x3d` | `AMD-Ryzen-7-9800X3D-Specs.pdf` | ✓ |
| 35 | 3700X 3.6/4.4 GHz, 65 W; 5800X 3.8/4.7 GHz, 105 W | `part5:45` | `AMD-Ryzen-3000-5000-Datasheet.pdf` | ✓ |
| 36 | 19% IPC, locked 4 GHz, 3800XT vs 5800X, DDR4-3600 (note 4, R5K-003) | `part5:47`, `tab:amd-reported` | `AMD-PR-Ryzen-5000-Launch-2020.pdf` notes | ✓ |
| 37 | 420 tests; tConvolve gridding 294%; OpenFOAM 68%; "a small set of tests" | `part5:193` | `Phoronix-5800X3D-vs-5800X-2022.pdf` pp. 1–2 | ✓ (294.4%, 68.1/68.4%) |
| 38 | Domke: 2.45 / 2.20 GHz base, 280 W, 16-channel DDR4, up to 3.4× | `part5:171–173` | `Domke-…-TACO-2023.pdf` Table 1, abstract | ✓ |

**Worked examples recomputed** (all ✓ unless noted):
- **Yields:** 82.4 / 68.8 / 86.6 / 38.3%.
- **Dies per wafer:** 955.2 − 77.5 = 877.7 and 119.4 − 27.4 = 92.0. Sets per wafer 95.0 / 35.2. Factors 1.89 / 2.70 / 3.52. Silicon ratios 0.442 / 0.631.
- **Stack yield:**
  - planar 154.2 mm²; D2W 139.3 mm²; W2W 154.9 mm²;
  - savings 9.7 / 5.1 / 13.7% at D₀ = 0.2 / 0.1 / 0.3.
- **Pad density:** 44 / 625 / 772 / 12 346 connections per mm². Interface area 5.3 and 92.2 mm².
- **Tags:** 9.96% overhead; 51.0 bits per line.
- **AMAT:** 1.459 and 1.379 ns; L3-and-memory share 0.534 and 0.454 ns.
- **Amdahl:** 5.93 / 9.14 / 15.42.
- **Cache–clock model:** all 15 table cells and the break-evens 0.12 / 0.35 / 0.50. Memory share 30.3% at 5.15 GHz, 26.2% at 4.2 GHz.
- **`tab:cache-vs-clock`:** −1.96 / 2.52 / 2.62 / 6.07 / 11.21%.
- **Clock correction:** 1.620 / 0.852 / 1.127 / 0.991.
- **MiniFE bytes per point:** 244–311 and 276–328.
- **Other values:**
  - link power 0.88 W;
  - Rome 1008 mm², 58.7%;
  - Xeon Max 1446/310 = 4.66;
  - STREAM efficiency 75.7%;
  - Black 14/4.5 = 3.1×;
  - Cezanne 12.6 × 4.0 = 50.4 cycles and 10.9 × 4.85 = 52.9 cycles;
  - 5800X/5700G clock ratio up to 1.078 (H15);
  - break-even 3.65/313 = 1.17 points, but 3.65/130 = 2.81 points (H2).

**Internal consistency of repeated values:**

| Value | Result |
|---|---|
| +4 cycles | Consistent in text, tables, `fig:libx264-waterfall`, mind maps and the conclusions. Milan-X is correctly given as 3–4. |
| 96 MB, 768 / 1152 MB | Consistent. |
| 7% clock gap and the 1.073 ratio | Consistent; the difference between them is explained. |
| 4.8 vs 5.15 GHz | Consistent in the text, the table, `fig:cache-clock-model`, `mindmap-stack-costs` and RQ4. |
| 130 cycles per removed miss | Consistent in Part IV, Part VI and the waterfall figure. Part V's 313-cycle reasoning contradicts it (H2). |
| <9 ns hop | Consistent in Part I, Part III, Part IV, `fig:l3-miss-path` and `mindmap-chiplets`. |
| 204.8 GB/s and 3.2 / 4.8 GB/s per core | Consistent; Table 13 rounds to 205. |
| 47 vs 39 cycles | This pair does not occur in the draft or the sources. The draft's L3 pairs are 47 (5600G) vs 47.49 / 51.14 (Milan / Milan-X) and ≈ 44 vs 53 (3700X / 5800X, AIDA64). All are consistent. |

## 5. RQ-by-RQ assessment

| RQ | Answered in Conclusions? | Supported by Parts II–V? | Consistent with `tab:evidence-strength`? |
|---|---|---|---|
| RQ1 | Yes (`part6:271`) | Yes: reticle (Naffziger), yield and cost models (Part III, App. C), uneven scaling (Naffziger; Wuu slide 6). The SRAM-scaling claim is vendor-only, which the text acknowledges (`part4:18`). | **No.** The answer and the table state the yield mechanism wrongly (H1), and grade a modelled claim "Strong" (H7). |
| RQ2 | Partly (`part6:273`) | Latency, bandwidth and NUMA: yes, from vendor figures plus worked examples. **Power:** only an illustrative 0.9 W per link from the predecessor link. **Product flexibility:** argued in Part III (`:66`, `:74`) but missing from the answer. The 19% latency *benefit* is also missing from the answer (H22). | Yes for the hop (Moderate). There is no table row for bandwidth, power or flexibility; consider adding one. |
| RQ2a | Yes | Yes. Naffziger's reach argument and Lambert's pitch targets. The answer is correctly limited to Rome and Matisse. | n/a (no row); the evidence is vendor-only and should be graded so. |
| RQ3 | Yes (`part6:275`) | Yes for capacity, planar limits and the stack. The thermal part is indirect: no thermal measurement of a hybrid-bonded stack, which `sec:limitations` admits. | Yes ("Moderate, indirect"). The Part IV summary is stronger than both (H3). |
| RQ4 | Yes (`part6:277`) | Yes. Lam (controlled), Domke and Lawenda (uncontrolled clocks), Phoronix (breadth), and the clock-correction and cache–clock models. | **No.** "supports the mechanism strongly" against "Moderate" in the table (H4). |

**Overreach** (brief item 7): causal claims from uncontrolled comparisons appear in H5 (Cezanne), H6 and H24.
Treating a measured latency as a measured saving appears in H2. Summaries stronger than `sec:limitations` allows appear in
H3 and H4. Models presented as measurements: none found; every model is labelled "illustrative". Simulations presented as
products: none; Black, Kim and Swaminathan's schemes are all labelled.

**Three weakest links in the argument:**
1. **The size of the V-Cache benefit rests on one controlled source.** Lam covers one processor and six workloads. The
   130-cycle calibration that drives `eq:cache-clock-model`, `fig:thread-placement` and the RQ4 threshold comes from one
   program (libx264). *Fix:* run the model's sensitivity to s (for example 100–200 cycles) and to the clock pair, and
   report the threshold as a range. Add any second fixed-clock source; the group's own fixed-clock measurement would serve
   if that decision is taken (H11).
2. **The cost of the chiplet hop is vendor-only, and the one independent check cannot isolate it.** Cezanne is compared
   with Zen 2 for latency, and with Vermeer at different memory, fabric and core clocks. CapFrameX suggests that power
   trade-offs in Cezanne's controller could mask the hop. *Fix:* present the hop's size as vendor-reported and unresolved
   by independent data (H5). A same-tool, same-memory pointer-chase comparison of the 5700G and 5800X, from a source or
   from the group, would settle it.
3. **The thermal argument is inferred, not measured.** It rests on clock and voltage limits that the sources attribute
   partly to voltage tolerance, a 2006 simulation, and AMD's stated motive for the inversion. *Fix:* phrase RQ3's thermal
   clause as AMD's stated design rationale plus consistent indirect evidence. The 300 MHz residual deficit of the
   inverted Zen 5 stack (Cozma) is the best available quantitative clue and could be developed: if the stack is inverted
   and a deficit remains, part of the first-generation penalty was probably not thermal.

**Anything important missing** (undergraduate level, only where it matters):
- **Power in RQ2** has almost no evidence: no figure for IOD power or idle package power. Either find a source, or say
  plainly that RQ2's power dimension is answered only qualitatively.
- **No non-AMD chiplet CPU** is discussed. Broadwell eDRAM and Xeon Max HBM are cache and memory examples, not chiplet
  CPUs, so the claim that the "architectural principles apply … in general" (`part1:128`) is untested. One paragraph on
  a non-AMD chiplet or tile CPU, from a local source, would support external validity. Add one only if a PDF can be
  obtained.

## 6. Page counts by part (PDF pages, including mind maps)

| Part | PDF pages | Pages | Target | Mind-map pages (approx.) | Needs |
|---|---|---|---|---|---|
| I Introduction | 20–27 | 8 | 10 | 2 (Figs 3, 4) | Close to target. Add a short related-work paragraph (what earlier surveys, such as Liu *et al.* and Mittal–Vetter, did and did not cover) and a statement of findings. |
| II Foundations | 28–43 | 16 | 25 | 1.5 (Figs 5, 10) | The largest gap (−9). Underused textbook material directly relevant to the paper: cache write policies and inclusion (Ch. 11); multithreading and memory-level parallelism (sec. 12.4.8, which supports the 130-cycle argument); a worked directory-protocol example; virtual memory and TLBs (Ch. 11), which Part V's TLB remark needs. |
| III Chiplets | 44–60 | 17 | 25 | 1.5 (Figs 14, 25) | −8. Develop RQ2 power and product flexibility (H22). Add a short treatment of cross-CCD coherence cost (with a source if available). Move part of `sec:cezanne` to an appendix (H19) and replace it with argument. |
| IV Stacked cache | 61–80 | 20 | 25 | 1.5 (Figs 26, 35) | −5. Could gain from a clearer comparison of the D2W cost model with AMD's flexibility argument. Moving the tag and indexing examples to an appendix (H19) will lower the count, so add argument rather than detail. |
| V Case study | 81–95 | 15 | 25 | 1.5 (Figs 39, 48) | The largest relative gap (−10). Room for a fuller per-source evidence table (conditions, metric, controls) and a geometric-mean summary as the method promises (H10). Also a per-workload discussion of Lam's six results and of the Genoa-X data, which is now one sentence. |
| VI Synthesis | 96–113 | 18 | 20 | 2.5 (Figs 50, 54, 56) | Close to target. Mostly needs consistency fixes (H1, H4, H6, H7), not length. |

The body runs to 94 pages against a 130-page target for the six parts. Without the mind maps, the prose-and-figure
content is about 83 pages. References, appendices and index take PDF pp. 114–121; front matter takes pp. 1–19.

## 7. What I checked and found correct

### Build, format and rules
- **Build freshness and log:** clean, with no overfull boxes. All `fig:`/`tab:` labels are referenced in the text.
- **Citations:** 36 distinct keys, all in `references.bib`, each with a local PDF marked present in
  `research/pdfs/README.md` and present on disk. The only missing file listed (Swaminathan 2022) is not cited.
- **Vendor attribution:** consistently done ("AMD reports", "AMD's own comparisons and should be read as engineering
  claims", the `tab:amd-reported` caption).
- **Format:**
  - A4, 12 pt, `\singlespacing`, `geometry` margin 1 in (`paper/styles/ell305-format.tex:9`, `:82`). Rendered margins
    measure 1 in.
  - Page order: cover (p. 1) → copyright and IP (p. 2) → acknowledgements (p. 3) → abstract (p. 4) → generated contents
    (p. 5), List of Tables (p. 10), List of Figures (p. 12), Glossary (p. 18).
  - Index on p. 121. Appendix A (p. 117) and B (p. 118) exist, with placeholder text that already uses "as displayed by
    the tool" wording.
  - All diagrams are TikZ or pgfplots. The only `\includegraphics` is the cover logo.
  - The draft contains no code, so the listings/minted rule is satisfied trivially.
  - Copyright and acknowledgement wording matches `Submission Format.md`.
- **Group attribution:** no work is attributed to an individual. The names appear only on the cover and in the
  acknowledgements' collective statement.

### Remaining markers
- Three `\todo`: the abstract (PDF p. 4), App. A (p. 117) and App. B (p. 118).
- No `\verify`, no "??", no undefined references or citations, no overfull boxes.
- The six `\partbudget` "Target length … Draft status" lines are working-draft markers that also need removal (H21).

### Mind maps (brief item 2)
- 9 of the 13 restate only what their part says, with correct values: `mindmap-rq`, `-paper`, `-foundations`,
  `-misses` (caption wording aside, W14), `-chiplets`, `-chiplet-tradeoff` (caption aside, H5), `-confounds`, `-future`
  and `-implications`. "Re-check by phase" in the last is from `fig:thread-placement`.
- The other four have the issues listed in H8.

### `sec:cezanne` / `tab:cezanne-vermeer` after G2/G3
- Every cell value checked against TechSpot, CapFrameX, 7-cpu, Chips and Cheese and The FPS Review. The caveats on tools,
  memory and clocks are accurate. The G2 and G3 fixes are present.
- The remaining issues are the "bound" inference (H5) and the 7% vs 8% clock gap (H15).

### Other checks
- **Figures:** I rendered PDF pp. 21–111 wherever a figure appears (53 pages), at 60 dpi, and zoomed in where needed.
  Apart from H20, no label overlaps a mark. The 68.8 / 61.8 bar labels on p. 84 touch but stay legible, as noted in the
  second review. No figure duplicates a table without adding something: `fig:numa-latency`, `fig:bandwidth-balance` and
  `fig:clock-correction` each add a visual comparison and are captioned as the same data. Mind-map leaf text is small
  (H18).
- **Earlier cannot-verify items:**
  - Lam's libx264 MPKI attribution: the chart values agree.
  - Broadwell vs Haswell OPIO: the draft now says "on the related Haswell design", matching the source.
  - The 9800X3D press-release quote: the legible fragments match.
  - Reguly's Fig. 1 sweep: still not re-read. It does not affect any conclusion.
