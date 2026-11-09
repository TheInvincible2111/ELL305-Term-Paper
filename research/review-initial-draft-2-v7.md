# Seventh review of initial-draft-2 (9 November 2026)

Brief followed: `research/review-prompt-initial-draft-2-v7.md`, applied to the 165-page draft. Findings are numbered M1, M2, ….
Only local files were used; nothing on the web. No project file other than this report was changed, and all reruns went to a temporary folder.
Page references are **PDF viewer pages** of `build/pdf/ELL305-initial-draft-2.pdf`. Line references are to `initial-draft-2/` unless a full path is given; `part5:538` means `sections/part5-case-study.tex`, line 538.

**Build currency.** The PDF was built on 9 Nov 2026 at 01:15:10. No file under `initial-draft-2/` or `paper/` is newer, so the PDF matches the sources. Build log (`tmp/linux-build/main-initial-draft-2.log`): no errors, no undefined references or citations, **0 overfull boxes**, 33 underfull boxes. `pdfinfo` gives 165 pages, A4.

**What this review did not do.**
- `test/crosscheck.js` was not run, because Node.js is not installed in Windows here. `test/check_golden.py` was run instead (§4.1).
- `sims.py` was rerun only for `s0 s4 policy`. S1–S3, S5 and S6 were not rerun, but every table and figure of `sec:sim-study` was regenerated from the stored CSV files (§4.1).
- All 61 pages carrying figures were rendered at 125 dpi and read, two pages per view. Pages holding only tables and text were checked from the sources and the PDF's text, not rendered.
- `Gem5/` is out of scope.

---

## 1. Overall assessment

The paper remains strong for an undergraduate term paper, and I hold it provisionally at A−, close to A. The sixth review's fixes are nearly all present, and the 5600X framing is now honest and clear in the body: on the plateaus the comparison checks published inputs, and the model's own behaviour shows only between them. All reruns are identical to the stored files, the C++ model agrees with the stored JavaScript results, and every 5600X number sampled matches the raw CSV files. What remains is smaller than in earlier rounds. One sentence was left wrong by the L7 fix (M1). The fitted 37 ns hop is read as "about twice the link" while Part III says the measured cost is eleven times the link, and the text does not reconcile them (M2). A few statements carry the wrong status: the paper says it did not measure a chiplet processor although the 5600X is one (M3), and Findings and Conclusions use the simulated 0.38 as support after S3 says it is not independent (M4). Attribution of AMD's figures is incomplete in one table (M5), and "first generation" still has three meanings (M7). None of these undermines a main conclusion, and most are single-sentence edits.

**The two changes that would improve the paper most:**
1. Fix M1–M4, which are the places where a careful examiner would find the paper disagreeing with itself or claiming more than its own method section allows.
2. Settle one vocabulary for generations and for the hop (M7, M15, M19), so that the same word means the same thing from the abstract to the appendices.

---

## 2. Findings (most severe first)

