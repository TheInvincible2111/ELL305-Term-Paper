# Prompt for a full review of the term paper (initial-draft-2, seventh pass, 9 November 2026)

You are an independent reviewer, acting both as a technical referee and as the course examiner, for an undergraduate term paper (IIT Delhi, ELL305 Computer Architecture, faculty advisor Prof. Sumantra Dutta Roy): "Modern Processor Design Beyond Monolithic Scaling: Chiplet Architectures and 3D-Stacked Cache in AMD Zen Processors". You did not write it. Find errors and weaknesses; do not rewrite the paper. Number your findings **M1, M2, …**.

## Materials (use only these)
- **Compiled draft:** `build/pdf/ELL305-initial-draft-2.pdf` (165 pages). First check that its build time is newer than every file under `initial-draft-2/` and `paper/`; if it is not, say so.
- **Paper sources:** `paper/main-initial-draft-2.tex`, and everything under `initial-draft-2/`:
  - `sections/*.tex`, `figures/*.tex`, `appendices/*.tex` (A–G);
  - `front-matter.tex`, `preamble.tex`, `glossary.tex`, `mindmap-style.tex`.
- **References:** `references/references.bib`; the source PDFs in `research/pdfs/` (index: `research/pdfs/README.md`); the textbook `sources/archbook.pdf` (Sarangi).
- **Software model:**
  - simulator `tools/cachesim/src/cachesim.cpp`, its README, and the JavaScript copy `gui/sim-core.js`. These are cross-checked by `test/crosscheck.js` (needs Node.js) or, without Node.js, by `test/check_golden.py` against the stored JavaScript results in `test/crosscheck-golden.json`;
  - study scripts `tools/cachesim/study/sims.py`, `make_figures.py`, `compare_5600x.py`;
  - raw results `research/measurements/cachesim/*.csv`.
- **The group's own measurements:**
  - raw results `research/measurements/5600X/results-20261108-0724/` (CSV files, `notes.md`, `sysinfo.txt`);
  - `research/measurements/5600X/model-comparison.csv` and `ANALYSIS.md`;
  - the kit that produced them, `tools/measurements/5600x-kit/` (C sources and `run_all.sh`).
- **Earlier reviews and responses, in order:**
  - `research/review-initial-draft-2.md` (F) and `-v2.md` (G), each with its response;
  - `-v3.md` (H, W) with its response;
  - `-v4.md` (I) with its response;
  - `-v4-rerun.md` (J) with its response;
  - `-v5.md` (K) with its response;
  - `-v6.md` (L) with its response.
- **Format rules:** `notes/Planning/Submission Format.md`.

**Rules for checking:**
- Do not use the web. If a claim cannot be checked against a local file, mark it "cannot verify", not "wrong".
- Render the page (`pdftoppm`) before deciding that a chart value or a figure label is wrong or missing. AMD's ISSCC 2022 slide deck contains images only.
- **Out of scope:** `Gem5/`.

## Decisions already taken (do not re-raise)
- The simulation section stays at full length; Part V is over its 25-page target by decision.
- All 13 mind maps stay. Check only that each is legible (about 7 pt or more at print size) and adds no claim the text lacks.
- The Cezanne comparison stays in Part III.
- The pointer-chase workload in the model is deferred. Do not ask for it to be added, but do check that the text never claims the model reproduces a cyclic chase.
- The four worked examples named in L24 (`sec:density-example`, the stack-yield example in Part IV, the bandwidth example in Part III and the AMAT example in Part II) stay in the main text.
- ED² is deliberately reduced to one sentence in Part II.

## Part 1: Technical accuracy
1. **Regression.**
   - For L1–L29 and the long sentences, confirm that each fix in `review-initial-draft-2-v6-response.md` is present everywhere it should be: body, captions, tables, mind maps, abstract, Findings, Conclusions, `tab:evidence-strength`, appendices and tool READMEs. Confirm also that it introduced no new error.
   - Spot-check that K1–K21 and J1–J33 have not regressed, with priority on items that touched the same text as L1–L29.
