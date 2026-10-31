# Second independent review: `initial-draft-2` (ELL305 term paper)

Reviewed 1 Nov 2026. I used only the project-local files: `research/pdfs/`, `sources/archbook.pdf`,
`references/references.bib` and the first review and its response. I did not use the web.

- **Compiled draft:** `build/pdf/ELL305-initial-draft-2.pdf`, 108 pages, built 1 Nov 2026 02:46. No file under
  `initial-draft-2/` is newer than the PDF, so it is current.
- **Page numbers:** "PDF p." means the physical page in that file. The printed page number is one lower.
- **Line numbers:** these refer to the `.tex` files under `initial-draft-2/`.
- **Files changed:** none, apart from this one.

## 1. Overall assessment

The new material is careful and mostly correct.

**What checks out:**
- Every row of `tab:cache-clock-model` and all three break-even points (0.12 / 0.35 / 0.50) reproduce exactly from the
  inputs stated in the text. The plotted curves use the same formulas.
- Every value in the new figures matches its source. I checked charts and screenshots by reading the source images
  directly:
  - Lawenda Fig. 4 labels and Table 3 cell counts;
  - the AIDA64 screenshots from The FPS Review and CapFrameX;
  - Naffziger's NUMA figure and 13-FCLK round trip;
  - the Chips and Cheese chart images;
  - Reguly's ratios and speed-ups;
  - the Alam bonding slides;
  - the EPYC 9004 datasheet.
- The regression check is good: 19 of the 23 first-review findings are fully fixed. F3 was correctly rejected: the
  embedded chart images do carry 342.11/313.11 cycles and 105.59/89.21 ns. F23 was left alone, as agreed. F6 and F9
  are only partly fixed, because their wording survives in the Conclusions.
- Build hygiene is clean:
  - the last build log has no undefined references or citations, no multiply-defined labels and no overfull boxes;
  - the PDF contains no "??";
  - all 36 citation keys exist in `references.bib` and have a local PDF listed in `research/pdfs/README.md`.

**What needs attention** is mainly reasoning, not arithmetic:
- **Evidence-strength table:** it cites, as independent support for the chiplet memory-latency hop, a comparison that
  cannot show that hop. The paper's own one-die-against-chiplet comparison (Part III, Cezanne) found no measurable
  advantage for the single die.
- **Cezanne section:** its closing paragraphs draw causal conclusions from a comparison it has just called uncontrolled.
- **Reguly tiling result:** the 4× speed-up from tiling on Milan-X is presented as a payoff of the stacked cache, but
  the study has no plain-Milan comparison.
- **Cache–clock model:** the stated reason for the gap between model and measurement is wrong, and the "equal clocks"
  column does not say which clock it uses.

## 2. Findings (most severe first)

