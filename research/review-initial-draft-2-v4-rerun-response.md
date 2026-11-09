# Response to the rerun of the fourth review (J1–J33)

Date: 8 November 2026. Review: `research/review-initial-draft-2-v4-rerun.md`.

Ishan's instructions:
- J19, J21, J24 and J27 first;
- then "fix everything, put the 5600X results, try to paint more of an optimistic picture about the results rather than focusing on the mismatches, but don't remove the mismatches";
- hold the pointer-chase workload for now.

All 33 items are applied.

**Build:** 169 pages, 0 overfull boxes, no undefined references or citations, no "??".

**Reproduction:**
- The simulation study reruns unchanged.
- New CSVs: `s1_policy.csv`; `sensitivity.csv` (without the two invalid policy rows); `s4_pingpong.csv` (adds 18 ns).
- `tools/cachesim/study/compare_5600x.py` regenerates the 5600X figure, table and comparison CSV byte for byte on Ishan's machine.

| ID | Status | What was done |
|---|---|---|
| J1 | Fixed (without the pointer-chase workload, as instructed) | Replacement policy is now tested on random, hot/cold and cyclic sequential workloads (new `tab:sim-policy`). The text explains why random accesses cannot show a policy effect. At 64 MB the gain ranges from 1.15 to 1.19× (hot/cold) and from 4.27 to 4.75× (cyclic). The "like a pointer chase" description in App. E is replaced. S0 no longer cites the policy test as ruling anything out. |
| J2 | Fixed | App. C (product-line example): a failed bond scraps the CCD as well, so a stacked part costs (94.8 + 44.5)/0.95 ≈ 146.6 mm². (C) is 100/108/121 mm², a saving of 0.7–3% against (B), and break-even against (A) at about 90% bonding yield, consistent with `tab:stack-yield`. The 99% clause is corrected (140.7 mm²). |
| J3 | Fixed | An exchange between CCDs makes two link round trips (18 ns). Changes: 18 ns marked in `fig:sim-pingpong` (2.9×); "about twice the bare link cost"; Part III "about eleven times the 18 ns"; Findings and limits list reworded. |
| J4 | Fixed | "Real Zen L3s are filled by L2 evictions" is removed from App. E, the limits list and the README; replaced by "the sources do not state how Zen's L3 is filled". |
| J5 | Fixed | The side die is faster below 32 MB (5.88 against 6.21 ns); the claim is limited to working sets beyond 32 MB (S2 and limits list). |
| J6 | Fixed (completed after the fifth review, K4) | Abstract and Findings say "from about 0.1 to about 0.35", with 0.38 from the simulation. The Part VI summary and RQ4 still said 0.12 when this file was first written; they were corrected in response to K4. |
| J7 | Fixed | Equal-clock robustness explained: the overlap factor cancels; only memory latency moves it. |
| J8 | Fixed | The L3 miss rate is now a "first screen" (Part V and Part VI implications): a low rate rules the cache out, and a high one leaves open whether the working set fits. |
| J9 | Fixed | "About 2% of a Genoa processor's power budget (memory traffic only)" in Findings, Part III summary, RQ2 and the evidence row. "Bound" is changed to "estimate" in the worked example. |
| J10 | Fixed | Contributions: "most changing one factor at a time", plus a separate 5600X bullet. `tab:sim-plan`: the S5 column is now "—", the S0 row adds the 5600X (not fitted), and the caption says which comparisons are fitted. |
| J11 | Fixed | "In the floating-point suite"; 18–26%. |
| J12 | Fixed | "Because, by AMD's account, that reach…". |
| J13 | Fixed | "Across the overlap factors fitted to Lam's workloads, with the libx264 mix held fixed" (S3, Findings, Part V summary). |
| J14 | Fixed | The calibration table shows gross savings (103/62/32/307 cycles), with the caption explaining them; the text says about 103; README corrected. |
| J15 | Fixed | App. E coherence bullet: write hit (one extra L3 latency, plus the hop if a holder is remote), write miss (fetch plus a further hop), and no-cost invalidation of L3-only copies. |
| J16 | Fixed | "Upper bound" removed; the text says 1.39× also charges memory accesses at 37 ns, and about 1.35× with 9 ns for those (authors' estimate). |
| J17 | Fixed | Part IV: 0.62 TB/s at 4.2 GHz and about 0.71 TB/s at the 4.8 GHz sustained at stock clocks, consistent with Lam's 702 GB/s. Part VI adds the same note. |
| J18 | Fixed | Evidence row: "Weak by this table's definition (model outputs), but the model's structure is confirmed on real hardware" (5600X). |
| J19 | Fixed (earlier today) | The cache–clock model moved into Part V (`sec:cache-against-clock`). |
| J20 | Fixed | The duplicate Genoa-X sentence is replaced by a cross-reference. The prefetch caveat is now stated in full once (`sec:tradeoff-example`); `sec:lam-detail` refers back to it. |
| J21 | Fixed (earlier today) | Directory example in App. F; product-line example in App. C; analytical calibration shortened. |
| J22 | Fixed | S0 is now "What the calibration fixes, and how the model compares with hardware"; the label is renamed `sec:sim-calibration`. |
| J23 | Fixed | `fig:sim-zen2-zen3`: one shared legend below both panels. |
| J24 | Fixed (earlier today) | The text says what each duplicate chart adds. |
| J25 | Fixed | "Corrected those results", "the correction", "Reguly's test" (caption), "Murphy regarded". |
| J26 | Fixed | IPC expanded in Findings. "UCIe, the Universal Chiplet Interconnect Express" cites Liu et al., the local source that gives the expansion. "Memory modules (DIMMs)". EFB has no local source for its expansion, so the existing descriptive phrase ("a 2.5D bridge (EFB)") stays. |
| J27 | Fixed (earlier today) | Terminology convention; glossary. |
| J28 | Fixed | "Entirely because the split L3 has the lower latency". |
| J29 | Fixed | "The 96 MB L3 holds the data of up to four threads; beyond that both caches overflow". |
| J30 | Fixed | Draft date set to 8 November 2026; the six `\partbudget` status lines updated. |
| J31 | Fixed | Butterfly diameter is log N + 1. |
| J32 | Fixed | "Four interactions". |
| J33 | Fixed | ≈ 206; SRAM "shrinks less than logic does"; the analytical row of `tab:sim-breakeven` is filled (0.10/0.17/0.24/0.31/0.35/0.45, computed in `make_figures.py` from `eq:cache-clock-model`). It agrees with the simulation within 0.05 from 2 to 10%, and the text now says so. |

## 5600X measurements (new)

**Where they appear in the paper:**
- **S0 out-of-sample check** (`fig:m5600x-latency`, new). L1 and L2 are exact. The L3 is 51–55 cycles against 47, close to the about 53 cycles reported for the 5800X. Memory at 1 GB is 98.6 ns against 82 ns. With two latencies set to this machine, the model matches within 5% (L3 plateau) and 1% (1 GB).
- **Overlap check** (`tab:m5600x-mlp`, new). The fitted factors 0.335, 0.202 and 0.105 correspond to about 3, 5 and 10 misses in flight. The core sustains at least 16.
- **Part II:** the TLB reach of 256 KB is confirmed, and 4 KB pages add about 17 ns at 1 GB.
- **Part III:** the same-CCD hand-over takes about 49 ns, the same order as Reguly's 58.6 ns.
- **S6:** the measured memory bandwidth wall is 41 GB/s, 80% of peak.
- **Appendix G** (`app:5600x`, new): conditions, method, results and limits.

**Mismatches that are kept:**
- The real L3 slows down from about 16–20 MB and is twice the model's latency at 32 MB.
- Just above each capacity the measured latency is higher than the model's.
- WSL2 caveats.

**How they are framed:** the text points out that both mismatches make the real 32 MB cache worse than the model. The model's gain is therefore conservative from about half the smaller cache's capacity up to about 64 MB, and optimistic only close to 96 MB.

**Other updates:** abstract, Findings, methodology ("five kinds of evidence"), threats to validity ("Limited own measurements"), the evidence table and open questions (native Linux and a V-Cache part). `CLAUDE.md` §3 is updated to record that the kit has been run.
