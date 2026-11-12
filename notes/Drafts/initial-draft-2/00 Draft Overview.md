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

## Update, 3 November 2026 — 13 mind maps (108 → 121 pages)
- Shared style `initial-draft-2/mindmap-style.tex` (TikZ mindmap library, `\mindmapfigure[width]{body}{caption}{label}`), loaded from `preamble.tex`.
- One overview map at the start of each part: fig:mindmap-foundations, -chiplets, -stacked, -case-study, -synthesis; whole-paper map fig:mindmap-paper (sec:organisation) and research-question map fig:mindmap-rq (after tab:rq-map).
- Topic maps: fig:mindmap-misses (after tab:cache-optimisations), fig:mindmap-chiplet-tradeoff (Summary of Part III), fig:mindmap-stack-costs (sec:thermal), fig:mindmap-confounds (sec:confounds), fig:mindmap-future (end of sec:future), fig:mindmap-implications (end of sec:implications).
- Maps only restate content already in the text; captions point to the sections that hold the sources.

## 3 November 2026 — Cache Hierarchy Lab (software model, Option B)
- `tools/cachesim/`: C++ trace-driven simulator (`src/cachesim.cpp`), browser GUI (`gui/index.html`, offline copy `gui/index-offline.html`), experiment runner (`run_experiments.py` → CSV/PNG), C++ vs JS cross-check (identical on 12 cases), self-test.
- Presets: zen2_2ccx (2×16 MB, 39 cyc), zen3_1ccx (32 MB, 47), vcache (96 MB, 51), planar96 (96 MB, 59 assumed), sidecar (32 MB + 64 MB L4), twoccd, mono16. Sources in tools/cachesim/README.md.
- 15 ready-made experiments (group plan Exp 1–5 plus 3D, cache-design and chiplet ones); every "what to look for" text checked against model output (test/experiments.js).
- Energy defaults are placeholders; IPC not modelled (no pipeline). Paper section on the model still to write once results are run on Ishan's machine.

## 5 November 2026 — third review applied (→ 122 pages)
- research/review-initial-draft-2-v3.md (H1–H24, W1–W18) and response file. New Appendix D (app:l3d-organisation). Abstract rewritten with findings.
- Open for Ishan: H18 (reviewer suggests keeping only 3–4 mind maps, leaf text ~5–6 pt) and whether to move the Cezanne detail to an appendix (H19).