2. **What changed since the sixth review.** Check each of these in full:
   - **The 5600X framing (L1, L29).** Check the abstract, Part I (Findings, contributions, method), the Part V method, S0 (`sec:sim-calibration`), the limits section, the Part V summary, the threats to validity, the evidence row and App. G.
     - Is it now clear that on the plateaus the comparison checks the model's published inputs against the 5600X, and that the model's own behaviour is exercised only between plateaus?
     - Is the positive half (input latencies within about 20%; at least 16 misses in flight) stated accurately and without overreach?
     - Is the result now under-stated anywhere?

     Check at least 15 5600X numbers against the raw CSVs (medians of three runs) or `model-comparison.csv`.
   - **S4 with an 18 ns hop (L7).** Check `tab:sim-split` and the text (1.20/1.26/1.39×) against `research/measurements/cachesim/s4_split.csv`, and confirm the other rows are unchanged from the earlier data.
   - **The evidence-grading rule (L5).** Check that the restated caption of `tab:evidence-strength` is coherent, and that every row now follows it.
   - **Vendor attribution (L6).** The 19% latency fall and "under 9 ns" must be attributed to AMD everywhere they appear.
   - **Corrected arguments.** L2 (prototype controls), L3 (product-line break-even against (B)), L4 (no like-for-like monolithic measurement), L19 (definition of "first-generation arrangement" before first use).
   - **Figures changed:** `fig:l3-miss-path`, `fig:vendor-vs-independent` (Phoronix to 3.94×), `fig:sim-pingpong` (legend, 18 ns line), and `tab:sim-split`.
   - **Float placement.** Check that no figure or table lands far from its first reference, more than about two pages away.
3. **Simulation and measurements.**
   - **Reproduction.** Build the simulator (`g++ -O2 -std=c++17 -o cachesim src/cachesim.cpp`, then `./cachesim --selftest`). Rerun at least `sims.py --only s0 s4 policy` and `compare_5600x.py`, and compare the results with the stored files (S4 takes several minutes). Run `node test/crosscheck.js ./cachesim` if Node.js is available. Otherwise run `python3 test/check_golden.py ./cachesim`, and report whether it warned that `gui/sim-core.js` changed after the golden file was written.
   - **Model description.** Check that Appendix E describes what `cachesim.cpp` does, in particular the coherence write costs and the overlap factor ω.
   - **Measurement method.** Check that Appendix G describes what the kit's programs (`latency.c`, `bandwidth.c`, `c2c.c`, `clock.c`) actually do, and that its stated limits match the raw files: WSL2, the slow third 2 MB-page run, the 12-thread bandwidth values, and the CPU 0 pattern in `c2c.csv`.
   - **Calibration against validation.** Flag any remaining place where a fitted agreement, or a comparison of two chips' inputs, is presented as an independent test.
4. **Spot-check the rest.** Re-verify at least 25 numbers across all six parts against their cited sources, choosing different ones from the fifth and sixth reviews' §5 where possible. Recompute every worked example you sample, including those now in Appendices C and F.
5. **Internal consistency.** The same quantity must have the same value everywhere. Check at least these:
   - V-Cache cost: 4 cycles; 96 MB;
   - clock gap: 7% / 1.073; 4.8 against 5.15 GHz;
   - cycles per removed miss: 130 apparent, 103 gross in the model;
   - break-evens:
     - analytical: 0.1 (0.12 at 4.2 GHz), 0.35 and 0.50;
     - simulated: 0.04 and 0.38;
   - link: 9 ns per link round trip (AMD); 18 ns per transfer between CCDs; 37 ns fitted; S4 shared-data ratios 1.20/1.26/1.39×;
   - core-to-core round trips:
     - Reguly: 58.6 ns within a CCD and about 265 ns between CCDs;
     - the model: 49 ns;
     - the 5600X: 98.5 ns;
   - link power: about 2% of Genoa's budget;
   - 5600X:
     - level latencies 4.0 / 12.1 cycles, 51–55 cycles, 98.6 ns;
     - input latencies "within about 20%";
     - up to 2.4× between plateaus (32 MB);
     - 16 misses in flight (0.071 of single-miss time);
   - product-line silicon: 100/108/121 mm²; 0.7–3%; about 90% bonding break-even.
