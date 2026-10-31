# Research landscape, verification framework and evidence matrix

**Reference file only. Not part of any submission.** Written 30 Oct 2026 to support `initial-draft-2`.
Nothing here may be copied into the paper without (1) the PDF being in `research/pdfs/` and (2) the claim being
checked against that PDF. Verification level is marked on every source:

- **R** = read directly from a local PDF in this project
- **P** = partially read (named sections only)
- **S** = summary only, obtained through a web reader during this sprint; *not* verified against the original
- **—** = identified but not examined

---

## 0. Was the supplied "research prompt" useful?

**Verdict: partly.** It bundles six separate role-play prompts. Four contain a useful idea; the wording around them
mostly adds noise. What was kept and what was dropped:

| Prompt block | Useful idea kept | Problems |
|---|---|---|
| "Asymmetric-Yield Literature Bottleneck Scout" | Gap analysis; look for outdated assumptions; verification of claims | "Map the complete landscape from the ground up" and "rapid" contradict each other; no scope, sources or output format |
| "Premium academic information architect" | Concept matrix: definitions, methodological discrepancies, quantitative anchors | "Eliminate qualitative filler" would delete the caveats that make numbers interpretable |
| "Humanized-Velocity Analogy Engine" | Plain-language explanations for writing and viva | Not research; analogies can mislead if presented as evidence |
| "Elite peer reviewer" two-step | Steel-man counterargument, then synthesis | Good as written; kept almost unchanged (§5) |
| "Investigative research auditor" | Source-credibility audit matrix | Overlaps with block 1; merged into §6 |
| "Pipeline operations auditor" | Honest retrospective of the sprint | Metrics like "[Logical Discrepancies Caught %]" have no denominator and cannot be measured; replaced by a list of actual discrepancies found (§8) |

General flaws: persona inflation ("elite", "premium", "master") does not change output quality; six tasks in one
message dilute each; no source constraints (e.g. "only sources I can archive locally"), no length or format target,
and inconsistent placeholder syntax (`[Source Papers Filtered]` vs prose instructions).

**Suggested replacement prompt** (one task at a time works better):

> For my ELL305 term paper on chiplets and 3D-stacked cache in AMD Zen processors, (1) list the main research
> strands with 2–4 key sources each, marking each source as peer-reviewed, vendor, independent measurement or
> preprint; (2) identify the three most important evidence gaps relevant to my research question, saying what
> evidence is missing and why it matters; (3) build a table of quantitative claims with source, conditions and
> whether it is vendor-reported; (4) write the strongest counterargument to my thesis and a synthesis.
> Only use sources I can save as PDFs. Mark anything you have not verified against the original.

---

## 1. Landscape map

