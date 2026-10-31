# Independent review: `initial-draft-2` (ELL305 term paper)

Reviewed 31 Oct 2026 against the project-local PDFs in `research/pdfs/` and `sources/archbook.pdf` only.
Compiled draft checked: `build/pdf/ELL305-initial-draft-2.pdf` (91 pages, built 31 Oct 2026 22:00, newer than
every section file). "PDF p." below means the physical page in that file. File line numbers refer to the
`.tex` files under `initial-draft-2/`. No project file other than this one was changed.

## 1. Overall assessment

The draft is unusually accurate. Nearly every cited number checked out against the local source, often to the
decimal. That includes values that exist only in images, which I read by rendering the pages: Lam's hit-rate
and IPC charts, the ISSCC 2022 slides and endnotes, Naffziger's figures, Suggs's slides, the AIDA64 screenshots,
Lawenda Table 6, Domke Fig. 1 and the EPYC 9004 datasheet. Every worked example recomputes correctly (section 4).
For the Phoronix comparison I re-derived all 350 results, not a sample: 106 vs 244, 12 V-Cache wins of 50% or
more, medians of about 11% and 4%, and three 5800X wins of 10% or more. All 291 bars whose colour could be
sampled had a colour that matched their side of the chart axis. The real problems are few and mostly local:

- one misdescribed TechSpot result;
- a mislabelled NUMA table;
- one 7-cpu figure taken from the wrong page-size table;
- one wrong slide citation;
- Chips and Cheese memory-latency values (342/313 cycles, 106/89 ns) that the local PDF copy cannot show,
  because its charts are clipped at the right edge;
- a cluster of thermal-causation sentences in Part IV that state as fact more than the sources establish, and
  that conflict with the paper's own open question in Part VI.

Every citation key exists in `references/references.bib` and has a local PDF listed in `research/pdfs/README.md`.
Every `\cref`/`\ref` target is defined, and the PDF contains no "??".

## 2. Findings (most severe first)

