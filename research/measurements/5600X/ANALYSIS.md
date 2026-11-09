# Ryzen 5 5600X measurements, 8 November 2026: analysis

Raw results: `results-20261108-0724/`; the original zip is kept beside this file.

**Conditions** (`notes.md`, `sysinfo.txt`):
- Ryzen 5 5600X (one CCD, 6 cores, 32 MB L3) with PBO enabled (no Curve Optimizer or other overclock), on an MSI B550 Gaming Edge WiFi, cooled by a DeepCool AS500.
- 32 GB of DDR4-3200, CL16-20-20-40, FCLK 1600 MHz (1:1 with the memory clock).
- Run under WSL2, with the Windows power plan set to High performance.
- Core clock 4.614 GHz by the kit's estimate, before and after the run; Task Manager showed 4.6 GHz.

Cycles below are ns × 4.614. Latency values are the median of three runs.

**WSL2 caveat.** WSL2 is a virtual machine with nested paging, so a guest 2 MB page need not be a 2 MB page in the host. In addition, CPU pinning inside the VM does not fix which physical core runs a thread. Native Linux would remove both effects.

## 1. Latency at each level, against the model's inputs (a comparison of inputs, not a test of the model)

| Level | Measured, 2 MB pages | Model default input | Note |
|---|---|---|---|
| L1 (≤ 32 KB) | 0.87 ns = **4.0 cycles** | 4 cycles | matches |
| L2 (64–256 KB) | 2.61–2.63 ns = **12.1 cycles** | 12 cycles | matches |
| L3 (4–16 MB) | 11.1–12.0 ns = **51–55 cycles** | 47 cycles | 9–17% higher; part may be WSL2 address translation |
| DRAM (1 GB) | **98.6 ns** (4 KB pages: 115 ns) | L3 + 74 ns ≈ 84 ns at this clock (model output at 1 GB: 82 ns) | 17% above the input |

The model's level latencies come from 7-cpu (measured on a different Zen 3 chip) and were never fitted to this machine.
- **L1 and L2:** both match exactly in cycles.
- **L3:** about 4–8 cycles longer than the model's input.
- **Memory:** about 14 ns longer than the model's input (17 ns longer than its output at 1 GB).

### Shape of the curve: model against measurement

| Working set | Measured (2 MB) | Model, default inputs | Model refit (L3 54 cycles, memory 88 ns) | Measured ÷ refit |
|---|---|---|---|---|
| 16 MB | 11.96 ns | 9.95 | 11.42 | 1.05 |
| 23–24 MB | 14.67 | 10.03 | 11.51 | 1.27 |
| 32 MB | 24.10 | 10.07 | 11.56 | **2.08** |
| 39–40 MB | 43.41 | 24.86 | 29.05 | 1.49 |
| 46–48 MB | 49.83 | 34.84 | 41.14 | 1.21 |
| 64 MB | 66.86 | 47.07 | 55.64 | 1.20 |
| 93–96 MB | 82.91 | 59.52 | 70.41 | 1.18 |
| 128 MB | 86.81 | 65.62 | 77.70 | 1.12 |
| 1 GB | 98.56 | 81.86 | 96.92 | 1.02 |

The paper's figure (`fig:m5600x-latency`) uses a slightly different refit, L3 54 cycles and memory 90 ns, chosen so that the 1 GB value matches; it is generated with `tools/cachesim/study/compare_5600x.py` and stored in `model-comparison.csv`. With 90 ns the refit matches the 1 GB value within 1%.

Even with the level latencies refitted, the model's shape differs from the hardware's:
- **Below capacity:** the measured L3 latency starts to rise at about 16–20 MB, half to two-thirds of capacity. At 32 MB it is twice the model's value. The model stays flat until the cache is full.
- **Above capacity:** the measured latency is 12–50% higher than the model's. The model's random-uniform workload keeps hitting in a fraction (32 MB ÷ working set) of accesses. A cyclic pointer chase, as in this test, loses more of those hits under LRU-like replacement. This is review point J1.
- **What this means for S0:** the result is consistent with S0's statement that the model is optimistic near each capacity edge. On this machine the real 32 MB L3 degrades well before 32 MB. For a latency sweep, the model therefore understates the benefit of a larger L3 for working sets of about 20–64 MB; how far this carries over to real programs depends on their order of access.
- **Page placement:** with 2 MB pages, one page covers every L3 set (32 MB ÷ 16 ways = 2 MB per way). In a native system, page placement therefore cannot explain the early rise, and S0's stated main reason (scattered 4 KB pages) cannot be the whole story. Under WSL2, the host's page size is unknown. The remaining candidates are:
  - replacement that is not true LRU;
  - L3 use by other software;
  - host-side page placement and address translation.

  This test cannot separate them.

## 2. TLB effect (4 KB against 2 MB pages)

