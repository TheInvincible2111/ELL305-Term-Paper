# Response to the v10 final review (11 November 2026)

Review: `research/review-initial-draft-2-v10-final.md`. Ishan chose Q1–Q9, K1–K3, Q14 and Q15. Not taken: K4, K5 (declined earlier as C7, C8), Q10 (resolved by K1–K3), Q11–Q13 (no change needed or Ishan's choice).

| ID | Status | What changed (modular source) |
|---|---|---|
| Q1 | done (part) | `preamble.tex`: `\verify`, `verifyamber`, `\partbudget` and `\plannedcontent` deleted. `\todo` and `todored` stay until Appendices A and B are filled in, then delete both. |
| Q2 | done | Short captions: "The five accesses of the MSI trace under a directory protocol" (App. F); "The libx264 calculation as a sequence" (`libx264-waterfall.tex`). |
| Q3 | done | `mindmap-foundations.tex`: leaf now "Thermal resistance". |
| Q4 | done | `mindmap-stacked.tex`: first hybrid-bonding leaf now "Oxide and copper pads". |
| Q5 | done | `part2-foundations.tex`: sentence split; "the L3 and a 60–70 ns memory together add only about half a nanosecond". |
| Q6 | done | `part5-case-study.tex` S3 check: "against 5.1% from Lam's chart IPCs (Lam states 4.9%)"; `appendix-e-simulation.tex`: "(5.2% against 5.1% from the chart IPCs; …)". |
| Q7 | done | `horizontal-vs-vertical.tex`: panels stacked vertically, `\resizebox` 0.6\textwidth (labels now about 8.9 pt); the "dense vertical bonds / TSVs" label wrapped so it stays inside the package outline. Checked by eye. |
| Q8 | done | `zen-ccd-evolution.tex`: the two "structural silicon over cores" labels get `minimum width=1.45cm, minimum height=1.6cm, inner sep=2pt`; they now cover the two core boxes cleanly. Checked by eye. |
| Q9 | done | `part1-introduction.tex`: "…agree with the measured ones, and its L3 and memory latencies…". |
| K1 | done | Sec. 4.6: write-through/write-back paragraphs cut to two sentences (both terms are already defined in sec. 4.3); the die-to-die write-back paragraph kept; one Sarangi 11.2.3 citation kept. |
| K2 | done | Coherence: the (0,1), (1,2), (2,2) example sentence removed. |
| K3 | done | Virtual memory: cut to three sentences; the "low 12 bits" sentence kept (used by the TLB paragraph and the address-split paragraph); Sarangi 11.4.3 kept. |
| Q15 | done | Sec. 4.6 retitled "Writes and inclusion". The "Write buffer" map leaf stays valid (sentence kept). |
| Q14 | done | 19 new `\index` entries at defining sentences: chiplet, 3D V-Cache (with sub-entry cache-on-top stack), CCD, IOD, CCX, NUMA, micro-bump, working set, set-associative cache, write-back cache, inclusion, TLB (with sub-entry reach), memory-level parallelism, cache coherence, snooping protocol, directory protocol, break-even (cache against clock). Index still one page; every page checked. |
| Q10 | resolved | With K1–K3, Fig. 13 now ends Part II on p. 41 together with Table 7; the paper is **151 pages** (was 152). |

**Checks.** Modular build: 0 errors, 0 overfull, nothing undefined, 151 pages. Single file regenerated with `scripts/flatten-initial-draft-2.py` and compiled alone in an empty folder (pdflatex, biber, makeglossaries, pdflatex ×2, makeglossaries, makeindex, pdflatex ×2, with the TL2022 shim): 151 pages, 0 errors, 0 overfull, `pdftotext -layout` identical to the modular PDF. The submission `.tex` contains no "Target length", "Planned content" or `\verify`. Pages viewed: lists (pp. 11, 13), Figs. 5, 13, 27, 31, 43, and the index.

**Still open:** Appendices A and B (Ishan's results), `\draftdate`, then remove `\todo`/`todored`, regenerate and recompile; publish when Ishan says so.
