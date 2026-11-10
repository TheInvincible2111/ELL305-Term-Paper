---
draft: draft-initial
created: 2026-10-28
status: working draft (not a course milestone)
---

# draft-initial — overview

Working draft of the full (~150-page) term paper, started 28 October 2026 at Ishan's request.
It is **not** a course milestone: the next submitted milestone still goes in `Draft 2/`.

## Decisions recorded (Ishan, 28 Oct 2026)

- Folder: `draft-initial/` as a separate working full-paper draft; `Draft 2/` stays reserved.
- Structure: Ishan's **six-part outline** (I Introduction 10 pp; II Foundations 25; III Chiplets 25;
  IV 3D-stacked cache / V-Cache 25; V AMD case study and quantitative analysis 25; VI Synthesis 20).
  Recorded in the project guidelines as an alternative; the seven-part plan was **not** removed.
- First pass: full skeleton + seeded prose where notes and read sources support it; marked placeholders elsewhere.
- Quantitative method: **Option A** — analysis of published research and benchmarks. No simulator, no new hardware measurement.

## Files

- Entry point: `paper/main-draft-initial.tex` (`paper/main.tex` still selects Draft 1).
- Modules: `draft-initial/` — `metadata.tex`, `preamble.tex`, `front-matter.tex` (+ `front-matter/`),
  `glossary.tex`, `sections/part1…part6`, `figures/` (7 TikZ/pgfplots figures), `appendices/` (A plagiarism, B readability, C yield/cost model).
- Working-draft markers: `\todo{}` (red) and `\verify{}` (amber); `\plannedcontent{}` boxes mark unwritten sections.
  **All must be resolved before any of this text is used in a submission.**

## Build

- Linux: `scripts/build-linux.sh all --draft-initial` (or steps `1`, `2`, `3` with `--draft-initial`).
  Output `tmp/linux-build/ELL305-draft-initial.pdf`; `--install` also writes `build/pdf/ELL305-draft-initial.pdf`.
- Windows (MiKTeX): `scripts\build.ps1 -Target draft-initial` → `build\pdf\ELL305-draft-initial.pdf`.
  Not yet run on Windows; the Linux path is tested.
- Both scripts still build the active milestone (Draft 1) by default; Draft 1 rebuilt identically on 28 Oct (19 pp, clean).

Last Linux build 28 Oct 2026: 0 errors, 0 warnings, 2 minor underfull vboxes, biber clean, 42 pages, A4.
Text-position check: no text outside the margins (one bibliography DOI 0.5 pt over).
**Not done:** visual inspection of rendered pages; the figure pages need a visual check.

## Evidence actually used (and its limits)

| Source | Used for | Status / limits |
|---|---|---|
| Sarangi (`sarangi2025basic`) | performance equation (sec 10.9.1), power/leakage (10.10.1–10.10.3), memory hierarchy & AMAT (11.1.1, 11.1.7 Ex. 147, 11.3.1), miss classes (11.3.2), multicore/coherence (12.1, 12.4.2) | Targeted passages read via text extraction on 28 Oct; still **not** full chapter readings. Cited by section, not page. |
| Naffziger 2020 (`naffziger2020chiplet`) | reticle limit, analog vs logic/SRAM scaling, 74 mm² CCD, 12 nm IOD, IFOP (10–20 mm, ~55 GB/s, 13 FCLK <9 ns, 2 pJ/b Zeppelin), 19% latency reduction, KGD test/down-bin | Full two-page text extracted and read on 28 Oct (figures not examined). |
| Suggs 2019 (`suggs2019zen2`) | 2×16 MB L3 per CCD (two CCXs), die sizes (CCD 74, server IOD 416, client IOD 125 mm²), "small die improve yield", Zen→Zen 2 15% IPC with many changes | Slides 2–14 OCR'd on 28 Oct; remaining slides not checked. |
| AMD EPYC 7003 overview (`amd2022epyc7003`) | 8-core CCX/32 MB L3, 512 KB L2, 96 MB L3 per CCD and 768 MB per socket with V-Cache, tiles over central L3, >200×/>15× density claims | Sections 2.1–2.4 read via text extraction. |
| Swaminathan 2021 (`swaminathanAdvancedPackagingEnabling2021`) | 64 MB cache die, Cu–Cu bond, TSVs; 9 µm vs 50→36 µm pitch; >15× density, >3× power benefit (AMD analysis); fixed-frequency prototype 15% gaming; future 3D schemes; cost/yielded mm²; die size vs reticle | Slides 13–20 OCR'd on 28 Oct (OCR partly illegible on slide 17; the >3× figure is from slide 18). AMD claims, attributed to AMD. |
| Wuu 2022 (`wuu2022vcache`) | 32→96 MB, up to 2 TB/s, 15% average gaming uplift | **Abstract only** (presentation-only record). |

