---
title: "Exploiting Data Compression for Adaptive Block Placement in Hybrid Caches"
authors: [Beomjun Kim, Yongtae Kim, Prashant Nair, Seokin Hong]
year: 2022
citation-key: kimExploitingDataCompression2022
status: partially-read
tags: [hybrid-cache, stt-ram, llc, draft-initial]
---

# Bibliographic record

Electronics 11(2), 240. DOI 10.3390/electronics11020240. Open access (CC BY 4.0).

# Relevance

Example of an alternative way to obtain large LLC capacity: SRAM/STT-RAM hybrid caches with an adaptive block-placement policy (Part II, alternative LLC technologies).

# Reading status

Added to Zotero (collection *ELL305 Term Paper*) on 28 October 2026. Only the abstract-level description has been seen (from search results): STT-RAM's density and low leakage, its longer write latency and energy, and a reported 26% average speedup over a baseline placement scheme in the authors' simulations. This is simulation evidence for a research proposal, not a product.

# Local source

`../../research/pdfs/Kim-Hybrid-Cache-Block-Placement-Electronics-2022.pdf` (also attached in Zotero). Abstract and introduction read 28 Oct 2026; cited in Part II (alternative LLC technologies) for the SRAM/STT-RAM trade-off and the 26% simulated speedup.

# Update 31 Oct 2026
Table 1 (NVsim, 16 MB caches, node not stated) read and used in Part VI: area SRAM 11.448 vs STT-RAM 5.024 mm²; read 6.589 vs 6.904 ns; write 3.274 vs 11.898 ns; read energy 0.191 vs 0.361 nJ; write energy 0.182 vs 1.127 nJ; leakage 462.891 vs 64.824 mW. Simulated system 3.2 GHz, 4 cores, OoO. ADAM speedup 26% avg (ideal placement 40%).
