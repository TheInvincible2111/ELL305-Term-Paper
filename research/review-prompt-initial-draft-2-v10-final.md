# Prompt for the final review before submission (initial-draft-2, v10, 11 November 2026)

You are an independent reviewer, acting both as a technical referee and as the course examiner, for an undergraduate term paper (IIT Delhi, ELL305 Computer Architecture; faculty advisor Prof. Sumantra Dutta Roy): "Modern Processor Design Beyond Monolithic Scaling: Chiplet Architectures and 3D-Stacked Cache in AMD Zen Processors".

**This is the last review before the paper is submitted.** The previous review (v9) led to many fixes and cuts. Your four jobs, in order of priority:
1. **Submission readiness.** Confirm that the two files to be uploaded, one `.tex` and one PDF, meet every course rule. List everything that still blocks submission.
2. **Damage from the last round.** Check that the v9 fixes are present and correct, and that the cuts removed nothing the argument needs and broke no reference, number, caption or summary.
3. **Remaining mistakes.** Do one more full accuracy pass, with priority on text that changed since v9.
4. **Readability.** Note any remaining passage that is tedious, repetitive or textbook-teaching rather than research. Recommend cuts only where nothing important is lost, and say what must change with each.

For every finding give a safe fix: one that names every other place that must change with it, so that applying it creates no new mistake. You did not write the paper. **Do not edit any project file.** Number findings **Q1, Q2, …** and cuts **K1, K2, …**.

## Materials (use only these)
- **The files to be submitted** (generated, never edited by hand):
  - `build/submission-final/ELL305-Term-Paper.tex`: the single self-contained source;
  - `build/submission-final/ELL305-Term-Paper.pdf`: the PDF compiled from it.
- **The generator:** `scripts/flatten-initial-draft-2.py`. It merges every `\input` of `paper/main-initial-draft-2.tex`, embeds `references/references.bib` with `filecontents*`, and drops full-line comments outside `filecontents*` blocks.
- **The modular sources** (the editing copy): `paper/main-initial-draft-2.tex` and everything under `initial-draft-2/`:
  - `sections/`, `figures/`, `appendices/` (A–H);
  - `front-matter.tex`, `front-matter/` (including `logo-embedded.tex`), `metadata.tex`, `preamble.tex`, `glossary.tex`, `mindmap-style.tex`;
  - `paper/styles/ell305-format.tex`.

  The modular PDF is `build/pdf/ELL305-initial-draft-2.pdf`.
- **References:** `references/references.bib`; the source PDFs in `research/pdfs/` (index `research/pdfs/README.md`); the textbook `sources/archbook.pdf` (Sarangi).
- **Simulation and measurements:**
  - simulator and scripts: `tools/cachesim/`;
  - CSV results: `research/measurements/cachesim/`;
  - 5600X results: `research/measurements/5600X/`;
  - measurement kit: `tools/measurements/5600x-kit/`.
- **Earlier reviews and responses:** `research/review-initial-draft-2*.md`, especially `review-initial-draft-2-v9-final.md` and `review-initial-draft-2-v9-final-response.md`. Do not repeat a finding that a response marks as fixed unless the fix is missing, wrong or broke something.
- **Course rules:**
  - `tmp/ell305-community/` (README, TERM_PAPER.md and the original emails in `sources/`; the emails are authoritative);
  - `notes/Planning/Submission Format.md`;
  - `sources/Term paper format PFD.pdf`.

**Rules for checking:**
- Do not use the web. If something cannot be checked against a local file, mark it "cannot verify".
- Render a page (`pdftoppm`) before calling a figure, label or chart reading wrong. AMD's ISSCC 2022 deck and the Hot Chips 33 slides are images.
- `Gem5/` is out of scope.

## Known open items (report their state; do not count them as new findings)
- Appendix A (plagiarism report) and Appendix B (readability indices) are still placeholders, waiting for Ishan's tool results. They must be typed as text or tables, not images, because of the single-file rule.
- The submission date on the cover and the copyright page is still 8 November 2026 (`\draftdate` in `metadata.tex`).
- Ishan will make the GitHub repository public himself. The paper's links assume this.

## Part 1: Submission readiness (mark failures **BLOCKER**)
1. **Two files only.** Copy `ELL305-Term-Paper.tex` alone into an empty folder, with no other file, and compile it with standard pdfLaTeX and no shell escape, in the order stated in its header comment: pdflatex, biber, makeglossaries, pdflatex ×2, makeglossaries, makeindex, pdflatex ×2. Then check:
   - the page count and `pdftotext` output match `build/submission-final/ELL305-Term-Paper.pdf` and `build/pdf/ELL305-initial-draft-2.pdf`;
   - the index and glossary page numbers are right (spot-check five index entries against the pages);
   - the log has no errors, overfull boxes, undefined references or citations, and no "Rerun" request at the end.

   If your TeX installation needs the `\IfDocumentMetadata` shim that `scripts/build-linux.sh` passes on the command line, say so. A current TeX Live, MiKTeX or Overleaf should not need it.