| ID | Severity | Location | What the draft says | What the source says | Suggested correction |
|---|---|---|---|---|---|
| F1 | Error | `sections/part5-case-study.tex:45`; PDF p. 66 | "The largest gains appear in applications the reviewer describes as relying heavily on single-core performance, such as Photoshop and After Effects." | TechSpot (`TechSpot-Ryzen-7-5800X-Review-2020.pdf`): V-Ray "30% faster", Photoshop 27%, Corona "26% performance uplift", 7-Zip 24%, After Effects 23%, Cinebench 22%. The largest gain is V-Ray, a multi-threaded renderer. After Effects is only fifth. | Say that Photoshop (27%) is among the largest gains and After Effects (23%) is mid-range, and that the largest gain (V-Ray, 30%) is a multi-threaded render. Or drop the "largest gains" argument. |
| F2 | Error | `sections/part3-chiplets.tex:131–133` (Table `tab:numa-latency`); PDF p. 42 | Naples rows labelled "NUMA0 (local) 90", "NUMA1 141", "NUMA2 234". | Naffziger Fig. 2.2.6 (`AMD-Chiplet-Architecture-ISSCC-2020.pdf`, p. 2) labels the Naples rows "NUMA1 90, NUMA2 141, NUMA3 234, Avg. Local 128". The Rome rows (Near 2ch 94, NUMA1 104, NUMA2 201, 0.81×) match. | Relabel the Naples rows NUMA1/NUMA2/NUMA3 as in the figure, or use descriptive labels and say they are the paper's own. |
| F3 | Unsupported | `sections/part5-case-study.tex:152`; caption and data of `figures/milanx-latency.tex`; PDF p. 70 | Memory latency "342 cycles for Milan and 313 for Milan-X"; "89 against 106 ns"; the figure plots end points of 342 and 313. | `ChipsAndCheese-VCache-Latency-2022.pdf`, pp. 1–2: both charts are cut off at the right edge, around the 512 MB point. The readable labels are 1.23/1.14 ns, 3.72/3.43 ns, 14.57 ns, 4.00, 12.03, 47.49 and 51.14 cycles. No memory-latency label is visible. At the clipped edge the curves sit near 256–300 cycles and about 80–100 ns. | Re-save the article with the full chart width and confirm the values, or remove the 342/313 and 106/89 figures. The 313-cycle break-even at line 156 and the 313–342 range in §15.1 depend on them. |
| F4 | Unsupported | `sections/part5-case-study.tex:154`; PDF p. 70 | With 4 KB pages, latency rises at 512 KB because the 64-entry L1 DTLB overflows, "adding 7 cycles even though the data is still in L2". | `7cpu-Zen3-Cezanne-latency.pdf`: the 7-cycle L1-TLB miss penalty is given for **2 MB pages**. For 4 KB pages the source says "Miss penalty = ? cycles", and the 4 KB table shows latency at 256 K → 512 K going 11 → 21 cycles. The 4 KB DTLB line reads "64 items (about 800 KB of memory)". | Say that with 4 KB pages, latency at 512 KB was 21 cycles against 12 with 2 MB pages, which the source attributes to L1-TLB misses. Don't quote 7 cycles for 4 KB pages. |
| F5 | Overstated | `sections/part4-stacked-cache.tex:211`; PDF p. 60 | "The redesign is itself the strongest evidence that heat removal, not cache capacity or latency, was the binding constraint of the first design." | Cozma (`ChipsAndCheese-9800X3D-2024.pdf`, conclusion) calls the support silicon's thermal resistance "the biggest weakness of the first generation", and attributes the first generation's limit to reduced "voltage tolerance". Lam (`ChipsAndCheese-7950X3D-2023.pdf`, p. 4): "AMD's stacked cache is less tolerant of high voltage". The paper's own open question (`part6-synthesis.tex:147`) asks how much of the clock penalty was thermal and how much electrical. | Weaken to "is consistent with heat removal being a major constraint". Cite Cozma's wording and mention the voltage-tolerance explanation. |
| F6 | Overstated | `sections/part4-stacked-cache.tex:202`; PDF p. 59 | "The measured clock and voltage limits of the first-generation parts … show that AMD chose the second [lowering voltage and frequency to compensate for a higher thermal resistance]." | The sources report the limits (7800X3D max 1.2 V; 7950X3D V-Cache CCD 4.8 vs 5.15 GHz). Lam attributes them to voltage tolerance, not to a thermal choice. No local source says AMD lowered V/f *because of* temperature. | Present it as an interpretation: "are consistent with the second choice". |
| F7 | Overstated | `sections/part4-stacked-cache.tex:262`; PDF p. 62 | "AMD reports a 15% average gaming performance uplift from V-Cache \cite{wuu2022vcache}." | ISSCC 2022 slide 29: "~15% faster gaming at 1080p high", 8-core 5800X3D vs **12-core** 5900X (endnote R5K-106, slide 35). That is not an iso-core or iso-clock "uplift from V-Cache". The iso-clock 15% is Swaminathan slide 19 (prototype vs 5900X at 4.0 GHz). | Attribute the 15% iso-clock figure to Swaminathan only. Describe the ISSCC figure as the 5800X3D-vs-5900X comparison, which §19 does correctly. |
| F8 | Overstated | `sections/part6-synthesis.tex:58`; PDF p. 76 | Broadwell's side-by-side eDRAM "was slower in both latency and bandwidth by an order of magnitude". | Lam's chart (`ChipsAndCheese-7950X3D-2023.pdf`, p. 18): eDRAM 34.18 ns against 10.66 ns for the 7950X3D cache-CCD L3, about 3.2×. Bandwidth 53.10 against 701.87 GB/s, about 13×. | "about three times slower in latency and more than ten times lower in bandwidth". |
| F9 | Unsupported | `sections/part3-chiplets.tex:198`; PDF p. 44 | Zen CPUs "from Rome and Matisse to the Ryzen 9000X3D series" connect CCDs to the IOD through the organic substrate. | Naffziger supports this for Rome/Matisse (EPYC 7002, Ryzen 3000). No local source states the CCD–IOD connection method for Ryzen 9000X3D. Lambert slide 6 only names the IOD and CCD. | Limit the claim to the generations a source covers, or add a source. |
| F10 | Unsupported (minor) | `sections/part4-stacked-cache.tex:209` ("To make room for the TSVs, the CCD is thinned") and `:219` ("thinned so that its TSVs pass through it"); PDF pp. 59, 61 | A causal reason for thinning. | Cozma says only that the CCD was "thinned to about 20 microns". Wuu slide 12 gives "Structural support for thinned CCD". Neither states the reason. | Drop the causal clause or cite a source that states it. |
| F11 | Minor (citation) | `sections/part6-synthesis.tex:112`; PDF p. 80 | 3D pitch below 9 µm and 2.5D below 40 µm, cited to Lambert "slides 11–12". | `AMD-IMAPS-2025-Heterogeneous-Integration-Lambert.pdf`: the pitch targets are on **slide 13** ("Interconnect Scaling Focus"). Slide 12 has UCIe, co-packaged optics and module size. Slide 11 is a section title. | Cite slides 12–13. |
| F12 | Overstated (minor) | `sections/part5-case-study.tex:152`; PDF p. 70 | Between 32 and 96 MB "a load costs about 51 cycles on Milan-X and several hundred on Milan, a difference of five to six times"; Milan-X "stays in its L3 until about 96 MB". | Cycle chart (`ChipsAndCheese-VCache-Latency-2022.pdf`, p. 2): Milan rises from about 50 cycles at 32 MB to about 256 at 64 MB, so "several hundred" and 5–6× hold only near the top of the range. The Milan-X curve starts rising just above 64 MB and passes 128 cycles by 128 MB. | "rising to roughly 250–300 cycles on Milan by 64–96 MB". Say Milan-X's curve starts to rise beyond about 64 MB. |
| F13 | Overstated (minor) | `sections/part4-stacked-cache.tex:189`; PDF p. 58 | The single-thread result was smaller than the headline "because" one thread uses one core's interface. | Cozma (`ChipsAndCheese-Zen3-VCache-Deep-Dive-2022.pdf`): "we are seeing about 25% Bytes per Cycle increase. But, the clock speed was estimated". The article doesn't link the gap to the per-core interface. | Present it as the paper's explanation, and mention the clock-estimation caveat. |
| F14 | Overstated (minor) | `sections/part4-stacked-cache.tex:274` (and the same idea at `:171`); PDF p. 63 | DCS "lost a little IPC, which Lam attributes to the added latency". | Lam p. 15: "DCS actually ends up losing a bit of IPC, likely due to increased L3 latency." | "which Lam suggests is likely due to the added latency". |
| F15 | Overstated (minor) | `sections/part5-case-study.tex:164`; PDF p. 71 | At n = 100–110, "Both systems hold the data in L3, and Milan's higher base clock decides." | Domke Fig. 1 shows a speedup of about 0.89–0.90 but gives no explanation. The draft's own clock correction (line 256) hedges this properly. | "probably because of Milan's higher base clock (see the clock correction below)". |
| F16 | Overstated (minor) | `sections/part4-stacked-cache.tex:209`, `part5-case-study.tex:88`; PDF pp. 60, 69 | 9684X vs 9654 shown as a clock cost (all-core 3.42 vs 3.55 GHz, 400 vs 360 W). | `AMD-EPYC-9004-Datasheet.pdf`, p. 2: values correct, but the 9684X has a **higher** base clock (2.55 vs 2.40 GHz) and the same 3.70 GHz max boost. | Add the base and max boost clocks so the comparison isn't one-sided. |
| F17 | Overstated (minor) | `sections/part3-chiplets.tex:211`; PDF p. 46 | Interface, packaging, assembly and test costs, "which Dong and Xie show can outweigh the yield gain for small designs, making splitting worthwhile only above a size threshold". | Dong & Xie's threshold ("enabling point", Table II; Fig. 8) is for **3D stacking** with TSV and bonding costs, not for 2D chiplet partitioning. Appendix C states this correctly. | "Dong and Xie find an analogous size threshold for 3D stacking". |
| F18 | Inconsistent (minor) | `sections/part5-case-study.tex:120` and `:123` (Table `tab:amd-reported`); PDF p. 69 | Two rows, "19% average IPC gain, Zen 3 vs Zen 2" (Wuu slides 10, 35) and "19% IPC improvement from Zen 2 to Zen 3" (AMD PR). | Both come from the same AMD test, endnote R5K-003 (ISSCC slide 35; PR note 4: 25 workloads, locked 4 GHz, 3800XT vs 5800X, DDR4-3600). | Merge into one row citing both sources, so one vendor claim isn't counted as two pieces of evidence. |
| F19 | Inconsistent (minor) | `sections/part5-case-study.tex:181`; `figures/phoronix-hist.tex`; PDF pp. 72–73 | "58 of its wins exceeded 10%"; histogram bins for the 5800X are 149 (2–5%) and 92 (5–10%). | Re-derived from all 350 labels: 57 V-Cache wins are strictly above 10% and 58 are at or above 10% (one is exactly 10.0%). For the 5800X, 150 fall in [2, 5)% and 91 in [5, 10)%. The difference is one result on the 5.0% boundary. All other counts match. | Write "58 were 10% or more" and state the bin-edge convention in the caption. |
| F20 | Inconsistent (minor) | `appendices/appendix-c-yield-cost-model.tex:23`; PDF p. 89 | Using the rectangular rather than the triangular model "changes the result by less than one percentage point" at the worked-example yields. | Recomputed: true for 1 and 2 cm² (82.4 vs 82.1%, 68.8 vs 67.9%). For the 592 mm² die used in Parts I and III, the models give 38.3% vs 34.4%, a 3.9-point gap. | Restrict the statement to the 1–2 cm² example, or note the larger gap for 5.92 cm². |
| F21 | Minor | `sections/part6-synthesis.tex:114`; PDF p. 81 | Peak temperature up "14 °C, or 26 °C if the power savings were ignored". | Black et al.: 26 °C applies "if there were no power savings from the 3D floorplan **and the stacking were to result in a 2x power density**". | Add the 2× power-density assumption. |
| F22 | Minor | `sections/part5-case-study.tex:162`; PDF p. 71 | "dual-socket Milan and Milan-X systems with the same 64 cores". | Domke Table 1: 2 sockets with 64 cores per socket (128 cores per system). | "64 cores per socket". |
| F23 | Minor (cross-reference) | `sections/part2-foundations.tex` (labels `sec:amat-example`, `sec:address-example`); `sections/part3-chiplets.tex:149` (`sec:bandwidth-example`); PDF p. 36 (Part II, line 341: "examined in section 8.2") | References to worked examples. | These labels follow `\subsubsection*`, so they resolve to the enclosing numbered subsection (e.g. "section 8.2 Scalability"). The target page is right, but the reference names the parent section, not the worked example. | Acceptable as is. Use `\nameref` or a numbered heading if the worked example should be named. |