| ID | Severity | Location | What the draft says | What the source, CSV, code or rule says | Suggested correction |
|---|---|---|---|---|---|
| M1 | Error (introduced by the L7 fix) | `part5:538`, p. 126 | "The second figure also charges every memory access at 37 ns; with AMD's 9 ns for those, it would be about 1.35 times." | The bullet now gives three figures: 1.20× (9 ns), 1.26× (18 ns), 1.39× (37 ns). "The second figure" is now the 18 ns one. 1.35× is correct for the 37 ns case: (7.896 − 28 × 0.00738) ÷ 5.684 = 1.353 from `s4_split.csv`. The same caveat applies to the 18 ns row, which becomes about 1.25×. | "The 37 ns figure also charges every memory access at 37 ns; with AMD's 9 ns for those it would be about 1.35 times (and the 18 ns figure about 1.25 times), by the authors' estimate." |
| M2 | Inconsistent (a fitted ratio read as a physical cost) | `part5:532`, caption `figures/sim-pingpong.tex:20` (p. 125); `part3:185` (p. 64); `part1:181`, `part5:571` | The extra cost across CCDs "is about eleven times the 18 ns that the link itself accounts for" (Part III). "If the extra cost of a request and reply between CCDs is modelled as one hop, that hop must be about 37 ns, about twice the 18 ns" (S4). | The two statements describe different things and the text does not say so. 37 ns matches only the *ratio* 4.5. `s4_pingpong.csv` gives a cross-CCD round trip of 72.5 + 4 × hop ns and a same-CCD one of 49 ns. Halved, as `part3:183` halves the 5600X's round trip, that is 24.5 ns per message within a CCD against Reguly's 58.6 ns, and 110 ns across CCDs at 37 ns against 265 ns: both about 2.4 times too fast. Matching Reguly's absolute extra cost would need a hop of about 97 ns. So "about twice the link" is a product of a fast base, not an estimate of the hidden cost. It also means 1.39× in `tab:sim-split` is not an upper limit. | Say that 37 ns is the value that matches the ratio on a model whose same-CCD exchange is about 2.4 times too fast, so it is not the real cost of a transfer; the measured extra cost is the 206 ns of `sec:cross-ccd`. Replace "about twice the 18 ns" with that statement in the text and caption. |
| M3 | Inconsistent | `part1:161`, also `part1:151` (p. 31) | "This paper makes no new measurements of chiplet or stacked-cache processors, and one set on a planar Ryzen 5 5600X." | The 5600X is a chiplet processor: one CCD plus an I/O die (`tab:product-matrix`, `app:5600x`, `part3:183`). "Planar" here can only mean "without stacked cache". The sentence contradicts itself. | "No new measurements of stacked-cache processors or of traffic between CCDs, and one set on a Ryzen 5 5600X, a single-CCD chiplet part without stacked cache." |
| M4 | Overstated (calibrated agreement used as support) | `part1:180` (p. 33); `part6:85` (p. 135); `part6:223` (p. 145) | "the controlled simulation gives nearly the same value, 0.38"; "and the simulation gives 0.38"; "0.38 in the controlled simulation". | `part5:522` says this agreement "is expected rather than independent, since both are built on the same calibration and the same structure". The headline places drop that limit, so the second number reads as a confirmation. | Add once in each place: "(built on the same calibration, so not an independent check)". |
| M5 | Unsupported (L6 partly fixed) | `tab:thought-experiment`, `part1:50–51` (p. 27); `figures/epyc-package.tex:34` (p. 59); `figures/mindmap-chiplets.tex` (p. 56) | "under 9 ns round trip" and "Rome's average about 0.81× that of its multi-die predecessor", with no attribution in the table; the legend and the mind-map node also state "under 9 ns" plainly. | The brief requires AMD attribution everywhere. L6 listed this table; the response fixed Parts I, III and VI text only. The table has no citation for either value. | "(AMD: under 9 ns round trip)"; "AMD reports …0.81×"; add `\cite{naffziger2020chiplet}`. Add "as reported by AMD" to the legend or caption. |
| M6 | Inconsistent (L5 largely fixed) | `tab:evidence-strength` first row, `part6:144`; `part6:160` (pp. 138–139) | "Moderate: robust mechanism, illustrative inputs; AMD's chart agrees". `:160` calls the four-cycle latency and the IPC gain "claims about mechanism" and contrasts them with "claims about magnitude". | The caption makes a mechanism moderate "when independent evidence is consistent with it". The only corroboration named is AMD's own chart, which is not independent. The caption's classes (performance, fact, mechanism) also differ from `:160`'s (mechanism, magnitude); four cycles is a measured size. All other rows follow the caption. | Name independent support for the first row or regrade it. Rewrite `:160` in the caption's terms. |
| M7 | Inconsistent (L19 partly fixed) | `part4:97–98`, `:141`, `:205` (pp. 80–87); `part4:216`; `part1:180`, `part5:400`, `:587`, `part6:170`; abstract | `:216` defines "first-generation" as the cache-on-top stack, "as in the Zen 3 and Zen 4 parts". | It has three meanings. `:141` says "In the first-generation stack… For Zen 4, AMD changed this detail", which excludes Zen 4. Five uses come before the definition. The abstract, Findings and Parts V–VI say "first two generations" for the same Zen 3 and Zen 4 parts that `:216` calls one generation. | Use "cache-on-top stack" or name the product. Keep "first two generations" and drop "first-generation" for the arrangement. Define the term at `:97`. |
| M8 | Overstated | `part5:286` (p. 109); `tab:evidence-strength` row "about four cycles" (p. 139); `part6:160` | "Three independent sources measured the same programs or the same quantity"; four cycles "independently replicated across three generations" (Strong). | Cozma 2022a and b, Lam 2023 and Cozma 2024 are all Chips and Cheese articles, and the 9800X3D was an AMD-supplied sample (`part4:222`). They are independent of AMD and consistent with AMD's figure, but they are one outlet's method on three chips. The grade can stand if this is stated. | "Three articles from one independent outlet (Chips and Cheese)". Add "one outlet" to the row. |
| M9 | Overstated (inference stated as fact) | `appendix-g:72` (p. 164) | Pinning does not fix the physical core. "This is why no pair … shows the short time expected for two threads on one core, and why pairs in which the responding thread ran on logical CPU 0 were faster." | `ANALYSIS.md` §5 says "probably a WSL2 scheduling effect" and "consistent with". The data show the pattern but not its cause. | "This probably explains why…". |
| M10 | Overstated (inference stated as fact) | `part3:152` (p. 61); caption `figures/numa-latency.tex:21` (p. 62); `part6:166` (p. 138) | Rome's fastest access is slower (94 against 90 ns) "because every access now crosses the IFOP link". | Naffziger gives the values and the 19% average, but not the reason for 94 against 90 ns. The chips also differ in core and memory support. | "probably because…", in all three places. |
| M11 | Writing (meaning unclear) | Abstract (p. 4); `part1:182` (p. 33); `part5:475` (p. 118); `part5:587` (p. 130) | "near the capacity of each cache the model is too optimistic about the smaller one"; "too optimistic about the smaller cache". | The 5600X has no 96 MB cache to be "smaller" than, and "each cache" includes L1 and L2. The measured fact is simple: just above each capacity, measured latency is higher than the model's. The comparison between 32 and 96 MB is a separate inference (`part5:479`). | "Close to each cache's capacity the model's latency is too low, by up to 2.4 times." |
| M12 | Under-stated (positive half) and missing limit (negative half) | Abstract; `part1:182`; `part5:444`, `:587`; `part6:149` | Latencies "within about 20%"; "up to 2.4 times too optimistic". | L1 and L2 agree within 1% (4.0 and 12.1 cycles); only L3 and memory reach 9–20%, and "within about 20%" hides that. The 2.4× is at 32 MB, which App. G calls "the least repeatable part of the measurement" (24.1, 23.9 and 73.8 ns) and says "may partly reflect the virtual machine". Away from the edges the refit is close: 1.04–1.10 from 1.7 to 16 MB and at most 1.06 above 150 MB. | "L1 and L2 agree; L3 and memory are within about 20%." Add "(at 32 MB, under WSL2)" to the 2.4× at least in the abstract and Findings. |
| M13 | Overstated (label) | `part5:475` heading (p. 118); `tools/measurements/5600x-kit/README.md:47`; `research/measurements/5600X/ANALYSIS.md:15` | "An out-of-sample check on the group's Ryzen 5 5600X", followed by text saying the plateau comparison does not show "how good the model is". | Only the behaviour between plateaus is an out-of-sample test. | "A comparison with the group's Ryzen 5 5600X". Update the two tool documents (M16). |
| M14 | Inconsistent (wording) | Abstract (p. 4); `part1:176` (p. 32); `part3:152` (p. 61) | Memory access "is no longer uniform across the socket"; "a small, uniform latency cost"; "a small, uniform penalty". | Two different senses of "uniform" appear on neighbouring pages. | Abstract: "and NUMA behaviour across the socket". Keep "uniform" for the penalty only if "paid by every access" is added. |
| M15 | Inconsistent (K8, L21 partly fixed) | `glossary.tex:116`; `figures/topologies.tex` (p. 54) | Glossary: "the simulations of Part V call the same quantity the cost of a crossing". Figure: "any two dies 2 hops apart". | Part V and its figures now say "hop", and S4's hop is a whole CCD–IOD round trip. L21 changed the text to "two links apart" but not the figure. | Rewrite the glossary entry: in S4 a hop is one CCD–IOD round trip, 9 ns. Change the figure to "2 links apart". |
| M16 | Inconsistent (tool documents) | `tools/measurements/5600x-kit/README.md:33, 47, 48, 61`; `run_all.sh:30`; `ANALYSIS.md:15, 27, 113` | "Validating the model (S0)"; "Calibrating the model's overlap factor"; "about 30 minutes"; WSL2 "does not change the cache levels"; latency sweeps "about 12 minutes"; round trip 98.6 ns; memory "about 17 ns longer than the model's input". | The paper says it compares inputs, does not calibrate the overlap on this data, and that WSL2 "can add to the L3 and memory latencies". `notes.md` shows the whole run took 9 minutes. `c2c.csv` gives a median of 98.5 ns. App. G gives 14 ns above the input (17 above the output). | Bring the two files into line with App. G. |
| M17 | Minor (terminology; J27 residue) | `figures/cache-clock-model.tex:8` (p. 116); `figures/thread-placement.tex:11–14` (p. 143); `part4:101–194`, Figs 30, 34 | "Net speed-up of the V-Cache die"; "plain die"; "Keep on the V-Cache die". L3D is used nine times in Part IV, plus figures. | The glossary convention is cache die, V-Cache CCD and plain CCD. "V-Cache die" reads as the cache die. It says L3D is "called the cache die in this paper". | "V-Cache CCD" and "plain CCD" in both figures. Use L3D only when describing AMD's slide, and say so at `:101`. |
| M18 | Minor (L14 residue) | `figures/vendor-vs-independent.tex:24` (p. 102) | Lam's bar has an arrow to 1.24; the caption says arrows mean "upper end not stated precisely". | The paper's own value is 19.7% from the chart (`tab:lam-detail`), so the bar can end at 1.197. The arrow tip implies more than any result. | End the bar at 1.197, drop the arrow and remove the caption's clause. |
| M19 | Minor (chart reading) | `part6:61` (p. 131) | "10.65 ns for the 7950X3D's V-Cache CCD". | The label on Lam's chart reads 10.63 ns (rendered at 230 dpi). | "10.63 ns". |
| M20 | Overstated (minor) | `part4:178` (p. 85), `part4:305` (p. 94) | "The model, the measurement and the miss-class argument … agree"; the trade-off "predicts a gain of the right size". | The prediction is the bracket 3–14% from the textbook's 100–300 cycles, a range nearly five times wide that contains 4.9%. The measured value is inside it, which is all that was shown. | "brackets the measured gain". |
| M21 | Inconsistent (minor) | `part3:295` (p. 70) against `part6:219` (p. 144) | "can therefore be answered only qualitatively"; "answered only for link energy, and otherwise qualitatively". | The two parts state different limits for one answer. | Use the Part VI wording in both. |
| M22 | Writing (abbreviation) | `part2:288` (p. 47) | First use is "(WSL2)", unexpanded. | The expansion is at `part5:475`, seventy pages later. | Expand at `part2:288`. |
| M23 | Minor (method detail) | `appendix-g:35`, `:61` | Round trip is a "median of the 132 ordered pairs". | `c2c.c` records the *fastest* of three trials for each pair, while the latency sweeps use medians. App. G does not say so. The difference may favour low values. | Add "each pair's value is the fastest of three trials". |
| M24 | Minor | `part5:553` (p. 127); `tab:sim-parameters` (p. 157) | "280–296 GB/s" for "data that fits in the L3"; Hop row gives 9 and 37 ns only. | At 4 MB six threads read 276 GB/s, so the range holds only for 8–16 MB (App. G says so; S6 does not). The S4 runs now include 18 ns and 60 ns. | Add "(8–16 MB)". Add "varied in `tab:sim-split`". |
| M25 | Minor (wording of a ratio) | `part3:181`, `:376` against `part1:176`, `part6:217` | "about 4.5 times slower" against "about 4.5 times as long" and "as slowly". | "4.5 times slower" is loose and differs from the other two. | "takes about 4.5 times as long". |
| M26 | Figure (minor; L26 residue) | `fig:sim-pingpong` (p. 125); table captions | The legend's lower right corner still hides a short piece of the model curve, near 140 ns. Of 55 table captions, 9 end with a full stop and 46 do not. | Rendered at 220 dpi; captions counted from the sources. | Shrink the legend or end the plot at 200 ns. Choose one caption style. |
| M27 | Format (layout) | p. 154 | The end of App. C spills four lines onto its own page, adding the 165th page. | Rendered text. | Trim four lines in App. C. |
| M28 | Structure (repetition) | 5600X framing: `part5:444`, `:475`, `:584`, `:587`, `part6:149`, `:192`, `appendix-g:74`, Fig. 52 caption. `part4:268` against `appendix-c:66`; `part2:390` against `appendix-f:33` | The same framing appears eight times. Whole sentences repeat between the main text and appendices ("This is how AMD describes its products…"; "A directory therefore trades latency for bandwidth…"). | L1 asked for it to be stated once and reused; the repeated form now costs reading time. | Keep it in S0, the limits section and Threats; shorten elsewhere to a clause and a cross-reference. Delete the duplicated sentences from the main text. |
| M29 | Structure (half-page rule, at submission) | `sec:bandwidth-example` (p. 65); `sec:clock-correction` (pp. 113–114) | Worked examples of about 0.75 page each, with table and figure. | These are not among the four kept by decision (L24). | Decide at submission; both can stay if they are treated as part of the argument. |