| Strand | Key sources | Type | Level | In `research/pdfs/`? |
|---|---|---|---|---|
| **A. Monolithic limits and yield** | Murphy 1964 (Proc. IEEE) | peer-reviewed | P | yes |
| | Dong & Xie 2009 (ASP-DAC), 3D-IC cost model | peer-reviewed | P | yes |
| | Stow et al. 2016/2017 (ICCAD), 2.5D/3D cost; Feng & Ma "Chiplet Actuary" (2022, arXiv 2203.12268 / DAC'22) | peer-reviewed / preprint | S | no |
| **B. Chiplet architecture and interconnect** | Naffziger et al. 2020 (ISSCC), Rome/Matisse | peer-reviewed, vendor-authored | R | yes |
| | Suggs et al. 2019 (Hot Chips), Zen 2 | vendor slides | P | yes |
| | AMD EPYC 7003 overview (pub. 57075); AMD EPYC 9004 overview (pub. 58015, rev 1.3, Jun 2023) | vendor docs | P / S | 7003 yes; 9004 **no** |
| | Liu, Li, Yin 2024, "Review of chiplet-based design", *Sci. China Inf. Sci.* 67:200401, doi 10.1007/s11432-023-3926-8 | peer-reviewed survey | S (abstract) | no |
| | UCIe introduction, ACM (doi 10.1145/3819235) | peer-reviewed / consortium | — | no |
| **C. 3D integration and stacked cache** | Wuu et al. 2022 ISSCC slides (36) | vendor slides | R | yes |
| | Swaminathan 2021 (Hot Chips 33) | vendor slides | P | yes |
| | Black et al. 2006, "Die Stacking (3D) Microarchitecture", MICRO-39 | peer-reviewed | S | no |
| | AMD IMAPS 2024 (Alam et al., "2nd Generation 3D V-Cache Enablement", Zen 4) and IMAPS 2025 (Lambert, Zen 5 cache-below-CCD) | vendor slides | S | no |
| | AMD press release, Ryzen 7 9800X3D (Oct 2024) | vendor PR | S | no |
| **D. Alternative LLC technologies** | Mittal & Vetter 2016 (TPDS), DRAM caches | peer-reviewed survey | P | yes |
| | Kim et al. 2022 (Electronics), SRAM/STT-RAM hybrid | peer-reviewed | P | yes |
| **E. Independent evaluation of V-Cache** | Domke, Vatai et al. 2023, "At the Locus of Performance", *ACM TACO*, doi 10.1145/3629520 (arXiv 2204.02235) | peer-reviewed | S | no |
| | Lawenda et al. 2025, L3 size and CFD on EPYC (arXiv 2505.17934) | preprint | S | no |
| | Reguly 2023, PMBS'23 (arXiv 2309.09084), includes Milan-X | peer-reviewed workshop | S | no |
| | Chips and Cheese: Milan-X latency (Jan 2022), Zen 3 V-Cache deep dive (Jan 2022), 7950X3D (Apr 2023), 9800X3D (Nov 2024) | independent technical press | S | no |
| | Phoronix: EPYC 7773X vs 7763 (Mar 2022); 5800X3D vs 5800X, 420 tests (Sep 2022) | independent press | S | no |
| | AnandTech: Zen 3 deep dive, core-to-core and L3 latency (Nov 2020) | independent press | S | no |
| **F. Systems software** | Chips and Cheese 7950X3D (scheduling across asymmetric CCDs); hwcooling.net 7000X3D | independent press | S | no |
| **G. Thermal** | Black et al. 2006; MDPI 2025 hybrid-bonding HBM thermal review (doi 10.3390/electronics14132682) | peer-reviewed | S / — | no |

---

## 2. Three biggest gaps (relevant to the paper's research question)

### Gap 1 — No independent, clock-controlled isolation of the stacked-cache effect across many workloads
- **What exists:** AMD's comparisons change cores or clocks along with cache (5800X3D vs 12-core 5900X; Milan-X vs
  high-frequency 73F3). Phoronix compares parts with different clocks. Lawenda et al. compare Milan vs Milan-X with
  different base clocks (2.45 vs 2.20 GHz) and no frequency locking. Domke et al.'s Milan-X pilot is limited to a few
  applications; its broad results are simulations (gem5) of hypothetical caches, not V-Cache.
- **Partial exceptions:** AMD's Hot Chips 33 fixed-frequency prototype test (vendor, six games); Chips and Cheese
  normalising Milan-X results to clock (gem5 +7.6% raw, ~12.5% clock-normalised) and measuring IPC and L3 hit rate per
  CCD on the 7950X3D (IPC +4.9% to +19%, one title slightly negative).
- **Why it matters:** the paper's RQ4 asks how to separate cache effects from frequency and core count. The best
  available method is *performance-counter evidence* (hit rate and IPC per CCD), not end-to-end time.
- **Opportunity:** build Part V around IPC and hit-rate evidence where available, and grade every end-to-end
  comparison with the confound table.

### Gap 2 — Thermal behaviour of hybrid-bonded SRAM-on-logic is publicly under-documented
- **What exists:** the main academic thermal result is Black et al. 2006 (stacked 8 MB SRAM: peak +4.5 °C vs
  +0.08 °C for 32 MB stacked DRAM), on a micro-bump-era, Core 2-class design. AMD gives qualitative claims
  ("superior thermal conductance", structural silicon for heat).
- **Indirect evidence the penalty was real:** V-Cache CCDs clock lower (7950X3D V-Cache CCD ~7% lower; 4.8 vs
  5.15 GHz all-core, per Chips and Cheese) and early parts were voltage-limited; AMD later moved the cache die *below*
  the CCD (9800X3D) explicitly to put the cores closer to the cooler (AMD press release).
- **Outdated assumption:** using 2006 thermal numbers for 2022 hybrid-bonded stacks.
- **Opportunity:** treat the first-to-second-generation flip as a natural experiment and present the thermal argument
  from it, clearly labelled as inference from vendor and press evidence.

