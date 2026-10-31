---
draft: initial-draft-2
created: 2026-10-30
status: working draft (not a course milestone)
---

# initial-draft-2 — overview

Copied from `draft-initial/` on 30 Oct 2026 at Ishan's request ("add onto initial-draft, don't start from scratch").
`draft-initial/` and its PDF are kept unchanged. Six-part outline and Option A method as before
(see [[Drafts/draft-initial/00 Draft Overview]]).

## Build

`scripts/build-linux.sh all --initial-draft-2 --install` (Linux) or `scripts\build.ps1 -Target initial-draft-2` (Windows, untested).
30 Oct 2026: 50 pages, 0 errors, 0 warnings, no overfull boxes, biber clean → `build/pdf/ELL305-initial-draft-2.pdf`.
New pages rendered and inspected.

## What was added (all from PDFs in the project)

| Where | Content | Sources |
|---|---|---|
| Part II §2.2 | Baseline SimpleRisc organisation, data/control path | Sarangi 9.2–9.9 |
| Part II §3.1 | Pipelining, hazards, CPI-with-stalls equation, optimal depth, out-of-order limits | Sarangi 10.4, 10.9.3, 10.11.4, 10.12.1 |
| Part II §4.4 | Cache organisation, replacement, write policies; Table of optimisations (larger cache → latency, power, area) | Sarangi 11.2.2–11.2.5, Table 11.2; ISSCC slides 19–20 |
| Part II §5.2 | Shared vs private caches (Table), banking, snooping/directory, Zen per-CCD L3 as NUMA | Sarangi 12.4.4–12.4.6, Table 12.3; EPYC 7003 doc |
| Part II §5.3 | NoC, bisection bandwidth, diameter, topology table; star of CCDs around IOD | Sarangi 12.6; Naffziger 2020 |
| Part III §7, §8.1–8.2, §9, §10 | Rome/Matisse packaging; latency, bandwidth (~55 vs ~205 GB/s) and link-power (≈0.9 W, illustrative) analysis; scalability; 8×74 mm² vs 592 mm² yield-cost example (44% / 63%); Part summary | Naffziger 2020; EPYC 7003; Dong & Xie; Appendix C model |
| Part IV §14.2, §17, §18 | Why interconnect density matters; workload classes by working set; Part summary | ISSCC slides 15, 20, 26, 29, 31; Mittal & Vetter |
| Part V §21, §24 | Source-selection rules; confound grid table | slides 29, 31, 35; Swaminathan 2021; Suggs 2019 |
| Part VI §27, §28 | Chiplet–stacked-cache interactions; workload map and remaining bottlenecks; DRAM/STT-RAM alternatives | slides 6, 10, 17; Mittal & Vetter; Kim 2022 |

## Estimates that are the paper's own (flagged in text as illustrative)

- 205 GB/s for 8 × DDR4-3200 assumes standard 64-bit channels (not stated in the EPYC doc).
- ≈0.9 W per link uses the *Zeppelin* 2 pJ/bit with *Rome* 55 GB/s.
- Chiplet cost example ignores interfaces, packaging, assembly yield and test.
- 300-cycle memory latency in Part IV is hypothetical (TODO marker).

## Still open

Independent benchmarks (Part V), thermal/frequency limits of X3D parts, later Zen X3D generations,
Part V configuration table (AMD product docs), conclusions, plagiarism/readability evidence, ChipScale 2022 PDF,
Hot Chips 33 prototype details for the confound table.

## Update 30 Oct 2026, afternoon

- New TikZ figures: `figures/vcache-stack.tex` (Part IV §14.1, numbered key; from Wuu slides 10–12, 14, 16–17 and
  EPYC 7003) and `figures/epyc-package.tex` (Part III §7; 8 CCDs, IOD, NPS=4 quadrants; Naffziger 2020, EPYC 7003).
  Both checked visually at full size and in the draft.
- Part II §4.4: Wang 2019 added as a brief example (data layout instead of capacity).
- Bibliography tidied in `preamble.tex` for this draft only: URL dropped when a DOI exists; access dates, ISSN,
  ISBN and journal editors removed; AMD report number shown as "Publication 57075"; article numbers shown as
  "Art. no."; "V-Cache" kept capitalised. Draft 1 untouched.
- Build: 52 pages, 0 errors/warnings, biber clean.
- Research reference file: `research/research-landscape.md` (not for submission).

## Update, 30 Oct 2026 (afternoon, later)
- Independent evidence added to Parts IV–VI; new tables (later X3D generations, configuration pairs, independent measurements); confound grid extended.
- New figure: first-generation vs inverted (Zen 5) V-Cache stack (Lambert IMAPS 2025 slide 7).
- From Sarangi: thermal-resistance model and hot spots (10.10.1, 10.10.4), ED² metric (10.10.5), SRAM/DRAM arrays (7.4.1, Table 11.1), 100–300-cycle memory stall (12.4.8) replacing the illustrative 300 cycles.
- Contributions list finalised. Memory-hierarchy figure labels un-overlapped.
- Remaining: Zen 5 CCD node / 96 MB check; die-thinning/test planned box; Appendices A and B.