**Writing: suggested rewrites (in addition to M11, M14, M25).** A script found 44 sentences of 55 words or more; the ten below are worth changing.

| Location | Length | Rewrite |
|---|---|---|
| `part5:440` (p. 115) | 74 words, new since L16 | Move the bracket on 1.9% and 2.0% into its own sentence, and start a new one at "while the refined model predicts". |
| `part5:58` (p. 99) | 69 | Put the eleven percentages in a short table or split after "7-Zip compression and decompression". |
| `part2:190` (p. 43) | 66 | End after "either a square tile or a row can be read in one access". |
| `part2:102` (p. 39) | 66 | End after "connect it to a pair of complementary bit lines". |
| `part4:305` (p. 94) | 64 | End after "(`tab:stack-yield`)". Start "The economic case therefore rests mainly on product flexibility". |
| `appendix-g:57` (p. 163) | 64 | Split at each semicolon. |
| `appendix-c:23` (p. 152) | 64 | End after "67.9%)". Start "For the 592 mm² die …". |
| `part6:113` (p. 136) | 63 | Give the definition of tiling a sentence of its own. |
| `part6:61` (p. 131) | 63 | End after "53 against 702 GB/s". Move the clause on 4.8 GHz into a second sentence. |
| `part6:223` (p. 145) | 62 | End after "for the libx264 example". Start "The 7% clock gap of the Zen 4 Ryzen 9 7950X3D raises it…". |

