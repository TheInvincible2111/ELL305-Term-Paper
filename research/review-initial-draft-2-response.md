# Response to the independent review of initial-draft-2 (31 Oct 2026)

Each finding was re-checked against the local source before changing the draft.

| ID | Verdict | Action |
|---|---|---|
| F1 | Confirmed (V-Ray 30% is the largest TechSpot gain) | Rewrote the sentence in Part V §19.1 |
| F2 | Confirmed (Naffziger Fig. 2.2.6 labels Naples rows NUMA1/2/3) | Relabelled Table `tab:numa-latency`; removed our "(other socket)" gloss |
| F3 | Not upheld | The page render is clipped, but the full-width chart images embedded in `ChipsAndCheese-VCache-Latency-2022.pdf` (extract with `pdfimages`) carry the labels 105.59/89.21 ns and 342.11/313.11 cycles. Values kept |
| F4 | Partly upheld | The 4 KB table does mark "+7 (L1 TLB miss)" at 512 K, but the 4 KB header gives the penalty as "?" and the rise is 11→21 cycles. Sentence rewritten to state 21 vs 12 cycles and leave the penalty unstated |
| F5 | Confirmed | "Strongest evidence" weakened to "consistent with"; added the voltage-tolerance explanation (Cozma, Lam) and pointed to the open question |
| F6 | Confirmed | Recast as "consistent with", citing Lam's voltage-tolerance remark |
| F7 | Confirmed | Removed "15% uplift from V-Cache" attributed to Wuu; the iso-clock 15% now cites only Swaminathan |
| F8 | Confirmed (34.18 vs 10.65 ns; 53.10 vs 701.87 GB/s) | Replaced "order of magnitude" with about 3× latency and 1/13 bandwidth; attributed the 6.4 GT/s OPIO figure to Haswell, as in the source |
| F9 | Confirmed | Limited the organic-substrate claim to Rome/Matisse |
| F10 | Confirmed | Removed the causal "to make room for the TSVs" clauses |
| F11 | Confirmed | Lambert pitch targets now cited as slides 12–13 |
| F12 | Confirmed | Reworded the Milan/Milan-X latency gap and the onset of Milan-X's rise |
| F13 | Confirmed | Presented as our explanation; added Cozma's clock-estimation caveat |
| F14 | Confirmed | "Lam suggests is likely due to" |
| F15 | Confirmed | "probably", with a pointer to the clock-correction table |
| F16 | Confirmed | Added base (2.55 vs 2.40 GHz) and max boost (3.70 both) in Part IV and Table `tab:config-pairs` |
| F17 | Confirmed | Dong & Xie threshold now described as applying to 3D stacking |
| F18 | Confirmed | Merged the two 19% IPC rows into one, citing both sources |
| F19 | Accepted | Text now "10% or more"; histogram 5800X bins 150/91; bin convention added to the caption |
| F20 | Confirmed (38.3% vs 34.4% at 5.92 cm²) | Appendix C statement restricted and the larger gap noted |
| F21 | Confirmed | Added Black's 2× power-density assumption |
| F22 | Confirmed | "64 cores per socket" |
| F23 | Noted | Left as is; references land on the right page |
