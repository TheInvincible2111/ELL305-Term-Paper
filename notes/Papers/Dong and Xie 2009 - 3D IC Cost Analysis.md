---
title: "System-level cost analysis and design exploration for three-dimensional integrated circuits (3D ICs)"
authors: [Xiangyu Dong, Yuan Xie]
year: 2009
citation-key: dongSystemlevelCostAnalysis2009
status: partially-read
tags: [cost-model, yield, 3d-integration, die-stacking, draft-initial]
---

# Bibliographic record

2009 Asia and South Pacific Design Automation Conference (ASP-DAC), Yokohama, pp. 234–241.
DOI 10.1109/ASPDAC.2009.4796486.

# Why this is the cost-model source for draft-initial (decision, 28 Oct 2026)

Ishan's notes cite a "Cost Modeling of Die-Stacked Silicon Systems" paper for the yield/cost argument
(Poisson yield example; larger die → lower yield and fewer dies per wafer → higher cost per good die;
exact cost depends on wafer cost, node, defect distribution and test cost). No paper with that title exists.
Of the two candidate cost-model lines, this paper matches that argument most directly:

- it builds die cost from wafer cost, **dies per wafer** and **die yield** (Sec. III);
- it models **known-good-die (KGD) testing** and **bonding yield**, comparing die-to-wafer (D2W) with
  wafer-to-wafer (W2W) stacking (Eqs. 16–17) — the test-cost point in Ishan's notes;
- it finds 3D stacking becomes cheaper than 2D only above a size threshold (about 250 mm² for a 2-layer
  stack at the nodes studied), i.e. splitting pays off for large dies — the chiplet/stacking argument;
- it includes a **heterogeneous SRAM-on-logic split** (OpenSPARC T2), which is the 3D V-Cache pattern.

Stow, Akgun, Barnes, Gu & Xie, "Cost analysis and cost-driven IP reuse methodology for SoC design based on
2.5D/3D integration" (ICCAD 2016, invited) is the alternative. It extends the same group's model to
**2.5D interposers** and IP reuse, so it is a better fit for the side-by-side (2.5D) half of the Part IV
comparison than for the basic yield argument. Its full text could not be opened here (the UCSB server refuses
automated access); only search-result abstract text was seen. Not added to Zotero; add later if Part III/IV
needs the 2.5D cost comparison.

# Use in draft-initial

Cited for Eq. 15 (Part III, `eq:yield`), the dies-per-wafer refinement, the 250 mm² threshold and D2W/KGD
(Appendix C). Ishan chose (28 Oct) to switch the worked example to this model: 82.4% / 68.8% at 1 / 2 cm².

# Important caveat for the manuscript

Dong & Xie use a **Murphy-type** yield model, `Y_die = Y_wafer · (1 − e^(−2·A·D0)) / (2·A·D0)`, not the
Poisson model `Y = e^(−A·D0)` in Ishan's worked example. Either keep the Poisson example as an explicitly
simplified model and cite Dong & Xie only for the general relationship, or recompute the example with
Murphy's model. (Murphy with D0 = 0.2 cm⁻²: 1 cm² → about 82.4% × Y_wafer, 2 cm² → about 68.8% × Y_wafer —
recheck before use.)

# Reading status

28 Oct 2026: the local PDF was checked directly for Sec. III (Eqs. 14–17: dies per wafer, die yield, D2W and
W2W stack cost) and Sec. IV.D–E (cost vs number of layers; 2-layer enabling point about 250 mm²; OpenSPARC T2
SRAM/logic split, about half of its 342 mm² die is SRAM). The paper gives Eq. 15 **without naming it**; the
'Murphy' label in the draft is our attribution and needs its own citation. Sections I–II and V not yet read.

# Local source

`../../research/pdfs/Dong-Xie-3D-IC-Cost-Analysis-ASPDAC-2009.pdf` (also attached in Zotero).