Abbreviations: eDRAM, TSV, PBO and ω are defined at first use; "MLP" as an abbreviation is not used; WSL is M22. No sentence attributes work to an individual, and no gendered pronouns occur (searched in all `.tex` files). Tense is consistent.

---

## 3. Regression check

| ID | Status | Note |
|---|---|---|
| L1 | Fixed | Body is clear and consistent in the abstract, Part I, method, S0, limits, summary, Threats, evidence row and App. G. Residue: M11–M13. |
| L2 | Fixed | `part5:343`, `tab:confound-grid` and `:369` agree. |
| L3 | Fixed | `appendix-c:66`. Recomputed: 139.3/154 = 0.904 for both. |
| L4 | Fixed | `part6:166`. |
| L5 | Partly fixed | Caption is coherent; first row and `:160` do not fit it (M6). |
| L6 | Partly fixed | Text in Parts I, III and VI fixed; table, legend and mind map not (M5). |
| L7 | **Fixed, with a regression** | Table and text correct; "The second figure" is now wrong (M1). |
| L8 | Fixed | App. G matches the raw runs. |
| L9 | Fixed | `part2:288`, `appendix-f:56`. |
| L10 | Fixed | "wide range" in all three places. |
| L11, L12, L13 | Fixed | |
| L14 | Fixed | Bar ends at 3.94×. Lam's arrow remains (M18). |
| L15, L16, L17, L18 | Fixed | |
| L19 | Partly fixed | Definition moved before "arrangement", but other first-generation uses remain (M7). |
| L20 | Fixed | |
| L21 | Partly fixed | Text fixed; `fig:topologies` still says "2 hops" (M15). |
| L22 | Kept by decision | One sentence; the mind-map node remains. |
| L23 | Fixed | |
| L24 | Kept by decision | |
| L25 | Fixed for the listed repeats | New repetition: M28. |
| L26 | Partly fixed | `fig:l3-miss-path` clear; pingpong legend still touches the curve (M26). Named captions fixed. |
| L27 | Fixed | S6 lacks the range (M24). |
| L28, L29 | Fixed | |
| Long sentences | Fixed | All twelve split. `part5:440` is new (above). |