| ID | Severity | Location | What the draft says | What the source says | Suggested correction |
|---|---|---|---|---|---|
| G1 | Inconsistent | `sections/part6-synthesis.tex:197`, `:208`; PDF p. 95 | `tab:evidence-strength` grades "Chiplets add a die-to-die hop to memory" as "Strong for the effect", citing AMD's NUMA latencies and "independent memory-latency measurements (`sec:zen2-zen3`)". The next paragraph calls the hop "well supported and independently replicated". | `sec:zen2-zen3` compares two **chiplet** parts (3700X, 5800X; FPS Review AIDA64 screenshots), so it cannot show the hop. The paper's only one-die-against-chiplet comparison, `sec:cezanne` (`part3-chiplets.tex:287`), concludes that "the sources thus show no memory-latency advantage for the monolithic die". CapFrameX found the 5700G "very similar" to a Zen 2 part with one CCD active (`CapFrameX-Cezanne-Memory-Latency-2021.pdf`, p. 3). The hop's existence and size (13 FCLK, under 9 ns) come from AMD alone (`AMD-Chiplet-Architecture-ISSCC-2020.pdf`, p. 2). | Grade the hop as vendor-described (moderate), with its size not independently isolated. Cite `sec:cezanne` as the independent check, and say it found the hop too small to see against memory-configuration differences. Drop "independently replicated" for this claim. |
| G2 | Overstated | `sections/part3-chiplets.tex:289`, `:291`; PDF p. 52 | "The boost clocks differ by only about 2% (4.6 against 4.7 GHz), so clock speed does not explain the gaming gap." Then: "it is outweighed in games by the 16 MB of extra L3 that the chiplet design carries … the chiplet part was the faster of the two", and the choice "was not a choice between speed and cost". | These are rated boost clocks, not measured ones. CapFrameX (p. 5) measured the 5700G at 4.5–4.55 GHz in games. The 5800X ran at 4.85 GHz in The FPS Review's run (`FPSReview-…-p6-AIDA64.pdf`). That gap is about 6–7%, not 2%. TechSpot (`TechSpot-Ryzen-7-5700G-Review-2021.pdf`) is tentative: "it **appears** as though … cache capacity plays a much more vital role". It also adds that at 1440p "there'll be basically no difference". Other differences remain uncontrolled: TDP 65 vs 105 W, PCIe 3.0 vs 4.0 with an RTX 3090, and integrated graphics. | Use measured clocks or say none are reported for TechSpot's runs. Present the L3 explanation as TechSpot's tentative reading. Replace "the chiplet part was the faster of the two … not a choice between speed and cost" with "in TechSpot's 1080p CPU-limited tests the chiplet part was faster". |
| G3 | Overstated | `sections/part3-chiplets.tex:287`; PDF p. 52 | The package link round trip is "under 9 ns … a few nanoseconds in a memory access of 60 to 90 ns". | Naffziger (p. 2): "13 FCLKs, or less than 9ns". At 1.46 GHz FCLK, 13 cycles = 8.9 ns, which is about 10–15% of a 60–90 ns access. | "up to about 9 ns, roughly a tenth of a 60–90 ns memory access". |
| G4 | Overstated (causal) | `sections/part6-synthesis.tex:169`, `:248`; PDF pp. 93, 97 | "The large stacked cache thus rewards code written to use it." Reguly's 4× tiling gain on Milan-X "shows how much a code can gain by being written for it". | Reguly (`Reguly-Bandwidth-Bound-Apps-PMBS-2023.pdf`, sec. 6) tests no plain Milan, so the 4× cannot be attributed to the stacked cache. The three platforms also differ in vendor, ISA, compiler (AOCC vs oneAPI), SMT and core count. Reguly says only that the gains "correlate well" with the cache-to-memory bandwidth ratio (14×/6.3×/3.8×). | "Consistent with the high cache-to-memory bandwidth ratio of the stacked-cache system; Reguly did not test a plain Milan, so the share due to V-Cache is unknown." |
| G5 | Inconsistent | `sections/part6-synthesis.tex:115`; PDF p. 91 | At equal clocks the model gives "a 5.2% gain, close to the 4.9% measured; the small difference comes from rounding s". | The model's 5.2% is a speed-up, T(plain)/T(stacked) − 1. Its calibration inputs, IPC 1.36 → 1.43, already imply a 5.15% speed-up. Using the unrounded stall (128.5 cycles instead of 130) still gives 5.1%, so rounding s explains only about 0.15 points. The rest is the rounding of the two IPC values: Lam's 4.9% IPC gain (`ChipsAndCheese-7950X3D-2023.pdf`, p. 16) comes from unrounded counters. The 4.9% in `part4-stacked-cache.tex:167` is a different quantity (36 of 735 fewer cycles), and it equals 4.9% only by coincidence. | "The model gives 5.2%; the IPCs used for calibration (1.36, 1.43) imply 5.1%, and Lam reports 4.9% from unrounded counts." |
| G6 | Inconsistent (minor) | `tab:cache-clock-model` "Equal clocks" column; `fig:cache-clock-model`; PDF pp. 91–92 | "Equal clocks" gives a 5.2% gain at 0.4 misses removed and a break-even of 0.12. The text says "the clock gap roughly triples the number of misses … from about 0.12 to about 0.35". | Because memory time is fixed in ns, the equal-clock result depends on the clock chosen. At 4.2 GHz: +5.2%, break-even 0.118. At 4.8 GHz: +6.1%, break-even 0.104. At 5.15 GHz: +6.6%. The 0.12 → 0.35 comparison therefore mixes 4.2 GHz with 4.8/5.15 GHz. Against equal clocks at 4.8 GHz the factor is 3.4. | Label the column "equal clocks (4.2 GHz)". The "roughly triples" conclusion survives either way. |
| G7 | Overstated (minor) | `sections/part6-synthesis.tex:140`; PDF p. 91 | "So the clock penalty matters as much as the four cycles of added latency." | In the model the four cycles alone set a break-even of 0.12. The clock gap adds about 0.23 more, roughly twice as much. | "matters about twice as much as". |
| G8 | Minor | `sections/part6-synthesis.tex:140`; PDF p. 91 | "about 30% of the plain die's time goes to memory stalls". | From the model inputs: 26% at 4.2 GHz, 29% at 4.8 GHz, 30% at 5.15 GHz. | "about 30% at 5.15 GHz (26% at the 4.2 GHz calibration point)". |
| G9 | Overstated | `sections/part6-synthesis.tex:265` (RQ4); PDF p. 99 | "the clock gap of the first two generations roughly triples that threshold". | The model uses only the Zen 4 7950X3D gap (4.8 vs 5.15 GHz, Lam p. 9). For Zen 3, Lam (p. 5) gives a different gap: 5800X3D 4.5 GHz against 5950X 5.05 GHz, "around 10%". The model was not run for that gap. | "the 7% clock gap of the Zen 4 part roughly triples that threshold". |
| G10 | Overstated (residual of F6) | `sections/part6-synthesis.tex:263` (RQ3); PDF p. 99 | "its price is a harder heat path, which AMD first managed with structural silicon and lower clocks". | Part IV now says the lower clocks are "consistent with" a thermal choice, and that the sources attribute them "at least partly to the stacked cache's lower voltage tolerance" (`part4-stacked-cache.tex:205`; Lam p. 4). Open question 5 (`:276`) asks exactly this. | "…which AMD first managed with structural silicon, alongside lower clocks and voltage limits that the sources attribute partly to voltage tolerance". |
| G11 | Inconsistent | `sections/part6-synthesis.tex:199`; PDF p. 95 | "Stacked cache raises IPC on cache-sensitive work" is graded "Strong for the mechanism". | The caption defines "strong" as independent, controlled **and** replicated. Only one source is controlled (Lam, one processor). The two HPC studies run with clocks not fixed, as the row itself says. Part VI `:232` agrees that "only one independent source controls every listed factor". | Grade it "Moderate (controlled but not replicated)", or relax the caption's definition. |
| G12 | Unsupported | `sections/part6-synthesis.tex:214`; PDF p. 96 | "For workloads with fine-grained sharing between many cores, a monolithic die remains faster." | No citation. No local source measures core-to-core sharing on a monolithic die against a chiplet part. The AnandTech core-to-core article is listed as missing in `research/pdfs/README.md`. Reguly measures Milan-X core-to-core latency only against Intel parts, and finds overall latencies "comparable" and cross-socket latency 1.6× worse. | "is expected to remain faster, since cross-CCD transfers cross the IOD (`sec:d2d`); no source here measures it." |
| G13 | Overstated (minor) | `sections/part6-synthesis.tex:220`; PDF p. 96 | Independent measurements "find a smaller bandwidth gain than AMD's peak figure". | Cozma's figure is about 25% more bytes per cycle for one thread, with the clock estimated (`ChipsAndCheese-Zen3-VCache-Deep-Dive-2022.pdf`). AMD's figure is an aggregate peak (>2 TB/s). `part4-stacked-cache.tex:192` itself says these are not the same quantity. | "no independent measurement tests AMD's aggregate peak; the one single-thread measurement shows a smaller per-core gain". |
| G14 | Minor | `sections/part6-synthesis.tex:169`; PDF p. 93 | Xeon Max STREAM "1446 GB/s, 4.8× the Milan-X figure". | 1446/310 = 4.66. Reguly's "4.8x" is stated against the 8360Y and 7V73X together (296 and 310 GB/s), and against the 8360Y alone it is 4.89. | "about 4.7×" or "4.8× according to Reguly". |
| G15 | Minor (figure) | `figures/vendor-vs-independent.tex`; PDF p. 79 | The AMD prototype vs 5900X result is drawn as a single dot at 1.15. | The paper itself gives the range 1.04–1.25 across five games (`part4-stacked-cache.tex:268`; Swaminathan slide 19). The figure's purpose is to compare spreads, so leaving this range out makes AMD's spread look narrower. | Draw a 1.04–1.25 bar with the dot at 1.15. |
| G16 | Minor (figure) | `figures/stack-process.tex`; PDF p. 68 | The "skip test" arrow to wafer-to-wafer bonding starts from the box "Test CCD and cache-die wafers; keep only known-good dies". | Wafer-to-wafer bonding skips that step (Alam slide 10: "KGD" applies to D2W). In the render, the grey group bracket lines also run along the left edges of the step boxes. | Start the W2W branch before the test box, or label the box "Die-to-wafer flow". Move the bracket lines left. |
| G17 | Minor | `sections/part5-case-study.tex:180` vs `figures/openfoam-sweep.tex`; PDF p. 81 | Text: "Milan-X had the advantage between about 15 000 and 100 000 cells per core". The figure shows 1.22× at 307 815 cells per core (xhigh). | The wording is Lawenda's (p. 7: "the 15k to 100k cell per core range"), but their Fig. 4 shows Milan-X still ahead at xhigh. | Attribute the range to Lawenda *et al.* and add "and still 1.22× at about 308 000 (xhigh)". |
| G18 | Minor (arithmetic display) | `sections/part4-stacked-cache.tex:254`, `figures/stack-process.tex`; PDF pp. 67–68 | "0.854 × 0.922 = 78.8%". | The displayed factors multiply to 78.74%. The 78.8% comes from the unrounded yields (0.8542 × 0.9223 = 0.7878). | Write 78.7%, or show three decimals. |
| G19 | Minor (residual of F9) | `sections/part6-synthesis.tex:261` (RQ2); PDF p. 98 | "it connects them through the organic substrate because that reach lets eight CCDs surround one IOD" (no generation stated). | Part III (`:216`) now limits this to Rome and Matisse, as F9 asked. | "In Rome and Matisse it connects them…". |
| G20 | Minor (wording) | `sections/part5-case-study.tex:45`; PDF p. 74 | "…Photoshop (27%), which the reviewer describes as relying heavily on single-core performance, which points to the core and clock as much as to the cache \cite{walton…}". | The facts are right (F1 fixed). The double "which", with the citation at the end, makes TechSpot appear to draw the core-and-clock inference, which is the paper's own. | Split the sentence: "…single-core performance \cite{…}. This points, in our reading, to…". |

