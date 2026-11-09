# Prompt for a full review of the term paper (initial-draft-2, third pass, 5 November 2026)

You are an independent reviewer, acting both as a technical referee and as the course examiner, for an undergraduate term paper (IIT Delhi, ELL305 Computer Architecture, faculty advisor Prof. Sumantra Dutta Roy): "Modern Processor Design Beyond Monolithic Scaling: Chiplet Architectures and 3D-Stacked Cache in AMD Zen Processors". You did not write it. Find errors and weaknesses; do not rewrite the paper.

## Materials (use only these)
- Compiled draft: `build/pdf/ELL305-initial-draft-2.pdf` (121 pages). First check that its build time is newer than every file under `initial-draft-2/`; if not, say so.
- Sources: `initial-draft-2/sections/*.tex`, `initial-draft-2/figures/*.tex`, `initial-draft-2/appendices/*.tex`, `initial-draft-2/front-matter*`, `initial-draft-2/mindmap-style.tex`.
- Bibliography `references/references.bib`; local source PDFs in `research/pdfs/` (index `research/pdfs/README.md`); textbook `sources/archbook.pdf` (Sarangi).
- Earlier reviews and responses: `research/review-initial-draft-2.md`, `research/review-initial-draft-2-response.md`, `research/review-initial-draft-2-v2.md`, `research/review-initial-draft-2-v2-response.md`.
- Format rules: `notes/Planning/Submission Format.md`.
- Do not use the web. If a claim cannot be checked against a local file, mark it "cannot verify", not "wrong". Some web-article PDFs clip charts at the page edge: extract embedded images (`pdfimages`) or render pages before concluding a value is missing.
- Ignore `tools/`, `Gem5/` and `research/measurements/`: the software model and measurements are not yet written into the paper.

## Part 1: Technical accuracy
1. **Regression.** For every finding F1–F23 (first review) and G1–G20 (second review), confirm that the stated fix is present in the current text and introduced no new error. Fixes may have been made in one place but not in the Conclusions or captions; check both.
2. **New since the second review.** Check in full:
   - the 13 mind-map figures (`fig:mindmap-*`): each node must restate something the text says, with no new claims, numbers or terms that appear nowhere else in the paper;
   - the Cezanne section `sec:cezanne` and `tab:cezanne-vermeer` after the G2/G3 fixes (TechSpot 5700G review, CapFrameX article, 7-cpu, The FPS Review).
3. **Spot-check the rest.** Re-verify at least 30 numbers chosen across all six parts against their cited sources, giving priority to figures, tables and worked examples. Recompute every worked example you sample.
4. **Internal consistency.** The same quantity must have the same value everywhere (for example the 4-cycle V-Cache latency, 96 MB, 7 % / 1.073 clock gap, 4.8 vs 5.15 GHz, 130 cycles per removed miss, under 9 ns hop, 204.8 GB/s, 3.2 / 4.8 GB/s per core, 47 vs 39 cycles). List every mismatch, including between text, figures, captions and mind maps.
5. **Citations.** Every `\cite` key must exist in `references.bib` and have a local PDF listed as present in `research/pdfs/README.md`. No citation may support a claim its source does not make. Vendor claims must be attributed to the vendor, not presented as independent.

## Part 2: Argument and research questions
6. For RQ1, RQ2, RQ2a, RQ3 and RQ4 (Part I, `sec:rq`): is each answered in the Conclusions, is the answer supported by the evidence in Parts II–V, and is its stated strength consistent with `tab:evidence-strength`?
7. Flag overreach: causal claims from correlational or uncontrolled comparisons, models presented as measurements, simulations presented as products, and conclusions stronger than the threats-to-validity section allows.
8. Identify the three weakest links in the overall argument and say what evidence or rewording would fix each.
9. Is anything important missing for this topic at undergraduate level (a well-known counter-argument, a standard concept, a key AMD generation)? Name it, and only if it matters.

## Part 3: Structure, writing and figures
10. **Structure.** Does each part do one job and hand over to the next? Point out repetition between parts (the same point made in full twice), sections in the wrong part, and places where the "half-page rule" requires material to move to an appendix.
11. **Writing.** Flag unclear sentences, undefined abbreviations at first use, inconsistent terminology (CCD/CCX/die, V-Cache/stacked cache/L3D), inconsistent tense, and any text attributing group work to an individual. Give file:line and a suggested rewrite for at most 25 of the most important cases.
12. **Figures and tables.** Render and inspect every figure page. Flag overlapping labels, unreadable text, captions that do not say what the reader should see, figures never referenced in the text, and figures that duplicate a table without adding anything.
13. **Length and balance.** Report the page count of each part against its target (I 10, II 25, III 25, IV 25, V 25, VI 20). Say which parts most need content and what kind.

## Part 4: Course format
14. Check the PDF against the mandatory format: A4, 12 pt, single spacing, one-inch margins; page order cover → copyright and IP assignment → acknowledgements → abstract → generated contents; generated List of Tables, List of Figures, Glossary and Index; Appendix A (plagiarism report) and Appendix B (readability indices) present, and their wording only says "the tool displayed…"; diagrams programmatic (TikZ/Graphviz); code only through `listings`/`minted`. Appendices A and B are known to be placeholders: report their state, do not count it as an error.
15. List every remaining `\todo`, `\verify`, "??", placeholder, undefined reference or citation, and overfull box.

## Output
Write `research/review-initial-draft-2-v3.md` with:
1. An overall assessment (at most 10 sentences), including a provisional grade-style judgement against what an examiner would expect of an undergraduate term paper, with the two changes that would improve it most.
2. A findings table, most severe first: ID (H1, H2, …), severity (Error / Unsupported / Overstated / Inconsistent / Structure / Writing / Format / Minor), location (file:line and PDF page), what the draft says, what the source or rule says (file and page), suggested correction.
3. The regression table for F1–F23 and G1–G20: fixed / partly fixed / not fixed / regressed, with a one-line note each.
4. The 30+ spot-checked numbers, with source and page, marked correct or not.
5. The RQ-by-RQ assessment (Part 2).
6. The per-part page count and the list of what each short part needs.
7. A list of what you checked and found correct.

Change no other file.
