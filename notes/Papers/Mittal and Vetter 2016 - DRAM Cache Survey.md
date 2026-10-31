---
title: "A Survey of Techniques for Architecting DRAM Caches"
authors: [Sparsh Mittal, Jeffrey S. Vetter]
year: 2016
citation-key: mittalSurveyTechniquesArchitecting2016
status: partially-read
tags: [dram-cache, llc, survey, draft-initial]
---

# Bibliographic record

IEEE Transactions on Parallel and Distributed Systems 27(6), 1852–1863. DOI 10.1109/TPDS.2015.2461155.

# Relevance

Ishan's notes cite this survey for the claim that very large SRAM caches become impractical because of leakage and cooling cost (Part IV, planar limits). Also a candidate source for the 'alternative LLC technologies' section in Part II.

# Reading status

Added to Zotero (collection *ELL305 Term Paper*) on 28 October 2026. 28 Oct 2026: Sec. 1 (p. 1852) read in the local PDF. **Claim confirmed in this paper**: SRAM's low density and high leakage power make large SRAM caches infeasible; such caches may need expensive cooling (e.g. liquid cooling), adding cost and complexity; SRAM LLCs could occupy 90% of chip area in future nodes. Now cited in Part IV (planar limits, Power). Also useful: the survey reviews Black et al., who stacked an 8 MB SRAM cache directly on a processor die and found higher thermal rise than stacked DRAM (p. 1853) — a precursor of V-Cache for Part IV (primary paper not in the library). Rest of the survey not yet read.

# Local source

`../../research/pdfs/Mittal-Vetter-DRAM-Cache-Survey-TPDS-2016.pdf` (IEEE version, downloaded by Ishan via IIT Delhi; also attached in Zotero).