### Gap 3 — Cost models predate hybrid bonding and do not model "cache die on a compute chiplet"
- **What exists:** Murphy 1964 yield functions; Dong & Xie 2009 at 90–45 nm with an assumed 99% per-step bonding yield;
  Stow et al. and Chiplet Actuary (2022) for 2.5D and multi-chip but not hybrid-bonded SRAM stacking.
- **Outdated assumptions:** defect densities, wafer costs and bonding yields from old nodes; no known-good-die
  economics for chip-on-wafer hybrid bonding.
- **Opportunity:** keep the paper's cost analysis explicitly illustrative (as it is), state these limits in Part VI,
  and list "a public cost model for stacked-cache chiplets" as an open question.

### Methodological weaknesses seen across the literature
1. Vendor numbers reported as averages that hide spread (AMD gaming: tie to 1.36×).
2. Peak vs effective bandwidth mixed (AMD "doubled" L3 bandwidth vs ~25% more bytes/cycle measured single-threaded by Chips and Cheese).
3. Different generations compared as if one variable changed.
4. Inconsistent naming across AMD's own talks ("2nd generation V-Cache" = Zen 4 in IMAPS 2024, Zen 5 cache-below design in IMAPS 2025 and the 9800X3D press release).
5. Heavy reliance on non-archival web reviews whose pages change (Chips and Cheese metadata shows later modification dates).

### Overlooked opportunities that fit this paper
- **Asymmetric-cache scheduling:** 7950X3D has one V-Cache CCD and one faster CCD; by default AMD places regular applications on the higher-clocked CCD (Chips and Cheese). A short subsection in Part VI on OS/runtime placement would be novel for a course paper.
- **The per-CCD cache boundary:** cross-CCD core-to-core latency 79–80 ns vs 15–19 ns within a Zen 3 CCD (AnandTech, 5950X). This quantifies the chiplet latency cost that the draft currently only argues qualitatively.
- **Why SRAM, not stacked DRAM:** Black et al. show stacked DRAM is thermally gentler and denser; AMD chose SRAM for latency. A clean comparison for Part VI.

---

## 3. Concept matrix

### 3a. Primary definitional axioms (statements the paper relies on)
| # | Axiom | Source (level) |
|---|---|---|
| A1 | Performance ∝ IPC × f / instructions | Sarangi §10.9.1 (R) |
| A2 | AMAT = hit time + miss rate × miss penalty, recursively | Sarangi §11.3.1 (R) |
| A3 | A larger cache removes capacity misses only | Sarangi §11.3.2 (R) |
| A4 | Larger cache ⇒ higher latency, power, area | Sarangi Table 11.2 (R) |
| A5 | Die yield falls with area; averaging over defect-density spread gives Murphy forms | Murphy 1964 Eqs 9–11 (R) |
| A6 | Private caches are fast but need coherence; shared caches are large and slow | Sarangi Table 12.3 (R) |
| A7 | Analog/IO scale worst, SRAM now scales worse than logic | Naffziger 2020 (R); Wuu slides 6 (R) |

### 3b. High-contrast methodological discrepancies
| Topic | Position A | Position B | Resolution in paper |
|---|---|---|---|
| Yield model | Dong & Xie use Murphy's rectangular form | Murphy prefers the triangular form | Keep rectangular, state difference (<1 pp at example yields) — done |
| V-Cache gain | AMD: ~15% gaming (vs 12-core part) | Fixed-frequency prototype; IPC-based measurements show 5–19% depending on title | Report as range, grade confounds |
| L3 bandwidth gain | AMD: >2 TB/s, "doubling" | Measured single-thread ~+25% bytes/cycle (Chips and Cheese) | Treat AMD figure as peak capability |
| Thermal impact | AMD: superior thermal conductance | Lower clocks and later cache-below redesign | Present both; label inference |
| "2nd gen" | IMAPS 2024: Zen 4 stack | IMAPS 2025 / 9800X3D: cache below | Name designs by product, not generation |