| Working set | 4 KB pages | 2 MB pages | Extra with 4 KB pages |
|---|---|---|---|
| 256 KB | 2.64 ns | 2.63 ns | 0 |
| 304 KB | 3.17 | 2.64 | +0.5 |
| 512 KB | 4.78 | 2.69 | +2.1 |
| 8 MB | 14.43 | 11.59 | +2.8 |
| 16 MB | 19.02 | 11.96 | +7.1 |
| 1 GB | 115.3 | 98.6 | +16.8 |

- **First rise:** with 4 KB pages latency starts to rise just above 256 KB. That is the reach of a 64-entry first-level data TLB (64 × 4 KB). It supports the 256 KB in `tab:tlb-reach` against 7-cpu's "about 800 KB" (review I32).
- **Second rise:** above 8 MB the 4 KB curve climbs again, the reach of a 2048-entry second-level TLB.
- **At 1 GB:** page walks add about 17 ns per access.

## 3. Memory-level parallelism (overlap)

Independent chains in a 1 GB buffer (DRAM) and a 16 MB buffer (L3), 2 MB pages:

| Independent chains *k* | DRAM ns/load | ÷ 1 chain | L3 ns/load | ÷ 1 chain |
|---|---|---|---|---|
| 1 | 104.9 | 1.000 | 11.88 | 1.000 |
| 2 | 53.5 | 0.510 | 6.65 | 0.560 |
| 3 | 36.7 | **0.349** | 4.47 | 0.376 |
| 4 | 27.8 | 0.265 | 3.37 | 0.284 |
| 6 | 18.8 | 0.179 | 2.29 | 0.192 |
| 8 | 14.8 | 0.141 | 1.74 | 0.147 |
| 10 | 11.9 | **0.113** | 1.41 | 0.119 |
| 16 | 7.5 | 0.071 | 0.91 | 0.077 |

- **Overlap scales almost perfectly.** The time per step grows only from 105 to 120 ns at 16 chains, so the core overlaps at least 16 DRAM misses with little loss.
- **Reading the model's overlap factors:** "time per load ÷ single-chain latency" is the quantity the overlap factor stands for. The three values fitted to Lam's workloads correspond to about:
  - 3 misses in flight for 0.335 (libx264);
  - 5 for 0.202 (Cyberpunk 2077);
  - 9–10 for 0.105 (GHPC).

  All three are well within what this Zen 3 core sustains. This is an independent plausibility check of the fitted range, not a measurement of those programs.

## 4. Bandwidth (read kernel unless stated)

| Case | Measured | In bytes per cycle |
|---|---|---|
| 1 thread, L2 (256 KB) | 116.5 GB/s | 25.3 B/cycle |
| 1 thread, L3 (4 MB) | 108.0 GB/s | 23.4 B/cycle (AMD's figure: 32 B/cycle per core) |
| 1 thread, DRAM (256 MB) | 30.3 GB/s | — |
| 6 threads, L3 (8–16 MB in all) | 280–296 GB/s | ≈ 47–49 GB/s per core |
| 6 threads, DRAM | 41.0 GB/s | 80% of the 51.2 GB/s peak of two DDR4-3200 channels; 6.8 GB/s per core |
| 6 threads, DRAM, triad | 25.1 GB/s counted (24 B per element) | ≈ 33 GB/s including write-allocate traffic |

**Not usable:**
- Buffers of 16–64 KB, where the parallel-region overhead of each repetition dominates.
- The 12-thread run below about 32 MB, where values are erratic (0.1–480 GB/s). SMT pairs and OpenMP synchronisation under WSL2 make the timing unreliable.

The 12-thread DRAM values (39–40 GB/s read) agree with the 6-thread ones.

## 5. Core-to-core hand-over

- **Typical round trip:** 98.5 ns (median over the 132 ordered pairs; each pair's value is the fastest of three trials; range 66–100 ns), that is about 49 ns per hand-over of the cache line between two cores of one CCD. This is the same order as Reguly's 58.6 ns within one Milan-X CCD, also measured in a virtual machine. The two tests differ in clock (4.6 GHz against a cloud server's) and in exactly what is timed.
- **Unexplained pattern:** every pair in which the responding thread ran on logical CPU 0 was faster, 66–72 ns. This is probably a WSL2 scheduling effect.
- **SMT siblings:** no pair shows the much shorter time expected for two threads on the same core. This is consistent with WSL2 not pinning virtual CPUs to physical cores.
- **Use:** these values should not be used for topology. Use them only as a rough same-CCD figure.

## 6. Reliability

- **Repeat runs:** the three 4 KB-page runs agree within about 1–3% except near capacity edges (up to 29%). The 2 MB-page runs 1 and 2 agree within about 1% up to 16 MB and at 64 MB and beyond. Between 19 and 40 MB they differ by up to 25%, close to the capacity edge. Run 3 is slower from about 19 MB and at DRAM (94–96 against 84–87 ns at 110–128 MB), probably because huge pages were only partly granted, so medians are used.
- **Clock:** the estimate was identical before and after (4.614 GHz), so the clock was stable during the run.
- **Background load:** the Windows power plan was High performance and nothing else was run deliberately, but ordinary Windows background processes may have been active. This could account for some of the run-to-run spread near the L3 capacity edge.
