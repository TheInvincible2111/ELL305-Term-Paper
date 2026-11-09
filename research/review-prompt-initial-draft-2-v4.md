# Prompt for a full review of the term paper (initial-draft-2, fourth pass, 8 November 2026)

You are an independent reviewer, acting both as a technical referee and as the course examiner, for an undergraduate term paper (IIT Delhi, ELL305 Computer Architecture, faculty advisor Prof. Sumantra Dutta Roy): "Modern Processor Design Beyond Monolithic Scaling: Chiplet Architectures and 3D-Stacked Cache in AMD Zen Processors". You did not write it. Find errors and weaknesses; do not rewrite the paper.

## Materials (use only these)
- **Compiled draft:** `build/pdf/ELL305-initial-draft-2.pdf` (155 pages). First check that its build time is newer than every file under `initial-draft-2/` and `paper/`; if it is not, say so.
- **Paper sources:** `paper/main-initial-draft-2.tex`, plus everything under `initial-draft-2/`: `sections/*.tex`, `figures/*.tex`, `appendices/*.tex`, `front-matter*` and `mindmap-style.tex`.
- **References:** the bibliography `references/references.bib`; the local source PDFs in `research/pdfs/` (index: `research/pdfs/README.md`); the textbook `sources/archbook.pdf` (Sarangi).
- **Software model** (new in this draft, part of the review):
  - simulator `tools/cachesim/src/cachesim.cpp`;
  - study scripts `tools/cachesim/study/sims.py` and `make_figures.py`;
  - raw results in `research/measurements/cachesim/*.csv`;
  - model description `tools/cachesim/README.md`.
- **Earlier reviews and responses:**
  - `research/review-initial-draft-2.md` and `-response.md` (F1–F23);
  - `-v2.md` and `-v2-response.md` (G1–G20);
  - `-v3.md` and `-v3-response.md` (H1–H24 and W1–W18, including the follow-up rows at the end of the response).
- **Format rules:** `notes/Planning/Submission Format.md`.
- **Rules for checking:**
  - Do not use the web. If a claim cannot be checked against a local file, mark it "cannot verify", not "wrong".
  - Some web-article PDFs clip text or charts at the page edge. Render the page or extract its images (`pdftoppm`, `pdfimages`) before concluding that a value is missing.
  - AMD's ISSCC 2022 slide deck (`AMD-3D-V-Cache-ISSCC-2022-Slides.pdf`) contains images only, so render it too.
- **Out of scope:** ignore `Gem5/` and `tools/measurements/` (the 5600X kit has not been run). Check only that the paper describes the kit accurately where it mentions it.

## Decisions already taken (do not re-raise)
- All 13 mind maps stay; Ishan chose this. Check only that each map is legible (smallest text about 7 pt or more at print size) and adds no claim, number or term that the text lacks.
- The Cezanne detail (`sec:cezanne`) stays in Part III for now.

## Part 1: Technical accuracy
1. **Regression.**
   - For H1–H24 and W1–W18, confirm that each fix recorded in `review-initial-draft-2-v3-response.md` is present and introduced no new error. Fixes may have reached the body but not the Conclusions, captions, mind maps, abstract or `tab:evidence-strength`; check all of them.
   - Spot-check that F1–F23 and G1–G20 have not regressed.