### 3c. Quantifiable metric anchors
| Metric | Value | Conditions | Source | Type | Level |
|---|---|---|---|---|---|
| Added L3 latency with V-Cache | +4 cycles | Zen 3 | Wuu slides 20 | vendor | R |
| ″ | ≈ +3–4 cycles | Milan-X vs Milan | Chips and Cheese, Jan 2022 | independent | S |
| ″ | ≈ +4 cycles, +1.61 ns | 7950X3D | Chips and Cheese, Apr 2023 | independent | S |
| ″ | +4 cycles | 9800X3D (cache below) | Chips and Cheese, Nov 2024 | independent | S |
| Zen 3 L3 latency | 46 cycles (AMD); ≈51 cycles measured at 4 MB | 5950X | AnandTech, Nov 2020 | independent | S |
| Core-to-core latency | 15–19 ns within CCD; 79–80 ns across CCDs | 5950X | AnandTech | independent | S |
| CCD–IOD link | ~55 GB/s; round trip < 9 ns | Rome, FCLK 1.46 GHz | Naffziger 2020 | vendor/peer-rev. | R |
| Hybrid bond pitch | 9 µm vs 36–50 µm micro-bump | AMD analysis | Swaminathan 2021; Wuu 16 | vendor | R |
| L3 per CCD / socket | 96 MB; 768 MB (8 CCD) | Milan-X | AMD 57075 | vendor | R |
| ″ | 96 MB; 1152 MB (12 CCD), 12 × DDR5-4800 | Genoa(-X) | AMD 58015 | vendor | S |
| OpenFOAM speedup | up to 1.54× (motorBike), 1.47× (UAP) | Milan-X vs Milan, 64 cores, unlocked clocks | Lawenda 2025 | preprint | S |
| L3 miss-rate reduction | up to ~30 percentage points | same | Lawenda 2025 | preprint | S |
| MiniFE speedup | up to 3.4× for some sizes | 7773X vs 7763 | Domke 2023 (TACO) | peer-reviewed | S |
| IPC gain on V-Cache CCD | +4.9% (x264) to +19% (COD); slight loss (DCS) | 7950X3D, per-CCD counters | Chips and Cheese 2023 | independent | S |
| Stacked-SRAM thermal | +4.5 °C peak (8 MB SRAM); +0.08 °C (32 MB DRAM) | 2006 simulation | Black et al. 2006 | peer-reviewed | S |
| 3D cost break-even | ~250 mm² (2-layer) | 2009 nodes | Dong & Xie | peer-reviewed | R |

---

## 4. Plain-language explanations (writing and viva aids — not evidence)

- **Yield and chiplets:** cutting tiles from a sheet of glass with random bubbles. One big tile almost always contains a bubble; many small tiles mostly don't, and you throw away only the bad ones.
- **I/O die:** a hub airport. Every CCD flies to the hub, which handles all connections to memory and I/O; two CCDs talk via the hub, so the trip is longer than within one CCD (≈80 ns vs ≈17 ns).
- **AMAT:** a commute. Most trips are short (cache hits), a few are long (memory). A bigger cache turns some long trips into short ones; V-Cache makes every short trip about four cycles longer.
- **V-Cache:** adding a mezzanine floor to a warehouse. Much more storage on the same footprint, reached by many short staircases (TSVs), but heat from the work floor must now rise through the mezzanine — which is why AMD later put the storage *below* the work floor.
- **Working-set sensitivity:** a desk vs a filing room. If your papers already fit on the desk, a bigger desk does nothing; if they fit only on the bigger desk, you stop walking to the filing room.

---

## 5. Pressure test of the thesis

**Thesis (paper):** chiplet organisation and 3D-stacked cache help AMD Zen processors overcome monolithic scaling
limits, each with its own trade-offs.

**Step 1 — strongest counterargument**
1. *Latency:* chiplets replace on-die wires with package links; cross-CCD communication costs ~80 ns vs ~17 ns within a CCD. For workloads with fine-grained sharing, a monolithic die is simply faster.
2. *Narrow benefit:* stacked cache helps only workloads whose working set falls in a window (≈32–96 MB per CCD); results range from slight loss to 1.36× in AMD's own data, and independent IPC measurements show single-digit gains for some code.
3. *Clock penalty:* V-Cache parts clock lower; for cache-insensitive work they are slower, so the "cost" is not only money.
4. *Thermal limits:* the first design's thermal penalty was large enough that AMD inverted the stack in the next design.
5. *Evidence base:* most quantitative claims are vendor-reported, and the independent academic evidence is small (one TACO paper, one preprint).
6. *Cost:* the cost advantage of chiplets is shown only by old or illustrative models; at low volume a monolithic die can be cheaper (Chiplet Actuary, summary only).