## 3. Claims I could not fully verify

- **Chips and Cheese latency teaser, memory-latency end points** (342/313 cycles, 106/89 ns): the charts in the
  local PDF are clipped at the right edge (see F3).
- **Lam, libx264 MPKI attribution**: the PDF's text is clipped at the right margin. The sentence reads "1.48 L3 MPKI
  with the n… / VCache CCD", which is very probably "non-VCache CCD", matching the draft. The chart values
  (61.55%, 71.86%, IPC 1.36 and 1.43) were verified visually.
- **Lam, eDRAM link speed** ("64-bit full-duplex at 6.4 GT/s"): the sentence ends "(on Haswe…" and is clipped.
  The draft attributes this link to Broadwell, which the local copy can't confirm.
- **AMD 9800X3D press release quote** ("relocated below the processor … closer to the cooling solution"): a cookie
  overlay garbles the text layer. "The 64MB cache memory has" and "CCD … closer to the cooling" are legible; I
  didn't render the page to read the full sentence.
- **TechSpot memory configuration** ("DDR4-3200 CL14", part5 line 45): not in the text layer. It may be in a
  test-system image that I didn't render. The percentages, 4.55 GHz and "~20 more watts" were verified.
- **Chips and Cheese 9800X3D "same four cycles"**: the sentence is clipped ("adds the sam… cycles"), but the same
  article's "not having the 4 cycle penalty" confirms the value.
