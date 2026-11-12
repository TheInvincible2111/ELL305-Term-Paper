# Chiplets and 3D-Stacked Cache in AMD Zen Processors

Term paper for **ELL305 Computer Architecture**, Department of Electrical Engineering, IIT Delhi (November 2026).
Authors: Ishan Krishna Agrawal, Vaidik Goyal and Moon Saraswat. Faculty advisor: Prof. Sumantra Dutta Roy.

**Modern Processor Design Beyond Monolithic Scaling: Chiplet Architectures and 3D-Stacked Cache in AMD Zen Processors**

The paper studies two responses to the limits of building ever-larger single dies: splitting a processor into chiplets (AMD Zen 2 onwards) and stacking extra last-level cache on the compute die (AMD 3D V-Cache). It explains both with the memory-hierarchy, power and multiprocessor models of the course textbook (Sarangi, *Basic Computer Architecture*), grades the published evidence, and adds a trace-driven cache simulation and measurements on the group's own Ryzen 5 5600X.

## Read the paper

| File | What it is |
|---|---|
| [`build/submission-final/ELL305-Term-Paper.pdf`](build/submission-final/ELL305-Term-Paper.pdf) | The submitted paper (152 pages) |
| [`build/submission-final/ELL305-Term-Paper.tex`](build/submission-final/ELL305-Term-Paper.tex) | Its single self-contained LaTeX source (bibliography and logo embedded) |
| [`build/pdf/ELL305-initial-draft-2.pdf`](build/pdf/ELL305-initial-draft-2.pdf) | The same paper built from the modular sources |
| [`build/pdf/ELL305-Draft-1.pdf`](build/pdf/ELL305-Draft-1.pdf) | The Draft 1 progress report (24 August 2026), kept as submitted |

## Repository layout

| Path | Contents |
|---|---|
| `initial-draft-2/` | **The paper's modular sources**: `sections/` (Parts I–VI), `appendices/` (A–H), `figures/` (TikZ and pgfplots), front matter, glossary and preamble |
| `paper/main-initial-draft-2.tex` | Entry point for the paper |
| `paper/styles/ell305-format.tex` | Shared course format (A4, 12 pt, one-inch margins) |
| `references/references.bib` | Bibliography, exported from Zotero with Better BibTeX |
| `tools/cachesim/` | The trace-driven cache simulator (C++ and a browser version) and the scripts of the paper's simulation study (Part V, Appendix E) |
| `tools/measurements/5600x-kit/` | The measurement kit run on the group's Ryzen 5 5600X (Appendix G) |
| `tools/readability/` | Script that computes the reading indices of Appendix B |
| `research/measurements/` | Raw results: `cachesim/` (simulation CSVs) and `5600X/` (hardware measurements, run notes and analysis) |
| `research/review-*.md` | Review rounds of the paper and the responses to them |
| `notes/` | Planning, reading and draft notes (an Obsidian vault) |
| `scripts/` | Build, packaging and single-file generation scripts |
| `Draft 1/`, `submissions/Draft-1/` | The Draft 1 milestone, kept unchanged |
| `draft-initial/` | The first working draft of the full paper, kept as the predecessor of `initial-draft-2/` |

Research papers and the course textbook are not in the repository for copyright reasons; `research/pdfs/README.md` lists every cited source.

## Build the paper

The paper needs a standard TeX distribution (TeX Live, MiKTeX or Overleaf) with `pdflatex`, `biber`, `makeglossaries` and `makeindex`.

**Single file.** The submitted `.tex` compiles on its own in an empty folder:

```bash
pdflatex ELL305-Term-Paper; biber ELL305-Term-Paper; makeglossaries ELL305-Term-Paper
pdflatex ELL305-Term-Paper; pdflatex ELL305-Term-Paper
makeglossaries ELL305-Term-Paper; makeindex ELL305-Term-Paper
pdflatex ELL305-Term-Paper; pdflatex ELL305-Term-Paper
```

**Modular sources.** Edit the files in `initial-draft-2/`, then build:

```bash
scripts/build-linux.sh all --initial-draft-2 --install    # Linux or WSL
```

```powershell
.\scripts\build.ps1 -Target initial-draft-2               # Windows (MiKTeX)
```

Then regenerate the single submission file from the modular sources (never edit it by hand):

```bash
python3 scripts/flatten-initial-draft-2.py build/submission-final/ELL305-Term-Paper.tex
```

## Repeat the simulation and measurements

```bash
cd tools/cachesim
g++ -O2 -std=c++17 -o cachesim src/cachesim.cpp
./cachesim --selftest
python3 study/sims.py --bin ./cachesim --out results    # reproduces research/measurements/cachesim/
```

`tools/cachesim/README.md` describes the model, and `tools/cachesim/gui/index.html` runs it in a browser. `tools/measurements/5600x-kit/README.md` explains how to run the hardware measurements.

## Working rules

- Edit the modular sources; regenerate the single `.tex` and the PDFs after every change.
- Every figure is drawn programmatically (TikZ or pgfplots); code appears only in appendices.
- Every cited source must have its PDF in `research/pdfs/` locally; research PDFs and the textbook stay out of Git.
- Simulation results are model outputs and are labelled as such in the paper.