2. **Freshness.** Check that the submission `.tex` is up to date with the modular sources: regenerate it into a scratch folder with the script and `diff`. Check also that the submission PDF is newer than the `.tex`.
3. **Nothing external.** The `.tex` must not need any other file: no image, `.bib`, style, logo, font file or `\graphicspath`. The logo and bibliography are written out by `filecontents*`. Check that the embedded logo PDF is ASCII-only and renders on page 1.
4. **No draft or tool leftovers** in the submitted `.tex` or PDF. Search for:
   - "working draft", "initial-draft", "Target length", `\partbudget`;
   - `\verify`, "??", and "[TODO" (allowed only in Appendices A and B, the known open items);
   - comments naming scripts, `tmp/` paths, or AI tools other than the page-3 statement;
   - the PDF title and author metadata (`pdfinfo`).
5. **Course rules:**
   - All diagrams programmatic (TikZ or pgfplots; no timing diagrams).
   - Code only in an appendix, with colour syntax highlighting. Render the Appendix E listing page and check the colours.
   - The bibliography comes from Zotero / Better BibTeX.
   - The textbook chapter mapping and the advisor are stated (Part I methodology) and match the chapters actually cited. Count the `\cite[sec.~N…]{sarangi2025basic}` chapters.
6. **Format:**
   - A4, 12 pt, single spacing, one-inch margins.
   - Page order: cover → copyright → acknowledgements (with the AI-use statement) → abstract → contents → List of Tables → List of Figures → glossary; references and appendices, then the index last.
   - Short captions in the lists read well, are not truncated mid-phrase, and contain no stray `\cref` text or "??".

## Part 2: Damage from the last round
Check each item in `review-initial-draft-2-v9-final-response.md`.
1. **P fixes (P3, P5, P7–P17, P19, P20).** For each: present, correct, and no new error introduced. In particular:
   - **P7:** Fig. 28(b) is now shape-only. Re-read the node positions from Wuu slide 6, and check that the caption describes what the panel shows.
   - **P9:** the chapter-mapping sentence in Part I.
   - **P10:** the 4.9% / 5.1% / 5.2% wording in Part IV, Part V and App. F.
   - **P13:** every figure whose text size changed. Render it and check for overlaps and that text is about 7 pt or larger.
2. **Cuts.** For each cut, read the text around it and check:
   - it still reads naturally;
   - no sentence refers to removed material ("the example above", "as computed earlier", a removed table, figure or equation);
   - no caveat that a finding depends on was lost.

   The cuts are:
   - **C1, caveats now stated once:**
     - the prefetch caveat must still be stated in full at `sec:tradeoff-example`;
     - the 5600X limits must still be in S0, App. G and `tab:evidence-strength`;
     - the 4.5× sharing figure must still carry "in the one measurement available" where it is first stated.
   - **C2:** the hybrid-bond process, cut to two sentences.
   - **C3:** the evidence ledger, moved to App. H.
   - **C4:** `tab:op-sequence` and the write-buffer paragraph.
   - **C5:** the page-table example.
   - **C6:** the "Beyond SRAM" paragraph.
   - **C9:** the NPS figure.
   - **C12:** the merged topology table. Recompute every N = 8 and N = 64 value.
   - **C13:** ED².
   - **Worked-example cuts:**
     - the CPI examples;
     - both AMAT examples: the new sentence on the 3700X/5800X must still be supported by its citation and say that its miss rates are illustrative;
     - the address split: now a short paragraph, with `sec:address-example` still referenced from the TLB section;
     - the overlap example;
     - the directory overhead;
     - Amdahl;
     - the MSI trace: its table must still serve App. F;
     - the Rome-silicon and shared-counter examples.
3. **Lost context.** Check that no conclusion, Findings bullet, Part summary, overview map, `tab:evidence-strength` row or Conclusions answer still relies on something that was cut:
   - Findings and the Conclusions must not quote a number that no longer appears in the body;
   - the maps must not name a removed topic: Amdahl and ED² in `mindmap-foundations`, "Write buffer" in `mindmap-misses`;
   - every glossary entry must still be used;
   - every `\index` entry must still point to a page that discusses its term.
4. **Orphans:**
   - figure files no longer `\input` (for example `amdahl.tex`, `nps-modes.tex`): list them and say whether anything still refers to them;
   - `\cite` keys that are now unused, and their README rows;
   - labels that now have no reference;
   - equations that are no longer referenced (for example `eq:cpi-stalls`).

