# Prompt for the final pre-submission review of the term paper (initial-draft-2, 10 November 2026)

You are an independent reviewer, acting both as a technical referee and as the course examiner, for an undergraduate term paper (IIT Delhi, ELL305 Computer Architecture; faculty advisor Prof. Sumantra Dutta Roy): "Modern Processor Design Beyond Monolithic Scaling: Chiplet Architectures and 3D-Stacked Cache in AMD Zen Processors".

**This is the last pass before submission.** You have two jobs:
1. Find every remaining mistake, and give a fix that is safe: one that does not create a new mistake elsewhere.
2. Recommend cuts that make the paper easier for the professor to read, without losing anything the argument needs.

You did not write the paper. Do not edit any project file. Number your findings **P1, P2, …** and your cuts **C1, C2, …**.

## Materials (use only these)
- **Compiled paper:** `build/pdf/ELL305-initial-draft-2.pdf` (162 pages). First check that it is newer than every file under `initial-draft-2/` and `paper/`; if not, say so.
- **Sources of the paper:** `paper/main-initial-draft-2.tex` and everything under `initial-draft-2/`:
  - `sections/`, `figures/`, `appendices/` (A–G);
  - `front-matter.tex`, `front-matter/`, `metadata.tex`, `preamble.tex`, `glossary.tex`, `mindmap-style.tex`;
  - `paper/styles/ell305-format.tex`.
- **References:** `references/references.bib`; the source PDFs in `research/pdfs/` (index `research/pdfs/README.md`); the textbook `sources/archbook.pdf` (Sarangi).
- **Simulation:** `tools/cachesim/` (C++ simulator, `gui/sim-core.js`, `test/`, `study/` scripts) and the CSV results in `research/measurements/cachesim/`.
- **The group's 5600X measurements:** `research/measurements/5600X/` (raw results, `notes.md`, `sysinfo.txt`, `ANALYSIS.md`, `model-comparison.csv`) and the kit in `tools/measurements/5600x-kit/`.
- **Earlier reviews:** `research/review-initial-draft-2*.md`, from the first review up to v8, each with its response. Use them to check for regressions. Do not repeat findings that a response marks as fixed unless the fix is missing or wrong.
- **Format rules:** `notes/Planning/Submission Format.md` and `sources/Term paper format PFD.pdf`.
- **Course submission instructions:** a student-compiled copy of the course emails, in `tmp/ell305-community/` (from github.com/yraretil/ell305-community). Read `README.md`, `TERM_PAPER.md` and every file in `sources/`. Treat the email texts in `sources/` as authoritative and the summaries as secondary. Where they disagree, say so.

**Rules for checking:**
- Do not use the web. If a claim cannot be checked against a local file, mark it "cannot verify", not "wrong".
- Before saying a chart value or figure label is wrong, render the page (`pdftoppm`). AMD's ISSCC 2022 deck and Hot Chips 33 slides are images only, so render the slide too.
- `Gem5/` is out of scope.

## Changed since the last review (check each in full)
1. **Front matter:**
   - The cover no longer says "Term Paper" and carries the GitHub link.
   - The copyright page is signed by the three authors.
   - The acknowledgements thank Prof. Subrat Kar for introducing the term-paper component of the course, and add a "Use of AI Tools" statement.
   - The running header now includes the topic.
2. **New figures with values read from AMD's charts:**
   - `fig:reticle-sizes` (sec. 6.1): Rome's 1008 mm² against a reticle limit of about 800 mm², read from Swaminathan's Hot Chips 33 slide 3.
   - `fig:area-scaling` (sec. 6.3, cited from the Part I bullet): Wuu ISSCC 2022 slide 6. Area scaling is shown as shape only; cost per yielded mm² runs 1.0 → 4.9.
   - `fig:isscc-charts` (sec. 13): slide 5 (IPC uplift, shape only) and slide 6 (node against year).

   Re-read each value from the rendered slide. Check that each caption states what was read, its accuracy, and that the shape-only panels claim no numbers. Check every sentence that quotes these values.
3. **New Part II material:** the DRAM figure (`fig:dram-array`) and its paragraph. Check them against Sarangi sec. 7.4.3.
4. **Removed material:**
   - The pipeline-depth and write-traffic examples of Part II were cut to their conclusions.
   - The label "worked example" was removed everywhere; App. F is now "Further Calculations".

   Check that nothing still refers to the removed material (labels, equations, "the example above") and that the remaining text reads naturally.