### Claims I could not fully verify

- **Reguly, `part6:167`:** "the same measurement at small array sizes shows the bandwidth of the on-chip caches". The
  text gives the ratios (verified), but I did not read Fig. 1's size sweep to confirm how the cache bandwidth was
  measured.
- **`fig:vendor-vs-independent`, Phoronix lower end:** "just under 20%" is consistent with the histogram (three 5800X
  wins in the 10–20% bin). I did not re-derive the largest 5800X margin.
- **EPYC 7763 256 MB L3 (`tab:per-core-resources`):** taken from the Phoronix 7773X page, as in the first review's
  verified `tab:config-pairs`. I did not re-read it.
- **F8 detail:** the first review read Lam's V-Cache CCD latency as 10.66 ns; the response and draft use 10.65 ns. The
  difference does not affect the "about three times" statement. I did not re-render the chart.

## 3. Regression check, F1–F23

| ID | Status | Note |
|---|---|---|
| F1 | Fixed | V-Ray 30% now named as the largest gain. The sentence is clumsy (G20). |
| F2 | Fixed | Table and new `fig:numa-latency` use NUMA1/2/3 for Naples, matching Fig. 2.2.6. |
| F3 | Not upheld, correctly | The embedded chart images (`pdfimages`) show 105.59/89.21 ns and 342.11/313.11 cycles. The values stand. |
| F4 | Fixed | Now 21 vs 12 cycles at 512 KB, with the 4 KB penalty left unstated (7-cpu). |
| F5 | Fixed | "consistent with … a major constraint", with Cozma's wording and voltage tolerance (`part4:214`). |
| F6 | Partly fixed | Part IV `:205` hedged. The Conclusions RQ3 (`part6:263`) still states it as fact (G10). |
| F7 | Fixed | The iso-clock 15% is cited to Swaminathan only, and the ISSCC figure is described as 5800X3D vs 5900X. |
| F8 | Fixed | "about three times" and "a thirteenth (53 against 702 GB/s)". OPIO 6.4 GT/s attributed to Haswell. |
| F9 | Partly fixed | Part III `:216` limited to Rome/Matisse. RQ2 in the Conclusions is still generic (G19). |
| F10 | Fixed | The causal "to make room for the TSVs" clauses are gone, and the new figure does not reintroduce them. |
| F11 | Fixed | Lambert pitch targets cited as slides 12–13. |
| F12 | Fixed | "roughly 250–300 cycles by 64–96 MB"; Milan-X "flat until beyond about 64 MB". |
| F13 | Fixed | "may explain" plus Cozma's clock-estimation caveat (`part4:192`). |
| F14 | Fixed | "which Lam suggests is likely due to" (`part4:280`). |
| F15 | Fixed | "probably Milan's higher base clock", with a pointer to the clock correction (`part5:169`). |
| F16 | Fixed | Base 2.55 vs 2.40 GHz and max boost 3.70 GHz for both added (`part4:212`, `tab:config-pairs`). |
| F17 | Fixed | Dong and Xie's threshold now described as "an analogous effect for 3D stacking" (`part3:229`). |
| F18 | Fixed | One merged 19% row citing both sources (`tab:amd-reported`). |
| F19 | Fixed | "10% or more"; histogram 5800X bins 150/91; bin convention given in the caption. |
| F20 | Fixed | Restricted to 1–2 cm². The 38.3% vs 34.4% gap at 5.92 cm² is now stated (App. C `:23`). |
| F21 | Fixed | Black's doubled power-density assumption added (`part6:181`). |
| F22 | Fixed | "64 cores per socket" (`part5:167`). |
| F23 | Unchanged (as agreed) | References still resolve to the parent subsection. Not an error. |