**K and J items.**
- K1 is fixed in the body (M12 and M13 remain). K3's rewording produced a new contradiction (M3). K8 and K11 have residue under M15 and M7. K2, K4–K7, K9, K10 and K12–K21 hold.
- J items checked in the text they touch: J1–J3, J5–J14, J16–J19, J21–J26, J28, J29, J31–J33. All hold, except that J3's correction now reads as a physical comparison (M2).
- **J27 has regressed slightly in two figures** (M17). J2's clause on (B) is now correct.
- J4 and J15 hold in App. E and the README. J20 is superseded by M28. J30 concerns draft-status lines and remains as listed in §8.

---

## 4. Simulation and measurement check

### 4.1 Reproduction

- Built with MSYS2 UCRT64 `g++ -O2 -std=c++17`. `--selftest`: **8 passed, 0 failures**.
- `python test/check_golden.py`: **15 of 15 cases identical** to the stored JavaScript results (run 2026-11-08, Node v22.23.4). **No warning**: the SHA-256 of `gui/sim-core.js` equals the one in the golden file.
- `sims.py --only s0 s4 policy` (2 min 39 s): `s0_calibration`, `s0_latency_sweep`, `s4_pingpong`, `s4_split`, `s1_policy` are **byte-identical** to `research/measurements/cachesim/`.
- `compare_5600x.py`: `model-comparison.csv` **byte-identical**; `m5600x-latency.tex` and `m5600x-table-mlp.tex` differ from the paper's only in line endings.
- `make_figures.py` run on the stored CSV files: all 15 `sim-*` figure and table files match the paper's apart from line endings, including `tab:sim-split` and `fig:sim-pingpong`.
- `tab:sim-split` against `s4_split.csv`: 1.2021, 1.2622, 1.3890 and the private rows agree. The 9, 37 and 60 ns rows are unchanged in value from the sixth review's data.

### 4.2 5600X numbers checked against the raw files (all match)

| Claim | Raw value (median of three runs) |
|---|---|
| L1 0.87 ns, 4.0 cycles | 0.868 ns; × 4.614 = 4.0 |
| L2 2.61–2.69 ns, 12.0–12.4 cycles | 2.614 and 2.695 ns; 12.06 and 12.43 |
| L3 11.1–12.0 ns, 51–55 cycles | 11.085 and 11.961 ns; 51.2 and 55.2 |
| 1 GB 98.6 ns; 4 KB pages 115.3 ns | 98.562; 115.335 |
| Translation about 17 ns | 16.77 |
| 4 KB rise from about 7 MB | 12.91 against 11.51 ns at 6.7 MB |
| Model 82 ns at 1 GB; input 84 ns | 81.85; 47/4.614 + 74 = 84.2 |
| Up to 2.4× at 32 MB | 24.096/10.066 = 2.39 |
| Refit within 5% and 1% | 1.04–1.05 from 4 to 16 MB; 1.00 at 1 GB |
| Refit 1.2–2.1× at 19–38 MB | 1.22, 1.28, 1.47, 2.08, 1.67 |
| Refit 1.1–1.3× at 45–108 MB | 1.31, 1.24, 1.18, 1.13, 1.19, 1.12 |
| 64 MB: 66.9 against 56.6 ns | 66.859; 56.593 |
| 32 MB runs: 24.1, 23.9, 73.8 ns | 24.096, 23.936, 73.761 |
| Slow 2 MB run: from 19 MB; ×3 at 32 MB; 3–7% from 150 MB to 1 GB | 1.52× at 19 MB; 3.07×; 1.03–1.07 |
| Overlap 0.349, 0.113, 0.071; L3 0.077 | 0.349, 0.113, 0.071; 0.077 |
| Single chain 104.9 ns; per step 105 to 120 ns | 104.88; 104.9 to 119.7 |
| One thread L3 108 GB/s; memory 30 GB/s | 108.01; 30.29 |
| Six threads 41 GB/s; 80%; 6.8 per core | 40.95; 80%; 6.83 |
| Six threads 280–296 GB/s, 8–16 MB | 279.77; 295.79 |
| Twelve threads erratic, 0.1–480 GB/s | 0.14 to 480.61 |
| c2c median 98.5 ns; CPU 0 as responder 66–72 ns | 98.5; 65.8–72.1 over 11 pairs |
| Clock 4.614 GHz before and after | both 4.614 |

