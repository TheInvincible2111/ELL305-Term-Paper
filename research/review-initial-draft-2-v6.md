# Sixth review of initial-draft-2 (8 November 2026)

Brief followed: `research/review-prompt-initial-draft-2-v6.md`, applied to the 164-page draft. Findings continue the series as L1, L2, ….
Only local files were used; nothing on the web. No project file other than this report was changed; all reruns went to a temporary folder.
Page references are **PDF viewer pages** of `build/pdf/ELL305-initial-draft-2.pdf` (the printed page number is one lower). Line references are to `initial-draft-2/` unless a full path is given; `part5:343` means `sections/part5-case-study.tex`, line 343.

**Build currency.** The PDF was built on 8 Nov 2026 at 18:25:38 (file time 18:25:56). No file under `initial-draft-2/`, `paper/` or `references/` is newer, so the PDF matches the sources. Build log (`tmp/linux-build/main-initial-draft-2.log`): 164 pages, no errors, no undefined references or citations, **0 overfull boxes**, 33 underfull boxes.

**What this review did not do.**
- `test/crosscheck.js` (C++ against JavaScript) could not be run: Node.js is not installed in Windows or WSL here. Its claimed pass remains unverified by any review.
- Reproduction covered the brief's minimum: `sims.py --only s0 s4 policy` and `compare_5600x.py`. The fifth review reran the rest. The simulator source is unchanged in behaviour as far as those reruns show, but S1–S3, S5 and S6 were not rerun in this pass.
- All 61 pages carrying figures were rendered at 125 dpi and read, two pages per view. Pages holding only tables and text were checked from the sources, not rendered.
- The glossary was searched, not read through. `Gem5/` is out of scope.

---

## 1. Overall assessment

The paper remains strong for an undergraduate term paper, and I would hold it provisionally at A−. The fifth review's corrections are nearly all present, the reruns are byte-identical, the 5600X numbers match the raw files, and the moved material resolves correctly. What remains falls into two groups. First, the 5600X result is now honestly hedged, but its positive half still does not mean what it says: the "structure of the hierarchy" and the plateau values are the model's own inputs echoed back, so the only place the model's logic is exercised against this machine is between the plateaus, where it is off by up to 2.4 times. Second, there is a small cluster of plain mistakes that a careful examiner would catch: one sentence that contradicts its own table (L2), one wrong claim in an appendix worked example (L3), a monolithic-against-chiplet comparison that is not like for like (L4), and an evidence table whose grades break the rule in its own caption (L5). None of these undermines a main conclusion, and each is a sentence-level or row-level fix.

**The two changes that would improve the paper most:**
1. Say what the 5600X comparison actually tests (L1): the plateaus compare two Zen 3 chips, and the model's behaviour is tested only near capacity edges, where it does poorly.
2. Clear L2–L5, which are the errors most likely to be found by someone checking the paper against itself.

---

## 2. Findings (most severe first)