## 4. Arithmetic recomputed

### Cache–clock model (`eq:cache-clock-model`, `tab:cache-clock-model`, `fig:cache-clock-model`)

**Inputs (from the text):**
- A = 3.85 L3 accesses per thousand instructions; M = 1.48 misses per thousand instructions (Lam).
- IPC 1.36 → 1000/1.36 = 735.29 cycles per thousand instructions.
- Stall 130 cycles at 4.2 GHz → s = 30.952 ns.
- C = 735.29 − 1.48 × 130 = 542.89 cycles.
- Δt = 4 cycles.
- Clocks 4.8 / 5.15 GHz, a ratio of 1.07292.
- The equal-clock column is evaluated at 4.2 GHz.
- The linear rule is (1 + equal-clock gain)/1.0729 − 1.

| ΔM | Equal clocks (4.2 GHz) | 4.8 vs 5.15 GHz, memory time fixed | Linear rule | Draft |
|---|---|---|---|---|
| 0 | −2.05% | −6.72% | −8.71% | −2.1 / −6.7 / −8.7 ✓ |
| 0.2 | +1.46% | −3.02% | −5.43% | +1.5 / −3.0 / −5.4 ✓ |
| 0.4 | +5.24% | +0.99% | −1.91% | +5.2 / +1.0 / −1.9 ✓ |
| 0.6 | +9.31% | +5.35% | +1.88% | +9.3 / +5.3 / +1.9 ✓ |
| 1.0 | +18.46% | +15.29% | +10.41% | +18.5 / +15.3 / +10.4 ✓ |
| Break-even | 0.1185 | 0.3520 | 0.5029 | 0.12 / 0.35 / 0.50 ✓ |

