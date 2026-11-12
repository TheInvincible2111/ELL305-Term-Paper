# Final pre-submission review of initial-draft-2 (v9, 10 November 2026)

Reviewer brief: `research/review-prompt-initial-draft-2-v9-final.md`. No project file was edited; this file is the only output. Scratch work (renders, rebuilt simulator, rerun CSVs) is outside the project.

**Page convention.** "p." is the printed page number. Printed = PDF page − 1 (the cover is PDF page 1 and unnumbered).

**PDF freshness.** `build/pdf/ELL305-initial-draft-2.pdf` (162 PDF pages, A4, built 10 Nov 2026 21:23 with pdfTeX 1.40.22, i.e. the Linux TeX Live 2022 build) is newer than every file under `initial-draft-2/` and `paper/` (`find -newer` returns nothing). The matching log `tmp/linux-build/main-initial-draft-2.log` has 0 overfull boxes, no undefined references or citations, and no "??". The only LaTeX warning is the expected `Writing or overwriting file ./iitd-logo-embedded.pdf`. Underfull vbox warnings come from float pages and are harmless.

---

## 1. Verdict

Provisional grade: **A− as an argument, but the paper is not ready to submit.** The technical content is in good shape. I recomputed more than 60 numbers and all of them hold. The simulator reruns byte-identically. The new chart readings are accurate except for one panel. No earlier fix has regressed.

The blockers are all about packaging and leftover draft material:

- **B1:** there is no single-file `.tex`. The paper is built from about 90 `\input` files plus an external `.bib`.
- **B2:** Appendices A and B are still `\todo` placeholders. They print "[TODO: …]" on pp. 146–147.
- **B3:** the cover still says "Second Full-Paper Working Draft (initial-draft-2)" and gives the draft date. The PDF title is "ELL305 Term Paper - initial-draft-2 (working draft)".
- **B4:** the project's own packaging rule (a ZIP with image assets) conflicts with the course email ("no second file … must not be a zip"). This conflict has to be settled before any flattening.

Two high-priority items are not blockers:

- the code in Appendix E is not colour-highlighted, although Prof. Kar asked for colour (P5);
- the GitHub links point to a repository that the project notes record as private, so the examiner may not be able to open them (P6).

---

## 2. Findings

