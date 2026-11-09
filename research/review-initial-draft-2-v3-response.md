# Response to the third review of initial-draft-2 (5 Nov 2026)

Each finding was checked against the cited local file before editing. Build after the changes: 122 pages, no errors, no undefined references or citations, no overfull boxes.

| ID | Verdict | Action |
|---|---|---|
| H1 | Confirmed (yield is convex; cost per good die is what rises faster than area) | RQ1 and the evidence-table row now say cost per good die rises faster than linearly; evidence cell cites Murphy and Dong–Xie, not the textbook |
| H2 | Confirmed | Part V break-even now given as 1.2–2.8 points (313 vs the ~130-cycle stall actually saved) |
| H3 | Confirmed | Part IV summary: thermal path is "the reason AMD gives", lower clocks partly attributed to voltage tolerance |
| H4 | Confirmed | RQ4, Part V summary and the evidence paragraph separate the latency claim (strong) from the IPC claim (moderate, one processor) |
| H5 | Confirmed (CapFrameX pp. 2–3: power-compromise question; result framed as a criticism of Cezanne) | "bound the cost" removed; added the power-compromise remark and CapFrameX's framing; mind-map caption and evidence row softened to "no visible hop, size not isolated" |
| H6 | Confirmed | "independent evidence of Part V confirms" → "the figures in tab:llc-alternatives suggest" |
| H7 | Confirmed | Peak-bandwidth row regraded Weak (vendor only); yield/cost row regraded Moderate |
| H8 | Confirmed | Mind maps: "Flat to beyond 64 MB"; milanx caption likewise; "Die-to-die hop" replaces "Cache against clock"; Broadwell node renamed to the Part IV concept; thinning moved under Manufacturing |
| H9 | Confirmed | OpenFOAM removed from the "little change" example in fig:stacking-decision |
| H10 | Confirmed | Geometric-mean sentence replaced by "ranges and, where given, medians" |
| H11 | Confirmed | Part V: "the group has no processor with stacked cache"; Part VI points to the open questions |
| H12 | Confirmed | "By AMD's account the full 64-core design could not be built as one die…" |
| H13 | Confirmed (Lam p. 12: GPU-bound, 0.5 FPS) | Footnote added to tab:cache-vs-clock |
| H14 | Confirmed (Cozma p. 3) | V-Cache-preplanning caveat added |
| H15 | Confirmed | 7 % → 8 % |
| H16 | Confirmed | One mention: 1.24× on xhigh (1.22× in Fig. 4) |
| H17 | Partly accepted | Kept the chemistry but added why it matters architecturally (no solder → fine pitch) |
| H18 | Not applied | Ishan asked for as many mind maps as possible; captions improved (W14, W15). Cutting or resizing is his decision |
| H19 | Partly applied | Tag-overhead, macro-count and set-count examples moved to new Appendix D (app:l3d-organisation) with a summary sentence in Part IV; Part V Zen 2→3 paragraph split into three. Cezanne section left in Part III (it is the section's argument, not a self-contained aside) — flagged to Ishan |
| H20 | Confirmed | Core grid narrowed, L3 box moved, link label raised |
| H21 | Partly applied | Abstract rewritten with findings; "Planned" removed from the evidence-method caption; draft date updated. \partbudget lines kept while the draft is a working draft |
| H22 | Confirmed | RQ2 now adds the 0.81× average-latency gain, product flexibility, and states power is answered only qualitatively |
| H23 | Confirmed | "probably explains much of why" |
| H24 | Confirmed | tab:three-way notes no visible monolithic advantage in the Cezanne comparison |
| W1, W2 | Done | Pronouns replaced by "the reviewer", "Lam" |
| W3, W4, W6–W9 | Done | SerDes, TDP, HBM, SoIC, RTL, OPIO expanded at first use |
| W5 | Done (Part II prose) | NUMA expanded at its first prose use |
| W11–W17 | Done | As suggested (W16 split by removing the duplicate Fig. 4 clause) |
| W10, W18 | Not done | GHPC description not in a local source; terminology convention left for a later glossary pass |

## Follow-up, 5 November 2026 (content and mind maps)

| Item | Status | Change |
|---|---|---|
| H18 | Partly applied | All 13 maps kept (Ishan's decision); leaf text raised from \tiny to \scriptsize (level 1 \footnotesize, root \normalsize) |
| W10 | Done | GHPC described in sec:lam-detail from Lam's article |
| §5 missing: power in RQ2 | Applied | sec:chiplet-power: AMD's clocking/DVFS statements and an illustrative bound; text states the power side is answered only qualitatively |
| §6 Part II | Applied | Writes and inclusion, virtual memory and TLB, overlapping misses and multithreading, directory worked example (all from Sarangi Ch. 11–12 plus 7-cpu, Chips and Cheese, AMD EPYC 7003) |
| §6 Part III | Applied | Cross-CCD sharing cost (Reguly), power and clocking, product flexibility (datasheets). Cezanne detail still in Part III (H19) |
| §6 Part V | Applied | Evidence ledger; Lam per-workload analysis with geometric mean; Genoa-X subsection |
| §6 Part I | Applied | Related-work paragraph and statement of findings |
| §5 missing: non-AMD chiplet CPU | Not done | No local PDF of a non-AMD chiplet CPU disclosure; Reguly's Xeon numbers used only as comparison points |
| §6 Part IV | Applied | D2W cost model set against AMD's flexibility argument (tab:product-line-silicon; node argument) |
| §5 point 3 (Zen 5 300 MHz residual) | Applied | Developed in sec:thermal-evidence: equal voltage limit, residual ≈ 5.5%, so the two named causes explain less than half of the first-generation penalty |
| §6 Part V (more per-source discussion) | Applied | sec:cross-check: Cozma Zen 3 vs Lam Zen 4 on the same programs; 9800X3D SPEC |