5. **Naming:** "controlled software model" became "simulation", and sec. 28 is titled "Simulation". Check that the term is used consistently, and that "the simulation" never reads as a measurement.
6. **Figures redrawn:**
   - The 13 overview maps, with captions now beginning "Overview of …".
   - The CCD block diagram `fig:zen-ccd-evolution`.
   - The EPYC package `fig:epyc-package`.

   For each, check legibility at print size (about 7 pt or larger), overlaps, and that every box states only what the text supports.
7. **Embedded logo:** the cover logo is now carried inside the source, in `front-matter/logo-embedded.tex`: the official PNG, converted to an ASCII-only PDF and written out by `filecontents*` at compile time. Check four things:
   - the logo renders correctly on page 1;
   - no other external file (image, `.bib`, style or asset) is needed to compile;
   - the generated `iitd-logo-embedded.pdf` is not committed as a separate file;
   - the approach works with a standard pdfLaTeX compile (Overleaf / TeX Live, no shell escape).
8. **GitHub links** (`\ghdir`, `\ghfile`, `\repourl` in `metadata.tex`). Check that every linked path exists in the repository and is tracked (`git ls-files <path>`). Check also that no reference to a repository folder lacks the statement that it is on GitHub.

## Part 1: Mistakes
1. **Regression:** for P-relevant items of earlier reviews, especially M1–M28 and N1–N12, confirm the fix is still present.
2. **Numbers:** re-verify at least 40 numbers across all parts against their sources, choosing different ones from the v7 and v8 spot-check lists where possible. Recompute every calculation you sample.
3. **Consistency:** the same quantity must have the same value and wording everywhere. Check at least:
   - 4 cycles and 96 MB;
   - the 7% / 1.073 clock gap and 4.8 against 5.15 GHz;
   - 130 apparent cycles, and 103 gross in the simulation;
   - break-evens 0.1 (0.12 at 4.2 GHz), 0.35 and 0.50; simulated 0.04 and 0.38, always marked "not independent";
   - 9, 18 and 37 ns, with 37 ns always "fitted to a ratio";
   - core-to-core: 58.6 / about 265 / 49 / 98.5 ns;
   - about 2% link power;
   - 5600X: L1 and L2 agree, L3 and memory within about 20%, up to 2.4× at 32 MB;
   - product line: 100/108/121 mm², 0.7–3% and about 90% bonding yield;
   - the reticle limit of about 800 mm²;
   - "first two generations (Zen 3 and Zen 4)", "cache-on-top stack", "V-Cache CCD / plain CCD", and "hop / transfer / round trip".
4. **Simulation and measurements:**
   - Build the simulator (`g++ -O2 -std=c++17`) and run `--selftest`.
   - Run `test/check_golden.py` (and `node test/crosscheck.js` if Node.js is installed).
   - Rerun at least `sims.py --only s0 s4 policy` and `compare_5600x.py` into a temporary folder, and compare with the stored files.
   - Check that App. E and App. G still describe what the code and the kit do.
5. **Citations:**
   - Every `\cite` key must exist in `references.bib` and have its PDF in `research/pdfs/`.
   - No source may be cited for a claim it does not make.
   - Vendor figures must be attributed to the vendor.
6. **Overreach and over-hedging:**
   - Flag model outputs or fits presented as tests, inferences presented as facts, chart readings presented as exact, and conclusions stronger than the threats-to-validity section allows.
   - Flag also any supported result hedged so much that it reads as weaker than it is.

## Part 2: Making the paper easier to read (cuts)
The body is about 121 pages. The professor will read it once, so recommend cuts where a passage is any of these:
- irrelevant to the central question;
- repeated (the same point, number or caveat made in several places);
- tedious (long derivations, long caveat chains, very long sentences or tables that add little);
- better placed in an appendix.

For each cut **C**, give all of the following:
- location and approximate length;
- what to cut, or what to shorten it to;
- why the argument does not need it;
- **everything that must change with it so that nothing breaks**:
  - cross-references and labels (`\cref`, `\ref`) that point to it;
  - summaries, the Findings, the Conclusions, `tab:evidence-strength` and the overview maps that quote it;
  - glossary entries used only there;
  - figures or tables left unreferenced;
  - citations left uncited;
- the estimated pages saved.

Also apply these rules:
- **Previous decisions:** the simulation section, the mind maps, the Cezanne comparison and four main-text examples were kept by earlier decision. You may still propose cuts to them, but list those separately as "re-opens a decision".
- **Rank by benefit:** order the cuts by benefit to the reader. Say which three would help most.
- **Never cut a caveat** that a finding depends on. Shorten it instead.
- **Never cut a source's only appearance** without saying that its citation and README row then become unused.