| ID | Severity | Location | What the paper says | What the source / data / rule says | Safe fix (and everything that must change with it) |
|---|---|---|---|---|---|
| P1 | **BLOCKER** | Build structure: `paper/main-initial-draft-2.tex`; `paper/styles/ell305-format.tex:40` | Modular build: about 90 `\input` files, `\addbibresource{../references/references.bib}`, and the shared style in a separate file. | Course email (`tmp/ell305-community/sources/subrat_mail_17thAug.md`): "A single LaTex file containing all diagrams … There must be no second file. The single file must not be a zip(ped) file containing multiple files", plus "a single PDF file, which must be produceable by compiling the first file". No single-file version of initial-draft-2 exists. `build/single-file-validation/` and `submissions/Draft-1/` hold Draft 1 only. | Produce `ELL305-<final>.tex` by inlining every `\input`, in this order: style; preamble, including `mindmap-style.tex`, `glossary.tex` and `logo-embedded.tex`; metadata; front matter; parts; appendices. Embed the bibliography with `\begin{filecontents*}[overwrite]{…-references.bib}` and point `\addbibresource` at that name, as Draft 1 did. The full list of what must be carried is in §4 under "Single-file checklist". Then compile it alone in an empty folder (pdflatex → biber → makeglossaries → makeindex → pdflatex ×2) and compare page count and text with the modular PDF. `scripts/validate-single-file.ps1` is Draft-1-specific (`$baseName = 'ELL305-Draft-1'`), so it needs a parameter or a copy. |
| P2 | **BLOCKER** | `appendices/appendix-a-plagiarism-report.tex:7`, `appendix-b-reading-indices.tex:6` (pp. 146–147) | "[TODO: No plagiarism-check evidence has been supplied for this draft…]" and "[TODO: No readability indices…]". | the project instructions §5: Appendix A is the plagiarism report and Appendix B the readability indices; each submission needs its own evidence from Ishan. | Run both tools on the **final** text, after every other fix and cut, and write the results in with the "the tool displayed…" wording. Do not use images: Draft 1 carried them as separate PNG files (`submissions/Draft-1/*.png`), which the single-file rule forbids. Either type the results as text or a table (preferred: the indices are seven numbers), or embed a screenshot the same way as the logo (`filecontents*` with an ASCII-hex PDF). Remove `\todo` here, and then drop the `\todo`/`\verify`/`\partbudget`/`\plannedcontent` definitions from the flattened preamble. |
| P3 | **BLOCKER** | `metadata.tex:5,7`; `front-matter.tex:20,36`; `front-matter/copyright-assignment.tex:21`; `preamble.tex:16` (cover; p. 1; PDF metadata) | Cover: "*Second Full-Paper Working Draft (initial-draft-2)*" and "8 November 2026". Copyright page signed "8 November 2026". `pdftitle={ELL305 Term Paper - initial-draft-2 (working draft)}`. | The brief's leftover list: "working draft" or "initial-draft-2" on the cover, in the PDF title, header or footer, and the draft date. The course template cover (`sources/Term paper format PFD.pdf`) reads "<course> Term paper". | Set `\draftstatusline` to "Term Paper" (this also restores the term-paper label the template uses). Set `\draftdate` to the submission date, which changes the cover and the copyright signature together. Set `pdftitle` to the paper title. Remove the draft wording from the comments in `metadata.tex:1`, `preamble.tex:1,18,68` and `paper/main-initial-draft-2.tex:1` in the flattened file. |
| P4 | **BLOCKER (a decision for Ishan)** | the project instructions §5 "Submission ZIP"; `notes/Planning/Submission Format.md` ("The final ZIP must contain … the three image assets") | The project packaging rule is a ZIP holding the `.tex`, the PDF, images and a README. | The course email forbids a second file and a zip, and asks for **two files**: one `.tex` and one PDF. | Do not resolve this silently. the project instructions says conflicts go to Ishan. My recommendation is to follow the course email: upload exactly one `.tex` and one PDF, with no ZIP, no README and no PNG. Then update §5 of the project instructions and `Submission Format.md` to match. |
| P5 | Course rule | `paper/styles/ell305-format.tex:48–56`; App. E listing (`appendix-e-simulation.tex:64–75`, p. 154) | `\lstset{basicstyle=\ttfamily\small, …}` sets no colours. The rendered listing on p. 154 is black only: keywords bold, comments italic. | Prof. Kar (`subrat_teams_21stAug.md`): code belongs "in an Appendix … with language specific color coded syntax". The code is correctly confined to App. E; no code appears in the main text. | Add `keywordstyle=\color{draftblue}\bfseries, commentstyle=\color{green!45!black}\itshape, stringstyle=\color{orange!70!black}` to `\lstset`. The style is shared, so either put the change in `initial-draft-2/preamble.tex` (an `\lstset{…}` after the style is loaded) to leave Draft 1 untouched, or accept the change for every draft. Re-render p. 154. |
| P6 | Error | Cover link (`front-matter.tex:34`); `\repourl`, `\ghdir`, `\ghfile` in Part I `:168`, App. E `:5,76`, App. G `:5` | The model, scripts, raw results and 5600X data are "on GitHub" at github.com/TheInvincible2111/ELL305-Term-Paper. | the project instructions §7 records the repository as **private** ("never make the repo public"). Without access the professor cannot open any of these links, and App. E's "After cloning the GitHub repository" cannot be followed. I could not check access (no web). Every linked path does exist and is tracked: `tools/cachesim` (18 files), `tools/cachesim/study` (3), `research/measurements/cachesim` (17), `research/measurements/5600X` (18), `tools/measurements/5600x-kit` (11), `tools/cachesim/gui/index.html`. Local `HEAD` equals `origin/main` (f19d19f). | A decision for Ishan, which I do not make here: (a) give the course staff read access (collaborator or a time-limited invite); (b) leave the repository private and add one sentence where the repository is first mentioned (Part I contributions bullet), e.g. "access on request"; or (c) remove the links. Do not make the repository public without Ishan's explicit decision; the project instructions forbids it. |
| P7 | Figure (chart reading) | `figures/isscc-cache-charts.tex:21,23`; Fig. 30(b), p. 74 | The last node is plotted at 7 nm in 2019, almost on the dashed 0.7×-per-two-years line (6.2 nm at 2019). The caption says "after 22 nm the nodes arrive later than that pace". | On Wuu slide 6 (rendered) the last point, labelled "10/7nm", lies clearly **above** the dashed extrapolation, about 24 px at 2019 against a step of about 30 px per node. On the slide's own spacing that is about the 10 nm position, not 7 nm. The slide's left chart has **no y-axis values**, so the redraw's numeric log axis (7–90 nm) is the paper's own construction. As drawn, the panel hides the slowdown the slide was made to show, and the "10/7" label overlaps the data line. | Plot the last point at 10 (the "10/7" class) or at the slide's measured position, so that it sits visibly above the dashed line; move the label to the right of the point (`anchor=west` at about (2019.2, 10)). Better still, make panel (b) shape-only like panel (a): remove `ytick`/`yticklabels`, label each point with its node, and add "no axis values on the slide" to the caption. Keep "Values are read from the slides and are approximate." Nothing in the text quotes these values (`part4:14` only says "the slowing pace of new nodes"), so no other place changes. |
| P8 | Inconsistent | `part1:149`; `part2:2` (comment), `part2:10` (p. 33) | "Chapters 9–12 of Sarangi's *Basic Computer Architecture* supply the models…"; Part II "follows Chapters 9–12". | The paper cites Sarangi ch. 7 ten times (secs 7.4.1 and 7.4.3: the SRAM and DRAM cells, Figs. 8–9), ch. 9 twice, ch. 10 21 times, ch. 11 33 times and ch. 12 34 times. That is **five chapters: 7, 9, 10, 11, 12**. | Write "Chapters 7 and 9–12" in both places (and in the flattened comment). This also feeds P9. |
| P9 | Course rule | Part I (`sec:method-overview` or `sec:scope`), p. 29–30 | Nowhere does the paper state in one place which textbook chapters the topic maps to, or that this makes Prof. Sumantra Dutta Roy (Chapters 1–12) the advisor. The advisor appears only in the acknowledgements. | Prof. Kar's Draft 1 brief asked for "How does it map to a Chapter in our textbook" and the advisor choice. The course routing: Chapters 1–12 → Prof. Dutta Roy; Chapter 13 → Prof. Kar. The paper uses only Chapters 7–12, which matches its stated advisor; Sarangi's DRAM section points to Ch. 13 for SDRAM timing, which the paper does not use. | Add two sentences to `sec:method-overview` item 1, e.g. "The topic maps to Chapters 11 (memory system) and 12 (multiprocessors) of the course textbook, with foundations from Chapters 7, 9 and 10; all lie within Chapters 1–12, so the faculty advisor is Prof. Sumantra Dutta Roy." Do not put this on the cover (the project instructions §5). |
| P10 | Inconsistent (minor) | `part4:171` (p. 83); `appendix-f-directory-example.tex:60` (p. 157); `part5:436` | "at an IPC of 1.43 the same work takes about 699 cycles, **4.9% fewer**"; App. F: "the model gives a 5.2% gain, against the 4.9% Lam reports, a difference within the rounding of the inputs". | Lam's 4.9% is an **IPC gain** (`ChipsAndCheese-7950X3D-2023.pdf`: "We still see a 4.9% IPC gain"). The paper's 36 cycles come from the rounded chart IPCs (1.36 → 1.43), which give a 5.1% IPC gain, or 4.9% fewer cycles. The two 4.9% figures are different quantities and match only by coincidence. The model's 5.2% is a speed-up, so it should be compared with 5.1%, not 4.9%. | `part4:171`: "about 699 cycles, 4.9% fewer (an IPC gain of 5.1% from the rounded chart values; Lam states 4.9%)". App. F `:60`: "the model gives a 5.2% gain, against 5.1% from the chart IPCs and the 4.9% Lam states". `part5:436`: replace "to within rounding (5.2%)" with "(5.2% against the chart's 5.1%)". `tab:lam-detail` and `tab:cache-vs-clock` keep 4.9% (Lam's figure), which is correct there. |
| P11 | Inconsistent (minor) | `part5:581` (p. 127) | "the overlap factor and the 37 ns hop are fitted to measurements". | Everywhere else the 37 ns is "fitted to a ratio" (S4 text, `tab:sim-parameters`, `fig:sim-pingpong`), as the brief requires. | "…the overlap factor is fitted to measurements and the 37 ns hop to a measured ratio; the latencies of…". |
| P12 | Writing (terminology) | `part5:444, 522, 524`; `part6:85`; `part1:180` | Section 28 is titled "Simulation", but its text calls the simulator "the model" ("the model's overlap factor hides two thirds…", `:522`) right next to "the analytical model". | In `:522` "the model" (the simulation) and "the analytical model" (`eq:cache-clock-model`) appear in one paragraph. A reader can take "the model" to mean the analytical one. Nowhere does "the simulation" read as a measurement: every use is labelled as model output or "not independent". | Inside `sec:sim-study`, say "the simulation" for results and "the simulator" for the program, and keep "the analytical model" for `eq:cache-clock-model`. At least fix `:522` ("the simulation's overlap factor hides…") and `:524` ("In the simulation the overlap factor scales…"). Also edit the Part V file comment (`part5:2–3`, "controlled software model") in the flattened file. |
| P13 | Figure (legibility) | `figures/zen-ccd-evolution.tex:7,54–55` (p. 95); `epyc-package.tex:5` (p. 57); `dram-array.tex:5,13`, `sram-array.tex:5–6` (p. 38); also `nps-modes`, `set-assoc`, `topologies`, `horizontal-vs-vertical`, and the data labels in `chiplet-cost-chart` and `zen2-zen3-latency` | Text set in `\tiny`: the "L2 512 KB" boxes, the "structural silicon over cores" labels, "MC", "cell", "T". | `\tiny` at a 12 pt base is 6 pt, below the brief's 7 pt print threshold. On p. 95 the "512 KB" labels are the smallest text in the paper. The 13 overview maps are fine: leaf text works out to about 8.5 pt after `\resizebox`. | Change `\tiny` to `\scriptsize` (8 pt) and widen the boxes where needed. For the CCD figure, an alternative is to write only "L2" in each box and give "512 KB per core" once in the caption (it is already in `tab:zen-progression`). Re-render each changed page. |
| P14 | Figure (minor) | `figures/dram-array.tex:38` (p. 38) | A "refresh" box floats beside the sense amplifiers, connected to nothing. | Text and caption: "a refresh circuit on its bit lines" / "that writes the data back" (Sarangi sec. 7.4.3: "a dedicated refresh circuit connected to the bit lines"). | Draw a short connector from the refresh box to the bit-line or sense-amplifier row. Everything else in Fig. 9 matches Sarangi 7.4.3 (checked against `archbook.pdf` p. 293): one bit line, refresh, sense amplifiers before the column multiplexer holding the open row. |
| P15 | Figure (minor) | `figures/mindmap-paper.tex:46` (Fig. 4, p. 31) | The "Synthesis (Part VI)" branch has the leaf "Cache against clock". | Cache against clock is sec. 27, in Part V; Part VI only cites it (sec. 33). | Move the leaf to the Part V branch (replacing "Confounds; model" with "Cache against clock; simulation") and give Part VI "Strength of evidence". |
| P16 | Writing (residue of the "worked example" removal) | `appendix-f-directory-example.tex:3,9,37,60`; `appendix-c-yield-cost-model.tex:43,70` | App. F is now "Further Calculations", with label `app:worked-examples`; its subsections still open "This example supports…" / "This example calibrates…"; App. C has "This example supports" twice. | The brief: the label "worked example" was removed everywhere. Nothing broken remains: the main text no longer refers to the cut pipeline-depth or write-traffic examples, and no stale `\cref` or "the example above" refers to removed material. App. C's "In the example above" (`:32`) refers to its own numbers, which are still there. | "This calculation supports…" (×4) and "This calculation calibrates…". Optionally rename the label to `app:further-calculations`; it has no `\ref` users. |
| P17 | Minor (source comments in the submitted file) | `figures/mindmap-*.tex:1` (13 files); `front-matter/logo-embedded.tex:3` | "% Generated from the original tree by tmp/gen_mindmaps.py"; "Generated by tmp/logo/make_embedded_logo.py". | `tmp/` is gitignored, so these scripts are not in the repository. The comments point to files nobody else can see. No AI-tool name appears in any source comment or anywhere in the PDF apart from the page-3 statement. The only "AI" matches are "Ryzen AI Max PRO 300" (p. 65). | Strip these comments while flattening. |
| P18 | Course rule (a discrepancy to note) | `tmp/ell305-community/README.md`, `TERM_PAPER.md` against `sources/` | README: Draft 1 "must include a section titled Background Preparations"; TERM_PAPER: milestone drafts are evaluated independently, but content is cumulative. | The email texts say different things. "Background Preparations" is Utkarsh Roy's instruction for **Project** reports (`utkarsh_teams_20thAug.md`), not term papers. Garima Singhal: "any preliminary draft … is evaluated independently and is not related to the final term paper submission". Prof. Kar: "The submissions are cumulative. What is included in Draft 1 is corrected … and included in Draft 2". The emails disagree with each other; the summaries blur this. | No change to the paper. The final paper is a corrected and extended version of the earlier material, carries no Draft 1 "Section 1: Work done as of…" text (checked) and no progress percentages, which satisfies both readings. Ask a TA if the Gradescope rubric matters. |
| P19 | Writing (long sentences, 56–63 words) | `part3:123` (two sentences), `:307`, `:367`; `part4:66`, `:152`, `:178`, `:188`; `part5:246`, `:250`, `:309`, `:475` (two, the longer 63 words), `:517`; `part6:123`; `appendix-c:43` | Fifteen sentences of 56–63 words. | The brief's threshold is about 55 words. | Split each at its semicolon or colon. Examples: `part5:475` "Fitting the L3 and memory latencies to this machine … is a calibration: it aligns … (within 5% and 1%). It does not remove the differences near the capacity edges, which remain …"; `part3:367` end the sentence after "(4.0 against about 4.85 GHz)" and start "CapFrameX notes…"; `part4:152` give the Zen 5 measurement its own sentence. |
| P20 | Writing (undefined abbreviation) | `part3:268` (p. 66) | "a 2.5D bridge (AMD's label, EFB)". | EFB is never expanded. All other abbreviations checked are defined at first use: CCD, IOD, GMI, xGMI, NPS, HBM, MPKI, TDP, DVFS, LRU, ECC/DECTED, SoIC, OPIO, UCIe, RTL, PBO, WSL2. | "(AMD's Elevated Fanout Bridge, EFB)" — but only if Lambert's slide 5 spells it out. Otherwise "(labelled EFB on AMD's slide)". |
| P21 | Minor (pronouns, group work) | — | — | No gendered pronouns in sections, appendices or front matter. Lam, Cozma and Reguly are referred to by name. Group work is always "the group". | No change. |