**Step 2 — synthesis**
- *Strong:* chiplets solve die-size and yield limits for high-core-count parts (64 cores beyond the reticle limit, per AMD; yield arithmetic is robust).
- *Strong but bounded:* stacked cache delivers large gains for working sets between the base and stacked capacity (CFD, EDA, some games), with small, measured latency cost (+4 cycles, independently confirmed).
- *Hidden assumptions:* workload mix; that frequency loss is small; that bonding yield and cost are acceptable at volume.
- *Validation gaps:* clock-controlled independent studies; thermal data; current cost models.
- *Most defensible conclusion:* chiplets are a general solution to *scaling and cost*; stacked cache is a *workload-specific* solution to *capacity*, whose value must be argued per workload class. The paper should phrase RQ answers this way.

---

## 6. Source-credibility audit matrix

**Tiers**
- T1 peer-reviewed archival paper (check: venue, method, data availability)
- T2 vendor technical document or conference slides (check: conflict of interest, test endnotes, what is held constant)
- T3 independent technical measurement with stated method (check: hardware listed, clocks, repeatability, page permanence)
- T4 preprint (check: method; treat as T3 until published)
- T5 news, forum, aggregator — **not cited**

**Checks applied to every claim before it enters the paper**
1. Is the original in `research/pdfs/`? (project rule)
2. Who measured it, and do they sell the product?
3. What was held constant (clock, cores, memory, software)?
4. Is it peak or measured, single- or multi-threaded?
5. Does another tier confirm it? (e.g. +4 cycles: T2 confirmed by T3 three times)
6. Is the page archival? If not, save a dated PDF.

| Source | Tier | Conflict of interest | Method stated | Confirmed elsewhere | Use |
|---|---|---|---|---|---|
| Wuu et al. slides | T2 | AMD | endnotes | latency yes (C&C) | structure, latency; performance as vendor claim |
| Naffziger 2020 | T1 (vendor-authored) | AMD | partial | — | architecture facts |
| AMD 57075 / 58015 | T2 | AMD | n/a | — | configuration facts |
| Domke 2023 TACO | T1 | none | yes | — | HPC sensitivity |
| Lawenda 2025 | T4 | none | yes; clocks not locked | partially (Phoronix direction) | CFD sensitivity, with confound note |
| Black 2006 | T1 (Intel-authored) | low | simulation | — | historical thermal baseline |
| Chips and Cheese | T3 | samples from AMD (stated) | yes | latency matches AMD | latency, IPC, clocks |
| AnandTech 2020 | T3 | none stated | yes | — | core-to-core latency |
| Phoronix | T3 | none stated | partial | — | breadth of workloads |

---

## 7. Download list (save as PDF into `research/pdfs/`; web pages via Print → Save as PDF)

