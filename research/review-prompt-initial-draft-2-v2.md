# Prompt for a second independent review of initial-draft-2 (1 November 2026)

You are an independent technical reviewer for an undergraduate term paper (IIT Delhi, ELL305 Computer Architecture): "Modern Processor Design Beyond Monolithic Scaling: Chiplet Architectures and 3D-Stacked Cache in AMD Zen Processors". You did not write it. Your job is to find errors, not to improve the prose.

## Materials (use only these)
- Compiled draft: `build/pdf/ELL305-initial-draft-2.pdf` (about 106 pages). Check its build time is newer than every file under `initial-draft-2/`; if not, say so.
- Sources: `initial-draft-2/sections/*.tex`, `initial-draft-2/figures/*.tex`, `initial-draft-2/appendices/*.tex`.
- Bibliography: `references/references.bib`; local source PDFs: `research/pdfs/` (index: `research/pdfs/README.md`); textbook: `sources/archbook.pdf` (Sarangi).
- The first review and the authors' response: `research/review-initial-draft-2.md`, `research/review-initial-draft-2-response.md`.
- Do not use the web. If a claim cannot be checked against a local file, mark it "cannot verify", not "wrong".
- Some web-article PDFs clip charts at the page edge; extract embedded images (`pdfimages`) or render pages before concluding a value is absent.

## Scope
1. **Regression check.** For every finding F1–F23 in the first review, confirm the response's stated action is actually present in the current text, and that the fix did not introduce a new error.
2. **New material (priority).** Since the first review, the draft grew from 91 to about 106 pages. Check every number, citation and claim in:
   - Part VI: `sec:cache-clock-model` (eq:cache-clock-model, tab:cache-clock-model, fig:cache-clock-model), `sec:bandwidth-wall` (tab:per-core-resources; Reguly 2023), the Xeon Max row of tab:llc-alternatives, `sec:evidence-strength`, `sec:case-against`, `sec:limitations` (now "Threats to Validity"), `sec:implications`, fig:reguly-ratio, fig:thread-placement, and the extended Conclusions and Open Research Questions.
   - Part III: fig:l3-miss-path, fig:bandwidth-balance, fig:numa-latency, fig:nps-modes, fig:two-socket, and the new section `sec:cezanne` (Cezanne vs Vermeer) with its table.
   - Part IV: fig:libx264-waterfall, fig:stack-process.
   - Part V: fig:openfoam-sweep (values read from Lawenda Fig. 4 labels), fig:zen2-zen3-latency, fig:clock-correction, fig:vendor-vs-independent.
3. **Arithmetic.** Recompute every worked example and model output in the new material, including the break-even values 0.12 / 0.35 / 0.50 misses per thousand instructions and every row of tab:cache-clock-model. State the inputs you used.
4. **Figures vs text vs tables.** For every new figure, check that plotted values match the table or source they claim to show, that captions state the right sources, and that any value read from a chart is labelled as such.
5. **Reasoning.** Flag claims that go beyond what the sources say: causal statements from correlational data, vendor claims presented as independent, models presented as measurements, and comparisons whose confounds are not stated (especially sec:cezanne, sec:case-against and tab:evidence-strength).
6. **Internal consistency.** The same quantity must have the same value everywhere (for example the 7% / 1.073 clock gap, 4.8 vs 5.15 GHz, 130 cycles per removed miss, 3.2 / 4.8 GB/s per core, the 4-cycle latency). List any mismatch.
7. **Citations and project rules.** Every `\cite` key must exist in `references.bib` and have a local PDF listed in `research/pdfs/README.md`. No citation may support a claim its source does not make. Group work must not be attributed to individuals.
8. **Build hygiene.** No "??", undefined references or citations, or overlapping figure labels (render the pages of every new figure and look).

## Output
Write `research/review-initial-draft-2-v2.md` with:
1. A short overall assessment.
2. A findings table, most severe first: ID (G1, G2, …), severity (Error / Unsupported / Overstated / Inconsistent / Minor), location (file:line and PDF page), what the draft says, what the source says (file and page), suggested correction.
3. The regression table for F1–F23: fixed / partly fixed / not fixed / regressed, with a one-line note.
4. The recomputed arithmetic, with inputs.
5. A list of everything you checked and found correct, so the authors know what was covered.

Change no other file.