## Update, 31 Oct 2026 (evening): Part IV expansion
- Part IV grown from ~9 to ~17 pages. New: working-set figure; worked example on pad density (eq. pad-density, bar chart); hybrid-bond process (IMAPS 2024 slide 9) with bond-interface figure (Wuu slide 16); worked example applying eq. vcache-tradeoff to Lam's libx264 data; "Inside the cache interface" (TSV columns, macros, tag overhead ~51 bits/line, 96 MB = 3×2^15 sets open question, 2 TB/s reconstruction, simple digital interface) with floorplan figure; thermal worked example with Sarangi's model; power delivery (slides 23–25); manufacturing subsection (D2W vs W2W, Dong & Xie Eqs 16–17, stack-yield worked example table, reliability, co-design); Lam IPC bar chart; expanded summary.
- Also from Zen 2 vs Zen 3 work: §19.1 with AMD 19% IPC footnote, TechSpot results, FPS Review AIDA64 (L3 9.9→10.9 ns).

## Update, 31 Oct 2026 (night): Parts II and III
- Part II: package heat-path figure + Sarangi temperature scale (10.10.1); SRAM cell/array figure (7.4.1); AMAT worked example on 3700X/5800X with FPS Review AIDA64 latencies (assumed miss rates 5/30/40%); set-associative lookup figure; Zen 3 address-split table (48-bit PA assumed).
- Part III: IFOP circuit details and package layers (Naffziger text); Naples vs Rome NUMA latency table (Naffziger Fig 2.2.6); link-vs-memory bandwidth balance table; AMD packaging timeline figure (Lambert slide 5); dies-per-wafer worked example (Dong & Xie Eq 14) — 95 vs 35 64-core sets per wafer; AMD cost chart redrawn (values read by eye from Naffziger Fig 2.2.2, ±0.05). Note: Naffziger Fig 2.2.1 prints "8.34 Billion FETs" for both CCD and server IOD (apparent error) — not cited; chart legend says 14 nm while text says 12 nm (flagged in draft).