- **Sensitivity to the calibration:**
  - With s = 31 ns exactly, every value changes by at most 0.03 points.
  - With the unrounded stall of 128.5 cycles (see below), the break-evens are 0.12 / 0.36 / 0.51 and the 0.4 row is
    +5.1 / +0.8 / −2.0. The conclusions are unchanged.
- **The equal-clock result depends on the clock (G6):**
  - at 4.8 GHz: +6.13% at ΔM = 0.4, break-even 0.104;
  - at 5.15 GHz: +6.62%.
- **Memory share of plain-die time:** 1.48 × 30.95 = 45.8 ns per thousand instructions. That is 26.2% of 175.1 ns at
  4.2 GHz and 30.3% of 151.2 ns at 5.15 GHz (G8).
- **Figure formulas:**
  - blue curve: 735.29/(558.29 + (1.48 − x) × 130), where 558.29 = 542.89 + 15.4;
  - red curve: (542.89/5.15 + 1.48 × 30.952)/(558.29/4.8 + (1.48 − x) × 30.952);
  - dashed curve: blue/1.0729.

  All three match the equation. The break-even markers are at 0.118 / 0.352 / 0.503 ✓.

### libx264 waterfall (`fig:libx264-waterfall`)

- 1000/1.43 = 699.3 cycles.
- Saving: 735.3 − 699.3 = 36.0 cycles.
- Added cycles: 3.85 × 4 = 15.4.
- Implied stall per removed miss: (36.0 + 15.4)/0.40 = 128.5 cycles, or 129.4 using ΔM = 0.397. The draft's "about
  130" ✓.
