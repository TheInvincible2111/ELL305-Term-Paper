# Response to the fourth review of initial-draft-2 (I1–I43)

Date: 8 November 2026. Review: `research/review-initial-draft-2-v4.md`.
Ishan's instruction: "dont shrink simulation section just fix everything". So every finding has been applied except the shortening in I43. The simulation section keeps its length. It has been reframed as an *illustration* of the mechanisms, not a confirmation of them.

**What changed in the model.**
- The simulator was corrected and extended, and the study was rerun from scratch (`tools/cachesim`, `tools/cachesim/study`).
- The CSVs in `research/measurements/cachesim/` were regenerated, and three were added: `s2_side_die`, `s3_sensitivity` and `seed_spread`.
- All `figures/sim-*.tex` files were regenerated from the new CSVs.
- `node test/crosscheck.js` passes with three new cases (hop on DRAM, victim L4, far region). The C++ and JavaScript models still agree exactly, and the self-test reports 0 failures.

**Build.** 160 pages (printed numbering), 0 overfull boxes, no undefined references or citations, no "??". The body grew by about 4 pages, nearly all in the simulation section, because of the new side-die and S3-sensitivity tables and the longer caveats.

## Findings

| ID | Status | What was done |
|---|---|---|
| I1 | Fixed | The simulator now reports both `amat_ns` (raw, no overlap) and a new `exposed_ns` (after the overlap factor). S1, S2, S4 and S5 now compare **exposed** latency. The text and all captions name the metric. The 8.5% against 5.6% clash is gone: at 32 MB the stacked L3 is 5.6% slower than 32 MB in both S1 and S2, and the planar L3 is 17% slower. S5 also gives the raw figures (19–20%, 4.0×). |
| I2 | Fixed | New `dram_hop` option: the `twoccd` preset charges the hop on every DRAM access. The private case now uses 8 MB per thread, 128 MB in all, which overflows both organisations. New results: shared data 1.20× (9 ns) and 1.39× (37 ns; replication causes 22 against 0 memory accesses per 1000); private data 1.08× at 9 ns. The text says the result follows from how the hop is charged, and S4 was removed from the "confirmed" list. |
| I3 | Fixed | S0 now says the model is optimistic near each edge. It understates the gain just above 32 MB (240 against 195 cycles at 64 MB) and overstates it just below 96 MB (65 against 51). The general "upper bounds" claim was removed from the limits. |
| I4 | Fixed | S5 numbers were reread from the new CSV. One thread: unified L3 about 12% higher exposed latency (20% raw) up to 16 MB, and 1.7–3.0× better between 16 and 32 MB (4.0× raw at 32 MB). Eight threads: 1.3–2.3×. "A few per cent" was replaced by "7–8 cycles on every L3 access; for a real program the cost scales with how often it reaches the L3". |
| I5 | Fixed | `hot_prob` resolution is now 1e-6. The S3 mix was rebuilt (98.889% hot, 0.799% cold, 0.312% far). It gives 3.78 L3 accesses per 1000 instructions at the operating point; stated in the text and in App. E. |
| I6 | Fixed (earlier this round) | Counter caveat stated in `sec:tradeoff-example`, `tab:lam-detail` and `sec:lam-detail`. Values are now "apparent" savings, with overlap and prefetch as the two explanations. The DCS 15% check is reported. Findings, RQ4, the Part V summary and the mind maps were softened to match. |
| I7 | Fixed (earlier) | 9224 counter-example in the text and the `tab:product-matrix` caption. The 9174F/9124 comparison is limited to stated quantities; "two fully used CCDs" and the link count were removed. |
| I8 | Fixed (earlier) | Cozma's whole-CCD −12.5% and Lam's 18.45 B/cycle (≈0.62 TB/s) are cited. `>2 TB/s` is marked as AMD's peak everywhere, including the Part IV summary and `mindmap-stacked`. The evidence row reads "Weak: vendor figure, not reproduced". |
| I9 | Fixed (earlier) | "Usually among those that miss most, but not always (xalancbmk, GHPC)". |
| I10 | Fixed | "Illustrates" or "is consistent with" throughout. S0 says the 1 GB match is set by the inputs and that the measured pair differs because of clocks (Cozma: Milan-X boosted higher). S3 calls the agreement expected rather than independent. S4 calls the 37 ns fitted, "about four times AMD's 9 ns". `sec:sim-limits` and the Part V summary say "largely by construction". |
| I11 | Fixed | S4 compares ratios only and states why: one message against two messages plus two upgrades, and a planar Zen 3 preset at 4 GHz. The `fig:sim-pingpong` caption says the same. |
| I12 | Fixed | Self-consistent recalibration: h = 0.335 (libx264), 0.202 (Cyberpunk 2077), 0.105 (GHPC). The equation is in App. E, and the new `tab:sim-calibration` shows net saving, factor and gross saving (101 cycles against the 130 apparent cycles, with the reason). README aligned. |
| I13 | Fixed | New S3 sensitivity table (`tab:sim-s3-sensitivity`). At 7.3%: 0.38 calibrated, 0.58 (0.202), 1.05 (0.105), 0.17 (no overlap); memory 60/90 ns gives 0.46/0.31. The text now says the realistic-gap break-even is the *more* sensitive one, about threefold across Lam's workloads. Part I Findings, RQ4 and the Part V summary carry this. |
| I14 | Fixed | The analytical row now uses 0.10 at equal 5.15 GHz, with 0.12 at 4.2 GHz noted in the caption. The text says "a factor of about 2.4", all from whether the four cycles are hidden. |
| I15 | Fixed | A 1 GB far region keeps the stacked part at 1.04 MPKI (Lam: ≈1.08), and `work_cycles` = 0.48 gives 729 cycles per 1000 instructions (Lam: 735). The validation point gives 5.2% against Lam's 4.9%, and is stated to be a check of the construction, not a test. "Upper bounds" was removed. |
| I16 | Fixed | New experiment: side-die latency 5–22 ns, inclusive and victim (`tab:sim-side-die`, `s2_side_die.csv`); victim L4 added to the model. Finding: the side die never matches the stacked L3, even at 5 ns, because it is looked up after an L3 miss. Victim mode is much better beyond 64 MB. The 22 ns default is labelled an assumption. |
| I17 | Fixed (by explanation) | S0 and App. E now say that the model maps working sets contiguously and so has no conflict misses below capacity. That is the main reason the curve stays flat, and "not exact LRU" was dropped. Randomised page placement was not added; it is listed as a limit. |
| I18 | Fixed (earlier) | "Estimated at roughly 1–2% … for memory traffic alone" in Findings, Part III summary, RQ2 and the evidence row. |
| I19 | Fixed (earlier) | Range stated within one generation. |
| I20 | Fixed (earlier) | "About half of a 47-cycle L3 hit". |
| I21 | Fixed (earlier) | "265 against 228–247 ns"; "about 1.5 times the cross-CCD figure". |
| I22 | Fixed (earlier) | Four miss-heavy workloads, 9.67–19.7%; GHPC has the largest *relative* fall. |
| I23 | Fixed (earlier) | "Four kinds of evidence"; "five of them set beside a published measurement"; full stop fixed. |
| I24 | Fixed (earlier) | Abstract sentence, Findings bullet, `tab:rq-map` entries, evidence row ("Illustrative"), mind maps (`mindmap-case-study`, `mindmap-paper`) and the stale part5 comment. **For Ishan:** `CLAUDE.md` §3 and §8 still say initial-draft-2 "uses published data only". That file is yours, so it was not changed. |
| I25 | Fixed (earlier) | New open question on 5600X measurements; `sec:sim-limits` points to it. |
| I26 | Fixed (earlier) | "Strong (datasheet facts) for the range; weak for configurations". |
| I27 | Fixed (earlier) | The four assumptions are listed after the 130-cycle derivation. |
| I28 | Fixed (earlier) | "Appear to remain"; Cozma's power-distribution note and the AMD-supplied sample are mentioned. |
| I29 | Fixed (earlier) | 11.4% is labelled as the authors' calculation wherever it appears. |
| I30 | Fixed (earlier) | "About 240 cycles at 64 MB, nearly five times". |
| I31 | Fixed (earlier) | L2-doubling note added. |
| I32 | Fixed (earlier) | 7-cpu's "about 800 KB" noted. |
| I33 | Fixed (earlier) | Cites `tab:core-to-core`. |
| I34 | Fixed | App. E uses `lstlisting[language=bash]`. |
| I35 | Fixed | Cites Sarangi sec. 11.1.1. The three S3 inputs (one access per three instructions, `l1_lat` = 1, `work_cycles` = 0.48) are called assumptions in `sec:sim-clock` and App. E. |
| I36 | Fixed | (a) App. E names the hand-typed values (Milan/Milan-X points, Reguly's ratio), and so does the `make_figures.py` docstring. (b) Time is the largest of three limits; the link limit is stated as off. (c) Ping-pong warm-up described. (d) Write cost, overlap 0.05 and 2.5×10⁵ accesses per thread for S6 are in the parameter table. README updated. |
| I37 | Fixed | "Below 1% for every plotted quantity … at most 1.4% for the miss counts stored alongside" (`seed_spread.csv`). |
| I38 | Fixed | Column renamed "Compared with". |
| I39 | Fixed | `sim-zen2-zen3` legend at `\scriptsize`. `zen-ccd-evolution` labels at `\scriptsize`, with the Zen 2 CCX outlines widened so they no longer cut the core boxes. `monolithic-vs-chiplet`: I/O box fits inside the die; the link label moved above the IOD, clear of the arrows. Sim floats rechecked: no large blank areas. |
| I40 | Fixed (earlier) | TLB, CCX, NUMA, TDP, HPC, FVOPS, ECC and PCIe expanded at first use. |
| I41 | Fixed | "Hop" is used throughout the simulation text and App. E ("crossing" removed). Glossary entries added: die-to-die hop, L3D (cache die), TLB, MLP. |
| I42 | Fixed (earlier) | Part II's worked example now uses the textbook only ("how much overlap saves"); the derivation stays in Part IV, and other places cite back. |
| I43 | **Declined (Ishan)** | The simulation section was not shortened or moved to App. E, on Ishan's instruction. Page counts (PDF pages) are now: I 10, II 22, III 21, IV 22, V 32 (target 25), VI 18; body 125 against 130. |

## Writing items

| Location | Status |
|---|---|
| `part5:263` (300 bytes per point) | Fixed: "at about 300 bytes per point, Milan-X's L3 holds three times as many grid points as Milan's". |
| `part5:402` ("a second kind of evidence") | Fixed: the opening now says the model illustrates and does not independently confirm. |
| `part5:466` (factor of three) | Fixed: about 2.4 (I14). |
| `part5:441` vs S2 metric | Fixed: both now use exposed latency (I1). |
| `part3:162` (directory placement) | Fixed: conditional on the directory's location. |
| `part6:145` (long sentence) | Fixed: split into two. |
| `part1:177`, abstract ("confirmed independently") | Fixed: "measured independently" in both places. |

## Other changes made while fixing
- Part V summary: the "Where they do not…" sentence was moved back after the sentence it qualifies. The per-miss values are now "apparent", with both explanations.
- Evidence ledger: a non-breaking "SPEC CPU 2017" caused a 5 pt overfull line; fixed.
- `tools/cachesim/gui`: labels for raw and exposed latency; experiment c2 updated to 8 MB per thread with the hop on DRAM. Rebuilt `index.html`, `index-offline.html` and `experiments.json`.
- The compiled binary `tools/cachesim/cachesim` was rebuilt from the new source (self-test 0 failures; C++/JS cross-check identical). A rerun of S0 with it reproduces the stored CSVs byte for byte.
- The 5600X kit's model (`tools/measurements/5600x-kit/model/cachesim.cpp`) now matches `tools/cachesim/src/cachesim.cpp`, `model_sweep.py` notes the raw-latency metric and the contiguous mapping, and `ELL305-5600X-kit.zip` was rebuilt.