6. **Citations.** Every `\cite` key must exist in `references.bib` and have a local PDF listed as present in `research/pdfs/README.md`. No citation may support a claim its source does not make. Vendor claims must be attributed to the vendor.

## Part 2: Argument and research questions
7. For RQ1–RQ4 (and RQ2a), check three things:
   - Is each answered in the Conclusions?
   - Is the answer supported by Parts II–V, the simulations and the 5600X data?
   - Is its stated strength consistent with `tab:evidence-strength`?
8. **Overreach.** Flag:
   - causal claims from uncontrolled comparisons;
   - model outputs or calibrated fits presented as measurements or tests;
   - chart readings presented as exact;
   - inferences presented as facts;
   - conclusions stronger than the threats-to-validity section allows.

   Also flag the opposite: places where the text is now so hedged that a supported result reads as weaker than it is.
9. Name the three weakest links in the argument, and what evidence or rewording would fix each.
10. Is anything important still missing at undergraduate level? Name it only if it matters.

## Part 3: Structure, writing and figures
11. **Structure.**
    - Does each part do one job and hand over to the next, now that Part V opens with its method and Appendices C, F and G carry moved material?
    - Check the half-page rule for any self-contained derivation still in the main text.
    - Point out repetition.
12. **Writing.**
    - Flag unclear or overlong sentences, especially those over about 60 words.
    - Flag abbreviations not defined at first use, especially eDRAM, TSV, WSL, PBO, MLP and ω.
    - Flag inconsistent terminology: cache die / V-Cache CCD / plain CCD; first-generation arrangement; hop / transfer / round trip / link.
    - Flag inconsistent tense, and any text attributing group work to an individual or using gendered pronouns for authors.

    Give file:line and a suggested rewrite for at most 25 cases.
13. **Figures and tables.**
    - Render and inspect every figure page, especially `fig:m5600x-latency`, `fig:sim-zen2-zen3` (its shared legend), `fig:sim-pingpong` and the mind maps.
    - Flag overlapping labels, unreadable text, and captions that do not say what the reader should see.
    - Flag unreferenced figures or tables, and pages left largely empty.
14. **Length and balance.** Report the page count of each part against its target (I 10, II 25, III 25, IV 25, V 25, VI 20; body 130). Part V's excess is decided; comment only on the others.

## Part 4: Course format
15. Check the PDF against the mandatory format:
    - A4, 12 pt, single spacing, one-inch margins;
    - page order cover → copyright and IP assignment → acknowledgements → abstract → generated contents;
    - List of Tables, List of Figures, Glossary and Index;
    - Appendices A (plagiarism report) and B (readability indices) are known placeholders: report their state but do not count it as an error;
    - diagrams made programmatically;
    - code only through `listings`/`minted`.
16. **Leftovers.** List every remaining `\todo`, `\verify`, "??", placeholder, undefined reference or citation, overfull box, and any draft-status text such as "Target length".

## Output
Write `research/review-initial-draft-2-v7.md` with these sections:
1. **Overall assessment** (at most 10 sentences): a provisional grade-style judgement and the two changes that would improve the paper most.
2. **Findings table** (M1, M2, …), most severe first. Columns:
   - ID;
   - severity (Error / Unsupported / Overstated / Inconsistent / Structure / Writing / Format / Minor);
   - location (file:line and PDF page);
   - what the draft says;
   - what the source, CSV, code or rule says;
   - suggested correction.
3. **Regression table** for L1–L29 (fixed / partly fixed / not fixed / regressed / kept by decision, one-line note each), and any J or K item that regressed.
4. **Simulation and measurement check:**
   - reproduction results;
   - the 5600X numbers checked;
   - model and kit description checks;
   - calibration-versus-validation findings.
5. **Spot-checked numbers** (25 or more), each with its source and page, marked correct or not.
6. **RQ-by-RQ assessment.**
7. **Per-part page counts.**
8. **What you checked and found correct.**

Change no other file.
