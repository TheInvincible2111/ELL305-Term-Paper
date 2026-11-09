# Response to the eighth review (N1–N12), and an own review pass

Date: 9 November 2026. Review: `research/review-initial-draft-2-v8.md`.
Ishan's instruction: fix everything, then run my own review pass over the whole draft, fixing what it finds, until satisfied.

**Build:** 164 pages, 0 overfull boxes, no LaTeX warnings, no undefined references or citations, no "??". Part boundaries are unchanged (I 25–34, II 35–54, III 55–74, IV 75–95, V 96–130, VI 131–145).

**Reproduction after the changes:**
- `cachesim --selftest`: 0 failures.
- `check_golden.py`: 15 of 15 identical, no SHA warning.
- `compare_5600x.py`: `model-comparison.csv` byte-identical. Both figure files are identical to the paper's apart from line endings. The script's caption and legend were edited together with the figure file.

## N items

| ID | Status | What was done |
|---|---|---|
| N1 | Fixed | App. C restores the limit: each V-Cache part costs 139.3/Y_bonding mm² under (C) against 154 under (A) and (B), so below about 90% bonding yield (C) loses its advantage over (A) for V-Cache parts and its lead over (B). `part4:268` keeps its sentence on how AMD describes its products. The v7 response is corrected (rows M27 and M28). |
| N2 | Fixed | RQ3: "No measurement of a V-Cache part's energy use, or of the temperature the stack adds, was found". The 9800X3D at 95 °C is named, and 400 W against 360 W are called rated defaults for parts that also differ in clocks (`tab:config-pairs`). Threats uses the same wording. |
| N3 | Fixed | `part4:129`: the interface is impractical at C4 pitch and costs several mm² at micro-bump or 2.5D pitch, against a fraction of a mm² with hybrid bonding. Part IV summary: "allows a wide, parallel interface in little area and helps keep the latency cost to four cycles". |
| N4 | Fixed | `part2:52`: the optimal-depth argument shows that deepening has limits of its own besides the power limit; "In our reading" a lower stall rate is "a useful alternative" to a higher clock. |
| N5 | Fixed | `part2:310`: each core's two threads share its 512 KB L2, and all sixteen share the L3. |
| N6 | Fixed | Findings bullet: "on every L3 miss". Found in the own pass: the same slip in `part3:152` (twice), the `fig:numa-latency` caption and `part6:166`, now "every memory access". |
| N7 | Fixed | "Only the ratio can be fitted; the absolute values can be compared only roughly". The 206 ns is "from one cloud instance" in the text and caption, and the caption says the ratio is "fitted to" Reguly's measurement. |
| N8 | Fixed | "which is probably one reason why". |
| N9 | Fixed | "On the group's Ryzen 5 5600X the model's input latencies are nearly right, but close to each cache's capacity its latency is too low." "Close to" is kept rather than the suggested "just above", because the 2.4× is at 32 MB, at the capacity itself. |
| N10 | Fixed | Abstract: "in the first two generations (Zen 3 and Zen 4)". |
| N11 | Fixed | "The group's own measurements check the model's inputs and expose its limits." |
| N12 | Fixed | `tools/measurements/ELL305-5600X-kit.zip` rebuilt from the current kit folder (same layout; the model is identical to `tools/cachesim/src/cachesim.cpp`). |
| Long sentences | Fixed | All ten split. Six more found in the own pass are also split: abstract (63 words), `part4:186`, `part4:192`, `part5:226`, `part6:221` and the `part5:584` paragraph. |

## Own review pass

**What was read:** all six parts line by line, and the relevant sections of Appendices C, E and G.

**What was recomputed:**
- worked examples: AMAT; address split; inclusion; Amdahl; directory overhead; write-back traffic; TLB reach; Lam's geometric mean; MiniFE bytes per point; clock corrections; per-core bandwidth; link power; the link-bandwidth balance; the product-line table;
- S6 against `s6_streaming.csv`;
- the 5600X refit ratios against `model-comparison.csv`.

**What was changed beyond the N items:**
- **Over-claims softened:**
  - "measured independently in three generations" now names the one outlet (abstract, Findings).
  - Part V said a removed miss saved about 130 cycles "because" of overlap; it now says probably overlap, and possibly prefetches, as elsewhere.
  - The 5600X refit is described as *fitted* (54 cycles, and 90 ns beyond the L3), not as "this machine's values": 90 ns is chosen to match 1 GB. The text, the caption, the figure legend and the script are changed together.
- **Precision:**
  - App. G: at 32 MB the measured latency is 2.4× the default model and 2.1× the refitted one. It previously said "about twice".
  - Cache against clock: the clock-gap factor is "between about three and three and a half". It previously said "three and four", but 0.35/0.12 = 2.9.
  - Evidence table: only Lam's figures imply 0.6–0.7 TB/s.
  - S6: the fall to 0.68 billion lines per second is latency-limited, before the DRAM limit applies from six threads.
  - Workload classes: "from about 10%" rather than "tens of percent".
- **Wording:**
  - RQ2: "took about 4.5 times as long" (M25 residue).
  - Part I's slide 6–7 sentence clarified.
  - Part IV summary sentence on the heat path untangled.
- **Layout:** the fixes had pushed Parts V and VI onto an extra page each (166 pages). The Part V limits paragraph that repeated S0 now points to it. The Valgrind bullet, the RQ2 and RQ3 power sentences, the RQ4 caveat and three open questions are tightened. The draft is back to 164 pages, with no content lost.

**Checked and found correct (no change needed):** about 60 further numbers in Parts II–VI, including:
- Part II: the AMAT rows, Amdahl and directory overhead.
- Part III: the NUMA table, the cross-CCD numbers, the dual-socket lane arithmetic, the bandwidth balance and the product matrix.
- Part IV: the density, slice-latency, libx264 and DCS arithmetic.
- Part V: Lam's means, MiniFE, OpenFOAM and Genoa-X clocks, and the SPEC per-clock estimate.
- Part VI: the per-core bandwidth and Reguly ratios.

**Noted, not changed (a choice for Ishan):** the List of Figures and List of Tables reproduce each caption in full, which makes the front matter 24 pages. Short captions (`\caption[short]{long}`) would cut several pages from it. That is a style decision, so it is left as it is.

**Where the pass stopped:** after one full reading and a second check of every changed passage. A further pass by the same reader would mostly re-check its own edits, so the next useful check is a fresh independent review.
