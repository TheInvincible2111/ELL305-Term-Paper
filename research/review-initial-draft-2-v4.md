# Fourth review of initial-draft-2 (8 November 2026)

Reviewer brief: `research/review-prompt-initial-draft-2-v4.md`. Only local files were used; nothing on the web.
Page references are **PDF viewer pages** of `build/pdf/ELL305-initial-draft-2.pdf` (155 pp; the printed page number is one lower).
Line references are to `initial-draft-2/` unless a full path is given.

**Build currency.** The PDF was built on 5 Nov 2026 at 23:35 (`pdfinfo`). No file under `initial-draft-2/` or `paper/` is newer, so the PDF matches the sources. Build log (`tmp/linux-build/main-initial-draft-2.log`, same time): no errors, no undefined references or citations, **0 overfull boxes**, 28 underfull boxes.

---

## 1. Overall assessment

As an undergraduate term paper this is strong work. It is argued carefully, nearly every number traces to a local source, and it is unusually honest about vendor claims and confounding factors. As it stands I would place it in the A−/B+ band. The paper Parts I–IV and most of Part V would support an A. The marks are lost mainly in the new simulation section, which contains real errors that an examiner who runs the code would find:
- three captions describe a metric that ignores the overlap factor;
- the input access mix is not the one stated;
- one "upper bound" argument runs the wrong way at the 32 MB edge;
- the chiplet-cost result (S4) is built into the model rather than found by it;
- the S5 numbers are misread from the CSV.

The second weakness is that the paper's most original quantitative idea, cycles saved per removed miss (50/80/130) and the overlap explanation, rests on L3 counters that Lam says include speculative and prefetch accesses. The paper never discloses this, and a check on DCS shows its equal-access-count assumption is off by about 15%.

**The two changes that would improve the paper most:**
1. Correct and reframe the simulation study as an *illustration* of the paper's mechanisms, not a confirmation of them: findings I1–I5 and I10–I17. Fix the captions and numbers, add S3 to the sensitivity analysis, charge the die-to-die hop on memory accesses in S4, and cut the section to about five pages, with the rest moved to Appendix E.
2. Re-ground the per-miss argument. Disclose Lam's speculative and prefetch counting, report the DCS inconsistency, and present 50–130 cycles as *apparent* savings with two candidate explanations (overlap and prefetch). Also stop stating inferred CCD configurations as facts (I6, I7).

---

## 2. Findings (most severe first)

