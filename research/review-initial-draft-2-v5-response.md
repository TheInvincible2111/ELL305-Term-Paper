# Response to the fifth review (K1–K21)

Date: 8 November 2026. Review: `research/review-initial-draft-2-v5.md`.
Ishan's instruction: "fix all of k1-k19 and writing items". K20, K21, float placement and the `\partbudget` lines followed on Ishan's "fix the remaining part".

**Build:** 164 pages after the follow-up (169 before), 0 overfull boxes, no undefined references or citations, no "??".

**Reproduction:** the regenerated `model-comparison.csv` is byte-identical to the stored one. Only two figure files changed, both in their captions: `sim-pingpong.tex` and `m5600x-latency.tex`. The C++/JavaScript cross-check (not run by the reviewer) passed on Ishan's machine earlier on 8 November.

| ID | Status | What was done |
|---|---|---|
| K1 | Fixed | The unfitted comparison is now the result reported: L1 and L2 agree (noted as a comparison of two chips of one design), L3 and memory latency are within about 20%, and the model is up to 2.4× off at 32 MB. The 54-cycle / 90 ns refit is called a calibration that aligns the plateaus by construction; edge differences of 1.2–2.1× and 1.1–1.3× are stated. "Holds up", "confirmed", "sound", "carries over" and "never fitted" were removed from the abstract, Part I (method, contributions, Findings), the Part V section introduction, S0, the limits section, the Part V summary, threats to validity, the evidence row, the App. G introduction and the figure caption. |
| K2 | Fixed | The claim is limited to latency sweeps ("from about 20 to about 64 MB"), and the order-of-access explanation is called partial: at 64 MB, 66.9 ns lies between 56.6 and about 99 ns. The run-to-run spread at 32 MB (24.1 / 23.9 / 73.8 ns) and a possible WSL2 contribution are stated. "Strengthen" was removed. The limits bullet and the closing paragraph now agree. |
| K3 | Fixed | Part I: "makes no new measurements of chiplet or stacked-cache processors, and one set on a planar Ryzen 5 5600X". The `fig:evidence-method` caption points to App. G. |
| K4 | Fixed | Part VI summary and RQ4 say "about 0.1" (RQ4 adds "0.12 at the 4.2 GHz of the calibration"). The J6 row of the rerun response is corrected. |
| K5 | Fixed | Part III body, Part III summary and RQ2 limit the range to the products of `tab:product-matrix`. The EPYC 9224 (2.7 MB per core) and the 112- and 128-core Zen 4c parts are named (datasheet and white paper). |
| K6 | Fixed | S4 and App. G compare like with like: the model's same-CCD round trip is 49 ns at 4 GHz against 98.5 ns measured (66–72 ns on the fastest pairs), so the model's sharing latencies are lower estimates. |
| K7 | Fixed | App. E now uses ω, the exposed fraction, for the overlap factor, with ω = 1 − h stated in App. E and in Part II's `sec:mlp`. The calibration equation uses ω. |
| K8 | Fixed | "Round trip" is used for the ping-pong; "one transfer between CCDs (a request and its reply)" for the four link crossings. Changed in S4, the `fig:sim-pingpong` caption, the limits list and Part I. |
| K9 | Fixed | "Most of the difference". |
| K10 | Fixed | The S0 paragraph says the check is weak (fractions run from 0.07 to 1) and shows only that the implied overlap is physically possible, not that overlap is the explanation. The summaries in Part I and the limits section say the same. |
| K11 | Fixed | Part IV defines "first-generation arrangement" once, as the cache-die-on-top stack of Zen 3 and Zen 4; the 7800X3D sentence uses it. |
| K12 | Fixed | "A deficit of similar size therefore remained"; the caveat is kept. |
| K13 | Fixed | The evidence row says "about 0.6–0.7 TB/s". |
| K14 | Fixed | App. G: model input L3 + 74 ns is 84 ns at this clock; the model gives 82 ns at 1 GB. The memory difference is about 14 ns to the input (17 ns to the output). |
| K15 | Fixed | "Almost every access reaches the L3 or memory once the working set is well above the L2". |
| K16 | Fixed | Median 98.5 ns over the 132 ordered pairs (App. G, Part III). |
| K17 | Fixed | README: "AMD's actual L3 fill policy" replaces "victim-cache behaviour". Run time: about 7 minutes on 16 threads (App. E, `sims.py`). |
| K18 | Fixed | `tab:m5600x-conditions` is now referenced. Float placement: the preamble now stacks floats from the top of float-only pages and lets floats share pages with text more readily (`\topfraction` 0.85, `\textfraction` 0.12, `\floatpagefraction` 0.75). The only pages that remain part-empty are the last pages of Parts I–V before each `\clearpage`. |
| K19 | Fixed | "Embedded DRAM (eDRAM)" at first use (S2); "through-silicon vias (TSVs)" at first use (Part III); abstract "7%". |
| K20 | Fixed (follow-up, same day) | `sec:evidence-method` now opens Part V, straight after the mind map. |
| K21 | Fixed (follow-up, same day) | Each moved piece leaves its result in the main text. Moves: the dies-per-wafer working to App. C (`app:dies-per-wafer`); the TLB-reach working and table to App. F; the cache–clock calibration and its table to App. F (`app:cache-clock`); the detail of S0's "Where the shapes differ" to App. G (`app:5600x-shapes`). App. F is renamed "Further Worked Examples" (directory protocol, TLB reach, cache–clock calibration). |
| `\partbudget` | Removed | All six status lines are removed; the macro stays defined in the preamble. |

## Writing items

| Location | Status |
|---|---|
| `part6:87` | Split into two sentences. |
| `part6:168` | New sentence at "For most other workloads". |
| `part6:219` | Split at "In Rome and Matisse" and at "On power the evidence is thin" (now its own paragraph). |
| `part2:89` | Split after "$E \propto V^2$". |
| `part6:127` | Split after "raise performance by 15%". |
| `part6:125` | Split after "rather than only cache". |
| `part5:53` | Split after "7 to 8 cycles of L3 latency". |
| `part5:498` | Changed to "Its other two inputs differ by about 20% or less". |