2. **New since the third review.** Check each of these in full against its sources:
   - **Part I:** `sec:related-work` and `sec:findings`. Every finding must match the part it cites.
   - **Part II:** `sec:writes-inclusion`, `sec:virtual-memory`, `sec:mlp` and the directory worked example (`tab:directory-example`). Check them against Sarangi Ch. 11–12, 7-cpu, Chips and Cheese and the EPYC 7003 overview. The message-counting assumptions in the directory example are the authors' own and must be labelled as such.
   - **Part III:** `sec:cross-ccd` (`tab:core-to-core`, read from Reguly's Fig. 2) and `sec:power-flexibility` (`sec:chiplet-power` and `sec:product-flexibility`, `tab:product-matrix`). The CCD counts in `tab:product-matrix` are inferred from L3 size; check that each inference is labelled as one and is arithmetically right.
   - **Part IV:** `tab:product-line-silicon` and its node-cost argument, which uses a value read from AMD's chart. Also check the "What the remaining deficit suggests" paragraph on the Zen 5 clock gap.
   - **Part V:**
     - `sec:evidence-ledger`;
     - `sec:lam-detail` (`tab:lam-detail`, read from Lam's charts; `tab:lam-per-miss`; the geometric mean);
     - `sec:genoax`, including the claim that Lawenda's Table 5 row labels are misprinted;
     - `sec:cross-check`.
   - **Part VI:** the updated RQ2 answer and the three new rows of `tab:evidence-strength`.
3. **The simulation study** (`sec:sim-study`, Appendix E `app:sim-setup`):
   - **Model description.** Check that Appendix E describes what `cachesim.cpp` actually does: the latency formula, the overlap factor (which part of a latency it scales), when the L3 and L4 are filled, warm-up and the statistics reset, coherence, and the time model.
   - **Numbers.** Every number in `sec:sim-study`, its figures and its tables must match the CSVs in `research/measurements/cachesim/`. Check at least 25 of them, including every number in the text of S0–S6 and in the sensitivity paragraph.
   - **Reproduction.** Build the simulator (`g++ -O2 -std=c++17 -o cachesim src/cachesim.cpp`, then `./cachesim --selftest`). Rerun at least `python3 tools/cachesim/study/sims.py --bin ./cachesim --only s0 s4 --out /tmp/check` and compare the output with the stored CSVs. Results should be identical for the same seeds; report any difference.
   - **Calibration versus validation.** The overlap factor (0.42) and the crossing cost (37 ns) are fitted to measurements. Flag any place where a fitted agreement is presented as independent validation.
   - **Overreach.** Model outputs must be labelled as model outputs. Memory-system speed-ups must not be presented as program speed-ups. Upper-bound statements must follow from the stated reasons. Assumed inputs (the planar 96 MB latency of 59 cycles, the L4 die, one memory access per three instructions, `l1_lat = 1` and `work_cycles = 0.31` in S3) must be labelled as assumptions where they are used.
   - **Comparison with Part VI.** Is the S3 comparison with the analytical cache–clock model (`tab:sim-breakeven` against `tab:cache-clock-model`) fair, given that the two use different equal-clock baselines (5.15 against 4.2 GHz)?
   - **Fit with the paper.** Is the study's design sound for its purpose (one factor changed at a time, five seeds, sensitivity analysis)? Does it fit the rest of the paper? Name any experiment that is missing and would matter, or that adds nothing.
4. **Spot-check the rest.** Re-verify at least 30 numbers chosen across all six parts against their cited sources, giving priority to the new material and to values read from charts. Recompute every worked example you sample.
5. **Internal consistency.** The same quantity must have the same value everywhere: in the text, figures, captions, tables, mind maps, abstract and Conclusions. Check at least these:
   - V-Cache cost: 4 extra cycles; 96 MB;
   - clocks: 7% / 1.073 clock gap; 4.8 against 5.15 GHz;
   - cycles per removed miss: 130 (and 50 / 80 / 130 across Lam's workloads); geometric mean +11.4%;
   - the die-to-die hop: under 9 ns; 37 ns calibrated; 58.6 against about 265 ns core-to-core;
   - bandwidth: 204.8 GB/s; 3.2 / 4.8 GB/s per core; 12 MB of L3 per core on Milan-X and Genoa-X;
   - L3 latency: 47 against 39 cycles;
   - break-evens: 0.12 / 0.35 / 0.50 analytical; 0.04 / 0.29 simulated;
   - overlap factor 0.42.
6. **Citations.** Every `\cite` key must exist in `references.bib` and have a local PDF listed as present in `research/pdfs/README.md`. No citation may support a claim its source does not make. Vendor claims must be attributed to the vendor.

## Part 2: Argument and research questions
7. For RQ1, RQ2, RQ2a, RQ3 and RQ4 (Part I, `sec:rq`), check three things:
   - Is each answered in the Conclusions?
   - Is the answer supported by the evidence in Parts II–V, and now also by the simulations?
   - Is its stated strength consistent with `tab:evidence-strength`?
8. **Overreach.** Flag:
   - causal claims from uncontrolled comparisons;
   - models or simulations presented as measurements;
   - values read from charts presented as exact;
   - inferences, such as the CCD counts or Lawenda's misprint, presented as facts;
   - conclusions stronger than the threats-to-validity section allows.
9. Identify the three weakest links in the overall argument and say what evidence or rewording would fix each.
10. Is anything important still missing at undergraduate level? Name it only if it matters.

## Part 3: Structure, writing and figures
11. **Structure.**
    - Does each part do one job and hand over to the next?
    - Point out repetition: the same point now made in full in more than one place, which is likely after this round, for example the 130-cycle argument in Parts II, IV, V and the simulation section.
    - Point out sections in the wrong part.
    - Point out places where the half-page rule requires material to move to an appendix.
    - Is the simulation section in the right place, and at the right length?
12. **Writing.** Flag:
    - unclear sentences;
    - abbreviations not defined at first use (check the new terms, such as TLB, MMU, SMT, MLP, DVFS, FVOPS and KGD);
    - inconsistent terminology (CCD/CCX/die, V-Cache/stacked cache/L3D, "crossing"/"hop");
    - inconsistent tense;
    - any text attributing group work to an individual.

    Give file:line and a suggested rewrite for at most 25 of the most important cases.
13. **Figures and tables.**
    - Render and inspect every figure page, especially the seven `fig:sim-*` figures and the mind maps.
    - Flag overlapping labels, unreadable text, and captions that do not say what the reader should see.
    - Flag figures or tables that are never referenced, and figures that duplicate a table without adding anything.
14. **Length and balance.** Report the page count of each part against its target (I 10, II 25, III 25, IV 25, V 25, VI 20; body 130). Say which parts are now too long or too short and what should move or be cut.

## Part 4: Course format
15. **The mandatory format.** Check the PDF against it:
    - A4, 12 pt, single spacing, one-inch margins;
    - page order: cover → copyright and IP assignment → acknowledgements → abstract → generated contents;
    - generated List of Tables, List of Figures, Glossary and Index;
    - Appendix A (plagiarism report) and Appendix B (readability indices) present, with wording that only says "the tool displayed…"; both are known placeholders, so report their state but do not count it as an error;
    - diagrams made programmatically (TikZ, pgfplots or Graphviz);
    - code only through `listings`/`minted`; the Appendix E commands use `verbatim`, so say whether that is acceptable.
16. **Leftovers.** List every remaining `\todo`, `\verify`, "??", placeholder, undefined reference or citation, overfull box, and `\partbudget` status line.

## Output
Write `research/review-initial-draft-2-v4.md` with:
1. **Overall assessment** (at most 10 sentences): a provisional grade-style judgement against what an examiner expects of an undergraduate term paper, and the two changes that would improve it most.
2. **Findings table**, most severe first. Columns:
   - ID (I1, I2, …);
   - severity (Error / Unsupported / Overstated / Inconsistent / Structure / Writing / Format / Minor);
   - location (file:line and PDF page);
   - what the draft says;
   - what the source, CSV, code or rule says (file and page or line);
   - suggested correction.
3. **Regression table** for H1–H24 and W1–W18 (fixed / partly fixed / not fixed / regressed, one-line note each), and any F or G item that regressed.
4. **Simulation check:** the model-description check, the 25 or more numbers checked against the CSVs, the reproduction result, and the calibration and overreach findings.
5. **The 30 or more spot-checked numbers,** each with its source and page, marked correct or not.
6. **RQ-by-RQ assessment** (Part 2).
7. **Per-part page counts,** and what each part needs, or should lose.
8. **What you checked and found correct.**

Change no other file.