The time per step stays between 118 and 120 ns from 8 to 16 chains, so the data do not suggest a limit below sixteen outstanding misses: "at least sixteen" is supported.

### 4.3 Model description (Appendix E against `cachesim.cpp`)

| Statement | Code | Verdict |
|---|---|---|
| Write hit with other holders: one L3 latency, plus the hop if a holder is on another die | lines 364–365 | Correct |
| L3-only copies invalidated at no cost | line 368 | Correct |
| Another group's L3 or core: two L3 latencies plus the hop | lines 293, 309, 318 | Correct |
| DRAM adds the hop only in the two-die configuration | line 334; `twoccd` sets `dram_hop` | Correct |
| ω scales the part beyond an L2 hit | line 373 | Correct |
| Ping-pong ignores its first 40 accesses | line 634 | Correct |
| Calibration: 0.335, 0.202, 0.105; about 103 cycles | recomputed: 0.3354, 0.2017, 0.1047; 102.8 | Correct |

### 4.4 Measurement kit against Appendix G

| Statement | Program | Verdict |
|---|---|---|
| Randomly ordered cyclic chain of 64-byte lines | `latency.c` | Correct |
| k chains, 1 to 16, at 1 GB and 16 MB, 2 MB pages | `latency.c` MLP mode, `run_all.sh` | Correct |
| Read and triad, 16 KB to 256 MB, 1/3/6/12 threads | `bandwidth.c`, threads on slices of one buffer | Correct |
| Two threads write a shared counter in turn, all pairs | `c2c.c`; `cpu_b` is the responder | Correct, but see M23 |
| Clock from dependent additions | `clock.c` | Correct |
| WSL2, slow third 2 MB run, 12-thread values, CPU 0 pattern | raw files | Correct; cause overstated (M9) |

The pointer-chase workload is deferred, as decided. No text claims that the model reproduces a cyclic chase. `appendix-g:65` comes closest, and says only that a cyclic workload shows the same LRU effect, while `part5:479` and `:579` say the random workload does not reproduce it.

### 4.5 Calibration against validation

S0's Milan comparison, the S3 libx264 check and the S4 37 ns are labelled as fitted in their own sections. Remaining problems: M2 (the 37 ns read as a physical cost), M4 (0.38 as support), M13 (label), M20 (a wide bracket described as a prediction). The genuinely out-of-sample results are the capacity-edge differences and the 49 against 98.5 ns round trip. Both are stated, and both are unfavourable to the model, which is to the paper's credit.

---

## 5. Spot-checked numbers (31; different from the fifth and sixth reviews' lists where possible)

| # | Claim (location) | Source and place | OK? |
|---|---|---|---|
| 1 | Eleven TechSpot percentages, 22 to 23% (`part5:58`) | TechSpot 5800X, each benchmark's text | ✓ |
| 2 | 50.7 GB/s; 68.8 and 61.8 ns (`part5:60`) | FPS Review p. 6 screenshots, rendered | ✓ |
| 3 | 633 and 631 GB/s; 9.9 and 10.9 ns; 4.40 and 4.85 GHz | same | ✓ |
| 4 | 25 workloads, 4 GHz, 3800XT, DDR4-3600 (`part5:56`) | AMD launch release, note 4 | ✓ |
| 5 | 5 cycles; 3–4 cycles; 3.3 and 3.15 GHz; 7.6%, 12.5% | Cozma 2022b, text | ✓ |
| 6 | L3 47.49 and 51.14 cycles (`part5:190`) | Cozma 2022a, chart labels, rendered | ✓ |
| 7 | Slice offsets 0, 6, 1, 10, 6, 13, 10, 20; 40 cycles | 7-cpu, text | ✓ |
| 8 | 4.8 and 5.15 GHz; 7%; 1.48, 5, 5.5, 0.35, 0.28 MPKI | Lam, text | ✓ |
| 9 | 34.18 ns; 53 and 702 GB/s (`part6:61`) | Lam charts, rendered (53.10, 701.67) | ✓ |
| 10 | 10.65 ns (`part6:61`) | Lam chart: 10.63 | **✗ M19** |
| 11 | Over 30 ns; about 50 GB/s; a quarter; 64 GB/s; 51.2 GB/s | Lam, text | ✓ |
| 12 | Genoa-X against Genoa 0.98–1.60× | Lawenda Table 6 | ✓ |
| 13 | 64-core Genoa against Milan-X 1.24–1.70×; Genoa-X up to 2.67× | Lawenda Table 6, text | ✓ |
| 14 | Clock ranges 2.9–3.2, 2.8–3.0; 3.4–3.5, 3.2–3.4; misprint | Lawenda Table 5 | ✓ |
| 15 | 10–15% to 80% miss rates; five repeats | Lawenda, text | ✓ |
| 16 | 9.56× geometric mean; 280 W | Domke, text and table | ✓ |
| 17 | 310 and 1446 GB/s; 75%; 14×, 6×, 3.8×; 4.8×; 1.6× worse | Reguly, text | ✓ |
| 18 | Cloud VM warning; latencies did not improve | Reguly, text | ✓ |
| 19 | 13%, 55%, 66%, 0.08 °C; 15% and 15%; 34% and 8% | Black, text | ✓ |
| 20 | 11.4/5.0 mm²; 6.6/6.9 ns; 3.3/11.9 ns; 0.18/1.13 nJ; 463/65 mW; 26% | Kim Table 1, text | ✓ |
| 21 | 55 GB/s at 1.46 GHz; 14.6 GT/s; 13 FCLKs, under 9 ns; 19%; 2 pJ/bit | Naffziger, text | ✓ |
| 22 | About 1000 mm²; 204.8 GB/s; eight channels | Suggs slide 19, rendered | ✓ |
| 23 | 1.04×–1.25×, five games, 4.0 GHz, 15% | Swaminathan slide 19, rendered | ✓ |
| 24 | Six games, 1.36× to a tie, about 15%; 24.4 and 40.6 jobs/hour, 66% | Wuu slides 29, 31, rendered | ✓ |
| 25 | 9554, 9654, 9684X, 9184X, 9224, 9174F rows | EPYC 9004 datasheet, rendered | ✓ |
| 26 | 3.22%; 4.5–4.55 GHz; "very similar"; ring-to-fabric step | CapFrameX, text | ✓ |
| 27 | 5700G 4.6 GHz, 65 W; PCIe 3.0; 10% and 9% | TechSpot 5700G, text | ✓ |
| 28 | 2.45 and 2.20 GHz, 3.5 GHz boost | Phoronix 7773X, text | ✓ |
| 29 | 420 tests; "a small set of tests"; tConvolve 294% | Phoronix 5800X3D, text | ✓ |
| 30 | 1.2 and 1.1 V; 1.4 V, 1.28–1.31 V; 10 and 70 MHz; 300 and 500 MHz | Cozma 2024, text | ✓ |
| 31 | Pitches below 150, 40, 9 µm; D2W "need not be same size"; 7 nm on 5 nm | Lambert slide 13; Alam, text | ✓ |