- Bars: 0.40 × 130 = 52; 735 − 52 + 15 = 698 against 699 ✓.

### Cache against clock (`tab:cache-vs-clock`, unchanged)

The earlier values (−2.0 / +2.5 / +2.6 / +6.1 / >+11%) still hold with the divisor 1.07.

### Per-core resources (`tab:per-core-resources`)

| Quantity | Calculation | Result |
|---|---|---|
| Zen 3 bandwidth | 8 × 3200 MT/s × 8 B | 204.8 GB/s |
| Zen 3 per core | 204.8/64 | 3.2 GB/s |
| Zen 4 bandwidth | 12 × 4800 MT/s × 8 B | 460.8 GB/s (datasheet value ✓) |
| Zen 4 per core | 460.8/96 | 4.8 GB/s |
| L3 per core, Milan / Milan-X | 256/64, 768/64 | 4 MB, 12 MB |
| L3 per core, Genoa / Genoa-X | 384/96, 1152/96 | 4 MB, 12 MB |
| Per-core bandwidth growth | 4.8/3.2 | +50% |
| Core-count growth | 96/64 | +50% |
| Total bandwidth growth | 460.8/204.8 | +125% |

All ✓.

### Reguly (`sec:bandwidth-wall`, `tab:llc-alternatives`, `fig:reguly-ratio`)

| Quantity | Calculation | Result |
|---|---|---|
| Milan-X STREAM efficiency | 310/409.6 | 75.7% (Reguly: "close to 75%") ✓ |
| Xeon Max vs Milan-X | 1446/310 | 4.66 (G14) |
| Xeon Max vs 8360Y | 1446/296 | 4.89 |

Ratios 14 / 6 (6.3) / 3.8 and tiling speed-ups 4 / 2.7 / 1.84 match sections 2 and 6 of the paper ✓. The Xeon
Max's 2–4.3× lead over the other two CPUs matches the paper's conclusion ✓. 7V73X with 60 cores per socket ✓.