**Checked and not a finding:**
- The "Use of AI Tools" statement (p. 3) is consistent with the collective-authorship line above it and with the rest of the front matter.
- The running header fits on one line on every page I viewed.
- The page order is cover, copyright (p. 1), acknowledgements (p. 2), abstract (p. 3), contents (p. 4), List of Tables (p. 9), List of Figures (p. 13), Glossary (p. 21). The template's physical pages 1–4 hold.

---

## 3. Cuts

Each cut lists everything that must change with it. "Refs" counts `\cref`/`\ref` uses found by a scan of all sources. Page estimates are for the body unless stated. No cut removes a caveat that a finding depends on.

### Cuts that do not re-open a decision (ranked by benefit to the reader)

| ID | Location, length | Cut or shorten to | Why the argument does not need it | Everything that must change with it | Pages saved |
|---|---|---|---|---|---|
| C1 | Repeated caveats: (a) "Lam's counters include prefetches and speculative accesses…" at `part1:179`, `part4:178`, `part5:194`, `:246`, `:481`, `:485`, `:587`, `part6:223`, App. E `:46`; (b) the 5600X framing ("inputs agree, within 20%, up to 2.4× at 32 MB, in a VM") at the abstract, `part1:182`, `part5:444`, `:475`, `:584`, `:587`, `part6:149`, `:192`, `appendix-g:74`; (c) "4.5 times as long, in the one measurement available" at `part1:176`, `part3:187`, `:382`, `part6:217` | State each caveat in full once, where its evidence is: (a) `part4:178`; (b) S0 `part5:475` and App. G; (c) `part3:187`. Elsewhere keep a short clause with a `\cref`: (a) "apparent, see `sec:tradeoff-example`"; (b) shorten `part6:192` from 8 lines to 2 and `part5:584` to one clause; (c) keep the number and drop the repeated qualifier in the Part III summary. | The caveats are needed, but a reader who meets them eight times starts to skim. Each finding keeps the caveat it depends on, either in full or by reference. | The abstract, Findings (`part1:179–182`) and Conclusions RQ4 keep their caveat words, shortened, not removed. `tab:evidence-strength` row "The simulations" keeps "up to 2.4 times too low". No labels, figures or citations are lost. | about 0.8 |
| C2 | `sec:bond-process` "How a hybrid bond is made", `part4:135–145`, about 0.6 page including the siloxane reaction | Keep two sentences: hybrid bonding joins oxide and slightly recessed copper pads without solder, which is why the pitch can be so fine; Zen 4 moved the bond-pad via to the aluminium pad (`alam…`, slide 11–12). Keep `fig:bond-interface` if wanted; it is referenced once (`:143`), so keep that sentence. | The scope list (`part1:131`) excludes "fabrication chemistry … beyond what is needed to explain an architectural decision", and the project instructions §3 says "No fabrication chemistry". The architectural point, no solder and therefore a fine pitch, needs one sentence. | `sec:bond-process` has 0 refs. `alam2ndGeneration3D2024` stays cited (slides 9 and 10–14 elsewhere). Glossary `hybrid-bonding` is unaffected. The `mindmap-stacked` leaf "Oxide bond, then anneal" (Fig. 29) must become "No solder" or be dropped. | about 0.5 |
| C3 | `tab:evidence-ledger` and `sec:evidence-ledger` (`part5:161–186`), about 0.8 page | Move the table to a new short appendix (or the end of App. G's neighbour), keep the "Two patterns stand out" paragraph in place, and point to the appendix. | It overlaps `tab:independent` (results) and `tab:confound-grid` (what is controlled). The reader needs the pattern, not every row. | `tab:evidence-ledger` has 1 ref (`part5:163`); update it to the appendix. `sec:evidence-ledger` has 0 refs. No citation becomes unused: each ledger source is cited elsewhere in Part V. | about 0.7 (moved) |
| C4 | `tab:op-sequence` and the write-buffer/critical-word paragraph, `part2:225–246`, about 0.7 page | Drop `tab:op-sequence` and its lead-in sentence. Shorten the write-buffer/critical-word paragraph to one sentence ("Write buffers and critical-word-first shorten the miss penalty rather than the miss rate, and complement a larger cache.") | Neither is used later. What matters for chiplets is write-back traffic over the link (`:244`), which stays. | `tab:op-sequence`: 1 ref (`:225`), remove it. `tab:cache-optimisations` keeps its "Write buffer, critical word first" row. `mindmap-misses` leaves "Write buffer" and "Critical word first" stay valid. `\cite[sec.~11.2.7…]` disappears with the table, but Sarangi stays cited. | about 0.6 |
| C5 | Two-level page-table example and MMU/page-fault detail, `part2:276–278`, about 0.4 page | Keep: pages and frames, 4 KB pages, TLB 32–64 entries, 99% hit rate, reach. Drop the 32-bit 2.5 MB/500 MB example, CR3 and the page-fault sentence. | The argument uses TLB reach (`app:tlb-reach`, the 5600X steps), not page-table structure. | No labels lost. `sec:virtual-memory` (3 refs) keeps its heading. The Sarangi 11.4.5 citations go, but the book stays cited. | about 0.35 |
| C6 | Part II "Beyond SRAM: alternative LLC technologies", `part2:304–305`, about 0.4 page | Shorten to two sentences pointing to `sec:llc-alternatives`, where `tab:llc-alternatives` and the "Denser memory technologies" paragraph give the same Mittal and Kim figures with more context. | The material is said twice, roughly 90 pages apart. | Kim (`kimExploitingDataCompression2022`) and Mittal stay cited in Part VI and Part IV, so no citation becomes unused. The `mindmap-foundations` leaf "Other LLC technologies" can stay. The Kim key in the `DeclareSourcemap` (`preamble.tex`) is unaffected. | about 0.3 |
| C7 | Wang's Z-order L1 cache paragraph, `part2:188`, about 0.25 page | Cut. | It is about L1 data layout for matrices and images, and the paragraph itself calls it "far from AMD's last-level cache". It is irrelevant to the central question. | **This is the only appearance of `wangDesignImplementationCache2019`.** Its reference entry then drops out of the bibliography, its row in `research/pdfs/README.md` (row 20) becomes unused, and its key in the `DeclareSourcemap` regex (`preamble.tex`) becomes dead (harmless). Update the Zotero notes accordingly. | about 0.25 |
| C8 | "Scaling beyond one socket" and `fig:two-socket`, `part3:233–236`, about 0.6 page | Keep one sentence: "Two sockets connect through xGMI links that reuse PCIe lanes, so inter-socket bandwidth is traded against I/O lanes \cite{amd2022epyc7003}." Drop the figure. | Two-socket lane budgeting is product configuration (the scope excludes product catalogues). | `fig:two-socket`: 1 ref (`:234`), remove it. Nothing else quotes the 128/160 lanes. `amd2022epyc7003` stays cited. | about 0.5 |
| C9 | `fig:nps-modes`, `part3:104–106`, about 0.35 page | Drop the figure and keep `tab:nps-modes`. | The table gives the same three groupings plus bandwidth. | `fig:nps-modes`: 1 ref (`:104`), remove it. `tab:nps-modes` (2 refs) stays. The `mindmap-chiplets` leaf "NPS1, 2, 4" stays. | about 0.35 |
| C10 | Findings `sec:findings`, `part1:174–183`, about 1.2 pages | Shorten each of the seven bullets to its bold claim plus one sentence with the key number and a `\cref`. The full statements are in the parts and the Conclusions. | A one-pass reader meets every finding again in the Part summaries and in sec. 40. | Keep the numbers the brief lists as consistency anchors (4 cycles, 96 MB, 0.1→0.35, 0.38 "not independent", 4.5×, 2%, 2.4×) in their current wording, so the consistency grep still passes. No labels change. | about 0.5 |
| C11 | Conclusions RQ2, `part6:217–219`, about 0.6 page | Remove the repeated product-range sentence (it also appears in `part3:381` and Findings) and the Zen 4c aside; keep RQ2a, the hop, sharing ×4.5, link power ≈2%. | Repetition. | None. | about 0.2 |
| C12 | `tab:topologies` plus `tab:topology-example`, `part2:389–433`, about 0.8 page | Merge them into one table with formula columns plus N = 8 and N = 64 columns (Ring, Mesh, Torus, Hypercube only). | Two tables for one point: rings are fine at 8 nodes and poor at 64. | `tab:topologies` has 3 refs (`:389`, `:412`, and the `tab:topology-example` caption); `tab:topology-example` has 1 (`:412`); point all of them to the merged label. `fig:topologies` (2 refs) stays. | about 0.3 |
| C13 | `sec:ed2`, `part2:79–81`, about 0.15 page | Cut. | ED² is never used later (`sec:ed2` has 0 refs). | The `mindmap-foundations` leaf "Thermal resistance, ED²" becomes "Thermal resistance". `\index{ED$^2$ metric}` goes with it. | about 0.15 |
| C14 | Abstract (p. 3), about 430 words | Cut to about 250: drop the textbook/sources sentence, the "trace-driven model … illustrates" sentence (keep the 0.1→0.35 result), and merge the two 5600X sentences into one. | The abstract is the professor's first page. It is now nearly a full page of dense text. | Keep "first two generations (Zen 3 and Zen 4)", "by one outlet", and "2.4 times (at 32 MB, measured in a virtual machine)". | 0 (readability) |
| F1 | List of Figures and List of Tables, pp. 9–20 (front matter, 12 pages) | Give each float a short optional caption (`\caption[short]{long}`), as the v8 response already proposed. | The lists reproduce every long caption in full. | Captions themselves are unchanged. Check that no list entry is left with "??". | about 6 (front matter) |

**Total, not re-opening decisions:** about 5.5 body pages, of which 0.7 are moved to an appendix, plus about 6 front-matter pages from F1.

### Cuts that re-open an earlier decision (listed separately, as asked)

| ID | Location, length | Proposal | Why | What must change with it | Pages |
|---|---|---|---|---|---|
| R1 | `sec:sim-study`, `part5:442–584` (about 13 pages, sec. 28) | Keep S0, S1, S3 and S4 in the body, cut to about 6 pages. Move S2's side-die details (`tab:sim-side-die`), S5 (`fig:sim-zen2-zen3`), S6 (`fig:sim-streaming`), `tab:sim-policy`, `tab:sim-sensitivity` and the sensitivity paragraph to App. E. | Sec. 28 is the longest section of the body. Its results are explicitly weak evidence (`tab:evidence-strength`), and S5 and S6 restate published points. | Refs to update: `sec:sim-designs` (1), `sec:sim-bandwidth` (1, from App. G), `tab:sim-policy` (cited from S0 `:479` and App. E/G), `sec:sim-sensitivity` (Conclusions RQ4). The `sec:sim-limits` bullets (S2 side die, S5) must say "App. E". `tab:sim-plan` rows S5 and S6 become "App. E". `tab:rq-map` row RQ3 cites `sec:sim-designs`; keep that label in the body (the S2 core stays). No citation becomes unused. | about 4–5 moved |
| R2 | Overview maps (13 figures, about 7 pages) | Keep `fig:mindmap-paper`, the four part-summary maps (chiplet trade-off, stack costs, synthesis, case study) and `mindmap-rq`. Drop the five that repeat an adjacent table or list: `mindmap-misses` (= `tab:cache-optimisations`), `mindmap-confounds` (= the bullet list above it), `mindmap-implications` (= the four paragraphs above it), `mindmap-future`, and `mindmap-foundations`. | Each dropped map restates the text on the same or the facing page. | Each dropped map has exactly 1 ref ("\Cref{fig:mindmap-…} maps / arranges / gathers…"); delete those one-line sentences. The LoF renumbers automatically. P15 applies only if `mindmap-paper` is kept. | about 3 |
| R3 | Cezanne comparison `sec:cezanne`, `part3:341–371` (about 2.3 pages with the table) | Keep `tab:cezanne-vermeer` and the "What the comparison shows" paragraph; shorten the three bold paragraphs to about 6 sentences in all. | The section reaches a deliberately weak conclusion ("no visible hop, without showing how large it is"). | `sec:cezanne` has 5 refs, `tab:cezanne-vermeer` 3 (S0 quotes the "about 53 cycles"). Keep both labels. `tab:three-way` and `tab:evidence-strength` cite `sec:cezanne`; keep their wording. `devtechprofileWhomCezanneCould2021` and `waltonAMDRyzen72021` must keep at least one citation each (the table keeps both). | about 1.2 |
| R4 | The four main-text examples kept by decision (AMAT on two processors; address split; MSI two-core trace; shared counter) | Move the AMAT and address-split examples (`part2:120–186`, about 1.5 pages) to App. F and keep their conclusions as two sentences each. | Each is a self-contained calculation of more than half a page, which falls under the half-page rule. | `sec:amat-example` and `sec:address-example` are referenced from `part2:282` and App. D `:9`; update them. `tab:amat-example` and `tab:address-split` move with them. `justiceAMDRyzen72021` stays cited (Part III, Part V). | about 1.3 moved |

**Total, re-opening decisions:** about 10 body pages, about 7 of them moved to appendices.

**The three cuts that would help most:** if earlier decisions may be re-opened, **R1** (halves the longest section), **C1** (removes the eightfold caveats) and **R2** (removes five pages of maps that repeat the facing page). Without re-opening any decision: **C1, C2 and C3**.

---

## 4. Fix order and final checklist

Apply the fixes in this order so that later steps do not undo earlier ones:

1. **Decisions first (Ishan):** P4 (two files, no ZIP); P6 (repository access); which re-opening cuts (R1–R4), if any, to take.
2. **Cuts**, from the end of the paper backwards, so that `file:line` positions in this review stay valid: R1 → C3 → C10/C11 → R3 → C8/C9 → C2 → C13/C12/C7/C6/C5/C4 → R2 → C1 (caveats last, once their surrounding text is final) → C14 (abstract, written last).
3. **Text fixes:** P8, P9, P10, P11, P12, P16, P19, P20.
4. **Figure fixes:** P7, P13, P14, P15. Re-render every changed page.
5. **Format and course fixes:** P3 (cover, date, PDF title), P5 (listing colours), F1 (short captions).
6. **Rebuild the modular PDF** and check the log.
7. **P2:** run the plagiarism and readability tools on the final text and write the results in as text.
8. **P1:** flatten to a single `.tex` (checklist below), compile it alone in an empty folder, and compare with the modular build.
9. **P17:** strip comments during flattening.

**Single-file checklist (P1).** The flattened file must carry or replace:
- every `\input`: style, preamble, `mindmap-style.tex`, `glossary.tex`, `logo-embedded.tex` (already a `filecontents*`), metadata, front matter, 6 parts, about 75 figure files, 7 appendices;
- the bibliography: `filecontents*[overwrite]` with the Better BibTeX export, then `\addbibresource{<that name>}`. The `.bib` has 37 entries and the paper cites 36; `swaminathanNextFrontierEnabling2022` is uncited and may be left in or out. Without C7, all 36 keys must be present;
- the Appendix A/B evidence, as text or an embedded ASCII PDF — no PNG;
- glossary and index generation: `\makeglossaries`, `\glsaddall`, `\printglossary`, `\makeindex`, `\printindex`. These need `makeglossaries` and `makeindex` runs. Overleaf's latexmk runs them automatically; a local check must run them explicitly;
- no `\graphicspath`. The only `\includegraphics` is the embedded logo, which I verified compiles with MiKTeX 25.12 `pdflatex -no-shell-escape` in an empty folder;
- the `\IfDocumentMetadata` shim that `build-linux.sh` passes on the command line is **not** in the source, so it must not be needed on MiKTeX or Overleaf. The validation compile must therefore use MiKTeX or a current TeX Live, not the 2022 workspace;
- **no other external dependency remains.** pgfplots, TikZ libraries, newtx, biblatex-ieee and glossaries are standard packages.

**Final checklist:**
- [ ] Modular rebuild: 0 overfull boxes, 0 undefined references or citations, no "??", no "[TODO"/"[VERIFY", no "Target length", no "working draft" or "initial-draft-2" in the PDF text or in `pdfinfo` Title.
- [ ] Single `.tex` compiled alone in an empty folder (pdflatex → biber → makeglossaries → makeindex → pdflatex ×2). Same page count as the modular build, and `pdftotext` diff limited to the build date.
- [ ] Grep for every number changed by P10 or the cuts (4.9, 5.1, 5.2, 0.35, 0.38, 2.4, 4.5, 37 ns), and for the consistency anchors in brief §1.3.
- [ ] Every `fig:`/`tab:` label still has at least one `\cref`. Today all 123 floats do (110 explicit labels, plus the 13 maps labelled through the `\mapfigure` macro).
- [ ] `python test/check_golden.py ./cachesim`: 15/15 identical; `--selftest`: 0 failures.
- [ ] Render pages 1, 38, 74, 95, 154 and every page touched by a cut, and view them.
- [ ] `git status`: `iitd-logo-embedded.pdf` not staged (today it is written to `tmp/linux-build/`, which is ignored; a Windows build writes it into `build/aux/`, also ignored).

---

## 5. Regressions

**None found.** I re-checked these earlier items against the current source and PDF:

- **v8 N1–N12:**
  - N1: App. C bonding-yield limit, 139.3/154 ≈ 90%;
  - N2: RQ3 "No measurement of a V-Cache part's energy use…";
  - N3: `part4:131`, C4 / micro-bump / hybrid wording;
  - N5: SMT sharing at `part2:302`;
  - N6: "every memory access" at `part3:158`;
  - N7: S4 "Only the ratio can be fitted…";
  - N8: "probably one reason why";
  - N9: "close to each cache's capacity…";
  - N10: abstract "first two generations (Zen 3 and Zen 4)";
  - N11: Findings heading;
  - N12: the kit zip is gitignored, which is correct, and is not linked from the paper.
- **v7 items:**
  - M2: S4 states 2.4× too fast and 97 ns;
  - M3: "single-CCD chiplet part";
  - M10: "probably because";
  - M14: "uniform" only for the per-access penalty;
  - M15: glossary "hop = one CCD–IOD round trip" and "2 links apart";
  - M17: "V-Cache CCD / plain CCD";
  - M18: Lam's bar;
  - M19: 10.63 ns;
  - M22: WSL2 expanded at first use (`part2:280`);
  - M25: "4.5 times as long" in all four places.

All of these are still fixed.

---

## 6. Spot-checked numbers (64)

"Recomputed" means I redid the arithmetic. "Source" means I checked it against the local PDF's text, or rendered the slide.

| # | Number (location) | Source / method | Result |
|---|---|---|---|
| 1 | Reticle about 800 mm² (`part3:13`, Fig. 16) | Swaminathan HC33 slide 3, rendered: the line at about 0.89 of a decade above 100, i.e. about 780 mm² | correct ("about 800", approximate) |
| 2 | 1008 mm²; 1008/800 ≈ 1.26; 592/800 = 0.74 | Recomputed | correct |
| 3 | Cost per yielded mm² 1.0, 1.5, 1.6, 2.0, 2.2, 3.7, 4.9 (Fig. 18b) | Wuu slide 6, pixel-measured at 300 dpi: 1.00, 1.44, 1.63, 1.95, 2.18, 3.69, 4.88 | correct within ±0.1 (32 nm is 1.44, labelled 1.5) |
| 4 | Area scaling shape (Fig. 18a) | Wuu slide 6 pixels: the SRAM/logic gap at 5 nm is 132/159 of logic's drop; redraw 3.85/4.55 | correct shape |
| 5 | "Analog / I/O" legend | Lambert 2025 slide 3 labels "ANALOG I/O" | supported |
| 6 | IPC-uplift steps (Fig. 30a) | Wuu slide 5: steps 84, 104, 98, 108, 72 px → 1.29, 2.90, 4.45, 6.11, 7.25 | correct |
| 7 | Node 10/7 at 2019 (Fig. 30b) | Wuu slide 6 | **P7** |
| 8 | DRAM array features (`part2:103`, Fig. 9) | Sarangi p. 293, sec. 7.4.3 | correct (P14 is a drawing detail) |
| 9 | 55 GB/s per IFOP link | Naffziger ISSCC 2020 text | correct |
| 10 | 13 FCLK, < 9 ns | Naffziger | correct |
| 11 | 2 pJ/bit (Zeppelin) | Naffziger | correct |
| 12 | 19% average memory-latency reduction | Naffziger | correct |
| 13 | 10–20 mm package routes | Naffziger | correct |
| 14 | 0.88 W per link; 3.3 W Rome; 7.4 W and 2.05% Genoa | Recomputed | correct |
| 15 | EPYC 9654: 96 cores, 2.40 / 3.70 / 3.55 GHz, 360 W, 384 MB | 9004 datasheet (raw text) | correct |
| 16 | EPYC 9684X: 2.55 / 3.70 / 3.42 GHz, 400 W, 1152 MB | Datasheet | correct |
| 17 | 9174F: 4.10 GHz base, 320 W, 256 MB; 9124: 3.00 GHz, 200 W, 64 MB | Datasheet | correct |
| 18 | 9224: 24 cores, 64 MB → 2.7 MB per core | Datasheet; recomputed | correct |
| 19 | 9354 280 W, 256 MB; 9334 210 W, 128 MB; 9184X 320 W, 768 MB | Datasheet | correct |
| 20 | 460.8 GB/s; 4.8 GB/s per core | Datasheet; recomputed | correct |
| 21 | Lam: plain CCD about 7% faster; 4.8 vs 5.15 GHz | Lam text | correct |
| 22 | Lam: 18.45 B/cycle/core; 64 GB/s per CCD | Lam text | correct |
| 23 | Lam: MPKI 1.48, 0.35, 0.28; 5 and 5.5 | Lam text | correct |
| 24 | Lam: libx264 hit rate 61.5 → 72.8% (text) vs 71.86 (chart), "16.75%" | Lam text; 71.86/61.55 = 1.1675 | correct, as the paper explains |
| 25 | Lam: about 10% gap, 5800X3D (4.5 GHz) vs 5950X (5.05 GHz) | Lam text; 5.05/4.5 = 1.12 | correct |
| 26 | 0.62 / 0.71 TB/s from 18.45 B/cycle | Recomputed | correct |
| 27 | libx264 chain: 3.85, 1.08, 0.40, 15, 735, 699, 3–14%, 130 | Recomputed | correct (P10 is wording) |
| 28 | DCS: 3.2 vs 3.7 accesses, +15%, predicted 0.24 | Recomputed | correct |
| 29 | `tab:lam-per-miss` GHPC 13.3 / 2.57 / 77 / 53 / about 50 (53 with 10.4%) | Recomputed | correct |
| 30 | Cyberpunk 9.3 / 1.64 / 94 / 37 / about 80 | Recomputed | correct |
| 31 | Geometric mean 1.114; ^(5/6) 1.094; median 9.75% | Recomputed | correct |
| 32 | Net-at-stock 0.98, 1.03, 1.03, 1.06, 1.12 | Recomputed | correct |
| 33 | Cache–clock model: C = 543, s = 31 ns, +5.2%, +1.0%, −6.7%, −8.7%, break-evens 0.12 / 0.35 / 0.50; 0.10 at 4.8 and at 5.15 GHz; memory share 26% / 30% | Recomputed from `eq:cache-clock-model` | correct |
| 34 | Overlap factors 0.335 / 0.202 / 0.105; 306.8 cycles; 103 cycles | Recomputed (App. E equation) | correct |
| 35 | Milan-X break-even 1.2–2.8 points (3.65/313, 3.65/130) | Recomputed | correct |
| 36 | 9800X3D: 1.2 V and 1.4 V; about 20 µm; 300 MHz and 500 MHz deficits; 7.5% / 15% | Cozma 2024 text | correct |
| 37 | 300/5500 = 5.5%; 5.2/5.7 → about 9%; per-clock 18–26% | Recomputed | correct |
| 38 | Reguly: 296 and 310 GB/s, about 75% of peak; 1446 GB/s, 4.8×; 14× / 6× / 3.8× | Reguly text | correct |
| 39 | Reguly tiling 4× / 2.7× / 1.84×; 1446/310 = 4.7× | Reguly text; recomputed | correct |
| 40 | Core-to-core 265/58.6 = 4.5; 206/18 = 11.4; 0.12 / 0.53 / 0.80 s | Recomputed (inputs from Reguly's Fig. 2, as tabulated) | correct |
| 41 | Lawenda: 0.81–1.54×, 1.24, 1.70×, 2.67× | Lawenda text | correct |
| 42 | Domke: up to 3.4× on MiniFE | Domke text | correct |
| 43 | MiniFE bytes per point 245–310 / 276–328 | Recomputed | correct |
| 44 | Phoronix 420 tests | Phoronix text | correct |
| 45 | 7-cpu: L3 47 cycles; 40 cycles to the nearest slice; RAM 47 cycles + 74 ns | 7-cpu text | correct |
| 46 | Slice average (0+6+1+10+6+13+10+20)/8 = 8.25 → about 48 | Recomputed | correct |
| 47 | Black: 88.35 → 92.85 °C; 88.43; +0.08 °C | Black text | correct |
| 48 | Kim Table 1: area 11.4 / 5.0 mm²; read 6.6 / 6.9 ns; write 3.3 / 11.9 ns; write energy 0.18 / 1.13 nJ; leakage 463 / 65 mW | Kim text (realigned columns) | correct |
| 49 | TechSpot 5700G: 10% multi-threaded, 11% games, 15% system power | TechSpot text | correct |
| 50 | CapFrameX: 4.5–4.55 GHz; 3.22% | CapFrameX text | correct |
| 51 | AMD 19% IPC; 25 workloads at a locked 4 GHz; 3800XT | AMD press release text | correct |
| 52 | Murphy yields 82.4 / 68.8 / 87 / 38%; 44% and 63% silicon ratios | Recomputed | correct |
| 53 | Triangular 82.1 / 67.9 / 34.4%; Poisson 81.9 / 67.0% | Recomputed | correct |
| 54 | Dies per wafer 955.2 − 77.5; 119.4 − 27.4; 95 vs 35; ×2.7 (1.9 / 3.5); edge loss 8% / 23% | Recomputed | correct |
| 55 | Stack yields 85.4 / 92.2 / 79.1%; 154 / 139.3 / 155 mm²; D0 = 0.1 → 5%, 0.3 → 14% | Recomputed | correct |
| 56 | Product line 101 / 110 / 124 vs 100 / 108 / 121 mm²; 0.7–3%; 140.7 at 99% | Recomputed | correct |
| 57 | Chiplet split 0.64 (4 cm² into 4 × 1.05 cm²) | Recomputed | correct |
| 58 | Pad density 772 / 12 346 / 44; 16×; about 280×; 4096 wires, 5.3 and 92 mm² | Recomputed | correct |
| 59 | L3D tags 6528 KB, 10%, 51 bits per line, 26-bit tag, 98 304 sets | Recomputed | correct |
| 60 | AMAT 1.60 / 1.46 / 1.38 ns; L3+memory 0.56 / 0.53 / 0.45; about 5% | Recomputed | correct |
| 61 | Amdahl 5.93 / 9.14 / 15.42; address split 36 / 32 / 27-bit tags; inclusion 12.5% / 4.2% / 2.8× | Recomputed | correct |
| 62 | 5600X: 4.0 / 12.0–12.4 / 51–55 cycles; 2.4× and 2.1× at 32 MB; 1.2–2.1× (19–38 MB); 1.1–1.3× (45–108 MB); 66.9 vs 56.6 ns at 64 MB | `model-comparison.csv` (regenerated byte-identically) | correct |
| 63 | 5600X: 4.614 GHz before and after; PBO; DDR4-3200 CL16-20-20-40 1T; FCLK 1600; WSL2; 132 c2c pairs | `results-…/notes.md`, `clock-*.csv`, `c2c.csv` | correct |
| 64 | S2 / S6: 6.21 vs 6.87 ns (−10%); 5.88 baseline (17% / 5.6%); 41/51.2 = 80%; 6.8 GB/s per core; 25% too high | Recomputed | correct |

---

## 7. Page counts (printed pages)

| Part | Pages | Count |
|---|---|---|
| Front matter: cover, copyright, acknowledgements, abstract, contents, LoT, LoF, glossary | cover + 1–23 | 24 (LoT 4, LoF 8, glossary 2) |
| I Introduction and research framing | 24–32 | 9 |
| II Architectural foundations | 33–51 | 19 |
| III Chiplet-based architecture | 52–72 | 21 |
| IV 3D-stacked cache | 73–92 | 20 |
| V Case study and quantitative analysis | 93–127 | 35 (sec. 28 "Simulation" alone is about 13) |
| VI Synthesis, limitations, future directions | 128–142 | 15 |
| References | 143–145 | 3 |
| Appendices A–G | 146–160 | 15 (A 1, B 1, C 3, D 1, E 3, F 3, G 3) |
| Index | 161 | 1 |
| **Body (I–VI)** | 24–142 | **119** |

---

## 8. What was checked and found correct

- **Build and freshness:** the PDF is newer than every source; the log has 0 overfull boxes, no undefined references or citations, and no "??".
- **Simulation:**
  - built with `g++ -O2 -std=c++17` (MSYS2 UCRT64): `--selftest` gives **0 failures**;
  - `check_golden.py`: **15/15 identical** to the stored JavaScript results (Node.js is not installed, so `crosscheck.js` was not run);
  - `sims.py --only s0 s4 policy` into a scratch folder gives `s0_latency_sweep.csv`, `s0_calibration.csv`, `s4_pingpong.csv`, `s4_split.csv` and `s1_policy.csv`, all **byte-identical** to `research/measurements/cachesim/` (2 min 49 s for those three groups);
  - `compare_5600x.py` gives `model-comparison.csv` byte-identical, and `m5600x-latency.tex` and `m5600x-table-mlp.tex` identical to the paper's figure files.
- **App. E and App. G against the code and kit:**
  - App. E's parameter table, calibration equation and S3 mix match the scripts' outputs;
  - App. G's conditions match `notes.md`, `sysinfo.txt` (THP `madvise`) and the clock files;
  - App. G's "fastest of three trials" matches the c2c method noted in v7 M23.
- **Citations:**
  - all 36 cited keys exist in `references.bib`, and every one has a PDF row in `research/pdfs/README.md` (the textbook is in `sources/`);
  - vendor figures are attributed to AMD throughout (e.g. "AMD reports", "by AMD's figure", "AMD's qualification results");
  - no source was found cited for a claim it does not make among the 64 spot checks;
  - the `.bib` entries have Better BibTeX form (`{{…}}` title protection, `urldate`, `date`, BBT-style keys). Five keys (`naffziger2020chiplet`, `suggs2019zen2`, `wuu2022vcache`, `amd2022epyc7003`, `sarangi2025basic`) are not BBT's auto pattern, which suggests pinned citation keys. Whether they come from Zotero cannot be verified without Zotero.
- **Embedded logo:**
  - renders correctly on the cover;
  - `iitd-logo-embedded.pdf` is not tracked (`git ls-files` shows only the old PNGs);
  - a minimal document that `\input`s `logo-embedded.tex` compiles with **MiKTeX pdflatex `-no-shell-escape`** in an empty folder with no warnings;
  - no other image file is needed by the paper.
- **GitHub links:** every `\ghdir`/`\ghfile` path exists and is tracked, and `HEAD` equals `origin/main`. Every mention of a repository folder in the body is a `\ghdir` link or sits in App. E's listing directly under "After cloning the GitHub repository" (access: P6).
- **Removed material:**
  - no reference remains to the cut pipeline-depth or write-traffic examples;
  - "worked example" does not occur in the PDF text;
  - `part2:46` and `:244` read naturally as conclusions.
- **Consistency anchors (brief §1.3):** all are consistent, except the minor P10 and P11:
  - 4 cycles and 96 MB;
  - 7% / 1.073 and 4.8 vs 5.15 GHz, with the rounding explained in `part5:440`;
  - 130 apparent cycles and 103 gross;
  - break-evens 0.1 (0.12 at 4.2 GHz), 0.35 and 0.50; simulated 0.04 and 0.38, each marked "not independent" or "expected rather than independent";
  - 9 / 18 / 37 ns;
  - 58.6 / about 265 / 49 / 98.5 ns;
  - about 2%;
  - the 5600X triple;
  - 100 / 108 / 121 mm², 0.7–3% and about 90%;
  - about 800 mm²;
  - "first two generations (Zen 3 and Zen 4)", "cache-on-top stack", "V-Cache CCD / plain CCD".
- **Floats:** all 123 floats (68 figures, 55 tables) are referenced. The only float far from its first reference is `fig:area-scaling` (first cited on p. 25, placed on p. 55), which is intended: it is cited from the Part I bullet and belongs to sec. 6.3.
- **Mostly empty pages:** only the Part title pages, the end of Part VI (p. 142), and Appendices A and B (placeholders, P2).
- **Format:** A4, 12 pt, single spacing, 1-inch margins (from the shared style; page size checked with `pdfinfo`). Page order cover → copyright → acknowledgements → abstract → contents → LoT → LoF → glossary, with the index last. All diagrams are TikZ or pgfplots. There are no waveforms or timing diagrams, so the WaveDrom rule does not apply. Code appears only in App. E via `listings`.
- **Course mapping:** the textbook chapters used (7, 9–12) all fall in Prof. Dutta Roy's range, matching the stated advisor. The Draft 1 "Work done as of" section does not appear. No AI-tool name appears outside the page-3 statement.
