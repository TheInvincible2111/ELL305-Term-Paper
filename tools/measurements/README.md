# Hardware measurements

The paper's hardware measurements were made with the kit in `5600x-kit/` on the group's Ryzen 5 5600X (Zen 3, one CCD, six cores, 32 MB L3) on 8 November 2026, under WSL2. See `5600x-kit/README.md` for how to run it.

- Raw results, run notes and an analysis: `research/measurements/5600X/`.
- How the paper uses them: Appendix G, and the comparison with the simulation in Part V (S0).
- `ELL305-5600X-kit.zip` is the kit as it was handed to the 5600X machine.
- `latency.c` in this folder is the earlier stand-alone latency test; the kit's `latency.c` supersedes it.
- `5600x-kit/uprof-windows.md` describes an optional AMD uProf run of cache miss rates. It was not run, and the paper does not use it.