| ID | Severity | Location | What the draft says | What the source / CSV / code / rule says | Suggested correction |
|---|---|---|---|---|---|
| I1 | Error | `sections/part5-case-study.tex:451, 455, 476, 482`; captions of `figures/sim-designs.tex:21`, `sim-table-planar.tex:3`, `sim-table-split.tex:3`, `sim-zen2-zen3.tex:29`; PDF pp. 119–124 | S2, S4 and S5 report "average access time" and the captions say "overlap 0.42". S2: the stacked design is "8.5%" slower than 32 MB when the data fits (14.5/11.6 vs 12.5/11.6). | `amat_ns` is `lat_cycles / accesses / f` (`tools/cachesim/src/cachesim.cpp:551`). It uses the **raw** latency; the overlap factor enters only `coreCycles` (`:367`). Reviewer's run (ws 24 MB): `amat_ns` = 11.5655 at both overlap 1 and 0.42, while `time_ns` falls from 11.82 to 6.85 ms. So the S2/S4/S5 numbers are overlap-free. The same comparison gives 5.6% in S1 and in the sensitivity table (`time_us`) and 8.5% in S2. | Either switch S2/S4/S5 to `time_us`, or say "raw average latency (no overlap applied)" in the text and the four captions. Reconcile 8.5% with 5.6%. |
| I2 | Error (result built into the model) | `part5:476` ("the cost of the split falls only on data shared across the boundary"), `:500`, `:513`; PDF pp. 122–126 | S4 "confirms" that the chiplet split costs time only for data shared across dies. | In the model a DRAM access costs `l3_lat + memC` in both the `twoccd` and `mono16` presets (`cachesim.cpp:328`). No CCD–IOD hop is charged on a memory access, which contradicts Part III's "every L3 miss pays a die-to-die round trip" (`part1:176`, `part3:124`). The "private" case uses 3 MB per thread (`sims.py` S4), which fits in L3, so it never reaches memory. The result is therefore an assumption, not a finding. | Charge the hop on every DRAM access in the two-die preset (or state that it is omitted). Rerun the private case with a working set larger than the L3. Remove S4 from the "confirmed" list. |
| I3 | Error (logic) | `part5:429` and `:506`; PDF pp. 117, 125 | "The model is therefore optimistic near the capacity edge, and its gains for working sets just below 32 or 96 MB should be read as upper bounds." | Near the 32 MB edge it is the *32 MB* model that is optimistic: at 64 MB the model gives 195 cycles against Milan's measured ~240 (`s0_latency_sweep.csv`; `make_figures.py:23`). There the real 96-vs-32 MB gain is *larger* than the model's (≈240/51 vs 195/51). Only just below 96 MB, where the 96 MB model is optimistic (51 vs ~65), is the model's gain an overestimate. | "…optimistic near each capacity edge. It therefore overstates the gain for working sets just below 96 MB and understates it for working sets just above 32 MB." Drop the general "upper bounds" in `:506`. |
| I4 | Error (numbers) | `part5:482`; PDF p. 123 | "Between 16 and 32 MB the unified L3 wins by up to three times (11.6 against 34.3 ns at 24 MB)"; "costs a few per cent for everything else". | `s5_zen2_zen3.csv`, 1t: 32 MB → 46.70 vs 11.61 ns = **4.0×** (4.2× against the 47-cycle split). At 4–16 MB, 8.9–9.5 vs 10.6–11.5 ns means the unified L3 is about **19% slower** (raw). That is not "a few per cent" for a workload that always reaches L3. | "…by up to four times (46.7 against 11.6 ns at 32 MB)". "…costs 7–8 cycles (about 19% of raw L3 access time) everywhere else; for a real program the cost scales with how often it reaches the L3." |
| I5 | Error (model input) | `part5:461`; `appendices/appendix-e-simulation.tex:43`; caption `figures/sim-cache-clock.tex:21`; PDF pp. 120–121, 153 | The S3 mix sends 1.155% of accesses to the cold region: "3.85 L3 accesses per thousand instructions". | `cachesim.cpp:413` rounds `hot_prob` to 0.1% (`jsround(hot_prob*1000)`), so 0.98845 becomes 0.988. Reviewer's run: 12.3 L3 lookups per 1000 accesses, i.e. **≈4.1 per 1000 instructions**. Effect: the 7.3% break-even moves only from 0.295 to 0.287 at hot_prob 0.989 (3.75/kinstr). | Increase the resolution of `hot_prob` (per million) and rerun, or state 4.1. |
| I6 | Unsupported (undisclosed measurement caveat) | `part4:163–176` (130 cycles), `part5:224–248` (`tab:lam-per-miss`), `part2:323–324`, `part5:433` (overlap calibration), Findings `part1:179`; PDF pp. 30, 46, 85–86, 106–108, 118 | Each removed L3 miss saved 50–130 cycles "because out-of-order cores overlap their misses". | Lam (`ChipsAndCheese-7950X3D-2023.pdf` p. 10): hit rate is counted "from the L3 cache's perspective… counting speculative L3 accesses, and not distinguishing between prefetch and demand requests". Removed prefetch misses need not save any stall, so the per-miss values are *apparent* savings, with prefetching as a second explanation. The method also assumes the same L3 accesses per kinstr on both CCDs. DCS is the only workload where both MPKIs are stated, and there 0.35/0.109 = 3.2 (plain) against 0.28/0.076 = 3.7 (V-Cache), a 15% difference. The method would predict 0.24 MPKI with V-Cache, not 0.28. | State the counter caveat in `sec:tradeoff-example` and `sec:lam-detail`, and report the DCS check. Call the values "apparent cycles saved per counted miss" and give MLP and prefetch as candidate explanations. Soften Findings bullet 4 and the RQ text accordingly. |
| I7 | Unsupported (inference stated as fact) | `tab:product-matrix` (`part3:325–351`) and `part3:355`; PDF pp. 70–71 | CCDs inferred from "32 MB of L3 per CCD": EPYC 9124 = 2 × 8. Then, as fact: "The 9124 puts them on two fully used CCDs… eight links… rather than four". | The same datasheet disproves the rule: the EPYC 9224 has **24 cores and 64 MB** (`AMD-EPYC-9004-Datasheet.pdf`, p. 2), which by the rule is 2 CCDs holding at most 16 cores. L3 can be partly disabled per CCD, so L3/32 does not identify the CCD count. AMD's white paper states the 9174F's configuration (8 × 2) but not the 9124's (`AMD-4th-Gen…`, p. 5). The other rows are arithmetically right *under* the rule. | Add the 9224 counter-example to the caption ("the rule fails when L3 is partly disabled, e.g. EPYC 9224"). Drop "two fully used CCDs" and the link count from `:355`, and compare the 9174F with the 9124 only on stated quantities (cores, base clock, TDP, L3). |
| I8 | Inconsistent / Unsupported | `part4:152, :192`; `tab:evidence-strength` row "Peak V-Cache bandwidth" (`part6:214`); `part6:232`; Part IV summary `part4:323`; `figures/mindmap-stacked.tex` ("Over 2 TB/s peak"); PDF pp. 85, 87, 96, 138–139 | "The one independent test measures single-thread bytes per cycle"; "no independent measurement tests AMD's aggregate peak bandwidth". The Part IV summary lists ">2 TB/s" as a benefit. | Cozma 2022b (`…Zen3-VCache-Deep-Dive-2022.pdf` pp. 7–8) also measured **one whole CCD**: Milan-X "about 12.5%" *lower* bytes per cycle than Milan. Lam (p. 9) measured all cores of a CCD: the V-Cache CCD averaged 18.45 B/cycle/core, "slightly lower" than the plain CCD. Part VI itself quotes Lam's 702 GB/s multi-threaded V-Cache bandwidth (`part6:63`), about a third of 2 TB/s. | Rewrite the row: "Independent CCD-wide tests (Cozma, Lam) show no gain and ≈0.7 TB/s, against AMD's >2 TB/s peak" (weak, contradicted). Remove ">2 TB/s" from the Part IV benefit bullet, or qualify it as AMD's peak. |
| I9 | Overstated (selective use of a source) | `part5:309–311`; PDF p. 112 | "The mechanism is stable across generations: … the program that gains most is the one that misses most." | Cozma 2024 (`…9800X3D-2024.pdf` p. 9): "the most memory bound test is 523.xalancbmk which doesn't really see a benefit from V-Cache", and 502.gcc is more memory-bound than 520.omnetpp yet gains less. Lam's GHPC (highest MPKI, smaller gain than Cyberpunk) also breaks strict ordering. | "…the programs that gain most are usually among those that miss most, but not always (xalancbmk, GHPC)." |
| I10 | Overstated (calibration presented as validation) | `part5:429` (S0 memory latency), `:466` ("The simulation confirms the main result"), `:472` ("The same conclusion therefore follows from two directions"), `:500` ("The simulations confirm… four conclusions"), `:513`; PDF pp. 117, 122, 125–126 | The model's memory latency "lies close to the measured 342 and 313". S3 "confirms" the analytical break-even. S4 reaches its conclusion "from two directions". | The 1 GB values follow from inputs (47 cycles + 74 ns at 4 GHz, from a 5600G). In ns the model gives 84 against the measured 106 and 89, and the model's 334/319 difference is a hit-fraction effect while the measured one is a clock effect (Cozma 2022a: Milan-X "boosting better"). S3 uses the same 130-cycle calibration and the same structure as `eq:cache-clock-model`, so agreement is expected. The 37 ns in S4 is *fitted* to Reguly's ratio. S1, S5 and S6 follow from the uniform-random or streaming workloads by construction. | Say "is consistent with" or "illustrates", not "confirms". In S0 say the 1 GB match is set by the inputs. In S4 replace "from two directions" with "the fitted 37 ns is about four times AMD's 9 ns". Reword `:500` and `:513` to "the model reproduces, by construction, …". |
| I11 | Inconsistent | `part5:472` vs `part3:185`; `fig:sim-pingpong`; PDF pp. 64, 122 | Model "49 ns per round trip … close to the measured 58.6 ns"; "220.5 ns against the measured 265". | Part III says Reguly's test measures how long **one message** takes. The model's "round trip" is two messages plus two write-upgrades (`cachesim.cpp` ping-pong: X written by a, read by b, Y written by b, read by a; 4 crossings per round trip). One-way equivalents are 24.5 and 110 ns. The `twoccd` preset also uses a 47-cycle L3 at 4 GHz for a Milan-X (51 cycles, ~3.x GHz). The fitted ratio is unaffected; the absolute comparisons are not valid. | Compare ratios only, or report a per-message model time. Say the preset is planar Zen 3 at 4 GHz. |
| I12 | Inconsistent (calibration) | `part5:433`; `tab:sim-calibration`; `appendices/appendix-e-simulation.tex:35`; `tools/cachesim/README.md:70`; PDF p. 118 | Overlap 0.42 "reproduces the 130 cycles inferred from Lam's libx264". | The 130 cycles were derived by charging the four extra cycles **in full** (`part4:176`: (36 + 15)/0.40), but the model hides 58% of those cycles. A self-consistent calibration solves 0.40 × 306.8h − 3.85 × 4h = 36, giving h = **0.335** (≈103 cycles per removed miss). The README says "about 0.36". | Recalibrate to ≈0.34, or state that 0.42 is calibrated on a full-charge inference. Align the README. |
| I13 | Unsupported (missing sensitivity) | `part5:466` ("The break-even at a realistic clock gap is much less sensitive to it"); `tab:sim-sensitivity` covers only S1; PDF pp. 122, 125 | S3 conclusions presented as robust. | Reviewer's rerun of the S3 mix (2 seeds, scratchpad `s3sens.py`). Break-even at the 7.3% gap for overlap 0.16/0.26/0.34/0.42/1.0: **0.65 / 0.43 / 0.35 / 0.30 / 0.17** misses per kinstr. At equal clocks it is 0.044 for every overlap. The realistic-gap break-even is therefore *more* sensitive to the overlap factor, not less. Within the paper's own "measured range" (0.16–0.42) it varies about twofold. | Add S3 rows to the sensitivity table and restate the claim. The sentence is true only for the narrower question of whether the four extra cycles are hidden. |
| I14 | Inconsistent (unfair baseline) | `tab:sim-breakeven` (`figures/sim-table-breakeven.tex`), `part5:466`; PDF pp. 121–122 | "At equal clocks the two disagree more, 0.04 against 0.12 … uncertain by a factor of about three." | The 0.12 is computed at 4.2 GHz; the simulation's equal-clock case is 5.15 GHz. At 5.15 GHz the analytical model gives 15.4/5.15/30.95 = **0.096**, and Part VI itself gives ≈0.10 at 4.8 GHz (`part6:145`). The fair gap is 0.04 vs 0.10 (×2.4), all of it from whether the four cycles are hidden. At 7.3% both use 5.15/4.8 GHz, so that comparison is fair. | Put 0.10 in the analytical row at 0%, footnote 0.12, and change "about three" to "about 2.4". |
| I15 | Overstated | `part5:468`, `:506`; `s3_validation_libx264.csv`; PDF pp. 122, 125 | At the 0.40-removed point the model "predicts a gain of about 8%"; "the simulated sizes of the gains … are therefore upper bounds". | At that point the stacked part has **0 MPKI** (CSV `stacked_mpki` = 0.0), whereas Lam's V-Cache CCD kept ≈1.08 MPKI. The mix cannot represent libx264's operating point, which is why the plain part runs at 590 rather than 735 cycles/kinstr. "Upper bound" does not follow: overlap 1.0 or memory 90 ns give larger gains (`sensitivity.csv`: 3.78 and 3.53 against 3.07). | Add a cold region larger than 96 MB so the stacked part keeps about 1.1 MPKI, and redo the validation point. Replace "upper bounds" with "the sizes depend on the calibration". |
| I16 | Unsupported | `part5:508` ("The latencies of the planar 96 MB L3 and of the side die are assumptions, varied above where they matter"); `part5:451`; PDF pp. 119–120, 125 | The side die is slower than the stacked L3 (19.0 vs 12.7 ns at 48 MB). | The side-die latency (22 ns) is never varied (`sims.py` S2 has no `l4_lat_ns` sweep). The side die is modelled as an inclusive L4 tuned to 2014-era Broadwell eDRAM, so S2's verdict on "beside" is fixed by the inputs. Open question 1 (`part6:288`) asks exactly about a modern 2.5D side die. | Missing experiment: sweep `l4_lat_ns` (for example 5–22 ns) and add an exclusive or "extended-L3" side-die variant. Until then, drop "varied above". |
| I17 | Unsupported | `part5:429`; PDF p. 117 | The flat-to-capacity curve is explained by TLB misses, "AMD's L3 replacement is not exact LRU", and other data. | The paper's own sensitivity runs show the replacement policy changes nothing (`part5:494`). In the model a uniformly random working set no larger than the cache occupies contiguous line numbers (`cachesim.cpp` `makeWorkload`), so it maps evenly onto the sets and never conflicts. The flat curve is largely this ideal physical mapping; real 4 KB pages are scattered over physical memory. | Replace "not exact LRU" with "the model maps the working set contiguously, so it has no conflict misses below capacity". Optionally randomise page placement. |
| I18 | Overstated | Findings `part1:176`; Part III summary `part3:400`; RQ2 `part6:277`; `tab:evidence-strength` row "Link power" (`part6:209`); PDF pp. 30, 75, 138, 143 | Link power is "bounded" at "a few per cent of the power budget". | `sec:chiplet-power` (`part3:313–319`) gives an *estimate*: memory traffic only, using the predecessor link's 2 pJ/bit, and it says that cross-CCD, I/O and idle power "come on top". That is not a bound. The computed shares are about 2% (Genoa, 7.4 of 360 W); no Rome TDP is given. | "estimated at roughly 1–2% of the power budget for memory traffic alone". |
| I19 | Inconsistent | Findings `part1:176`; `part3:399`; RQ2 `part6:277`; PDF pp. 30, 75, 143 | "One compute die serves products from 6 to 96 cores." | `tab:product-matrix`: the 6-core parts are Zen 2/Zen 3 *desktop* CCDs, and the 96-core parts are Zen 4 *server* CCDs, which are different dies. The table body says it correctly ("The Zen 4 server products alone span 16 to 96 cores", `part3:353`). | "Within one generation one CCD spans a 6-core desktop part to a 64-core (Zen 3) or 96-core (Zen 4) server part." |
| I20 | Error (wording reverses a number) | `part2:310`; PDF p. 46 | "the second figure [24 cycles] is half as much again as a 47-cycle L3 hit". | 24 is about *half of* 47; "half as much again" means 1.5×. | "…about half the 47-cycle L3 hit time." |
| I21 | Error (comparison) | `part3:183`; PDF p. 64 | "a core on another CCD in the same socket is almost as far away as a core on another socket is on the Intel machines"; "crossing to the other EPYC socket costs about 1.5 times as much again". | Reguly Fig. 2 (`Reguly…pdf` p. 3): EPYC cross-CCD 265.2–266.2 ns, *above* Intel cross-socket 228.3–246.6 ns. "1.5 times as much again" reads as 2.5×; the data give 397–415/265 ≈ 1.5×. | "…is farther away than a core on the other socket of either Intel machine"; "…costs about 1.5 times the cross-CCD figure". |
| I22 | Inconsistent | `part5:228`; PDF p. 108 | "the three workloads with roughly half their L3 accesses missing gained 9.75–19.7%. Within that group, however, GHPC had the highest MPKI (5.5) and the largest fall in miss rate". | `tab:lam-detail`: the three are CoD, Cyberpunk and 7-Zip (53.5–54.2% missing). GHPC misses 41.4%, so it is not in the group, and it gained 9.67% (below 9.75). The largest fall in points is CoD's (22.2 vs GHPC's 19.4); GHPC's fall is the largest relative one. | "The four miss-heavy workloads gained 9.7–19.7%. Among them GHPC had the highest MPKI and the largest relative fall in miss rate, yet gained less than Cyberpunk." |
| I23 | Inconsistent | `part1:148`, `:168–169`; PDF pp. 29–30 | "The study combines three kinds of evidence" followed by four items. Contribution: "seven controlled simulations, each … compared with the published measurement it mirrors". | `tab:sim-plan`: S2 has no measured counterpart ("no product exists"); S3 is compared with the paper's own analytical model and S6 with `sec:bandwidth-wall`. Bullet `:168` ends with a full stop mid-list. | "four kinds of evidence"; "…seven controlled simulations, each changing one factor, five of them set beside a published measurement". |
| I24 | Inconsistent (integration) | Abstract (`front-matter.tex`, PDF p. 4); `tab:rq-map` (`part1:102–118`); Findings `part1:172–181`; `tab:evidence-strength`; Conclusions `part6:273–283`; mind maps `mindmap-case-study`, `mindmap-paper`; comment `part5:2–3` ("no simulator") | The 10-page simulation study, called a contribution in Part I, appears in none of these. | — | Add one abstract sentence and one Findings bullet (what the model shows and what it cannot), a `tab:rq-map` entry, and an evidence row ("model, illustrative"). Fix the stale comment. **For Ishan:** `CLAUDE.md` §3 and §8 still say initial-draft-2 "uses published data only". |
| I25 | Inconsistent (regression of H11) | `part6:252` vs `sec:open-questions` (`part6:285–296`); PDF pp. 140, 144 | "measurements on the hardware it does have … are listed among the open questions (sec:open-questions)". | None of the eight open questions mentions measurements on the group's hardware. The 5600X kit is mentioned only at `part5:510`. | Add an open question ("Measure latency, overlap and core-to-core cost on the group's Ryzen 5 5600X to test the model's inputs") or change the cross-reference to `sec:sim-limits`. |
| I26 | Inconsistent (grading rubric) | `tab:evidence-strength` row "One compute die serves a wide product range" (`part6:208`); PDF p. 138 | "Strong for the range; configurations partly inferred". | The caption defines weak as "vendor-only". The evidence is AMD statements and AMD datasheets. The core/L3 *range* is a datasheet fact (strong as a fact); the configurations are inferred and the rule is unreliable (I7). | "Strong (datasheet facts) for the range; weak for configurations, which are inferred (I7)". |
| I27 | Overstated | `part4:176`; PDF p. 86 | "The worked example therefore uses no assumed values except the textbook's range for memory latency". | It also assumes that all of the IPC change comes from L3 misses and latency, that every L3 access pays all four extra cycles, that L3 accesses per kinstr are equal on both CCDs (contradicted for DCS, I6), and that counted misses are demand misses (I6). | List these four assumptions. |
| I28 | Overstated (minor) | `part4:220` and the Part IV summary `part4:327`; PDF pp. 90, 97 | The residual "suggests that voltage tolerance and the structural silicon over the cores together explain less than half of the first-generation clock penalty". | The arithmetic is right (5.5/7 = 0.79; 5.5/10 = 0.55), but it mixes rated maxima (9700X's "implied" 5.5 GHz, 9800X3D 5.2) with Lam's measured *average* per-core gap (7%) and a 4.5 vs 5.05 GHz comparison of different SKUs. Cozma also notes "additional power distribution under the CPU cores" in the new cache die (p. 1), so power delivery is mentioned, though not as a cause. Cozma's sample was supplied by AMD (p. 2). | Keep it as "suggests that other factors remain", drop "less than half", and note in `tab:evidence-ledger` that the 9800X3D was an AMD-supplied sample. |
| I29 | Inconsistent (method) | `part5:113` vs `:224`; Findings `part1:178`; `tab:independent` (`part5:148`); Part V summary `:513` | Method: ranges and source medians "rather than as averages". The geometric mean of 11.4% is then a headline figure. | The deviation is acknowledged at `:224`, but the mean is the authors' calculation over six workloads chosen by Lam. | Write "(authors' calculation over Lam's five quantified workloads)" wherever 11.4% appears, or amend the method sentence. |
| I30 | Inconsistent (minor) | `part5:192` vs `:429` and `make_figures.py:23`; PDF pp. 107, 117 | "on Milan it rises to roughly 250–300 cycles by 64–96 MB, five to six times as long". | The same chart reading gives 240 at 64 MB and 290 at 128 MB: 240/51 = 4.7. | "about 240 cycles at 64 MB, nearly five times as long". |
| I31 | Minor | `part5:280`; PDF p. 111 | "The two stacked products have the same L3 per core … The wider window therefore cannot come from more cache per core." | Lawenda p. 3: Genoa and Genoa-X have 1 MB L2 per core against 512 KB on Milan(-X). | "…cannot come from more L3 per core (the L2 does double)". |
| I32 | Minor (cannot verify cause) | `tab:tlb-reach` (`part2:302`); PDF p. 46 | First-level DTLB reach with 4 KB pages: 256 KB. | The cited 7-cpu page says "Data TLB L1: 64 items (about 800 KB of memory)" (`7cpu-Zen3-Cezanne-latency.pdf` p. 2). The cause, possibly page coalescing, cannot be verified. | Note the discrepancy in one clause. |
| I33 | Minor (stale) | `part6:226`; PDF p. 139 | "a monolithic die is expected to remain faster … although no source used here measures this directly". | `tab:core-to-core` now gives Reguly's monolithic Xeon 8360Y adjacent-core latency (106–110 ns) against the EPYC cross-CCD 265 ns: partial, cross-vendor evidence. | "…only Reguly's cross-vendor test bears on it (`tab:core-to-core`)". |
| I34 | Format | `appendices/appendix-e-simulation.tex:47–53`; PDF p. 154 | Shell commands in `verbatim`. | `CLAUDE.md` §5: "Code: only via listings or minted". Shell commands are code. | Use `lstlisting` (style already configured). `verbatim` is not acceptable under the rule. |
| I35 | Minor (citation) | `appendices/appendix-e-simulation.tex:43` | "one memory access per three instructions \cite[sec.~11.2.5]{sarangi2025basic}". | Sarangi sec. 11.2.5 is "The replace Operation". The one-third figure is in sec. 11.1.1 (the CPI = 34 example) and sec. 1.7.3. | Cite sec. 11.1.1 and call it an assumption here and in `sec:sim-clock`, together with `l1_lat = 1` and `work_cycles = 0.31` (the main text currently does not use the word "assumption" for any of the three). |
| I36 | Minor (model description) | `appendices/appendix-e-simulation.tex:5, 12–14`; `tab:sim-parameters` | (a) "no plotted value was typed by hand"; (b) time is the largest of four limits, including link bandwidth; (c) "every run warms the caches … statistics are reset"; (d) S6 parameters. | (a) The measured Milan and Milan-X points are hard-coded in `make_figures.py:23–24`. (b) `link_gbs` defaults to 0 (`cachesim.cpp:68, :562`) and `sims.py` never sets it, so the link limit is inactive in every experiment; the README says 55 GB/s. (c) Ping-pong runs have no warm-up or reset; they skip the first 40 accesses. (d) A write to a shared line costs L3 + hop (`cachesim.cpp` `access`), which is half of S4's crossings and is undocumented. S6 uses overlap 0.05 and 250 000 accesses per thread (`sims.py:223`), which are not in the table, against "10^6 measured accesses" at `part5:405`. | Correct each statement. |
| I37 | Minor | `part5:405`; PDF p. 117 | "The spread between seeds was below 1% of the mean at every point". | `s1_working_set.csv`: hot/cold `p32_dram_per_kacc` spreads 2.5% at 40 MB and 1.6% at 48 MB. Every *plotted* quantity is below 1%. | "below 1% for every plotted quantity". |
| I38 | Minor | `tab:sim-plan` column header (`part5:414`); PDF p. 118 | "Measured counterpart" lists `sec:cache-clock-model` (S3) and `sec:bandwidth-wall` (S6). | These are the paper's own models, not measurements. | Rename the column "Compared with". |
| I39 | Figure | `figures/sim-zen2-zen3.tex` legend; `figures/zen-ccd-evolution.tex` "C" labels; `figures/monolithic-vs-chiplet.tex`; PDF pp. 124, 99, 58 | — | Measured from the PDF word boxes: the `fig:sim-zen2-zen3` legend is about 6 pt and the core labels in `fig:zen-ccd-evolution` are about 6 pt (below the 7 pt guide). In `fig:monolithic-vs-chiplet`(a) the "Memory controllers, PCIe, SerDes" box sticks out past both sides of the die outline, and the "die-to-die link" label (about 5 pt) still touches its arrow (H20). Pages 123–124 leave large blank areas because both S5 and S6 figures float to p. 124. | Enlarge the legend and labels to ≥7 pt; narrow the box or widen the die; move the label; use `[!t]` or reorder the floats. |
| I40 | Writing (abbreviations) | `part2:192` (TLB used before `:288`); `part2:261` (CCX before Part III); `part1:112` (NUMA in `tab:rq-map`); `part3:309, :334` (TDP before `:387`; regression of W4); `part1:141` (HPC); `part5:178` (FVOPS); `appendices/appendix-d…:7` (ECC); `part3:72` (PCIe) | Used before definition. | — | Expand at first use: "translation lookaside buffer (TLB)", "core complex (CCX)", "non-uniform memory access (NUMA)", "thermal design power (TDP)" at `part3:309`, "high-performance computing (HPC)", "FVOPS (finite volumes solved per second)", "error-correcting code (ECC)", "PCI Express (PCIe)". |
| I41 | Writing (terminology) | Parts III/VI "hop" (23 uses) against the simulation's "crossing" (7); "stacked die", "cache die", "L3D", "stacked cache"; W18 still open | Same quantity, different names. | — | Glossary entry: "die-to-die hop (called a crossing in the simulation)"; "L3D = cache die"; "V-Cache CCD = CCD with an L3D". |
| I42 | Structure (repetition) | The 130-cycle derivation at `part2:323–324`, `part4:163–176`, `part5:196`, `part5:228–248`, `part5:433`, `part6:120`, `appendix-e:35` | The same argument is restated in full in several places. Part II's worked example also uses a Part IV result before Part IV derives it. | — | Derive it once (Part IV). Have Part II state the MLP principle with the textbook range only, and make the other places cite back in one sentence. |
| I43 | Structure / length | Part V, PDF pp. 98–126 (29 pp, target 25), of which `sec:sim-study` is pp. 117–126 | — | — | Keep S0–S4 in Part V as about 4–5 pages. Move S5, S6, `tab:sim-planar`, `tab:sim-split`, the sensitivity table and the model limits list to Appendix E. Parts II–IV are 3–4 pages under target each (see §7). |

**Writing items with suggested rewrites (in addition to I20–I23 and I40–I41):**

| Location | Problem | Rewrite |
|---|---|---|
| `part5:263` | "about 300 bytes per grid point fit in three times as many points' worth of L3 on Milan-X" is hard to parse | "At about 300 bytes per point, Milan-X's L3 holds three times as many grid points as Milan's." |
| `part5:402` | "so that agreement adds a second kind of evidence" overstates a calibrated model | "so that agreement shows the model is consistent with the measurement, and disagreement shows…" |
| `part5:466` | "Neither assumption has been measured, so the equal-clock break-even is uncertain by a factor of about three" | After I14: "…uncertain by a factor of about 2.4 (0.04 against 0.10 at the same clock)." |
| `part5:441` | "the larger one is 5–6% slower in the random workload because of its four extra cycles" (S1, time with overlap) vs S2's 8.5% | Name the metric in both places: "memory-system time (overlap 0.42)" vs "raw access latency". |
| `part3:162` | "here each of those steps also crosses the package" ignores that the sources do not place AMD's directory (said at `part2:437`) | "…would also cross the package if the directory sat on another die (`part2:437`)." |
| `part6:145` | One 120-word sentence on the 4.8 GHz baseline in parentheses | Split it: give the factor of three, then the 4.8 GHz caveat as its own sentence. |
| `part1:177` | "a cost confirmed independently in three generations" | "measured independently in three generations" ("confirmed" sits oddly with the 3–4 cycle range on Zen 3). |

No sentence attributes work to an individual. Group names appear only in `metadata.tex`, and the single "our" (`part5:49`, "In our reading") is collective. The prose is consistently in the present tense; past tense is used only for completed measurements, which is appropriate.

---

## 3. Regression check

**H1–H24 (third review).**

| ID | Status | Note |
|---|---|---|
| H1 | Fixed | RQ1 (`part6:275`) and the evidence row say cost per good die; Moderate; Murphy/Dong–Xie cited. |
| H2 | Fixed | `part5:196`: 1.2–2.8 points. |
| H3 | Fixed | `part4:327` "the reason AMD gives", voltage tolerance named. |
| H4 | Fixed | RQ4 (`part6:281`), Part V summary (`part5:513`) and the evidence row now separate latency (strong) from IPC (moderate). |
| H5 | Fixed | `part3:389` "no visible hop, without showing how large"; row and mind-map caption softened. |
| H6 | Fixed | `part6:148` "suggest". |
| H7 | Fixed | Bandwidth row Weak; yield row Moderate. (The bandwidth row now has a new factual problem, I8.) |
| H8 | Fixed | "Flat to beyond 64 MB" in `mindmap-case-study.tex:17`; `milanx-latency` caption consistent. |
| H9 | Fixed | OpenFOAM removed from the "little change" box. |
| H10 | Partly fixed | The method sentence is corrected, but a new author-computed geometric mean is now a headline (I29). |
| H11 | Partly fixed / regressed | Part V and VI wording fixed, but `part6:252` points to open questions that do not contain the item (I25). |
| H12 | Fixed | `part1:59` "By AMD's account…". |
| H13 | Fixed | Footnote to `tab:cache-vs-clock`. (`tab:lam-detail` and `fig:lam-ipc` still give Cyberpunk's IPC without the GPU-bound note; minor.) |
| H14 | Fixed | `part5:53`. |
| H15 | Fixed | 8%. |
| H16 | Fixed | One mention, 1.24× (1.22× in Fig. 4). |
| H17 | Partly applied | Architectural justification added (`part4:137`); Ishan's decision. |
| H18 | Decision taken | 13 maps kept. All are legible: smallest map text measured at 7.5–8.3 pt (smallest in `mindmap-chiplet-tradeoff`, 7.5 pt). No map adds a claim the text lacks. Only "Over 2 TB/s peak" (`mindmap-stacked`) repeats a figure the evidence now contradicts (I8). |
| H19 | Partly applied | Appendix D created; Cezanne kept by decision. |
| H20 | Partly fixed | Core grid fixed; the I/O box now overflows the die outline and the link label still touches its arrow (I39). |
| H21 | Partly fixed | Abstract rewritten (but omits the simulation, I24); `\partbudget` lines and App. A/B `\todo` remain; `\draftdate` = 5 Nov 2026 matches the build. |
| H22 | Fixed | RQ2 covers power and flexibility. (New overstatements I18 and I19 were introduced there.) |
| H23 | Fixed | "probably explains much of why". |
| H24 | Fixed | `tab:three-way` note. |

**W1–W18.**

| ID | Status | Note |
|---|---|---|
| W1, W2 | Fixed | No gendered pronouns for authors found (grep). |
| W3 | Fixed | |
| W4 | Regressed | TDP used at `part3:309` and in `tab:product-matrix` before its expansion at `part3:387` (I40). |
| W5 | Partly fixed | Expanded at `part2:439`; still bare in `tab:rq-map`. |
| W6–W9 | Fixed | |
| W10 | Fixed | GHPC described at `part5:202`. |
| W11–W17 | Fixed | |
| W18 | Not done | I41. |

**F1–F23 and G1–G20 (spot-check).** I re-checked the numbers these earlier rounds touched and found no regression:
- yield 82.4/68.8/38.3/86.6%;
- dies per wafer 878/92/95/35 and the factors 1.9/2.7/3.5;
- NUMA latencies 90/141/234 and 94/104/201, and 0.81×;
- AMAT 1.60/1.46/1.38 ns;
- the address split 36/32/27 bits;
- Phoronix 244/106/350, 12 ≥ 50%;
- OpenFOAM 0.81–1.54× and 1.24×/1.22×;
- MiniFE 3.4× and 1.04×;
- the clock-correction table;
- Cezanne 47/47.49 cycles, 76.1 vs 61.8 ns, 3.22%.

---

## 4. Simulation check

### 4.1 Model description (Appendix E against `tools/cachesim/src/cachesim.cpp`)

| Appendix E statement | Code | Verdict |
|---|---|---|
| L1 private; L2 private, contains L1 | `l2Fill` invalidates the L1 copy on L2 eviction | Correct |
| L3 per group, "filled on every miss" | `fetch` → `l3Insert` on DRAM and remote fills | Correct. Note that real Zen L3s are fed by L2 evictions; the README says the model omits "victim-cache behaviour", but the paper does not. |
| L4 shared, filled on every miss, holds copies | `fetch`: `l4Insert(ln,false)` on each DRAM read | Correct |
| Directory; write invalidates; modified line served core to core | `access` / `fetch` | Correct. Undocumented: a write to a line held elsewhere adds an L3 latency, plus the hop if remote (I36). |
| Latency formula: L1/L2/L3; remote = 2 × L3 + hop; L4 = L3 + L4; DRAM = L3 + fixed ns | `fetch` returns these values | Correct. However, **no hop on DRAM access** (I2). |
| Overlap scales the part beyond an L2 hit | `exposed = l2_lat + overlap·(lat − l2_lat)` (`:367`) | Correct, but reported `amat_ns` ignores it (I1). |
| Time = max of four limits incl. link | `summarize` | The link limit is inactive (`link_gbs = 0`, I36). |
| Warm-up and statistics reset | `run`: in-order touch up to capacity, then random warm-up, then `sim.reset()` | Correct for random/hot-cold/sequential; ping-pong differs (I36). |
| Coherence/time model as described | — | Otherwise accurate. |

### 4.2 Numbers checked against the CSVs (38)

| # | Paper value (location) | CSV value | OK? |
|---|---|---|---|
| 1 | S0 L3 plateaus 46.4 / 50.8 cycles | `s0_latency_sweep` 46.45 (32 MB), 50.79 (96 MB) | ✓ |
| 2 | S0 1 GB: 334 / 319 | 333.70 / 319.13 | ✓ |
| 3 | S0 model at 64 MB: 195 | 194.59 | ✓ |
| 4 | S0 model Milan-X at 96 MB: 51 | 50.79 | ✓ |
| 5 | Calibration 0.42 → 127 (130) | `s0_calibration` 127.2 | ✓ |
| 6 | 0.26 → 79; 0.16 → 48 | 78.74; 48.46 | ✓ |
| 7 | 0.6 → 182; 1.0 → 303 | 181.71; 302.86 | ✓ |
| 8 | S1 fit: 5–6% slower (random) | 0.9432–0.9499 | ✓ |
| 9 | S1 fit: 1–5% slower (hot/cold) | 0.9462–0.9905 | ✓ |
| 10 | S1 1.8× at 40 MB | 1.7944 | ✓ |
| 11 | S1 3.8× at 96 MB | 3.7718 | ✓ |
| 12 | S1 hot/cold 1.04–1.31 | 1.037–1.3072 | ✓ |
| 13 | S1 2.0× at 128, 1.3× at 256 | 2.0023, 1.2748 | ✓ |
| 14 | S2 12.6 vs 14.6 ns, about 14% | 12.70 vs 14.69 at 96 MB (13.5%) | ✓ (but raw latency, I1) |
| 15 | S2 19.0 vs 12.7 ns at 48 MB | 18.985 vs 12.647 | ✓ |
| 16 | S2 planar 14.5 vs 11.6 (25%); stacked 8.5% | 14.50/11.56 = 1.254; 12.54/11.56 = 1.085 | ✓ (raw, I1) |
| 17 | `tab:sim-planar` 47/107/147/196/226/245 | 47.0/106.9/146.7/196.0/225.7/245.3 | ✓ |
| 18 | S3 break-even 0.04/0.11/0.18/0.25/0.29/0.39 | `s3_breakeven` 0.044/0.112/0.181/0.249/0.294/0.387 | ✓ |
| 19 | S3 validation ≈ 8% at 0.40 removed | 6.73% (0.337) and 9.19% (0.440) → 8.2% by interpolation | ✓ |
| 20 | Plain ≈ 590 cycles/kinstr there | 585.9–599.6 | ✓ |
| 21 | ≈ 735 cycles/kinstr at 1.48 MPKI (App. E) | 731.8 at 1.452 MPKI, 4.2 GHz | ✓ |
| 22 | S4 same-CCD 49 ns | `s4_pingpong` 49 | ✓ |
| 23 | 9 ns → 108.5 ns, 2.2× | 108.5, 2.214 | ✓ |
| 24 | 37 ns → 220.5 ns, 4.5× | 220.5, 4.5 | ✓ |
| 25 | S4 split 66 crossings per 1000 | 66.33 | ✓ |
| 26 | 1.29× / 1.52× / 1.71× | 1.2928 / 1.5243 / 1.7145 | ✓ |
| 27 | Split two-die 14.3/16.8/18.9 ns; private 10.3, 1.00× | 14.26/16.82/18.92; 10.27 | ✓ |
| 28 | S5 Zen 2 8.9–9.5 ns, Zen 3 10.6–11.5 ns (≤ 16 MB) | 8.89–9.54; 10.64–11.48 | ✓ |
| 29 | S5 "up to three times (11.6 vs 34.3 at 24 MB)" | 24 MB: 34.29/11.57 = 2.96; but 32 MB: 46.70/11.61 = 4.0 | ✗ (I4) |
| 30 | S6 1.08 → 0.68 G lines/s at 5 threads | 1.0847 → 0.6768 | ✓ |
| 31 | S6 DRAM limit 0.8 | 0.8 | ✓ |
| 32 | S6 96 MB reaches 2.1, i.e. 2.7× the limit | 2.1405; 2.68 | ✓ |
| 33 | Sensitivity: loss 3–11% when data fit | 0.9674 → 0.8932 | ✓ |
| 34 | Gain 2.2–3.8× in the window | 2.1999–3.7838 | ✓ |
| 35 | Window gain ±30% from overlap and memory | 2.20/3.07 = −28%; 3.78/3.07 = +23%; memory −13/+15% | ✓ |
| 36 | Replacement within 0.1% | max difference 0.06% | ✓ |
| 37 | Stacked L3 at 55 cycles: loss 5.6 → 10.7% | 0.9436 → 0.8932 | ✓ |
| 38 | Seed spread < 1% "at every point" | max 2.5% (hot/cold DRAM count, 40 MB) | ✗ (I37) |

Values in the S3 table and figure are also consistent with `s3_cache_vs_clock.csv` (for example, the 7.3% speed-ups 0.9201 at 0 removed and 1.0115 at 0.337).

### 4.3 Reproduction

- Built with MSYS2 UCRT64 `g++ -O2 -std=c++17` (Windows; the prompt's WSL path was not needed). `--selftest`: **8 PASS, 0 failures**.
- Ran `sims.py --only s0 s4` and then all remaining experiments (`s1 s2 s3 s5 s6 sens`; `derive` via s3) into the scratchpad. **All 13 CSVs are byte-identical** to `research/measurements/cachesim/` (`diff --strip-trailing-cr`). The study is deterministic for the given seeds and reproduces exactly. S0 + S4 took about 4 minutes on 16 threads.
- Extra reviewer runs (scratchpad, not in the repo):
  - S3 break-even against the overlap factor (I13);
  - the effective L3 access rate of the S3 mix (I5);
  - the effect of overlap on `amat_ns` (I1);
  - the self-consistent overlap factor (I12).

### 4.4 Calibration against validation

- **Fitted:** overlap 0.42 (to the 130 cycles, itself inferred with a full-charge assumption, I12); crossing 37 ns (to Reguly's 4.5× ratio); `work_cycles = 0.31` and `l1_lat = 1` (to 735 cycles/kinstr); and the L4 latency of 22 ns (to Broadwell).
- **Presented as validation:**
  - the S0 memory-latency match (inputs) and the S0 plateaus (correctly called inputs);
  - S3 "confirms" the analytical model (same calibration);
  - S4 "two directions" (fitted);
  - `sec:sim-limits` "The simulations confirm…" (I10).
- **Genuinely independent of the fit:** the S0 *shape* between the levels, where the model disagrees and says so (good practice, but with a wrong explanation, I17, and a wrong "upper bound" conclusion, I3), and the S3 libx264 check (8% vs 4.9%), which is reported honestly but at a mis-specified operating point (I15).

### 4.5 Overreach

- **Model outputs labelled:** mostly yes ("model outputs", "memory-system speed-up, not of a program"; S1 caption good).
- **Memory-system speed-ups vs program speed-ups:** kept apart in S1. S5's "wins by up to three times" and S4's 1.29–1.71× are raw access-time ratios with no overlap (I1) and could be read as performance.
- **Upper-bound statements:** they do not follow from the stated reasons (I3, I15).
- **Assumed inputs:**
  - planar 59 cycles: labelled ✓;
  - L4 die: labelled in the caption ✓, but not varied, despite the claim that it was (I16);
  - one access per three instructions, `l1_lat = 1`, `work_cycles = 0.31`: labelled only in the appendix, and with a wrong citation (I35);
  - S6 overlap 0.05: caption only (I36).
- **S3 against Part VI (5.15 vs 4.2 GHz):** not a fair comparison at 0% (I14). At 7.3% it is fair; the remaining difference (0.29 vs 0.35) is entirely whether the four extra cycles are hidden.

### 4.6 Design and fit

One factor at a time with five seeds is sound for what the model is. Seeds add little, because the spread is under 1%; a sensitivity analysis across *inputs* matters far more, and it covers only S1.

The study supports RQ3 and RQ4 as an illustration, and it is in the right Part (V). At 10 pages it is too long for what it adds.

Experiments that are missing and would matter:
- S3 sensitivity (I13);
- a side-die latency sweep and an exclusive L4 (I16);
- a two-die model that charges the hop on memory access (I2);
- a libx264-like mix that keeps misses on the stacked part (I15).

S6 adds little beyond the bandwidth arithmetic of Part III and could move to the appendix.

---

## 5. Spot-checked numbers (41)

| # | Claim (location) | Source | OK? |
|---|---|---|---|
| 1 | Reguly core-to-core 58.6; 265.2–266.2; 396.9–415.3; Xeon 0.1/106.1–109.5/228.3–233.9; Max 0.7/83.6–84.4/241.6–246.6 (`tab:core-to-core`) | Reguly p. 3, Fig. 2 (rendered) | ✓ |
| 2 | 265/58.6 = 4.5×; 207 ns > 20 × 9 ns | arithmetic | ✓ |
| 3 | Reguly cross-socket "1.6× worse" | Reguly p. 3 | ✓ |
| 4 | Shared counter: 0.12 / 0.53 / 0.80 s | arithmetic | ✓ |
| 5 | Lam GHPC 58.65→78.00%, IPC 1.15→1.27 | Lam p. 12 (rendered) | ✓ |
| 6 | Lam Cyberpunk 63.7%, IPC 1.26→1.43; MPKI 5 | Lam pp. 13, 16 | ✓ |
| 7 | Lam DCS 89.06→92.42%, MPKI 0.35→0.28 | Lam p. 14 (rendered) | ✓ (but see I6) |
| 8 | Lam CoD 46.51→68.68%, IPC 0.71→0.85 | Lam p. 15 (rendered) | ✓ |
| 9 | CoD MPKI "not legible" | Lam p. 15: the text is clipped at the page edge in the PDF itself ("eating a staggerin…") | ✓ |
| 10 | Back-end slots 29.65→24.17%, front end 42–43% | Lam p. 16 chart | ✓ |
| 11 | 7-Zip 45.76→59.21%, IPC 1.33→1.46 (9.75%) | Lam p. 17 | ✓ |
| 12 | libx264 61.55→71.86%, 1.36→1.43; 1.48 MPKI; 16.75% | Lam p. 16 | ✓ |
| 13 | Geometric mean 1.114; median 9.75%; 1.114^(5/6) = 1.094 | arithmetic | ✓ |
| 14 | `tab:lam-per-miss` 13.3/2.57/77/53/≈50; 9.3/1.64/94/37/≈80; 3.85/0.40/36/15/≈130 | arithmetic | ✓ |
| 15 | Lam 4.8 vs 5.15 GHz all-core; 7% average; 5800X3D 4.5 vs 5950X 5.05 (≈10%) | Lam pp. 5, 9 | ✓ |
| 16 | 9800X3D: 1.4 V, 1.28–1.31 V; 7800X3D 1.2/1.1 V; 10 vs 70 MHz; 300 MHz deficit; 95 °C at 4.7 GHz | Cozma 2024 pp. 2–3, 11 | ✓ |
| 17 | 9800X3D 5.2/4.7 GHz, 96 MB, 4 nm CCD, 6 nm IOD | AMD spec sheet | ✓ |
| 18 | SPEC fotonik3d +7.5%, roms +15%; 500 MHz deficit | Cozma 2024 p. 10 | ✓ (but I9) |
| 19 | Lawenda Table 5 clock ranges; two rows labelled "64-core Genoa", none "Genoa X" | Lawenda p. 6 (rendered) | ✓. The misprint reading is plausible and is labelled as an assumption. |
| 20 | Genoa-X 0.98–1.60×; Genoa vs Milan-X 1.24–1.70×; Genoa-X vs Milan-X up to 2.67× | Lawenda Table 6, p. 7 | ✓ |
| 21 | Windows 15k–100k / 10k–200k cells per core; 14 821 and 4715 cells per core | Lawenda p. 7 | ✓ |
| 22 | EPYC 9654 2.40/3.70/3.55 GHz, 360 W, 384 MB; 9684X 2.55/3.70/3.42, 400 W, 1152 MB | 9004 datasheet p. 2 | ✓ |
| 23 | 9554/9354/9334/9124/9174F/9184X rows (cores, L3, TDP) | 9004 datasheet p. 2 | ✓ (CCD inference: I7) |
| 24 | 9174F 8 × 2, 4.10 vs 3.00 GHz; one or two GMI links; 4/8/12 dies | 4th-Gen white paper pp. 5, 9 | ✓ |
| 25 | Ryzen 5950X/5900X/5800X/5600X/3950X/3900X TDP and L3 | Ryzen datasheet | ✓ |
| 26 | Product-line silicon: 101/110/124; 99/107/118; 75% bonding break-even | arithmetic from `tab:stack-yield` | ✓ |
| 27 | Stack yields 85.4/92.2/79.1%; 139 vs 154 mm²; 5% and 14% at D0 = 0.1/0.3 | arithmetic | ✓ |
| 28 | AMD cost per yielded mm² rises "roughly a third" from 7 to 5 nm | ISSCC slide 6 (rendered): ≈3.7 → ≈4.9 | ✓ |
| 29 | Link power 3.3 W (Rome), 7.4 W ≈ 2% (Genoa) | arithmetic; datasheet 460.8 GB/s, 360 W | ✓ (wording I18) |
| 30 | Directory example 2+4+4+4+4 = 18; bus 5(N−1) = 35/315; sharer-vector overhead 1.6/12.5/25% | arithmetic; Sarangi sec. 12.4.6 ("superset" statement verified) | ✓; counting assumptions labelled as the authors' (`part2:413`) ✓ |
| 31 | Write-traffic example: 160 KB vs 16 KB; 20 480 vs 256 transactions | arithmetic | ✓ |
| 32 | Inclusion table 36/100 MB, 12.5%/4.2%, 3.0×/2.8× | arithmetic | ✓ |
| 33 | TLB reach 256 KB/8 MB/128 MB/4 GB; 24 576 pages = 12 × 2048 | arithmetic (see I32 for 7-cpu's 800 KB) | ✓ |
| 34 | 7-cpu: 7 / 24-cycle TLB penalties; 1.7 / 5 parallel; 64 and 2048 entries | 7-cpu p. 2 | ✓ |
| 35 | MLP: 1 − h = 130/(313–342) = 0.38–0.42; 2.4–2.6 misses; 57% at 300 | arithmetic | ✓ |
| 36 | Sarangi: TLB 32–64 entries, fraction of a cycle, ≈99%, tens of cycles, CR3; write buffer 4–8 entries; window 64–128; 100–300 cycles (sec. 12.4.8); "as of 2025" exclusive caches | Sarangi text | ✓ |
| 37 | Cozma 2022b: 3.15 vs 3.3 GHz; gem5 +7.6%/≈12.5%; libx264 ≈+5%/≈10%; 25% single-thread bytes per cycle; 24–28 cycles vs Intel | Cozma 2022b pp. 3–14 | ✓ (but I8 omission) |
| 38 | Naffziger: 55 GB/s at 1.46 GHz, 14.6 GT/s, ≥ 4 CCDs, 13 FCLK < 9 ns, 2 pJ/b, 9-2-9 / 5-2-5, 19% | Naffziger p. 44 | ✓ |
| 39 | EPYC 7003: 1600 MHz FCLK, 4 TB, 128/160 lanes, 64→48 lanes for xGMI, diagonal quadrants, 14 nm label, > 200× / > 15× density | EPYC 7003 overview | ✓ |
| 40 | Black: 88.35→92.85 °C, 88.43 °C; 13% / 55%; 66%; 15%/15%, 1.3×, +14/+26 °C; 34%/8% | Black 2006 | ✓ |
| 41 | TechSpot 5800X vs 3700X: 22/24/19/16/30/26/12/6/14/27/23%, 4.55 GHz; 5700G: −10%, −9%, −11%, 15% less power | TechSpot reviews | ✓ |

Also verified: CapFrameX 3.22%, 4.5–4.55 GHz, ring-to-fabric explanation, "very similar"; Liu et al. challenges; Kim 26%; Mittal "half or one-third the latency", "hundreds of megabytes"; Domke 280 W, 2.45/2.20 GHz, 256/768 MiB, 9.56×; AMD press release 19% IPC at a locked 4 GHz, 3800XT vs 5800X; Phoronix "In a small set of tests the Ryzen 7 5800X3D does lose out" (quoted correctly at `part5:315`).

Citations: all 36 cited keys exist in `references.bib` and are listed as present in `research/pdfs/README.md`; the only uncited bib key is `swaminathanNextFrontierEnabling2022` (no PDF; correctly not cited). Vendor claims are attributed to AMD throughout.

---

## 6. Research questions and argument

| RQ | Answered in Conclusions? | Supported by Parts II–V (and the simulations)? | Strength consistent with `tab:evidence-strength`? |
|---|---|---|---|
| RQ1 | Yes (`part6:275`) | Yes: yield and dies-per-wafer models, AMD chart, reticle statement, uneven scaling (Naffziger, ISSCC slide 6). | Yes (Moderate). |
| RQ2 | Yes (`part6:277`), including power and flexibility | Latency (NUMA table, Cezanne), bandwidth (link vs memory), sharing (Reguly) and flexibility: yes. Power: estimate only, correctly called qualitative. The simulation adds S4, but its result is built in (I2). | Mostly. The power wording says "bounds" (I18); "6 to 96 cores" conflates generations (I19); the flexibility row grades vendor-only evidence Strong (I26). |
| RQ2a | Yes (inside RQ2) | Yes: Naffziger on reach and two-deep columns; AMD packaging talk. | No row of its own; adequate. |
| RQ3 | Yes (`part6:279`) | Yes for capacity, latency and footprint. The thermal side is indirect, as stated. The simulation's S2 adds the planar vs stacked latency argument but cannot price area. | Yes. The bandwidth benefit should be dropped or qualified (I8). |
| RQ4 | Yes (`part6:281`) | The direction and latency cost are well supported. The size of the IPC gain rests on one controlled study whose counters include prefetch (I6). The simulations illustrate the window and the clock effect but do not test them independently (I10, I13). | Yes for the latency claim (strong) and the IPC claim (moderate). |

**Overreach** (item 8):
- Causal claims from uncontrolled comparisons: well handled overall. The exception is "because out-of-order cores overlap their misses" (I6).
- Models or simulations presented as measurements or confirmations: I10.
- Chart readings presented as exact: generally labelled; "four cycles" is fine.
- Inferences presented as facts: CCD counts (I7). The Lawenda misprint reading is correctly labelled.
- Conclusions stronger than the threats section allows: the threats section omits the simulation's own limits.

**The three weakest links, and what would fix each:**
1. **Cycles per removed miss (50–130) and the MLP explanation.** It feeds the Part II worked example, the break-evens, the cache–clock model and the calibration of the simulator. The fix: disclose the speculative and prefetch counting, report the DCS inconsistency, present the values as "apparent", and show that the break-even conclusions survive a ±50% change in the per-miss value. Part VI's model makes this easy.
2. **The simulation as confirmation.** The fix: the corrections in I1–I5 and I10–I17, recast as "a model that makes the paper's mechanisms explicit and shows which inputs matter", with S3 and S4 rerun as described.
3. **Product flexibility as the economic case for stacking and chiplets.** It rests on AMD statements, datasheets and inferred configurations. The fix: drop the inferred configurations (I7), keep the datasheet facts, and grade the row as such. `tab:product-line-silicon` is the paper's own quantitative support for this claim and is sound.

**Anything important still missing (item 10).** The only gap that matters is a short statement of how the L3 is filled in Zen: it is fed by L2 evictions (a victim cache). The README admits the model omits this and Part II leaves the inclusion policy open. If no local source states it, say so in Part II and in the model limits.

---

## 7. Page counts per part (PDF pages)

| Part | Pages | Count | Target | Comment |
|---|---|---|---|---|
| Front matter (cover to glossary) | 1–22 | 22 | — | Order verified: cover (1), copyright (2), acknowledgements (3), abstract (4), contents, list of tables, list of figures, glossary |
| I Introduction | 23–32 | 10 | 10 | On target |
| II Foundations | 33–54 | 22 | 25 | Could gain a page by stating the L3 fill/victim behaviour and a short MLP note in place of the forward-dependent worked example |
| III Chiplets | 55–75 | 21 | 25 | Short; fine as is |
| IV Stacked cache | 76–97 | 22 | 25 | Short; fine as is |
| V Case study | 98–126 | 29 | 25 | Too long. The simulation section (pp. 117–126) should shrink to about 5 pages (I43) |
| VI Synthesis | 127–144 | 18 | 20 | Short by 2; adding an evidence row and a Findings link for the model would use part of it |
| **Body** | 23–144 | **122** | 130 | |
| References; App. A–E; index | 145–155 | 11 | — | |

---

## 8. What I checked and found correct

- **Build currency and log:** the PDF is newer than all sources; 0 errors, 0 overfull boxes, no undefined references or citations.
- **Format:**
  - A4 (595.3 × 841.9 pt); measured left and right text margins of 71–72 pt (1 in); 12-pt body text;
  - page order cover → copyright → acknowledgements → abstract → contents;
  - generated contents, list of tables, list of figures, glossary and index present;
  - diagrams all TikZ/pgfplots;
  - App. A and B are known placeholders with `\todo` notes that use "displayed" wording (not counted as errors);
  - `verbatim` in App. E is not acceptable under the code rule (I34).
- **Leftovers:**
  - two `\todo` (App. A, B, PDF pp. 148–149);
  - six `\partbudget` status lines (one per Part);
  - no `\verify`, no "??", no undefined references;
  - unreferenced labels only for App. A/B and four equations (acceptable).
- **Simulation:** the code matches Appendix E apart from I1, I2 and I36; the self-test passes; all 13 CSVs reproduce byte for byte; 36 of 38 checked numbers match.
- **Correct in the new material:**
  - Part I: related work (Liu, Mittal, Black, Dong–Xie, Domke 9.56×), with its claims matching the sources.
  - Part II: writes and inclusion, virtual memory and TLB, MLP and SMT, the MSI and directory examples (assumptions labelled), topologies, Amdahl — all correct against Sarangi, except I20.
  - Part III: the cross-CCD numbers (except I21); the power section's arithmetic; the 9174F statements; the Cezanne section's numbers.
  - Part IV: the D2W/W2W cost model, `tab:stack-yield` and `tab:product-line-silicon` arithmetic, and the node-cost reading of AMD's chart.
  - Part V: the evidence ledger matches each source's stated conditions; `tab:lam-detail` values match the rendered charts; MiniFE bytes-per-point inference; OpenFOAM and Genoa-X numbers; cross-check arithmetic (17–26%).
  - Part VI: cache–clock model numbers (−2.1/+5.2/+1.0/−6.7%, 0.12/0.35/0.50, 30%/26% memory share); per-core resources; Broadwell comparison; Reguly bandwidth ratios.
- **Mind maps:** all 13 legible (≥7.5 pt). They add no unsupported number; the 2 TB/s node is the only issue (I8).