| Priority | Source | Link | Save as |
|---|---|---|---|
| 1 | Domke, Vatai et al., ACM TACO 2023 | https://dl.acm.org/doi/full/10.1145/3629520 (or arXiv: https://arxiv.org/pdf/2204.02235) | `Domke-Vatai-3D-Stacked-Cache-HPC-TACO-2023.pdf` |
| 1 | Lawenda et al. 2025 (preprint) | https://arxiv.org/pdf/2505.17934 | `Lawenda-L3-Size-CFD-EPYC-arXiv-2025.pdf` |
| 1 | Chips and Cheese, Zen 3 V-Cache deep dive | https://chipsandcheese.com/p/deep-diving-zen-3-v-cache | `ChipsAndCheese-Zen3-VCache-Deep-Dive-2022.pdf` |
| 1 | Chips and Cheese, V-Cache latency teaser | https://chipsandcheese.com/p/amds-v-cache-tested-the-latency-teaser | `ChipsAndCheese-VCache-Latency-2022.pdf` |
| 1 | Chips and Cheese, 7950X3D | https://chipsandcheese.com/p/amds-7950x3d-zen-4-gets-vcache | `ChipsAndCheese-7950X3D-2023.pdf` |
| 1 | Chips and Cheese, 9800X3D | https://chipsandcheese.com/p/amds-9800x3d-2nd-generation-v-cache | `ChipsAndCheese-9800X3D-2024.pdf` |
| 1 | AnandTech, Zen 3 deep dive (core-to-core page) | https://at-web1.www.anandtech.com/show/16214/amd-zen-3-ryzen-deep-dive-review-5950x-5900x-5800x-and-5700x-tested/5 | `AnandTech-Zen3-Core-to-Core-Latency-2020.pdf` |
| 2 | Phoronix, EPYC 7773X vs 7763 | https://www.phoronix.com/review/amd-epyc-7773x-linux | `Phoronix-EPYC-7773X-MilanX-2022.pdf` |
| 2 | Phoronix, 5800X3D vs 5800X (Linux 6.0) | https://www.phoronix.com/review/amd-5800x3d-linux6 | `Phoronix-5800X3D-vs-5800X-2022.pdf` |
| 2 | Black et al. 2006, MICRO | https://courses.grainger.illinois.edu/CS534/fa2021/reading_list/13a.pdf | `Black-Die-Stacking-3D-Microarchitecture-MICRO-2006.pdf` |
| 2 | Reguly 2023, PMBS | https://arxiv.org/pdf/2309.09084 | `Reguly-Bandwidth-Bound-Apps-PMBS-2023.pdf` |
| — | **Later X3D (AMD primary)** | | |
| 1 | AMD EPYC 9004 Architecture Overview (58015) | https://www.amd.com/content/dam/amd/en/documents/epyc-technical-docs/tuning-guides/58015-epyc-9004-tg-architecture-overview.pdf | `AMD-EPYC-9004-Architecture-Overview-58015.pdf` |
| 1 | AMD IMAPS 2024, 2nd-gen V-Cache (Zen 4) | https://imapsource.org/api/v1/articles/129075-2nd-generation-3d-v-cache-tm-enablement.pdf | `AMD-IMAPS-2024-2nd-Gen-VCache-Zen4.pdf` |
| 1 | AMD IMAPS 2025, Lambert (Zen 5 cache below CCD) | https://imapsource.org/article/147811.pdf | `AMD-IMAPS-2025-Heterogeneous-Integration-Lambert.pdf` |
| 1 | AMD press release, Ryzen 7 9800X3D | https://ir.amd.com/news-events/press-releases/detail/1225/the-gaming-legend-continues-amd-introduces-next-generation-amd-ryzen-7-9800x3d-processor | `AMD-PR-Ryzen-7-9800X3D-2024.pdf` |
| 3 | Liu, Li, Yin 2024 chiplet review (Sci. China) | https://link.springer.com/article/10.1007/s11432-023-3926-8 (via IIT Delhi) | `Liu-Li-Yin-Chiplet-Review-SciChina-2024.pdf` |
| 3 | Chiplet Actuary (DAC 2022 / arXiv) | https://arxiv.org/pdf/2203.12268 | `Feng-Ma-Chiplet-Actuary-2022.pdf` |

---

## 8. Sprint retrospective (instead of the prompt's unmeasurable metrics)

- **Sources examined this sprint:** ~20 (11 already local; 9 new via web reader, all marked S).
- **Discrepancies actually caught so far in the project:**
  1. Dong & Xie's yield form is Murphy's *rectangular* case, which Murphy called inappropriate.
  2. "Barriers to large on-die caches" was a section heading, not an article title.
  3. The SRAM-leakage claim needed checking between two Mittal surveys (confirmed in TPDS 2016).
  4. AMD's headline gaming and server comparisons both change a second variable (cores or clock).
  5. AMD uses "2nd generation V-Cache" for two different designs.
  6. AMD's L3 bandwidth claim vs ~25% measured single-thread gain.
  7. Black et al. state 50% and 55% for the same peak reduction.
  8. Domke et al.'s hardware table lists inconsistent memory configurations.
- **Bottleneck:** many independent sources are web pages that the workspace cannot download; they need saving by hand and become stale. Prefer TACO/arXiv versions where they exist.
- **Next sprint:** once PDFs are saved, re-read each S item, upgrade its level, and only then cite.

## 9. Update, 30 October 2026

All sources marked S in sections 1 and 3 that are now in `research/pdfs/` (see its README) have been read against the original and are effectively level R. Corrections found on reading: Milan-X single-thread L3 bandwidth rose about 25% per cycle, not AMD's doubling; Lam's 7950X3D per-CCD tests were run with both CCDs fixed at 4.2 GHz, which partly fills Gap 1 (for five workloads only); "2nd generation V-Cache" means Zen 4 in IMAPS 2024 but Zen 5 in the 2024 press release and IMAPS 2025, so the draft names products instead. AnandTech's cross-CCD latency figures stay unverified (no local PDF) and the EPYC 9004 overview was replaced by the 4th Gen EPYC white paper and datasheet.