| ID | Severity | Location | What the draft says | What the source, CSV, code or rule says | Suggested correction |
|---|---|---|---|---|---|
| L1 | Overstated (remaining part of K1 and I10) | Abstract `front-matter.tex:49` (p. 4); `part1:181` (p. 33); `part5:14` (p. 96, "tested"); `part5:444` (p. 116); `part5:475` (p. 118–119); `part5:584`, `:587` (p. 130); `part6:149` (p. 139–140), `:192` (p. 142); `appendix-g:74` (p. 163); caption `figures/m5600x-latency.tex:24` | "With nothing fitted, the model reproduces the staircase"; "gets the structure of the hierarchy right and its level latencies within about a fifth"; the measurements "test the model's structure and inputs". | `compare_5600x.py` runs preset `zen3_1ccx`, whose capacities (32 KB, 512 KB, 32 MB) are this chip's published sizes. A staircase with steps at those sizes is therefore guaranteed. On a plateau the model's output is simply its input, so "within about 20%" compares 7-cpu's 5600G latencies with the 5600X. That is what `part5:475` already says of L1 and L2, but the same applies to L3 and memory, and the Abstract, Findings, `:584`, `:587` and the evidence row do not carry even the L1/L2 caveat. The model's own logic (replacement, placement, mixing of hits and misses) acts only between plateaus, and there `model-comparison.csv` gives measured ÷ default of 2.24 at 38 KB, 1.51 at 724 KB and 1.40–2.39 from 19 to 38 MB. This is the same kind of test that can barely fail as K10. | State it directly once and reuse it: "The model's capacities and level latencies are inputs, so its plateaus show how close another Zen 3 chip's published latencies are to this one's (0–20%). Its own behaviour is exercised only between plateaus, where it differs from the measurement by up to 2.4 times." Replace "tested on" (`part5:14`) with "compared with", and "test the model's structure and inputs" with "compare the model's inputs and its behaviour near capacity". |
| L2 | Error (contradiction) | `part5:343` (p. 112) against `part5:354`, `:369` (p. 113), `part4:278` | "The fixed-frequency prototype comparison controls clock speed but not core count." | `tab:confound-grid` gives the prototype ✓ for Cores. `part5:369`: "holds both clock (4.0 GHz) and core count (12) constant". `part4:278`: "12-core 3D-chiplet prototype with the 12-core Ryzen 9 5900X". | "The fixed-frequency prototype comparison controls clock speed and core count but does not state the memory configuration." |
| L3 | Error (arithmetic of the argument) | `appendix-c:66` (p. 153) | Strategy (C) loses its advantage over (A) for V-Cache parts below about 90% bonding yield, "and it loses its small silicon lead over (B) sooner still". | For a V-Cache part both (A) and (B) cost 154 mm², and (C) costs 139.3/Y. So (C) falls behind (B) at exactly the same Y = 139.3/154 ≈ 90.5%, for any p, since the 32 MB parts cost 94.8 mm² in both (B) and (C). It is not "sooner". | Delete "and it loses its small silicon lead over (B) sooner still", or write "and at the same point it loses its small silicon lead over (B)". |
| L4 | Overstated (unlike comparison; one premise cannot be verified) | `part6:166` (p. 138) | "a monolithic Xeon's adjacent cores exchanged data in about 106–110 ns against about 265 ns between EPYC CCDs", offered as "the only evidence" that a monolithic die stays faster for fine-grained sharing. | The Xeon figure is the *nearest* pair of cores; the 265 ns is EPYC's cross-CCD pair. The like-for-like nearest-pair value on EPYC is 58.6 ns, *faster* than the Xeon (`tab:core-to-core`), and Reguly reports no far-apart pair on the Xeon. In the same table a Xeon that Reguly calls chiplet-based (Max 9480, Reguly p. 3) is faster on adjacent cores (84 ns) than the 8360Y. Reguly does not state that the 8360Y is monolithic: **cannot verify** from local files. | Say the sources contain no like-for-like measurement: "A monolithic die is expected to remain faster for sharing across the whole die, because transfers between CCDs cross the IOD (`sec:d2d`), but the sources do not measure this: Reguly reports only adjacent cores on the Xeons." |
| L5 | Inconsistent (grades against the table's own rule) | `tab:evidence-strength`, `part6:137–154` (p. 139–140) | Caption: strong = independent, controlled and replicated; moderate = one missing; weak = vendor-only, uncontrolled or modelled with illustrative inputs. | Four rows break this. "Cost per good die": illustrative models plus a vendor chart, graded Moderate. "Chiplets add a hop": "vendor-described", graded Moderate. "One compute die": datasheet facts, vendor-only, graded Strong. "First-generation stack carried a thermal cost": uncontrolled and indirect, graded Moderate. `part6:160` then builds on these grades. | Either regrade these rows, or change the caption to say that mechanism claims and product facts are graded differently from performance claims, and give that rule. |
| L6 | Overstated (vendor figure, single cause) | `part6:166` (p. 138), `part6:217` (p. 143), `part1:176` (p. 32), `part3:152`, `tab:thought-experiment` (p. 27) | "a central I/O die made Rome's average memory latency about a fifth lower"; "because the central IOD removed the long, uneven paths". `part1:176` and the thought-experiment table state 19% and "under 9 ns" with no attribution. | Naffziger, as the paper itself records at `part3:113` and `tab:amd-reported`, attributes the 19% to the central IOD, decoupled clocks and the latency-optimised link together, and it is AMD's own figure comparing different generations. The brief requires vendor claims to be attributed. | "AMD reports that Rome's average memory latency was 19% lower than Naples's, which it attributes to the central I/O die, decoupled clocks and the optimised link." Add "AMD reports" in `part1:176`. |
| L7 | Inconsistent | `part5:538` (p. 125), `tab:sim-split` (p. 126) against `part5:532` | Shared data costs "1.20 times … with a 9 ns hop". | `part5:532` says one transfer between CCDs takes at least 18 ns, two of AMD's round trips, and the hop is charged per transfer. So 9 ns is half the paper's own lower bound for sharing, though right for memory accesses. Interpolating the table gives about 1.25–1.26× at 18 ns. | Add an 18 ns row, or present 1.20× as a lower limit that undercounts the link. |
| L8 | Overstated (understates the raw spread) | `appendix-g:71` (p. 163) | "The three runs … agree within about 1–3% except close to a cache's capacity. Close to the L3's capacity one of the three 2 MB-page runs was slower." | 2 MB run 3 is slower from 19 MB all the way to 1 GB: by 3–7% from about 150 MB to 1 GB (e.g. 103.5 against 96.9 ns at 609 MB) and by a factor of 3 at 32 MB; `notes.md` says "from about 19 MB upwards". 4 KB runs differ by up to 31% at 256–512 KB and by 6–29% at 8–27 MB. The median does remove run 3, but not "only close to capacity". | "One of the three 2 MB-page runs was slower from about 19 MB upwards (by a factor of up to 3 at 32 MB and by 3–7% from about 150 MB to 1 GB); the median removes it. The 4 KB runs differ by up to about 30% near the TLB and cache limits." |
| L9 | Overstated (drops a stated limit) | `part2:288` (p. 47), `appendix-f:56` (p. 159) | "at 1 GB address translation adds about 17 ns to every access". | The value is 115.3 − 98.6 ns under WSL2. `appendix-g:72` says the virtual machine's second level of translation can add to latency, and huge pages may be only partly granted. It is this VM's figure, not Zen 3's. | "…adds about 17 ns under WSL2, whose nested translation probably inflates it." |
| L10 | Inconsistent (K5 partly fixed) | `part1:176` (p. 32); `part3:375` (p. 73); `part6:217` (p. 143) | "within each generation one compute die serves the whole product range, from desktop parts to 64-core (Zen 3) or 96-core (Zen 4) servers". | `part3:329` and RQ2 limit the claim because Zen 4c parts use a different die. `part1:176` has no such limit, and "whole product range" remains in all three places while the text admits it is not the whole range. `tab:product-matrix` has no Zen 4 desktop row. | "one compute die serves a wide range of products". |
| L11 | Inconsistent | `part6:174` (p. 141) against `tab:stack-yield`, `tab:product-line-silicon`, `part4:265–267` | "The paper therefore makes no quantitative claim about the cost of stacking". | The paper gives "about 10% less silicon", "a third of the silicon" and "0.7–3%". | "makes no quantitative claim about the money cost of stacking; its silicon-area examples are illustrative". |
| L12 | Overstated | `part6:172` (p. 141) | "The paper uses vendor figures only where nothing independent exists". | AMD's 15%, 66% and 4 cycles are all used beside independent results (`tab:amd-reported`, `part4:150`). | "The paper labels vendor figures as such and prefers independent results where they exist." |
| L13 | Inconsistent | `part4:148` (p. 83) against `part4:118`, `:150`, `:192`, `:300` | "AMD reports up to 2 TB/s". | Wuu slide 20 and every other mention: more than 2 TB/s. | "more than 2 TB/s". |
| L14 | Inconsistent (figure against text) | `fig:vendor-vs-independent` (p. 102) against `part5:313` | Phoronix's bar ends with an arrow at about 1.6×; the caption says its upper end is "50% or more" and that arrows mean "upper end not stated precisely". | `part5:313` gives the top result, 294% (3.94×), and the axis reaches 4. | Extend the bar to 3.94 and drop the arrow. |
| L15 | Inconsistent (K15 partly fixed) | `part5:497` and the caption of `fig:sim-working-set` (p. 121) | "the model's random workload sends every access to the L3"; "every access in these synthetic workloads reaches the L3 or memory". | K15's correction ("almost every access … once the working set is well above the L2") was made only at `part5:491`. | Apply the same wording in both. |
| L16 | Minor (two values, unexplained) | `tab:cache-vs-clock` (p. 115) against `part5:440`, `tab:cache-clock-model` | The linear rule gives libx264 −2.0% in one place and −1.9% in the other. | −2.0 = 1.049/1.07; −1.9 = 1.052/1.073. Both correct, but a reader sees one rule with two answers. | Add "(−1.9% with the model's 5.2% and the measured 1.073)". |
| L17 | Minor (unexplained difference) | `tab:m5600x-levels` (98.6 ns) against `tab:m5600x-mlp` (104.9 ns), `appendix-g:57` | Single-chain 1 GB latency differs by 6% between two tables. | Same program family, same page size, same buffer. `mlp.csv` medians 104.9 ns; 2 MB sweep 98.56 ns. Not mentioned. | One clause saying the two runs differ and that fractions use 104.9 ns as the base. |
| L18 | Minor (chart reading) | `part2:288`, `appendix-f:56` | With 4 KB pages latency rises "again above 8 MB". | 4 KB against 2 MB is +12% already at 6.9 MB (12.91 against 11.51 ns), and +25% at 8 MB. | "from about 7 MB". |
| L19 | Writing (K11 partly fixed) | `part4:216`, `:218`, `:220` (p. 88–89) against `:224` | "first-generation arrangement" is used three times before it is defined. | K11 asked for one definition. | Move the definition sentence before `:216`. |
| L20 | Writing (ambiguous) | `part1:178` (p. 32), `part5:587` (p. 130) | "Memory-bound simulation gains up to 1.5–1.6×". | These are OpenFOAM measurements on real hardware. In a paper with its own simulator, "simulation" reads as model output. | "memory-bound computational fluid dynamics (OpenFOAM)". |
| L21 | Writing (terminology) | `part2:441`, `:445` against `part5:532`, glossary `d2d-hop` | In Part II "two hops apart" counts links; in S4 one "hop" is a whole CCD–IOD round trip (9 ns) and one transfer between CCDs is two round trips. K8 fixed "round trip" and "transfer" but left "hop" with two meanings. | — | In Part II use "two links apart". |
| L22 | Structure | `part2:85–87` (p. 39) | The ED² metric is introduced as "a useful lens for 3D V-Cache". | It is never used again (no occurrence in Parts III–VI). | Cut to one sentence, or apply it once, for example to the EPYC 9684X/9654 pair. |
| L23 | Structure | `part1:109`, `tab:rq-map` (p. 29); `appendix-c:70` | RQ1's row lists `sec:dies-per-wafer` inside "Part III (…)". | After K21 that label is in Appendix C and carries two names. The link resolves, but the row says Part III. | Cite `app:dies-per-wafer` outside the bracket and remove the second label. |
| L24 | Structure (judgement, half-page rule) | `sec:density-example` `part4:120–131`; `part4:247–265`; `part3:201–225`; `part2:122–142` | Worked examples with table or figure of about 0.55–0.8 page in the main text. | The rule applies at submission. K21 moved the largest ones. | Before submission, decide on these four. |
| L25 | Structure (repetition) | `part2:441` and `:445` (star, two hops, in one page); `part3:267` and `:287` (testing and down-binning); `part4:280` and `:288` (tie to 1.36×); `part4:218` ("biggest weakness" twice in one paragraph) | Same point made twice within a few paragraphs. | — | Keep one of each. |
| L26 | Figure (minor) | `fig:l3-miss-path` (p. 60); `fig:sim-pingpong` (p. 125); captions of `tab:lam-detail`, `tab:sim-calibration`, `tab:sim-planar`, `tab:sim-side-die`, `tab:sim-sensitivity` | "package link" label touches the compute-die dashed box. The legend clips the model curve near 125–145 ns and covers the top of the 9 and 18 ns lines. Those captions lack a final full stop. | — | Move the label and the legend; add the stops, in the generator `make_figures.py` where it applies. |
| L27 | Minor (rounding) | `tab:m5600x-levels`; `appendix-g:59`, `part5:553` | L2 "12.1–12.4 cycles"; six threads "280–296 GB/s" from the L3. | 2.61 ns × 4.614 = 12.04. At 4 MB six threads read 276 GB/s; `ANALYSIS.md` limits the range to 8–16 MB. | "12.0–12.4"; add "(8–16 MB)". |
| L28 | Writing | `part3:262`, `fig:packaging-timeline` | "EFB" is never expanded. | The local slide gives only the abbreviation. | Say "(AMD's label, EFB)", or expand it from a source added to the project. |
| L29 | Over-hedged | `part4:220` (p. 89); `part5:485` (p. 119); `part1:181` (p. 33) | `part4:220` closes with three successive qualifications after its one firm result. `part5:485` calls the overlap test "weak", which is right for the inference but buries a solid measurement. The last Findings bullet runs to about 140 words of caveats. | The firm results are that the voltage limit cannot explain the residual, and that the 5600X sustains 16 overlapping misses at 0.071 of the single-miss time in three runs. | State the firm result first and the limit once. Separate "the measurement is clear" from "the inference to Lam's fitted factors is weak". Split the Findings bullet. |

**Writing: suggested rewrites (in addition to L19–L21, L28).** A script found 30 sentences of 60 words or more; the twelve below are the ones worth changing.

| Location | Length | Rewrite |
|---|---|---|
| `appendix-c:23` | 79 words | End the sentence after "Dong and Xie"; begin "For the 1 and 2 cm² dies…". |
| `part6:217` | 76 | Split at "and within each generation". |
| `part6:219` | 71 | End after "(`sec:chiplet-power`)"; begin "The power side of RQ2 is therefore answered only qualitatively". |
| `part6:61` | 71 | End after "Broadwell's own L3 bandwidth"; begin "Lam explains why:". |
| `part5:192` | 70 | Split after "although the data still fits in L2". |
| `appendix-e:13` | 70 | Make the five latency cases a short list. |
| `part5:434` | 69 | Define $C$, $A$, $M$ in one sentence and $\Delta t_{\mathrm{L3}}$, $\Delta M$, $s$ in the next. |
| `part4:161` | 67 | Split after "(MPKI)". |
| `part3:329` | 67 | Move the parenthesis to its own sentence after "per core". |
| `part3:285` | 67 | Split after "set independently". |
| `part5:579` | 65 | Split after "cyclic access pattern would lose". |
| `part3:375` | 65 | Split at "and, in the Zen 4 server products". |

Other terminology: `figures/stack-process.tex:28` says "a stacked CCD" where the glossary convention is "V-Cache CCD". No sentence attributes work to an individual, and no gendered pronouns occur in any section, appendix, figure or the glossary (searched). eDRAM, TSV, WSL, PBO and ω are defined at first use; "MLP" as an abbreviation is not used.

---

## 3. Regression check

**K1–K21 and the K writing items.**

| ID | Status | Note |
|---|---|---|
| K1 | **Partly fixed** | The unfitted result is reported and the refit labelled a calibration. Residual: L1. |
| K2 | Fixed | `part5:479`, `:579`, `appendix-g:65–67` agree and are limited to latency sweeps. |
| K3 | Fixed | `part1:161`; `figures/evidence-method.tex:13`. |
| K4 | Fixed | `part6:85`, `:223`; `part5:522` gives 0.10 at 5.15 GHz. |
| K5 | **Partly fixed** | Body, RQ2 and Part III summary limited; "whole product range" remains and `part1:176` is unlimited (L10). Datasheet rendered: 9224 is 24 cores, 64 MB; 9754 is 128; 9734 is 112. The white paper calls the 112-core part "9634", which disagrees with the datasheet (9634 has 84 cores, 9734 has 112); the paper avoids the model number, correctly. |
| K6 | Fixed | `part5:532`, `appendix-g:61`. |
| K7 | Fixed in the paper | `part2:294`, `appendix-e:14`, `:46`. `study/sims.py:28–37` still names the factor `h` in a comment and a function (tool only). |
| K8 | Fixed | "Round trip" and "transfer" correct in S4, caption, limits and Part I. "Hop" remains double (L21). |
| K9 | Fixed | `part5:522`. |
| K10 | Fixed | `part5:485`, `:584`, `part1:181`. |
| K11 | **Partly fixed** | Definition added, but after first use (L19). |
| K12 | Fixed | `part4:220`. |
| K13 | Fixed | `part6:154`. |
| K14 | Fixed | `tab:m5600x-levels`, `appendix-g:57`. |
| K15 | **Partly fixed** | L15. |
| K16 | Fixed | 98.5 ns, recomputed from `c2c.csv`. |
| K17 | Fixed | README says "exclusive victim cache" only of the optional L4; run time 7 minutes in both places. |
| K18 | Fixed | The table is referenced. Float distances in §8. |
| K19 | Fixed | eDRAM `part5:511`; TSVs `part3:239`; "7%" in the abstract. |
| K20 | Fixed | `sec:evidence-method` opens Part V (p. 97–98). |
| K21 | Fixed | See §4.5. L24 lists further candidates. |
| K writing items | Fixed | All eight changed as listed in the response. |

**I and J items spot-checked for regression** (those touching K-affected text): I1, I2, I17, I19, I28, I41, I42; J3, J5, J6, J17, J18, J19, J21, J24, J27. All hold.
- **I10** (fitted agreement presented as a test): improved but still open through L1.
- **J2** (product-line silicon): numbers correct (100/108/121; 0.7–3%; 90%), but its final clause is wrong (L3).

---

## 4. Simulation and measurement check

### 4.1 Reproduction

- Built with MSYS2 UCRT64 `g++ -O2 -std=c++17`. `--selftest`: **8 passed, 0 failures**.
- `sims.py --only s0 s4 policy` (2 min 15 s, 16 threads): `s0_calibration`, `s0_latency_sweep`, `s4_pingpong`, `s4_split`, `s1_policy` are **byte-identical** to `research/measurements/cachesim/`.
- `compare_5600x.py`: `model-comparison.csv` **byte-identical**; `m5600x-latency.tex` and `m5600x-table-mlp.tex` differ from the paper's only in line endings.
- `node test/crosscheck.js`: **not run** (no Node.js).

### 4.2 The 5600X numbers checked against the raw files (22; all match unless noted)

| Claim | Raw value | OK? |
|---|---|---|
| L1 0.87 ns, 4.0 cycles | 0.87 (median, 2 MB); × 4.614 = 4.01 | ✓ |
| L2 2.61–2.69 ns | 64 KB 2.61, 512 KB 2.69 | ✓ (cycles: L27) |
| L3 11.1–12.0 ns, 51–55 cycles | 4 MB 11.09, 16 MB 11.96; 51.2–55.2 | ✓ |
| 1 GB 98.6 ns, 4 KB 115.3 ns | 98.56; 115.33 | ✓ |
| Translation about 17 ns | 16.77 | ✓ (L9) |
| Model 82 ns at 1 GB | 81.85 | ✓ |
| Input 84 ns; 14 and 17 ns differences | 47/4.614 + 74 = 84.2; 14.4; 16.7 | ✓ |
| Unfitted plateau and 1 GB within about 20% | 1.19–1.20 | ✓ |
| Up to 2.4× at 32 MB | 2.39 | ✓ |
| Refit within 5% and 1% | 1.04–1.05 at 4–16 MB; 1.00 at 1 GB | ✓ (by construction, as stated) |
| Refit 1.2–2.1× at 19–38 MB | 1.22, 1.28, 1.47, 2.08, 1.67 | ✓ |
| Refit 1.1–1.3× at 45–108 MB | 1.31, 1.24, 1.18, 1.13, 1.19, 1.12 | ✓ |
| 64 MB: 66.9 ns against refit 56.6 | 66.86; 56.59 | ✓ |
| 32 MB: 24.1 / 23.9 / 73.8 ns | 24.10, 23.94, 73.76 | ✓ |
| Early L3 slowdown 16–20 MB | 14.00 ns at 19.5 MB against 11.96 at 16 | ✓ |
| Overlap fractions 0.349, 0.113, 0.071, L3 0.077 | medians 0.349, 0.113, 0.071, 0.077 | ✓ |
| 105 to 120 ns per step | 104.9 to 119.7 | ✓ (L17) |
| 108 GB/s L3, 23 B/cycle; 30 GB/s memory | 4 MB read 108; 23.4; 256 MB read 30 | ✓ |
| Six threads 41 GB/s, 80%, 6.8 GB/s per core | 41; 80.1%; 6.83 | ✓ |
| Six threads 280–296 GB/s | 280, 296 at 8–16 MB | ✓ (L27) |
| 12 threads erratic 0.1–480 GB/s | 0 to 481 below 32 MB | ✓ |
| c2c median 98.5 ns; CPU 0 pattern 66–72 ns | 98.5; second CPU = 0 gives 65.8–72.1 for all 11 pairs | ✓ |
| Clock 4.614 GHz before and after | `clock-before.csv`, `clock-after.csv` | ✓ |
| Conditions (board, cooler, RAM, FCLK, PBO, WSL2 kernel, THP) | `notes.md`, `sysinfo.txt` | ✓ |

### 4.3 Model description (Appendix E against `cachesim.cpp`)

| Statement | Code | Verdict |
|---|---|---|
| Read of another core's modified line served core to core; remote costs two L3 latencies plus the hop | `fetch`, owner branch | Correct |
| Write hit with other holders: one extra L3 latency, plus the hop if any is on another die | `if (privHit) lat += c.l3_lat; if (remote) lat += hopC` | Correct |
| Write miss: fetch as a read, plus a further hop if a holder is on another die | `remote` branch after `fetch` | Correct |
| L3-only copies invalidated free | `for (gg) l3[gg]->invalidate(ln)` | Correct |
| ω scales the part beyond an L2 hit | `lat <= l2 ? lat : l2 + overlap * (lat - l2)` | Correct |
| Calibration: ω(306.8) per removed miss, 4ω per access | 47 + 74 × 4.2 − 51 = 306.8; 107.32ω = 36 → 0.335 | Correct |
| Round trip has two messages and two upgrades; four hops per round trip | cross-CCD round trip = 72.5 + 4 × hop reproduces 108.5, 144.5, 220.5 ns; same-CCD 49 ns | Correct |

### 4.4 Measurement kit against Appendix G

| Statement | Program | Verdict |
|---|---|---|
| Randomly ordered cyclic chain of 64-byte lines | `latency.c:38` | Correct |
| k chains, 1 GB and 16 MB, 2 MB pages | `latency.c` MLP mode: k pointers at equal spacing on one cycle | Correct; "independent" is true of the addresses' dependence |
| Read and triad, 16 KB–256 MB, 1/3/6/12 threads | `bandwidth.c`; threads work on slices of one total buffer | Correct (L27 on the size stated) |
| Two threads write a shared counter in turn, all pairs | `c2c.c:31–54`; `cpu_b` is the responder, so "responding thread on CPU 0" is right | Correct |
| Dependent additions for the clock | `clock.c` | Correct |
| WSL2 and pinning limits; 12-thread values; slow run | raw files | Correct except L8 |

### 4.5 Moved material

| Moved | Main-text summary agrees? | Reference resolves? | Lost or duplicated? |
|---|---|---|---|
| Dies per wafer → App. C | Yes: 95, 35, 2.7, 1.9, 3.5 | Yes; L23 | No |
| TLB reach → App. F | Yes: 256 KB, 8 MB, a quarter, a twelfth, 128 MB | Yes | Small deliberate overlap |
| Cache–clock calibration → App. F | Yes: 543, 31 ns, 5.2% | Yes | No |
| S0 shapes → App. G | Yes | Yes | No |
| `sec:evidence-method` | Opens Part V | Yes | No |

### 4.6 Calibration against validation

S0's Milan comparison, S3 and S4 are correctly labelled as fitted or built in. `part5:436` ("reproduces Lam's 4.9% … to within rounding") is a calibration and is introduced as one. The remaining place where a comparison of inputs is presented as a test of the model is L1. The genuinely out-of-sample results are the capacity-edge differences and the 49 against 98.5 ns round trip, and both are unfavourable, which is worth saying plainly.

---

## 5. Spot-checked numbers (34; different from the fifth review's list where possible)

| # | Claim (location) | Source and place | OK? |
|---|---|---|---|
| 1 | L3D 64 MB, 41 mm², 7 nm, 13 Cu + 1 Al (`part4:101`, `:141`) | Wuu slide 11, rendered | ✓ |
| 2 | >15× density, >3× energy, thermal (`part4:118`, `:203`) | Wuu slide 15, rendered | ✓ |
| 3 | RVDD, VDDM through power TSVs in channels (`part4:212`) | Wuu slide 24, rendered | ✓ |
| 4 | UCIe, co-packaged optics, modules beyond wafer (`part6:123`) | Lambert slide 12, rendered | ✓ |
| 5 | "continued strategic use of 2.5D" (`part3:262`) | Lambert slide 8, text | ✓ |
| 6 | 96 h uHAST, 2500 cycles, 1000 h (`part4:271`) | Alam slide 14, text | ✓ |
| 7 | Si-OH reaction, F2B (`part4:135`, `:141`) | Alam slides 9, 11, text | ✓ |
| 8 | 9654: 2.40/3.70/3.55 GHz, 360 W, 384 MB (`part4:216`) | EPYC 9004 datasheet p. 2, rendered | ✓ |
| 9 | 9684X: 2.55/3.70/3.42, 400 W, 1152 MB | same | ✓ |
| 10 | 9354, 9334, 9124 rows of `tab:product-matrix` | same | ✓ |
| 11 | 9174F 4.10 against 9124 3.00 GHz; "one or two" links; four or fewer dies (`part3:287`, `:331`) | 4th-Gen white paper, text | ✓ |
| 12 | Over 200× and over 15× (`part4:116`) | EPYC 7003 overview, text | ✓ |
| 13 | 14 nm label; diagonal quadrants; FCLK 1600 MHz | EPYC 7003 overview, text | ✓ |
| 14 | 10–20 mm; 9-2-9 and 5-2-5; reticle; two-deep; copper pillars; down-bin | Naffziger, text | ✓ |
| 15 | 90% of chip area (`part4:28`) | Mittal and Vetter sec. 1: "may occupy 90 percent". "Up to" is the paper's | ✓ (not rechecked by the fifth review) |
| 16 | 8–15× bandwidth; half to a third latency; about 8× density (`part2:313`) | same, sec. 1 | ✓ (same) |
| 17 | Liquid cooling; hundreds of megabytes | same | ✓ |
| 18 | Hit rate +47%, IPC over 19% (`part4:290`) | Lam, text | ✓ |
| 19 | 16.75%, typo 72.8% (`part4:161`) | Lam, text | ✓ |
| 20 | 5800X3D 4.5, 5950X 5.05 GHz, about 10% (`part4:220`) | Lam, text | ✓ |
| 21 | 128 MB L4; 64-bit link, 6.4 GT/s (`part6:61`) | Lam, text | ✓ |
| 22 | 7800X3D 1.2 V and 1.1 V; 20 µm; "biggest weakness" | Cozma 2024, text | ✓ |
| 23 | 24–28 cycles faster than mesh (`part2:441`) | Cozma 2022b, text | ✓ |
| 24 | 25% more B/cycle; no doubling; 12.5% lower | Cozma 2022b, text | ✓ |
| 25 | 60 usable cores per socket; VM warning; 2.7×, 1.84×; 2–4.3× (`part6:111–113`) | Reguly, text | ✓ |
| 26 | 88.35, 92.85, 88.43 °C; 1.3×; 26 °C | Black, text | ✓ |
| 27 | Up to 3.4×; 100³–400³ | Domke, text | ✓ |
| 28 | mhigh 6 657 491, xhigh 39 400 357; 14 821, 4715; 10k–200k; 30 points | Lawenda, text | ✓ |
| 29 | W2W "always" dearer; Eqs. 16–17 | Dong and Xie, text | ✓ |
| 30 | "almost certainly inappropriate" (App. C) | Murphy, text (split across a line) | ✓ |
| 31 | 48-bit, 43 and 44-bit with SEV (`part2:170`) | AMD 58207, text | ✓ |
| 32 | 512 K: 21 cycles against 12; 2 MB TLB 7/24, 1.7/5 | 7-cpu, text | ✓ |
| 33 | About 20 W more than the 3700X; 4.55 GHz (`part5:58`) | TechSpot 5800X, text | ✓ |
| 34 | Example 140 (CPI 1.5); 64–128 entries; 20–40% leakage; 0.08 µm²; TLB 32–64, 99%; 100–300 cycles | Sarangi, PDF text of Ch. 10–12 | ✓ |

**Worked examples recomputed by hand (all correct except L3).** CPI 1.5; depth 13; AMAT 1.60/1.46/1.38; write traffic 160 KB, 16 KB, 80×; inclusion 36/100 MB; tags 36/32/27 bits; Amdahl; directory 1.6/12.5/25%; topology values; 1008 mm²; 3.2 GB/s; link powers 0.9/3.3/7.4 W; 3.7 CCDs; xGMI 128/160; counter 0.12/0.53/0.80 s; yields 82.4/68.8/86.6/38.3%; 44% and 63%; Poisson and triangular values; 34.4%; 0.64 chiplet split; dies per wafer 878/92/760/35, 1.9/2.7/3.5, edge 8%/23%; pad densities 772/12 346/44, 16×, 280×; 4096 wires, 5 and 93 mm²; 8.25 slice cycles; 2.05 TB/s; 0.62/0.71 TB/s; libx264 chain 3.85/1.08/0.40/735/699/130; DCS 3.2/3.7/15%/0.24; `tab:lam-per-miss`; geometric mean 1.114 and 1.094, median 9.75%; stock-clock nets; 245–310 and 275–330 bytes; stack yields, 94.8/44.5/139/154/155; product line; `tab:cache-clock-model` at all break-evens and rows 0 and 0.4; 26% and 30%; ω 0.335/0.202/0.105; 103 cycles; S4's 2.2, 2.9, 4.5; App. D 51 bits, 26-bit tag, 3 × 2¹⁵; App. F 24 576 pages; clock corrections.

**Internal consistency (brief item 5).** All listed quantities were checked while reading every section and agree, except the wording of L13 and the two rounded forms in L16: V-Cache 4 cycles and 96 MB; 7%/1.073 and 4.8/5.15 GHz; 130 and 103 cycles; break-evens 0.1 (0.12), 0.35, 0.50 and simulated 0.04, 0.38; 9, 18, 37 ns; 58.6, about 265, 49, 98.5 ns; about 2%; 5600X values; 100/108/121, 0.7–3%, about 90%.

**Citations.** All 36 cited keys are in `references.bib`, and each has a row marked present in `research/pdfs/README.md` with the file on disk. The only uncited bib key is `swaminathanNextFrontierEnabling2022`. Vendor attribution is sound apart from L6. The model never claims to reproduce a cyclic chase; `part5:479` and `:579` state the opposite.

---

## 6. Research questions and argument

| RQ | Answered in Conclusions? | Supported? | Consistent with `tab:evidence-strength`? |
|---|---|---|---|
| RQ1 | Yes (`part6:215`) | Yes: models, reticle statement, uneven scaling | Graded Moderate, though the rule would make it Weak (L5) |
| RQ2 | Yes (`part6:217–219`) | Yes on latency, bandwidth, sharing, flexibility. Power is an estimate and is said to be. | L5, L6, L10 |
| RQ2a | Yes, inside RQ2 | Yes, with AMD's reasoning attributed | No separate row; adequate |
| RQ3 | Yes (`part6:221`) | Yes for capacity and latency; thermal indirect, as stated | L5 on the thermal row |
| RQ4 | Yes (`part6:223`) | Direction and latency strong; size moderate; model illustrative | Consistent, apart from L1 in the model row |

**Overreach.** L1, L4, L6, L9, L12. Causal claims elsewhere are careful, chart readings are labelled, and inferences such as CCD counts and Lawenda's misprint are marked. **Over-hedging.** L29.

**The three weakest links, and what would fix each.**
1. **"The model matches a real machine."** Fix by rewording (L1). More evidence would help only if it exercises the model between plateaus, for example fitting nothing and predicting the measured curve shape under a cyclic workload on the 5600X.
2. **The break-evens rest on one program and borrowed clocks.** The 0.35 comes from libx264's 130 apparent cycles and from clocks Lam measured under a different load. The paper says both, and the threefold sensitivity covers the first. Rewording the headline as "of order 0.1 to 0.4" would match the evidence.
3. **Power and heat, in a question that names power.** RQ2's power answer rests on the predecessor link's 2 pJ/bit, and the thermal argument on inference from clocks and a 2006 simulation. The fix is honest grading (L5) and one sentence in the Conclusions saying that the central question's power part is answered only for link energy.

**Anything important still missing.** Only one thing at this level: no energy or power measurement of a V-Cache part appears anywhere, so "power" in the central question is left largely open. L22 is the visible trace of it.

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
| Appendices A–G | 149–163 | 15 | — | |
| Index | 164 | 1 | — | |

Each part does one job and hands over cleanly; Part V's opening method section now reads properly. Part VI is the part most worth extending if pages are wanted, and the power point above is the natural content.

---

## 8. Format, leftovers and what was found correct

**Format.** A4 (595.3 × 841.9 pt); 12-pt class option; `\singlespacing`; side margins measured at 0.98–0.99 in on three pages; page order cover → copyright → acknowledgements → abstract → contents confirmed on pp. 1–5; contents, lists of tables and figures, glossary and index generated. Diagrams are all TikZ or pgfplots (the only image is the logo); no waveforms are present; code only through `lstlisting`.

**Leftovers.**
- Two `\todo` notes: App. A (p. 149) and App. B (p. 150), known placeholders.
- Cover line "Second Full-Paper Working Draft (initial-draft-2)" and PDF title "(working draft)": correct for now, to change at submission.
- `\partbudget` calls are gone; the macro and its "Target length" text remain defined in `preamble.tex:23–25` but do not print. "(target: about N pages)" remains in the source comments of each part.
- No `\verify` use, no "??", no undefined references or citations, no overfull boxes.

**Float placement.** Of 119 floats, none lies more than two pages from its nearest reference, except appendix tables referenced from the main text, as intended. Ten sit exactly two pages away (Figs 2, 15, 34, 41, 58, 62; Tables 22, 26, 43, 44). Sparse pages are only p. 95 (end of Part IV), pp. 149–150 (placeholders) and p. 160 (end of App. F).

**Figures.** All 61 figure pages were rendered and read, including `fig:m5600x-latency`, `fig:sim-zen2-zen3` and its shared legend, `fig:sim-pingpong` and all 13 mind maps. L14 and L26 are the only problems found. Mind-map leaf text is `\scriptsize` (8 pt) at about full size; the narrowest, `fig:mindmap-chiplet-tradeoff`, is about 7.3 pt, estimated from rendered node size. No mind-map node adds a claim the text lacks. Every figure and table is referenced.

**Correct in the material new since the fifth review.** The 5600X numbers (§4.2); the "real gain is larger" limit to latency sweeps; the weak-check label; the refit labelled as a calibration; App. E's coherence and ω descriptions; ω = 1 − h between Parts and appendix; round trip against transfer in S4; the product-range figures against the datasheet; and all moved material.
