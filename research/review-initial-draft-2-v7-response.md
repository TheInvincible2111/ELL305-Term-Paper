# Response to the seventh review (M1–M29)

Date: 9 November 2026. Review: `research/review-initial-draft-2-v7.md`.
Ishan's instruction: fix M1–M28, the ten long sentences and the RQ3 power sentence; leave M29 for submission.

**Build:** 164 pages (the App. C spill is gone), 0 overfull boxes, no undefined references or citations.

| ID | Status | What was done |
|---|---|---|
| M1 | Fixed | S4 shared-data bullet: "The 18 and 37 ns figures also charge every memory access at that hop; with AMD's 9 ns for memory accesses they would be about 1.25 and 1.35 times, by the authors' estimate." |
| M2 | Fixed | S4 text and `fig:sim-pingpong` caption: 37 ns is fitted to the ratio only; the model's exchanges are about 2.4 times too fast (25 against 58.6 ns, 110 against 265 ns); matching the absolute extra cost would need about 97 ns; the measured extra cost is the 206 ns of `sec:cross-ccd`. 1.39× is stated not to be an upper limit. Part I and the limits list say the two link round trips (18 ns) explain only part of the measured cost. |
| M3 | Fixed | Part I and abstract: the 5600X is "a single-CCD chiplet part without stacked cache"; no new measurements of stacked-cache processors or of traffic between CCDs. |
| M4 | Fixed | "built on the same calibration and so not an independent check" at `part1:180`, `part6:85` and `part6:223`. |
| M5 | Fixed | `tab:thought-experiment` attributes both values to AMD with `\cite{naffziger2020chiplet}`; the `epyc-package` legend and the chiplets mind map say "AMD". |
| M6 | Fixed | First evidence row reworded ("established yield theory, independent of AMD … no independent cost data, though AMD's chart agrees"); `part6:160` rewritten in the caption's terms. |
| M7 | Fixed | "First-generation" for the arrangement replaced by "cache-on-top stack" or the product name; "first two generations" kept for Zen 3 and Zen 4. |
| M8 | Fixed | "Three articles from one independent outlet (Chips and Cheese)" in `part5:286`, the evidence row and `part6:160`. |
| M9 | Fixed | App. G: "This probably explains why…". |
| M10 | Fixed | "probably because…" in `part3:152`, `fig:numa-latency` caption and `part6:166`. |
| M11–M12 | Fixed | Abstract, Part I, S0, Part V summary and Findings: "L1 and L2 agree; L3 and memory are within about 20%"; the 2.4× is "at 32 MB, under WSL2"; "too optimistic about the smaller cache" replaced. |
| M13 | Fixed | The S0 heading and the two tool documents no longer say "out-of-sample check". |
| M14 | Fixed | Abstract uses "NUMA behaviour"; "uniform" kept only for the penalty paid by every access. |
| M15 | Fixed | Glossary: "In the simulations of Part V a hop is one CCD–IOD round trip, by default AMD's 9 ns". `fig:topologies`: "2 links apart". |
| M16 | Fixed | Kit README and `ANALYSIS.md` aligned with App. G (comparison not validation; no overlap calibration; WSL2 can add to L3 and memory latency; 98.5 ns; 14 ns above the input, 17 ns above the output). Kit run time corrected to about 10 minutes (README, `run_all.sh`). |
| M17 | Fixed | "V-Cache CCD" and "plain CCD" in `cache-clock-model.tex` and `thread-placement.tex`; L3D kept only for AMD's slide. |
| M18 | Fixed | Lam's bar ends at 1.197 without an arrow; caption clause removed. |
| M19 | Fixed | 10.63 ns. |
| M20 | Fixed | "brackets the measured gain" (`part4:178`, `part4:305`). |
| M21 | Fixed | Part III uses the Part VI wording: "answered only for link energy, and otherwise qualitatively". |
| M22 | Fixed | WSL2 expanded at `part2:288`. |
| M23 | Fixed | App. G: each pair's value is the fastest of three trials (method and results). |
| M24 | Fixed | S6 says "(8–16 MB in all)"; parameter table hop row adds "also 18 and 60 ns in `tab:sim-split`". |
| M25 | Fixed | "takes about 4.5 times as long". |
| M26 | Fixed | Ping-pong legend moved below the plot; table captions now consistent. |
| M27 | Fixed, with a regression (see N1 in the v8 response) | App. C trimmed; 164 pages. The trim removed the ~90% bonding-yield limit, restored on 9 Nov. |
| M28 | Fixed (corrected 9 Nov, after N1) | 5600X framing kept in full in S0, the limits list and Threats; elsewhere a clause with a cross-reference. The duplicated sentences were removed from the **appendices** (App. C and App. F), not from the main text as first reported here; `part4:268` and `part2:390` keep them. The App. C cut also removed the product-line limit, which N1 restored. |
| M29 | Deferred (decision at submission) | Both examples stay for now. |
| Long sentences | Fixed | All ten split as suggested. |
| RQ3 power | Added | `part6:221`: "No energy or thermal measurement of a V-Cache part was found; the only direct indication is the datasheet pair…". |