## Sources named by Ishan — status after Zotero import (28 Oct 2026)

All in Zotero collection *ELL305 Term Paper* and exported to `references/references.bib`. **None has been read yet**; no claims in the draft cite them.

| Ishan's name for it | Zotero item / citation key | Notes |
|---|---|---|
| IEEE TPDS 2016 DRAM-cache survey | Mittal & Vetter 2016, `mittalSurveyTechniquesArchitecting2016` | Check whether the SRAM-leakage claim is in this paper or the related 2015 eDRAM/NVM survey |
| Exploiting Data Compression … Hybrid Caches (2022) | Kim et al. 2022, `kimExploitingDataCompression2022` | Open access |
| Cache Memory with Dual Unit Tile/Line Accessibility | Wang 2019, `wangDesignImplementationCache2019` | Relevance unclear |
| ChipScale Review 2022 "Barriers to Large On-Die Caches" | Swaminathan 2022, `swaminathanNextFrontierEnabling2022` | Real title is "The next frontier: Enabling Moore's Law using heterogeneous integration"; the phrase is a section heading. Page 16 read. |
| AMD ISSCC 2022 slides | part of `wuu2022vcache` | Slides on AMD's SlideShare; not yet viewed |
| Cost Modeling of Die-Stacked Silicon Systems | Dong & Xie, ASP-DAC 2009, `dongSystemlevelCostAnalysis2009` | No paper has that title. Chosen over Stow et al. ICCAD 2016 (2.5D/IP-reuse focus) — see its reading note. Uses Murphy yield, not Poisson. |

PDFs: see `research/pdfs/README.md` (the index of local copies). Missing as of 28 Oct: Wang 2019, the ChipScale 2022 article and the ISSCC 2022 slides; Ishan to download them. Yield example switched to the Dong & Xie / Murphy model on 28 Oct.

## Open markers (24 in the PDF as of 28 Oct)

Main groups: abstract/contributions/conclusions to finalise; new sources above; yield-model citation;
AMD ISSCC 2022 slide verification; structural silicon and thermal behaviour; independent L3-latency
measurement; later Zen X3D generations; independent benchmark collection (Part V); Appendix A/B evidence for this draft.

## Update 28 Oct 2026, evening

- New local sources: ISSCC 2022 slides (36 slides, read), Murphy 1964 (yield equations read), Wang 2019, Kim 2022; all
  attached in Zotero and listed in `research/pdfs/README.md`. ChipScale 2022 still missing (dead links) and not cited.
- Draft changes: Part I step 2 and Part IV §11–12 now cite slides 5–7 (VERIFY markers removed); Part IV stack
  description, latency (+4 cycles, new Eq. for the trade-off), thermal and power-delivery text written from the slides
  and Mittal & Vetter (Black et al.); Part IV workloads and Part V table/confounds use slides 29, 31, 35; Part II
  "alternative LLC technologies" written from Mittal & Vetter and Kim et al.; Murphy citation and triangular-vs-
  rectangular note in Part III / Appendix C; Zen 2 L2 = 512 KB confirmed (Suggs slide 12).
- Build: `scripts/build-linux.sh all --draft-initial --install` → 45 pages, 0 errors/warnings, biber clean;
  installed to `build/pdf/ELL305-draft-initial.pdf`. Changed pages rendered and inspected.