## Part 3: Course submission requirements
Check the paper against the course instructions in `tmp/ell305-community/`. Mark anything that would fail a requirement **BLOCKER**.
1. **Two files only.** The final submission must be:
   - one LaTeX file containing all diagrams, graphs, flowcharts and circuit diagrams, with no second file and no zip;
   - one PDF that is produced by compiling that file.

   The paper is currently built from many `\input` files with a separate `references.bib`. Check whether a single-file version exists or can be produced. Draft 1 used one, in `submissions/Draft-1/` and `build/single-file-validation/`. If it can, check that it compiles alone, in an empty folder, to the same PDF. Identify everything the flattening must carry:
   - the bibliography (embedded, for example with `filecontents*`);
   - the logo (already embedded);
   - the Appendix A and B evidence (plagiarism report, readability indices);
   - glossary and index generation;
   - any `\graphicspath` or assets folder.

   Name every remaining external dependency.
2. **Textbook mapping and advisor:**
   - The course routes Chapters 1--12 to Prof. Sumantra Dutta Roy and Chapter 13 to Prof. Subrat Kar. Confirm that the paper's textbook use matches its stated advisor. Count the Sarangi chapters cited.
   - Check that the paper states which textbook chapters the topic maps to. Prof. Kar asked for this in Draft 1, and it is not yet stated in one place.
3. **Mandatory tooling** (TA Garima Singhal, 21 Aug 2026):
   - Diagrams generated programmatically with TikZ, Graphviz or Mermaid.
   - Waveforms only in WaveDrom; flag any timing diagram drawn otherwise.
   - Bibliography managed in Zotero, generating the final `.bib`. Check that every cited entry in `references/references.bib` has the form Zotero/Better BibTeX produces, and that none appears hand-edited.
   - Obsidian used for notes (the `notes/` vault).
4. **Code** belongs in an appendix with language-specific colour syntax highlighting (Prof. Kar). Check that the `listings` style in Appendix E actually colours the code. Check that no code appears in the main text.
5. **Drafts are cumulative.** Check that the final paper is a corrected and extended version of the earlier drafts and carries no draft-specific wording. Draft 1's "Work done as of" progress section belongs to Draft 1 only and must not appear unless intended.
6. **Use of AI tools:** the course material says nothing about AI use. Check only that the statement on page 3 is consistent with the rest of the front matter, and that no AI-tool names remain elsewhere in the PDF or in the source comments of the submitted `.tex`.

## Part 4: Writing, figures and format
1. **Writing:**
   - Sentences over about 55 words, unclear sentences, and undefined abbreviations at first use.
   - Inconsistent terminology or tense; gendered pronouns; group work attributed to an individual.
   - Give file:line and a rewrite for each, at most 30.
2. **Figures and tables:**
   - Render every figure page.
   - Flag overlaps, unreadable text and captions that do not say what to see.
   - Flag unreferenced floats, and floats more than about two pages from their first reference.
   - Flag pages left largely empty.
3. **Submission format** (blockers for a final submission must be marked **BLOCKER**):
   - Everything in Part 3 above.
   - A4, 12 pt, single spacing, one-inch margins.
   - Page order: cover → copyright → acknowledgements → abstract → contents, followed by the List of Tables, List of Figures, Glossary and Index.
   - Diagrams made programmatically; code only through `listings` or `minted`.
   - Every draft leftover: "working draft" or "initial-draft-2" on the cover, PDF title, header or footer; the draft date; `\todo`, `\verify`, "??"; placeholders (Appendices A and B, plagiarism report and readability indices); "Target length" or `\partbudget` text; undefined references; overfull boxes.

## Output
Write `research/review-initial-draft-2-v9-final.md` with these sections:
1. **Verdict** (at most 10 sentences): a provisional grade, whether the paper is ready to submit, and the BLOCKERS.
2. **Findings P1, P2, …**, most severe first, in a table with these columns:
   - ID;
   - severity (BLOCKER / Error / Unsupported / Overstated / Inconsistent / Writing / Figure / Format / Course rule / Minor);
   - location (file:line and PDF page);
   - what the paper says;
   - what the source, data, code or rule says;
   - the safe fix, naming every other place that must change with it.
3. **Cuts C1, C2, …** as specified in Part 2, with the total pages saved.
4. **Fix order:** an order in which to apply the fixes and cuts so that later ones do not undo earlier ones, and a final checklist to run after applying them:
   - rebuild;
   - produce the single-file `.tex`, then compile it alone in an empty folder and compare its PDF with the modular build;
   - 0 overfull boxes and 0 undefined references;
   - grep for every changed number;
   - check that every float is still referenced;
   - rerun the golden check.
5. **Regression table** for earlier review items that regressed (only those).
6. **Spot-checked numbers** (40 or more), each with source, page and result.
7. **Per-part page counts.**
8. **What was checked and found correct.**

Change no other file.