- **Suggs, L1 bandwidth**: the draft follows slide 12 ("2X L1D cache load/store bandwidth"), but slide 3 of the same
  deck says "3x L1 load+store bandwidth". The source contradicts itself; the draft's citation is correct.
- **Lam's conclusion** says V-Cache "provided an IPC gain in every one" of the tested scenarios, which contradicts
  his DCS section. The draft correctly follows the DCS section.
- **Figure schematics** (`vcache-generations`, `vcache-stack`, `epyc-package`, `vcache-floorplan`, `bond-interface`)
  are labelled schematic. I checked only their labelled values (64 MB, 32 MB, 81/41 mm², BPM/BPV/M13), which match.

## 4. Worked examples recomputed

| Worked example | Location | Result |
|---|---|---|
| CPI with stalls (Ex. 140), 1 + 0.1·1 + 0.2·2 = 1.5 | part2 | confirmed (textbook Ex. 140, sec. 10.9.3) |
| Optimal pipeline depth (Ex. 142), √(20/0.12) = 12.9 ≈ 13 | part2 | confirmed |
| CPI with a 100-cycle memory, 1 + (1/3)·99 = 34 | part2 | confirmed |
| AMAT (Ex. 147), 1 + 0.1(10 + 0.1·100) = 3 | part2 | confirmed (sec. 11.1.7) |
| AMAT on 3700X/5800X: 1.60/0.56, 1.46/0.53, 1.38/0.45 ns; 4 cycles at 4.85 GHz = 0.82 ns; about 5% AMAT reduction | part2, Table `tab:amat-example` | confirmed (1.596, 1.459, 1.379; 0.561, 0.534, 0.454; drop 5.5%) |
| Address split: L1 64 sets 6/6/36; L2 1024 sets 6/10/32; L3 32768 sets 6/15/27 | part2, Table `tab:address-split` | confirmed |
| Amdahl, f = 5%: 5.9 / 9.1 / 15.4, limit 20 | part2 | confirmed (5.93, 9.14, 15.42) |
| Directory overhead 8/512 = 1.6%, 64/512 = 12.5%, 128/512 = 25% | part2 | confirmed |
| Topology table, N = 8 and 64 (ring 4/2, 32/2; mesh 14/8; torus 8/16; hypercube 3/4, 6/32) | part2, Table `tab:topology-example` | confirmed against sec. 12.6.3 formulas |
| Zen 2 efficiency product 1.15 × 1.17 × 1.47 = 1.98 | part3 | confirmed |
| Rome silicon 8 × 74 + 416 = 1008 mm²; 59% / 41% | part3 | confirmed (58.7% / 41.3%) |
| Murphy yield, D₀ = 0.2: 82.4% (1 cm²), 68.8% (2 cm²) | part3 Table `tab:yield-example`, App. C | confirmed |
| Yields 87% (74 mm²) and 38% (592 mm²); silicon ratio 44% at D₀ = 0.2, 63% at 0.1 | part3 §10, Part I table | confirmed (86.6%, 38.3%; 0.442; 0.631) |
| Dies per wafer: 955.2 − 77.5 ≈ 878; 119.4 − 27.4 ≈ 92; good dies 760 and 35; 95 vs 35 sets; factors 2.7 / 1.9 / 3.5; edge loss 8% / 23% | part3, Table `tab:dies-per-wafer` | confirmed (2.70, 1.89, 3.52; 8.1%, 22.9%) |
| NPS bandwidth 8 × 25.6 = 204.8, 102.4, 51.2 GB/s; 204.8/64 = 3.2 GB/s; Matisse 51.2/16 = 3.2 | part3 | confirmed |
| Link balance 2/4/8 CCDs × 55 = 110/220/440 GB/s; 6.9 / 6.4 / 3.2 GB/s per core; 55/204.8 ≈ a quarter | part3, Table `tab:bandwidth-balance` | confirmed |
| Link power 55 GB/s × 8 × 2 pJ/bit ≈ 0.9 W | part3 | confirmed (0.88 W). The source's 2 pJ/b is at 6.4 Gb/s per lane, excluding regulation; the draft labels it illustrative. |
| xGMI lanes 128 − 64 = 64 per socket (128 total); 128 − 48 = 80 (160 total) | part3 | confirmed against the EPYC 7003 overview |
| L3 slice average (0+6+1+10+6+13+10+20)/8 ≈ 8; 40 + 8 = 48 vs measured 47 | part4 | confirmed (8.25) |
| Pad density (1000/p)²: 772, 12 346, 44 per mm²; ratios 16× and about 280× | part4 §14.3 | confirmed (771.6, 12 345.7, 44.4; 16.0, 278) |
| Interface budget 8 × 256 × 2 = 4096 wires; >5 mm² at 36 µm; >90 mm² at 150 µm | part4 | confirmed (5.3 mm², 92.2 mm²) |
| libx264 trade-off: 3.85 accesses/kI; 1.08 still missing; 0.40 removed; 40–120 saved; 15 added; net 25–105; 3–14%; 735 vs 699 cycles (4.9%); about 130 cycles per removed miss | part4 §15.1 | confirmed (3.849, 1.083, 0.397; 24.6–104; 3.4–14.3%; 4.90%; 127.5). 71.86/61.55 = 1.1675, which matches Lam's 16.75%. |
| Break-even 4/300 ≈ 1.3, 4/100 = 4 points; with measured values 3.65/313 ≈ 1.2 | part4, part5 | arithmetic confirmed; 313 itself is unverified (F3) |
| DCS: 0.07 kI⁻¹ removed → 7–21 cycles | part4 | confirmed |
| Tag overhead 1088 × 6 KB = 6528 KB ≈ 10%; 1 048 576 lines; ≈ 51 bits per line; 2¹⁶ sets; 26-bit tag; ≈ 25 bits left | part4 | confirmed (9.96%; 51.0 bits) |
| 96 MB 16-way: 98 304 = 3 × 2¹⁵ sets | part4 | confirmed |
| 2 TB/s check, 8 × 32 B × 2 × 4 GHz | part4 | confirmed (2.05 TB/s) |
| Thermal illustration 60 K × 1.1 = 66 K | part4 | confirmed |
| Stacked vs planar silicon: 122 mm² at 79.1% → 154 mm²; 94.8 + 44.5 = 139 mm²; 78.8% → 155 mm²; savings about 10% / 5% / 14% | part4, Table `tab:stack-yield` | confirmed (154.2; 139.3; 154.9; 9.7%, 5.1%, 13.7%) |
| AIDA64 cycles 9.9 ns × 4.40 GHz ≈ 44; 10.9 × 4.85 ≈ 53 | part5 | confirmed (43.6, 52.9) |
| 7-cpu memory 47 + 74 ns × 4.45 GHz ≈ 375 cycles | part5 | confirmed (376) |
| MiniFE bytes per point 512 MiB/(1.73–2.20 M) = 245–310; 1536 MiB/(4.91–5.83 M) = 275–330 | part5 §15.2 | confirmed (244–311; 276–328). Milan-X's FoM already falls between n = 160 and 170 (about 255 → 212), not only between 170 and 180, so the bracket is approximate. |
| Clock correction: 2.9/3.05 = 0.95 → 1.62 and 0.85; 3.15/3.3 → 1.13; 2.20/2.45 = 0.90 → 0.99 | part5, Table `tab:clock-correction` | confirmed (0.951; 1.620, 0.852; 1.127; 0.991) |
| Cache vs clock: (1 + g)/1.07 − 1 → −2.0, +2.5, +2.6, +6.1, >+11% | part6, Table `tab:cache-vs-clock` | confirmed (−1.96, 2.52, 2.62, 6.07, 11.2) |
| Black: 14 °C vs 4.5 °C ≈ 3× | part6 | confirmed (3.1×) |
| App. C: triangular 0.821 / 0.679, Poisson 0.819 / 0.670; doubling factor 2 × 0.824/0.688 ≈ 2.40; chiplet split (4.2/0.817)/(4/0.499) ≈ 0.64 | appendix C | confirmed (0.8215, 0.6793, 0.8187, 0.6703; 2.395; 0.641). See F20 on the "<1 point" remark. |
| Values read by eye from charts: Naffziger cost chart (1.00/0.90/0.77/0.72/0.67; 1.88/1.65/1.39/1.19), Domke Fig. 1 bars, Lam bars | `figures/chiplet-cost-chart.tex`, `minife-sweep.tex`, `lam-ipc.tex` | confirmed to within ±0.05 by re-reading the rendered source charts |