## Update, 31 Oct 2026 (late): assumptions resolved + Part V
- §15.1 libx264 example now uses Lam's chart values (hit rate 61.55→71.86%, IPC 1.36→1.43); the article text's 72.8% is a typo vs its chart. IPC assumption removed; implied effective miss penalty ≈130 cycles.
- D2W/W2W paragraph now relies on Dong & Xie's text and AMD slide text, not our reading of colours.
- Part V new: Milan vs Milan-X latency sweep figure (C&C teaser: L3 47.49→51.14 cycles; memory 342 vs 313 cycles); MiniFE sweep figure (Domke Fig 1, read by eye) with inferred ~300 B/grid point; OpenFOAM detail (Lawenda Tables 5–6: 0.81–1.54×, clocks 2.9–3.2 vs 2.8–3.0 GHz); Phoronix distribution (106 vs 244 wins, our colour classification); clock-correction worked example table.
- Remaining assumptions: 48-bit physical address (check with `grep "address sizes" /proc/cpuinfo` on the 5600X under WSL, or AMD's Zen 3 PPR); 4 GHz L3 clock in the 2 TB/s check; AMAT miss rates 5/30/40%.

## Update, 31 Oct 2026 (night): Part I + measurement kit
- Part I: "How processors used to scale" (Sarangi 12.1.1–12.1.2; 32–64-core prediction vs 64-core Rome on chiplets); Zen timeline figure; "one die or eight?" thought-experiment table with cross-references; RQ reading-guide table; methodology paragraph on worked examples and source grading.
- tools/measurements/: latency.c (pointer-chase sweep, tested) and README with WSL and AMD uProf steps for the 5600X. If data is collected, Part I methodology and contributions must be updated (they currently say "no new measurements").

## Update, 31 Oct 2026 (night): Part VI
- Three-way table de-provisionalised, quantitative rows added. New §"Other ways to enlarge the LLC" with table (planar SRAM, V-Cache, Broadwell eDRAM L4 via Lam, Black stacked DRAM, Kim STT-RAM Table 1) and the Broadwell side-by-side example. Decision-sequence figure; cache-vs-clock worked example on Lam's 7950X3D data; Black logic-on-logic numbers in future directions; open question refined. Part IV open detail now cites Lam's inference on slice-to-extension interfaces.

## Update, 31 Oct 2026 (late night): Part II deepened
- Optimal pipeline depth worked example (Sarangi Eq 10.11, Example 142: ~13 stages); Amdahl's law subsection + figure (5%: 5.9/9.1/15.4, limit 20) and loosely-coupled point; coherence axioms + write-update vs write-invalidate; MSI state-diagram figure; two-core MSI worked trace table; directory bit-vector overhead worked example (1.6%/12.5%/25%); topology worked table for N=8 and 64; topologies figure (ring, mesh, IOD star); C&C ring-vs-mesh L3 latency point. Part V §19.1: Cozma 7–8 cycle unification cost added.

## Update, 31 Oct 2026 (late night): Part III deepened
- EPYC 7003 overview read in full: new §7.1 "Inside the I/O die" (GMI links, 8 UMCs, 2 DPC, 4 TB, 128 PCIe lanes, FCLK=MEMCLK 1600 MHz, 4/6/8-channel, IOD labelled 14 nm vs Naffziger 12 nm — flagged), NPS modes table + worked bandwidth/locality example, LLC-as-NUMA; dual-socket xGMI lane budget (128 vs 160 lanes).
- Suggs HC31 slides read (4, 12, 13, 15, 19): 2× perf/energy = 1.15×1.17×1.47 worked example; Zen 2 CCX (4×4 MB slices, 512 KB L2, 32 B/cycle); AMD's challenge/solution list; ~1000 mm² Rome = 8×74+416 = 1008 mm² check; Rome 204.8 GB/s now cited from Suggs; Matisse 51.2 GB/s → 3.2 GB/s per core, same as 64-core Rome.

## Update, 1 November 2026 — Part VI expanded (91 → 97 pages)
- New cache–clock model (eq:cache-clock-model, tab:cache-clock-model, fig:cache-clock-model): memory stall fixed in ns, calibrated on Lam's libx264 data; break-even 0.12 / 0.35 / 0.50 MPKI removed (equal clocks / measured 4.8 vs 5.15 GHz / linear rule). Clocks are Lam's all-core L3-load values, labelled as an assumption.
- New sec:bandwidth-wall with tab:per-core-resources (Milan, Milan-X, Genoa, Genoa-X) and Reguly 2023 (now cited): STREAM 310 GB/s, cache:memory bandwidth 14x, tiling 4x on Milan-X; HBM row added to tab:llc-alternatives.
- New sec:evidence-strength (tab:evidence-strength), sec:case-against (five objections), Limitations rewritten as Threats to Validity (label kept: sec:limitations), new sec:implications.
- Conclusions RQ4 and open questions extended.

## Update, 1 November 2026 — five new figures (97 → 102 pages)
- Part III: fig:l3-miss-path (L3-miss path with Rome/5800X timings), fig:bandwidth-balance (link vs memory bandwidth, crossover ≈3.7 CCDs).
- Part IV: fig:libx264-waterfall (735 → −52 → +15 → 699 cycles; caption notes the 130-cycle stall is inferred from the same measurement), fig:stack-process (extra steps for a stacked CCD; D2W vs W2W branch; order marked indicative).
- Part V: fig:openfoam-sweep (Milan-X/Milan by mesh, read from Lawenda Fig. 4 labels; xhigh 1.22× in figure vs 1.24× in text noted; small meshes shaded, min 0.81× from Table 6).
- Four more figures (102 → 105 pages): fig:numa-latency and fig:nps-modes (Part III), fig:zen2-zen3-latency and fig:clock-correction (Part V). All plot values already in the paper's tables.

## Pending — 5600X measurements (Ishan has access from 4 November 2026)
- Run `tools/measurements/` kit (latency.c sweep with and without `--huge`; AMD uProf L3 miss rates) on the Ryzen 5 5600X; save outputs to `research/measurements/`.
- Then update wording that assumes no hardware/measurements:
  - Part V §21 (sec:evidence-method): "the group does not have access to the relevant hardware".
  - Part I methodology/contributions: "no new measurements".
  - Part VI threats to validity: "No new measurements" paragraph.
- Use measured values to replace remaining labelled assumptions: AMAT miss rates 5/30/40% (tab:amat-example), 4 GHz clock in the 2 TB/s check (Part IV).
- If measurements are not taken, reword the Part V sentence to say no measurements were taken (not that hardware was unavailable).
- Four optional figures added (→ 106 pages): fig:two-socket (Part III), fig:vendor-vs-independent (Part V), fig:reguly-ratio and fig:thread-placement (Part VI; placement policy labelled as a proposal, not AMD's).
- Reminder scheduled for 4 Nov 2026, 09:00 IST about the 5600X measurements.

## Update, 1 November 2026 — Cezanne section, second review, Zotero import queue (→ 108 pages)
- Part III sec:cezanne (tab:cezanne-vermeer): Zen 3 with and without chiplets (TechSpot 5700G review, CapFrameX Cezanne article, 7-cpu, FPS Review).
- Second independent review (research/review-initial-draft-2-v2.md): G1–G20 all confirmed and applied; see research/review-initial-draft-2-v2-response.md.
- New source-import workflow: research/zotero-queue.json + scripts/zotero-import.js (one-line loader in research/zotero-queue.md).