### Part III figures

- **Bandwidth balance:** crossing at 204.8/55 = 3.72 CCDs ✓. Link totals 55 × n ✓.
- **NPS modes:** 204.8, 102.4 and 51.2 GB/s for 8, 4 and 2 channels ✓.
- **Two sockets:** 4 × 16 = 64 lanes; 128 − 64 = 64 per socket and 128 in total; 3 × 16 = 48; 128 − 48 = 80 per socket
  and 160 in total ✓.
- **L3 miss path:** 13 FCLK at 1.46 GHz = 8.9 ns, "< 9 ns" ✓. 94 ns (Rome, near 2 ch), 61.8 ns and 10.9 ns (5800X) ✓.
- **NUMA latency:** 90 / 141 / 234 and 94 / 104 / 201 ns; average 0.81× ✓.

### Cezanne (`tab:cezanne-vermeer`)

| Quantity | Calculation | Result |
|---|---|---|
| 5700G L3 latency in cycles | 12.6 ns × 4.0 GHz | 50.4 cycles ✓ |
| 5800X L3 latency in cycles | 10.9 ns × 4.85 GHz | 52.9 cycles ✓ |
| 5600G memory latency | 47 cycles/4.45 GHz + 74 ns = 10.6 + 74 | 84.6 ns ("about 85") ✓ |
| Boost-clock ratio | 4.7/4.6 | 1.022 ("about 2%") ✓ (see G2 for why this is the wrong comparison) |
| Link share of a memory access | 9/60 and 9/90 | 15% and 10% (G3) |

### Part V figures

- **OpenFOAM cells per core**, from Lawenda Table 3 over 128 cores:

  | Mesh | Calculation | Cells per core |
  |---|---|---|
  | mid | 1 897 187/128 | 14 822 |
  | high | 4 166 441/128 | 32 550 |
  | mhigh | 6 657 491/128 | 52 012 |
  | uhigh | 11 900 363/128 | 92 972 |
  | xhigh | 39 400 357/128 | 307 815 |

  All ✓. The plotted ratios 1.23 / 1.50 / 1.54 / 1.46 / 1.22 match the Fig. 4 labels ✓. The 0.81 minimum matches
  Table 6 (row Milan, column Milan X) ✓.
- **Zen 2 vs Zen 3 latency:** 68.8 − 61.8 = 7.0 ns; 10.9 − 9.9 = 1.0 ns ✓.
- **Clock correction:**
  - 0.89/0.898 = 0.99;
  - 1.076/0.9545 = 1.127;
  - 0.81/0.951 = 0.852;
  - 1.54/0.951 = 1.620 ✓.

### Part IV figures

- **Stack yield:** 0.854 × 0.922 = 0.7874. With unrounded yields, 0.8542 × 0.9223 = 0.7878 (G18).

## 5. Checked and found correct

### Part VI
- `tab:three-way` values.
- The Broadwell paragraph: 34.18 / 10.65 ns, 53 / 702 GB/s, about 3× and 1/13.
- The Xeon Max row of `tab:llc-alternatives`: 1446 vs 310 GB/s, 3.8× vs 14×, "communication latency unchanged". The
  last one matches Reguly's "hasn't been a significant improvement (in some cases even slight regression)".
- `sec:cache-clock-model`:
  - the equation and its definitions;
  - the calibration;
  - Lam's all-core L3-load clocks of 4.8 / 5.15 GHz (Lam p. 9);
  - the honest statement that the libx264-run clocks are an assumption;
  - Lam's "it'll probably come close" (p. 16).
- `tab:per-core-resources` and its sources.
- All Reguly numbers and system descriptions.
- `fig:reguly-ratio`: values, and the caption's note on 6× vs 6.3×.
- `fig:thread-placement`: its logic matches the model, and it is labelled as a proposal, not AMD's policy.
- `sec:limitations`: consistent with the body.
- The `sec:case-against` values: 94 vs 90 ns; average latency down about a fifth (0.81).
- Black's figures in `sec:future`.
- The open questions do not contradict the body.

