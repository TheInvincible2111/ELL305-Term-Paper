# Response to the sixth review (L1–L29)

Date: 9 November 2026. Review: `research/review-initial-draft-2-v6.md`.

Ishan's instruction: "fix the node.js thing for the reviewer, fix l1-21, l23, l25-29 and long sentences. … add the row for l7. in l22, cut ed^2 to one sentence. for l24, keep the examples where they are."

**Build:** 165 pages, 0 overfull boxes, no undefined references or citations, no "??".

## Node.js for reviewers

`test/crosscheck.js` has a new option, `--write-golden`. When the C++ and JavaScript results agree, it saves the JavaScript results to `tools/cachesim/test/crosscheck-golden.json`, together with the Node version, the date and the SHA-256 of `gui/sim-core.js`.

The new `tools/cachesim/test/check_golden.py` needs only Python. It runs the C++ binary on the same 15 cases and compares the output with the stored JavaScript results. It warns if `sim-core.js` has changed since the golden file was written.

Status:
- The golden file was generated on 9 November with Node v22.23.4, and all 15 cases were identical.
- `python3 test/check_golden.py ./cachesim` passes.
- App. E's reproduction commands and the README list the new check.

## Findings

| ID | Status | What was done |
|---|---|---|
| L1 | Fixed | The text now says once that the model's capacities and level latencies are inputs, so on the plateaus the 5600X comparison checks another Zen 3 chip's published latencies (within about 20%). The model's own behaviour is exercised only between the plateaus, where it is up to 2.4× optimistic. Applied in the abstract, Part I (Findings split into a model bullet and a measurement bullet), the Part V method ("compared with"), the S0 introduction and text, the closing paragraph of the limits section, the Part V summary, the threats to validity, the evidence row (now "Weak: model outputs"), App. G's scope bullet and the figure caption. |
| L2 | Fixed | "Controls clock speed and core count but does not state the memory configuration." |
| L3 | Fixed | App. C: (C) loses its lead over (A) and over (B) at the same bonding yield, since both spend 154 mm² on a V-Cache part. |
| L4 | Fixed | Part VI: the sources contain no like-for-like measurement. Reguly reports only adjacent cores on the Xeons, and EPYC's adjacent cores are faster still. |
| L5 | Fixed | The `tab:evidence-strength` caption now states separate rules for facts from datasheets and for mechanisms (moderate when independent evidence is consistent without measuring size). The four rows now follow the stated rules. |
| L6 | Fixed | The 19% is attributed to AMD, with AMD's three causes (central I/O die, decoupled clocks, latency-optimised link), in Part I, Part III and Part VI (two places). "Under 9 ns" is attributed to AMD in Findings. |
| L7 | Fixed | S4 was rerun with an 18 ns hop added to the split experiment. The other rows are byte-identical. Shared data: 1.20× (9 ns), 1.26× (18 ns), 1.39× (37 ns); 1.20× is called a lower limit. `tab:sim-split` now has four hop costs. |
| L8 | Fixed | App. G gives the full spread: the slow run from 19 MB upwards (up to 3× at 32 MB, 3–7% from 150 MB to 1 GB), and up to about 30% between 4 KB runs near the TLB and cache limits. |
| L9 | Fixed | "About 17 ns … a figure that the virtual machine's nested translation (WSL2) probably inflates" (Part II, App. F). |
| L10 | Fixed | "Serves a wide range of products" replaces "whole product range" in Part I, Part III's summary and RQ2. |
| L11 | Fixed | "No quantitative claim about the money cost of stacking; its silicon-area examples are illustrative." |
| L12 | Fixed | "The paper labels vendor figures as such and prefers independent results where they exist." |
| L13 | Fixed | "More than 2 TB/s". |
| L14 | Fixed | The Phoronix bar now ends at 3.94× with no arrow; the caption gives the 294% result. |
| L15 | Fixed | "Almost every access … once the working set is well above the L2" in S1 and in the `fig:sim-working-set` caption. |
| L16 | Fixed | The analytical-model text explains −1.9% against the table's −2.0%. |
| L17 | Fixed | App. G explains the 104.9 against 98.6 ns base and says which one the fractions use. |
| L18 | Fixed | "From about 7 MB" (Part II, App. F). |
| L19 | Fixed | The naming paragraph moved to the start of `sec:thermal-evidence`, before the first use of "first-generation arrangement". |
| L20 | Fixed | "Memory-bound computational fluid dynamics (OpenFOAM)" (Part I, Part V summary). |
| L21 | Fixed | Part II says "two links apart"; the repeated star sentence is shortened. |
| L22 | Fixed (as instructed) | ED² is cut to one sentence in Part II. |
| L23 | Fixed | `tab:rq-map` cites `app:dies-per-wafer` outside the Part III bracket; the second label is removed. |
| L24 | Kept (Ishan's decision) | The four worked examples stay in the main text. |
| L25 | Fixed | Changes: Part II star sentence shortened; Part III testing and down-binning stated once, with a cross-reference; Part IV's tie-to-1.36× repeat replaced by a back-reference; "biggest weakness" stated once. |
| L26 | Fixed | Figure fixes: the `fig:l3-miss-path` label is two lines and clear of both boxes; the `fig:sim-pingpong` legend is at the top left, with the 9 and 18 ns lines shortened beneath it. Caption fixes: the generator now ends every table caption with a full stop, and the `tab:lam-detail` caption has one too. |
| L27 | Fixed | "12.0–12.4 cycles"; "280–296 GB/s (8–16 MB in all)". |
| L28 | Fixed | "(AMD's label, EFB)": no local source expands it. |
| L29 | Fixed | Part IV's deficit paragraph states the firm result first ("the voltage limit cannot explain the clock deficit that remains") and gives the limit once. S0's overlap paragraph separates the clear measurement (16 misses in flight, three runs) from the weak inference. The long Findings bullet is split in two. |

## Long sentences

All twelve listed sentences were split:
- App. C:23;
- Part VI:217, :219 and :61;
- Part V:192, :434 and :579;
- App. E:13, now a sequence of short sentences;
- Part IV:161;
- Part III:329, :285 and :375.

The "stacked CCD" in the `fig:stack-process` caption is now "V-Cache CCD".