### Repeated values checked for consistency across parts

| Value | Places | Result |
|---|---|---|
| 38% / 87% yields | Part I Table `tab:thought-experiment`; part3 §10 text; Table `tab:dies-per-wafer` (38.3 / 86.6) | consistent |
| 95 vs 35 sets per wafer | Part I table; part3 Table `tab:dies-per-wafer` and text; part6 Table `tab:three-way` | consistent |
| +4 cycles | part2 (AMAT row, Table 11.2 discussion); part4 §15, summary; part5 Tables `tab:zen-progression`, `tab:later-x3d`, `tab:independent`; part6 | consistent (Milan-X correctly given as 3–4) |
| 47.5 / 51.1 cycles (47.49 / 51.14) | part5 §15.1, `figures/milanx-latency.tex`; part6 Table `tab:three-way` | consistent and verified |
| 313 / 342 cycles | part5 §15.1 (twice), the figure | consistent but unverified (F3) |
| 7% clock gap | part4 §17, §19; part5 Table `tab:config-pairs`; part6 table, §21, Table `tab:cache-vs-clock` | consistent |
| 204.8 GB/s, 3.2 GB/s per core | part3 Table `tab:nps-modes`, NPS worked example, bandwidth text, Table `tab:bandwidth-balance` (rounded to 205) | consistent |
| 74 / 81 / 41 / 416 mm² | Part I; part3; part4 (stack, D2W, yield table); part5 Table `tab:zen-progression`; part6; figures | consistent and verified |