### Part III
- `fig:l3-miss-path`, `fig:bandwidth-balance`, `fig:numa-latency`, `fig:nps-modes` and `fig:two-socket`: values,
  captions and sources. This includes Naffziger's "≥ 4 CCDs populated in most configurations".
- `tab:cezanne-vermeer`:
  - TechSpot: 4.6 GHz / 65 W vs 4.7 GHz / 105 W; PCIe 3.0 vs 4.0; Cinebench about 10%; 7-Zip 9%; games 11% average,
    4–20% by title; power about 15%; Cezanne is the mobile die.
  - CapFrameX: 76.1 ns, 12.6 ns, 1600 MHz, DDR4-3200 CL16 at 4 GHz, "very similar", the AIDA64 caveats and the
    die-shot explanation. The AIDA64 screenshot was read directly.
  - 7-cpu: 47 cycles; 40 + up to 20 cycles across slices; 47 cycles + 74 ns; PC4-24000 15-16-16-35.
  - The FPS Review: 61.8 ns and 10.9 ns at 4.85 GHz and FCLK 1800.
- The Cezanne section's own caveats (not a controlled experiment; different tools and settings) are accurate. Only
  its closing inferences overreach (G2, G3).

### Part IV
- `fig:libx264-waterfall`: values, plus a caption that honestly says the stall is inferred from the same measurement.
- `fig:stack-process` content: Si–OH termination, room-temperature hydrogen bonding, siloxane anneal with H₂O
  released, Cu dishing and diffusion (Alam slide 9); D2W vs WoW, with KGD for D2W (slide 10); thinning to about
  20 µm (Cozma); structural silicon and equal height (Wuu slides 12, 17).

### Part V
- `fig:openfoam-sweep`: values, cells per core, and the caption's notes on 1.22 vs 1.24 and on 0.81.
- `fig:zen2-zen3-latency`: all eight values read from the AIDA64 screenshots, plus the memory and FCLK settings.
- `fig:clock-correction`: matches `tab:clock-correction`.
- `fig:vendor-vs-independent`, all other bars: AMD 1.00–1.36 and 1.15 / 1.66; Lam 1.0 to >1.19; Cozma 1.05–1.076;
  Lawenda 0.81–1.54; Domke 0.89–3.4; Phoronix to "≥ 1.5".

### Consistency across parts
- **7% / 1.073 clock gap:** 7% is Lam's single-core average; 1.073 is his all-core L3-load ratio. They are used
  consistently and the difference is explained.
- **4.8 / 5.15 GHz:** same everywhere.
- **About 130 cycles per removed miss:** Part IV, Part VI and the waterfall figure.
- **3.2 / 4.8 GB/s per core:** Part III and Part VI.
- **4-cycle latency:** throughout; Milan-X 3–4.
- **Other repeated values:** 47.49 / 51.14 cycles; 342 / 313 cycles; 204.8 GB/s; 74 / 81 / 41 mm².

### Rules and build
- **Citations:** all 36 keys in `references.bib`, each with a local PDF listed as present. Newly cited:
  `regulyComparative…`, `waltonAMDRyzen72021` and `devtechprofileWhom…`; all three files exist in `research/pdfs/`.
- **Group attribution:** no work is attributed to an individual group member in the sections.
- **Build:**
  - the latest build log (`tmp/linux-build/main-initial-draft-2.log`, 1 Nov 02:46) has no undefined, multiply-defined
    or overfull warnings (22 underfull boxes only);
  - the PDF has no "??".
- **Rendered pages:** I rendered PDF pp. 43, 45–48, 51, 63, 68, 75, 79, 81, 85, 91, 92, 94 and 98. No label overlaps
  a mark or another label. The 68.8 / 61.8 bar labels on p. 75 touch but remain legible. The bracket lines in
  `fig:stack-process` run along the left box edges (G16).