## Part 3: Accuracy pass
1. **Changed text first.** Re-verify every number in text that changed since v9 (the `git diff` against commit `f19d19f`, or the v9 response's list), against its source or by recomputing.
2. **Wider sample.** Re-verify at least 30 further numbers across all parts, chosen to differ from the v9 spot-check list, and recompute every calculation you sample.
3. **Consistency anchors.** The same quantity must have the same value and wording everywhere:
   - 4 cycles and 96 MB;
   - 7% / 1.073, and 4.8 against 5.15 GHz;
   - 130 apparent cycles, and 103 gross in the simulation;
   - break-evens 0.1 (0.12 at 4.2 GHz), 0.35 and 0.50; simulated 0.04 and 0.38, always marked "not independent";
   - 9, 18 and 37 ns, with 37 ns always "fitted to a ratio";
   - core-to-core 58.6 / about 265 / 49 / 98.5 ns;
   - about 2% link power;
   - the 5600X: L1 and L2 agree, L3 and memory within about 20%, up to 2.4× at 32 MB;
   - 100 / 108 / 121 mm², 0.7–3% and about 90% bonding yield;
   - a reticle limit of about 800 mm² and 1008 mm²;
   - cost per yielded mm² rising to about 4.9×;
   - terminology: "first two generations (Zen 3 and Zen 4)", "cache-on-top stack", "V-Cache CCD / plain CCD", "simulation" for the model's results, and "the analytical model" for `eq:cache-clock-model`.
4. **Simulation:**
   - build the simulator (`g++ -O2 -std=c++17`) and run `--selftest`;
   - run `test/check_golden.py`, and `node test/crosscheck.js` if Node.js is available;
   - rerun `sims.py --only s0 s4 policy` and `compare_5600x.py` into a scratch folder and compare with the stored files.
5. **Citations:**
   - every key exists in `references.bib` and has its PDF;
   - no source is cited for a claim it does not make;
   - vendor figures are attributed to AMD.
6. **Overreach and over-hedging:**
   - model outputs or fits presented as tests;
   - inferences presented as facts;
   - chart readings presented as exact;
   - conclusions stronger than the threats-to-validity section;
   - and the opposite: results hedged so much that they read weaker than the evidence.

## Part 4: Readability (optional cuts K)
The paper should be easy for the professor to read once, and should present research, not re-teach the textbook.
1. **What to look for:** any remaining passage that is mainly textbook explanation the professor already knows, repeated, or tedious (long caveat chains, long tables of little use).
2. **Do not re-open these decisions:** the simulation section, the overview maps, the Cezanne comparison, the Findings and the abstract were kept by decision.
3. **For each cut K, give:**
   - location and length;
   - what to cut or shorten it to;
   - why the argument does not need it;
   - every place that must change with it: references, labels, summaries, maps, glossary, index, citations;
   - pages saved.
4. **Never** cut a caveat a finding depends on, or a source's only citation, without saying so.

## Part 5: Writing and figures
1. **Sentences:**
   - over about 55 words;
   - unclear;
   - undefined abbreviations at first use;
   - inconsistent tense or terminology;
   - gendered pronouns;
   - group work attributed to an individual.

   Give file:line and a rewrite, at most 25.
2. **Pages:**
   - Render every page that changed since v9, and all figure pages.
   - Flag overlaps, unreadable text, captions that do not say what to see, unreferenced floats, floats far from their first reference, and pages left largely empty. Example: a single figure alone at the end of a Part.

## Output
Write `research/review-initial-draft-2-v10-final.md` with these sections:
1. **Verdict** (at most 10 sentences): a provisional grade; whether the two files are ready to upload once Appendices A and B and the date are filled in; the BLOCKERS.
2. **Findings Q1, Q2, …**, most severe first, in a table with these columns:
   - ID;
   - severity (BLOCKER / Error / Unsupported / Overstated / Inconsistent / Broken by cut / Writing / Figure / Format / Course rule / Minor);
   - location: file:line in the **modular** source, which is where fixes are made (never the generated file), plus the page in the submission PDF;
   - what the paper says;
   - what the source, data, code or rule says;
   - the safe fix, with every other place that must change.
3. **Single-file check:** the exact commands run, their results, and the comparison with the modular build.
4. **v9 regression table:** every P item and cut, with status (correct / incorrect / broke something) and a one-line note.
5. **Optional cuts K1, K2, …**, with the total pages saved.
6. **Fix order and final checklist:** apply fixes to the modular files → rebuild → regenerate the single `.tex` with the script → compile it alone in an empty folder → compare.
7. **Spot-checked numbers** (40 or more), each with its source and result.
8. **Page counts** per part and in total.
9. **What was checked and found correct.**

Change no other file.