## 5 November 2026 — mind-map text enlarged; content added per the third review (122 → 138 pages)
- Mind maps: all 13 kept (Ishan's decision on H18); text enlarged in `mindmap-style.tex` (root \normalsize, level 1 \footnotesize, level 2 \scriptsize, larger circles); chiplet-tradeoff map resized to fit. All 13 render-checked, no overlaps.
- Part II (+7 pp.): sec:writes-inclusion (write-through/write-back, write buffer, critical word first, inclusion; tab:op-sequence, write-traffic worked example, tab:inclusion-example), sec:virtual-memory (pages, page tables, TLB, MMU; tab:tlb-reach from 7-cpu and Chips and Cheese), sec:mlp (overlapping misses, eq:mlp-stall, what the 130-cycle saving implies, 7-cpu parallel TLB misses, multithreading and SMT), directory worked example (tab:directory-example).
- Part III (+4 pp.): sec:cross-ccd (Reguly core-to-core latency on Milan-X, tab:core-to-core: 58.6 ns same CCD vs ~265 ns across CCDs; shared-counter worked example); sec:power-flexibility with sec:chiplet-power (decoupled clocks, uncore DVFS, down-binning, one or two links per CCD; illustrative link-power bound ~2% of TDP) and sec:product-flexibility (tab:product-matrix from the Ryzen and EPYC 9004 datasheets; 9124 vs 9174F). Summary bullets updated.
- Part V (+4 pp.): sec:evidence-ledger (tab:evidence-ledger), sec:lam-detail (tab:lam-detail from Lam's charts; geometric mean +11.4% over five workloads, ≤ +9.4% with DCS; tab:lam-per-miss: ~50/80/130 cycles per removed miss; Call of Duty pipeline-slot breakdown; stock-clock bounds), sec:genoax (Genoa-X 0.98–1.60×, same 12 MB L3 per core as Milan-X, Genoa 64c beats Milan-X; Lawenda Table 5 row labels appear misprinted — flagged in text). fig:lam-ipc Call of Duty value now 19.7% from the chart.
- Part I: sec:related-work (Liu et al., Mittal–Vetter, Black, Dong–Xie, Domke) and sec:findings.
- Part VI: RQ2 answer cites the new sections; three rows added to tab:evidence-strength (cross-CCD sharing, product range, link power); table columns widened.
- Page counts now (PDF): I 21–28, II 29–51, III 52–72, IV 73–92, V 93–111, VI 112–129. Still under target: III (−4), V (−6), IV (−5).

## 5 November 2026 (evening) — further content after resuming (138 → 141 pages)
- Part IV: worked example "silicon across a product line" (tab:product-line-silicon: one planar die vs two planar dies vs one CCD with optional stack; plus the 7 nm cache die / 5 nm CCD node argument from AMD's cost-per-yielded-mm² chart, read approximately); "What the remaining deficit suggests" (Zen 5: equal 1.4 V limit yet 300 MHz ≈ 5.5% boost deficit, so voltage tolerance and support silicon explain less than half of the first-generation clock penalty). Part IV summary updated.
- Part V: sec:cross-check (tab:cross-check: 7-Zip agrees ~10% on Zen 3 and Zen 4; libx264 differs by half — possible reasons incl. Zen 4's 1 MB L2; 9800X3D SPEC fotonik3d +7.5%, roms +15% despite ~9% clock deficit).
- Page counts now: I 21–28, II 29–51, III 52–72, IV 73–94, V 95–114, VI 115+.

## 5 November 2026 (night) — simulation study and 5600X kit (141 → 155 pages)
- New Part V section sec:sim-study "A Controlled Software Model" (S0–S6 + sensitivity), 7 figures (fig:sim-latency, -working-set, -designs, -cache-clock, -pingpong, -zen2-zen3, -streaming) and 6 tables (tab:sim-plan, -calibration, -planar, -breakeven, -split, -sensitivity); new Appendix E app:sim-setup (tab:sim-parameters, workloads, reproduction).
- Figures and tables are generated from CSVs by tools/cachesim/study/make_figures.py; runs by tools/cachesim/study/sims.py (5 seeds, 10^6 accesses). Raw CSVs in research/measurements/cachesim/.
- Calibrations: overlap 0.42 ↔ 127 cycles per removed miss (Lam libx264 130); crossing cost 37 ns ↔ Reguly's 4.5× cross-CCD ratio (AMD's 9 ns gives 2.2×).
- Key results: S1 window 32–96 MB (memory-system speed-up up to 3.8×, −5–6% when data fits); S2 planar 96 MB break-even latency 107–245 cycles vs 32 MB baseline; S3 break-even 0.04 (equal) → 0.29 (7.3% gap) vs analytical 0.12 → 0.35; S3 libx264 check overstates (≈8% vs 4.9%); S4 two dies 1.29–1.52× slower on shared data, 1.00× on private; S5 unification helps only 16–32 MB; S6 96 MB keeps scaling to 2.1 G lines/s, 32 MB falls to DRAM limit 0.8.
- Valgrind traces of real programs tried and abandoned (too slow); stated as a limitation.
- Part I methodology/contributions, Part V method and summary, Part VI threats paragraph updated to mention the model.
- 5600X kit: tools/measurements/5600x-kit/ (latency sweep 4K/2M ×3, MLP chains, bandwidth 1/3/6/12 threads, core-to-core all pairs, clock estimate, model prediction, sysinfo) and tools/measurements/ELL305-5600X-kit.zip (gitignored). Results go to research/measurements/5600X/.

## 8 November 2026 — fourth review applied; rerun review items J19, J21, J24, J27 (155 → 160 pages)
- research/review-initial-draft-2-v4.md (I1–I43) applied except I43 (simulation section kept at full length, Ishan's decision); see `-v4-response.md`. Simulator fixed and the whole study rerun: raw vs exposed latency, overlap recalibrated to 0.335 (0.202 / 0.105 for Cyberpunk / GHPC), hop charged on DRAM accesses in the two-die preset, victim L4 and side-die latency sweep (new tab:sim-side-die), far region in the S3 mix, S3 sensitivity table (tab:sim-s3-sensitivity). Compiled binary rebuilt; 5600X kit model updated and kit zip rebuilt.
- Second pass on the corrected draft: research/review-initial-draft-2-v4-rerun.md (J1–J33). Applied so far:
  - J19: the cache-against-clock worked example and the analytical model (sec:cache-clock-model, tab:cache-vs-clock, tab:cache-clock-model, fig:cache-clock-model) moved from Part VI into a new Part V section sec:cache-against-clock, before sec:sim-study; Part VI keeps a one-paragraph summary.
  - J21: directory worked example moved to new Appendix F (app:directory-example); product-line silicon example moved to Appendix C (app:product-line); analytical-model calibration shortened. Part II and Part IV keep short summaries.
  - J24: text for fig:numa-latency, fig:bandwidth-balance and fig:clock-correction now says what each chart adds.
  - J27: terminology — "cache die" for the SRAM die, "V-Cache CCD" / "plain CCD" for the CCDs, "V-Cache part" for products; glossary entry l3d states the convention.
  - All other J items applied later the same day (see the next entry).
- Page counts now (PDF): I 24–33, II 34–54, III 55–75, IV 76–96, V 97–130, VI 131–146; 160 pages in all; 0 overfull boxes, no undefined references.

## 8 November 2026 (afternoon) — all J items fixed; 5600X measurements added (160 → 169 pages)
- research/review-initial-draft-2-v4-rerun.md (J1–J33): all applied; see `-v4-rerun-response.md`. Main changes: product-line silicon corrected (stack scrapped with a failed bond: 0.7–3% saving vs two dies, ~90% bonding break-even); 37 ns hop compared with the 18 ns of two link round trips; replacement policy tested on hot/cold and cyclic workloads (new tab:sim-policy, s1_policy.csv); headline "roughly triples" restated as 0.1 → 0.35 (0.38 simulated); analytical break-even row filled (agrees within 0.05 from 2 to 10%); calibration table shows gross 103 cycles; S0 renamed sec:sim-calibration.
- 5600X results (research/measurements/5600X) integrated, framed positively with mismatches kept: S0 out-of-sample check with fig:m5600x-latency (L1/L2 exact; L3 51–55 vs 47 cycles; 1 GB 98.6 vs 82 ns; refit within 5% / 1%), overlap check tab:m5600x-mlp (fitted 0.335/0.202/0.105 ≈ 3/5/10 misses in flight), TLB reach in Part II, same-CCD hand-over ~49 ns in Part III, 41 GB/s DRAM wall in S6, new Appendix G (app:5600x). Abstract, Findings, methodology (five kinds of evidence), threats and evidence table updated. Figures from tools/cachesim/study/compare_5600x.py (reproduces byte for byte).
- Page counts now (PDF): I 25–34, II 35–56, III 57–77, IV 78–98, V 99–135, VI 136–152; 169 pages; 0 overfull boxes, no undefined references.


## 8 November 2026 (evening) — fifth review K1–K19 and writing items fixed (169 pages)
- research/review-initial-draft-2-v5.md (K1–K21) and `-v5-response.md`. The 5600X result is now stated as the unfitted comparison (L1/L2 agree; L3 and memory within about 20%; up to 2.4× off at 32 MB); the 54-cycle / 90 ns refit is labelled a calibration; "real gain larger" limited to latency sweeps; overlap check called weak. Also: Part VI/RQ4 break-even 0.1; Zen 4 range limited to the product table (9224, Zen 4c noted); model vs 5600X core-to-core round trip (49 vs 98.5 ns); ω for the overlap factor; "round trip" vs "transfer"; terminology, numbers and long sentences. K20, K21, float placement and \partbudget lines deferred to the submission pass.
- Follow-up ("fix the remaining part"): K20 (`sec:evidence-method` now opens Part V); K21 (dies-per-wafer working to App. C, TLB reach and cache–clock calibration to App. F, which is renamed "Further Worked Examples", and S0 shape detail to App. G, each leaving its result in the main text); float placement tuned in the preamble; all `\partbudget` lines removed. 164 pages; Parts I 25–34, II 35–54, III 55–74, IV 75–95, V 96–130, VI 131–145; 0 overfull boxes, no undefined references.

## 9 November 2026 — sixth review L1–L29 (165 pages)
- research/review-initial-draft-2-v6.md and `-v6-response.md`. All items fixed except L24 (four worked examples kept in the main text, Ishan's decision); L22 cut ED² to one sentence. 5600X wording now separates input comparison (plateaus, within ~20%) from the model's own behaviour (up to 2.4× optimistic between plateaus); S4 split rerun with an 18 ns row (shared 1.26×); evidence-table grading rule restated; AMD's 19% attributed with its three causes.
- Node.js-free crosscheck for reviewers: `tools/cachesim/test/check_golden.py` against `test/crosscheck-golden.json` (written by `node test/crosscheck.js ./cachesim --write-golden`).

## 9 November 2026 — seventh review M1–M29 (164 pages)
- research/review-initial-draft-2-v7.md (A−, close to A) and `-v7-response.md`. M1–M28, ten long sentences and an RQ3 power sentence fixed; M29 (half-page rule for two worked examples) left for submission. Main changes: 37 ns hop described as a ratio fit, not a physical cost (~97 ns would match the absolute cost); 5600X called a single-CCD chiplet part; simulated 0.38 marked "not an independent check"; AMD attribution completed; one vocabulary for generations ("cache-on-top stack") and hops; 5600X kit documents aligned with App. G.

## 9 November 2026 — eighth review N1–N12 and own review pass (164 pages)
- research/review-initial-draft-2-v8.md (A−, close to A) and `-v8-response.md`. All N items fixed. Main ones: the App. C product-line limit (~90% bonding yield), lost in the M27 trim, is restored; the RQ3/Threats thermal sentence now names the 9800X3D at 95 °C and calls 400/360 W rated defaults; the bond-pitch argument is limited to C4 versus micro-bump/2.5D. The v7 response's M27/M28 rows are corrected.
- Own full review pass: several "every access" slips changed to "every memory access"; the 5600X refit is described as fitted (90 ns beyond L3); the one-outlet caveat is added to the abstract and Findings; six more long sentences are split; layout is tightened back to 164 pages. The kit zip is rebuilt. Open style choice: full captions in the List of Figures and List of Tables (short captions would shorten the front matter).

## 9 November 2026 (evening): presentation changes requested by Ishan (162 pages)
- **Front matter:**
  - The cover no longer says "Term Paper" and now carries the repository link.
  - The copyright page is signed with the three authors' names.
  - The acknowledgements thank Prof. Subrat Kar ("for his support"; the wording is a placeholder until his role is confirmed).
  - The running header now carries the topic, "Chiplets and 3D-Stacked Cache in AMD Zen Processors". It is redefined in `preamble.tex` only, so Draft 1's shared style is unchanged.
  - The repository link is also in Apps E and G.
- **New data figures** (values read from AMD's charts and labelled approximate):
  - `fig:reticle-sizes` (sec. 6.1): Rome's 1008 mm² against the reticle limit of about 800 mm² drawn in Swaminathan's slide 3;
  - `fig:area-scaling` (sec. 6.3, cited from the Part I bullet): Wuu slide 6, area scaling by function (shape only) and cost per yielded mm² (1.0 → 4.9);
  - `fig:isscc-charts` (sec. 13): Wuu slide 5, IPC uplift (shape only), and slide 6, node against year.
- **Part II:**
  - New DRAM cell and array figure (`fig:dram-array`, Sarangi sec. 7.4.3), with a paragraph on DRAM.
  - The pipeline-depth and write-traffic examples are cut to their conclusions.
  - "Worked example" is removed everywhere. App. F is now "Further Calculations".
- **Simulation naming:** "controlled software model" is now "simulation"; sec. 28 is titled "Simulation".
- **Mind maps:** all 13 are regenerated in the box-and-arrow style Ishan supplied. The generator is `tmp/gen_mindmaps.py`, and the originals are in `tmp/mindmap-orig/`. Captions now start "Overview of …", not "Mind map of …".
- **Block diagrams:** `fig:zen-ccd-evolution` is redrawn as colour block diagrams of the Zen 2, Zen 3 and V-Cache CCDs; `fig:epyc-package` uses the same colours.

## 10 November 2026 — final review v9 applied (152 pages)
- Review: research/review-initial-draft-2-v9-final.md; response: `-v9-final-response.md`.
- Applied: all P fixes except P2 (Appendices A and B need Ishan's plagiarism and readability results) and the submission date; the safe cuts; short captions; cuts of textbook-style worked examples.
- **Submission file:** `python3 scripts/flatten-initial-draft-2.py build/submission-final/ELL305-Term-Paper.tex` merges the modular files into one self-contained `.tex`, with the bibliography and logo embedded. Edit the modular files as usual, then rerun the script; the build/submission-final copy is generated and is never edited by hand.
- **Checked:** the merged file compiles alone in an empty folder, its text is identical to the modular PDF, and every float is referenced.


## 11 November 2026 — final review v10 applied (151 pages)
- Review: research/review-initial-draft-2-v10-final.md; response: `-v10-final-response.md`.
- Applied Q1–Q9 (draft macros removed, two list captions, two map leaves, AMAT sentence, 5.1% wording, Fig. 31 enlarged, Fig. 43 labels, comma splice), K1–K3 (write policies, ordering example, virtual memory cut to essentials), Q15 (sec. 4.6 "Writes and inclusion") and Q14 (19 more index entries).
- Paper is now 151 pages; the single `.tex` was regenerated, compiled alone, and its text is identical to the modular PDF.
- Remaining before upload: Appendices A and B, `\draftdate`, remove `\todo`/`todored`, regenerate.

## 12 November 2026 — prose-style pass and Appendix B (151 pages)
- Checkpoint before the pass: commit `7896898` (pushed to GitHub at Ishan's request).
- Style pass on Parts I–VI and the abstract: removed the repeated "N things stand out" openers, staged sentences ("The pattern is clear", the maxim opening the case against, one objection closer), weight-only "not X but Y" contrasts, three "Taken together" openers, about ten padding "rather than" clauses and "serves as". 32 edits; no facts, numbers or citations changed.
- **Appendix B filled:** readability indices for Parts I–VI, calculated by the group (Ishan approved computing them, 12 Nov 2026) with `tools/readability/readability.py` and textstat 0.7.13. The script strips LaTeX to prose (37,244 words, 1,929 sentences). Results: Gunning Fog 11.95, Flesch–Kincaid 9.43, SMOG 11.60, Coleman–Liau 9.33, ARI 10.42; average 10.55, median 10.42; Flesch Reading Ease 61.81. Labelled as the group's own calculation, not comparable with Draft 1's tool output. Rerun the script after any later text change.
- Submission file regenerated and compiled alone in an empty folder (pdflatex, biber, makeglossaries-lite, pdflatex ×2, makeglossaries-lite, makeindex, pdflatex ×2): 151 pages, A4, no errors or undefined references. On Windows, use `makeglossaries-lite`, because MiKTeX's `makeglossaries` cannot find Perl.
- Remaining before upload: Appendix A, `\draftdate`, remove `\todo`/`todored`, regenerate.

## 12 November 2026 — Appendices A and B filled
- App. A: Turnitin result typed as text and a table (12 Nov 2026, submission trn:oid:::1:3709247204, 151 pages; bibliography and quoted text excluded; 2% overall; 142 not-cited matches at 2%, 1 missing quotation at 0%; internet 2%, publications 1%, student papers 0%; 67 sources, each under 1%).
- App. B: shortened to one sentence stating the tool and scales, plus the table.
- `\todo` macro removed from `preamble.tex` (the `todored` colour stays: figures use it).
- Single `.tex` regenerated and compiled alone: 151 pages, text identical to the modular PDF.
- Remaining: `\draftdate` (still 8 November 2026).

## 12 November 2026 — Section 1.2 and similarity report
- New sec. 1.2 "Significance: how this paper extends the textbook" (`sec:significance`), required by the course's Gradescope question Q1.2; the same text is the Gradescope answer. Paper now 152 pages.
- Sec. 1.2 reworded by Ishan (humanizer pass); facts and references unchanged.
- App. A now lists the Turnitin digital receipt (table) and says the similarity report is attached after the index. The joint PDF (paper + report) is made by hand with `qpdf` as `build/submission-final/ELL305-Term-Paper-with-Similarity-Report.pdf`; not part of the build.
- After the final plagiarism check, update App. A with the new receipt and remake the joint PDF.
