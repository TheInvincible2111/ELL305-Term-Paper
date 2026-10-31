---
title: "3D V-Cache: The Implementation of a Hybrid-Bonded 64MB Stacked Cache for a 7nm x86-64 CPU"
authors: [John Wuu et al.]
year: 2022
citation-key: wuu2022vcache
status: preliminary
tags: [amd, cache, 3d-integration, isscc, draft-1]
---

# Relevance

Primary source for the implementation of AMD's hybrid-bonded stacked SRAM and its architectural connection to last-level-cache capacity.

# Reading status

The official IEEE PDF has been checked in full. It is a two-page presentation-only record: page 1 contains the abstract and page 2 is an empty presentation placeholder. Only the abstract and bibliographic record have therefore been examined. Swaminathan's Hot Chips 33 AMD presentation is now the fuller primary source identified for the first-generation stack and hybrid-bonding details.

# Local source

`../../research/pdfs/AMD-3D-V-Cache-ISSCC-2022-Presentation-Only.pdf`

# Presentation slides (read 28 Oct 2026)

Local copy: `../../research/pdfs/AMD-3D-V-Cache-ISSCC-2022-Slides.pdf` (built from the 36 slide images in
Ishan's SlideShare download, `AMD-3D-V-Cache-ISSCC-2022-Slides.pptx`, which has no text layer). All slides OCR'd;
slides 5–7, 10–12, 14–17, 19–20, 24–25, 29, 31 and 35 (endnotes) checked visually. Cite as `\cite[slide~N]{wuu2022vcache}`.

| Slide | Content used in draft-initial |
|---|---|
| 5 | "Large L3 Caches Provide IPC Uplift": IPC % uplift (linear, no values) vs L3 size 1x–32x; no workloads named |
| 6 | "Barriers to Large Cache Size": Moore's law slowing; cost per yielded mm² (250 mm² die) rising 45→5 nm; area scaling by function (logic > SRAM > analog, 28→5 nm); "SRAM scaling & cost = barriers to large on-die caches" — cost, product flexibility, latency. **This is Ishan's original slide image.** |
| 7 | "More than Moore": 2.5D chiplets give product flexibility and reduce cost; 3D better — improves effective memory latency, reduces long-datapath and I/O dynamic power, fits more transistors in a package cavity |
| 10–12 | CCD: TSMC 7 nm, 8 cores, 32 MB L3, +19% IPC vs Zen 2, 81 mm², V-Cache support from day 1; L3D: 7 nm, 13 Cu + 1 Al layers, 64 MB, 41 mm²; structural dies: support for thinned CCD, thermal dissipation for cores |
| 14, 16–17 | CCD face-down (C4 to substrate, TSVs to L3D); L3D face-down, hybrid bonded; structural dies oxide-bonded; TSMC SoIC, 9 µm min TSV pitch; support silicon matches 2D CCD Z-height, same package |
| 15 | Hybrid bond vs micro-bump: >15x density, >3x energy efficiency, "superior thermal conductance" (AMD simulation) |
| 19–20 | Zen 3 hierarchy; with V-Cache: 96 MB, 16-way, 32 B/cycle per core, >2 TB/s, **+4 cycles latency**; each die's L3 has own data/tag/LRU arrays |
| 24–25 | Power TSVs between CCD array macros; L3D 512 × 128 KB data macros, dual-rail (VDDM bit cells, RVDD periphery) |
| 29, 35 | 5800X3D vs 5900X, ~15% at 1080p high, 1.36x … tie (CS:GO); AMD testing 14 Dec 2021, DDR4-3600, RTX 3080 |
| 31, 35 | 16C EPYC + V-Cache vs 16C EPYC 73F3: 24.4 → 40.6 jobs/h (~66%), Synopsys VCS RTL simulation, AMD testing 20 Sep 2021 |

All are AMD claims; attribute to AMD.