**Worked examples recomputed (all correct except M1's reference).** Yields 82.4, 68.8, 86.6, 38.3, 85.4, 92.2, 79.1%; triangular 82.1, 67.9, 34.4%; chiplet split 0.64; 44% and 63%; dies per wafer 955.2 − 77.5, 119.4 − 27.4, 95, 35, factors 2.7, 1.9, 3.5; `tab:stack-yield` 94.8, 44.5, 139.3, 154, 155; 5% and 14%; **App. C product line** 100/108/121 and 101/110/124, 0.7–3%, 90.3–90.5% threshold, 140.7 and 146.6; `tab:cache-clock-model` all rows and break-evens 0.12, 0.35, 0.50, also 0.10 at 4.8 and 5.15 GHz, 30% and 26% memory share (the 0.6 row gives 5.3% or 5.4% depending on rounding of the inputs); **App. F** 18 messages, 35 and 315 deliveries, 24 576 pages, 12×, reach 256 KB, 8 MB, 128 MB, 4 GB; `tab:lam-per-miss` 50, 80, 130; 11.4% and 9.4%; AMAT 1.60, 1.46, 1.38 and 0.56, 0.53, 0.45; Amdahl 5.9, 9.1, 15.4; depth 13; pad densities 772, 12 346, 44, 16×, about 280×, 5 and 92 mm²; link powers 0.9, 3.3, 7.4 W and 2%; 3.7 CCDs; 8.25 slice cycles; 2.05, 0.62, 0.71 TB/s; DCS 3.2, 3.7, 15%, 0.24; 0.12, 0.53, 0.80 s; 206 ns and 11×; MiniFE 245–310 and 275–330 bytes; clock corrections 1.62, 0.85, 1.13, 0.99; 5.5%, 18–26%; 1.98; 1008 mm².

**Internal consistency (brief item 5).** All listed quantities were checked and agree: V-Cache 4 cycles and 96 MB; 7%/1.073 and 4.8/5.15 GHz; 130 and 103 cycles; break-evens 0.1 (0.12), 0.35, 0.50, and simulated 0.04, 0.38; 9, 18, 37 ns; 1.20/1.26/1.39×; 58.6, about 265, 49, 98.5 ns; about 2%; the 5600X values; 100/108/121, 0.7–3%, about 90%. The exceptions are M1 and the wording items M14, M21, M25.

**Citations.** All 36 cited keys are in `references.bib`, each with a README row marked present and the file on disk. The only uncited bib key is `swaminathanNextFrontierEnabling2022`. No citation was found to support a claim its source does not make. Vendor attribution is sound apart from M5.

---

## 6. Research questions and argument

| RQ | Answered in Conclusions? | Supported? | Consistent with `tab:evidence-strength`? |
|---|---|---|---|
| RQ1 | Yes (`part6:215`) | Yes: models, reticle statement, uneven scaling | Moderate; see M6 |
| RQ2 | Yes (`:217–219`) | Yes on latency, bandwidth, sharing and flexibility. Power is an estimate and says so. | Yes; M2 and M5 affect wording |
| RQ2a | Yes, inside RQ2 | Yes, with AMD's reasoning attributed | No separate row; adequate |
| RQ3 | Yes (`:221`) | Yes for capacity and latency. Thermal evidence is indirect, as stated. | Yes |
| RQ4 | Yes (`:223`) | Direction and latency well supported; size moderate; model illustrative | Yes, apart from M4 |

**Overreach.** M2, M4, M8, M9, M10, M13, M20. Chart readings are labelled, and vendor claims are otherwise attributed. **Over-hedging.** Only M12. The hedging elsewhere is now proportionate, and L29's firm results read as firm.

**The three weakest links, and what would fix each.**
1. **How much a stacked cache helps in general.** The only fully controlled evidence is six workloads on one processor, from one outlet. The paper says so. More evidence would need a broad fixed-clock study, which is out of reach here; the fix is to keep the wording it has and add M8.
2. **The break-evens rest on one program and borrowed clocks.** The 0.35 uses libx264's 130 apparent cycles and clocks Lam measured under a different load. The simulated 0.38 adds no independence (M4), and the realistic range across Lam's workloads is threefold. Presenting the headline as "of order 0.1 to 0.4 for this program" would match the evidence.
3. **Power and heat, in a question that names power.** RQ2's answer rests on the predecessor link's 2 pJ/bit. RQ3's Conclusions paragraph gives no energy result for the stacked cache, and the thermal argument is inferred from clocks, AMD's redesign and a 2006 simulation. One sentence in RQ3 saying that no energy or thermal measurement of a V-Cache part was found would close the gap in the argument.

**Anything important still missing.** Only that item: no energy or power measurement of a V-Cache part appears, so "power" in the central question remains partly open. The datasheet pair at `part4:218` (400 against 360 W) is the only direct indication.

---

## 7. Page counts per part (PDF pages)

| Part | Pages | Count | Target | Comment |
|---|---|---|---|---|
| Front matter | 1–24 | 24 | — | In order |
| I Introduction | 25–34 | 10 | 10 | On target |
| II Foundations | 35–54 | 20 | 25 | Short by 5, mostly moved material |
| III Chiplets | 55–74 | 20 | 25 | Short by 5 |
| IV Stacked cache | 75–95 | 21 | 25 | Short by 4 |
| V Case study | 96–130 | 35 | 25 | Over by decision |
| VI Synthesis | 131–145 | 15 | 20 | Short by 5 |
| **Body** | 25–145 | **121** | 130 | Short by 9; no padding is advised |
| References | 146–148 | 3 | — | |
| Appendices A–G | 149–164 | 16 | — | App. C now runs to p. 154 (M27) |
| Index | 165 | 1 | — | |

Each part does one job and hands over cleanly. Part V now opens with its method, and Appendices C, F and G carry the moved material without loss. Part VI is the natural place for the extra pages if they are wanted, and the power point in §6 is the obvious content.

---

## 8. What was checked and found correct

**Format.** A4 (595.3 × 841.9 pt); `12pt` class option; `\singlespacing`; one-inch `geometry` margins, with side margins measured at 0.98–0.99 in on four pages; order cover, copyright, acknowledgements, abstract, contents confirmed on pp. 1–5; contents, lists of tables and figures, glossary and index generated. All diagrams are TikZ or pgfplots (the only image is the logo). There are no waveforms. Code appears only through `lstlisting`.

**Leftovers.**
- Two `\todo` notes: App. A (p. 149) and App. B (p. 150), known placeholders, not counted as errors.
- Cover line "Second Full-Paper Working Draft (initial-draft-2)" and PDF title "(working draft)": correct for now, to change at submission.
- The `\partbudget` macro with "Target length" remains defined at `preamble.tex:23–25` but does not print. "(target: about N pages)" remains only in source comments on line 1 of each part.
- No `\verify` use, no "??", no undefined references or citations, no overfull boxes. "Placeholder" at `part5:582` is a description of the unused energy model, not a leftover.

**Float placement.** Of 119 floats, 8 sit exactly two pages from their nearest reference (Figs 2, 15, 34, 41, 62; Tables 22, 26, 44). One is three pages from its first reference: `tab:llc-alternatives` is on p. 134, first cited on p. 131, because the mind map and Table 44 come between; it is cited again on p. 135. Appendix tables cited from the main text and forward references from Part I lie further away, as intended. Sparse pages are p. 95 (end of Part IV), pp. 149–150 (placeholders), p. 154 (M27) and p. 161 (table at the end of App. F).

**Figures.** All 61 figure pages were read, including `fig:m5600x-latency`, `fig:sim-zen2-zen3` and its shared legend, `fig:sim-pingpong`, `fig:l3-miss-path`, `fig:vendor-vs-independent` and all 13 mind maps. Problems are limited to M15, M17, M18 and M26. The mind-map style and text sizes are unchanged since the sixth review's estimate of about 7.3 pt at the narrowest, and no node adds a claim the text lacks. Every figure and table is referenced. Captions say what the reader should see.

**Correct in the material new since the sixth review.** The 5600X framing in substance (L1, L29); S4 with the 18 ns row; the L2, L3 and L4 arguments; the rewritten Part IV deficit paragraph; the App. G repeatability text; the Node-free crosscheck, which works as the response describes.
