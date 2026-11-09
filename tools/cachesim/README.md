# Cache Hierarchy Lab (ELL305 software model)

A trace-driven cache-hierarchy simulator in C++, with an interactive browser GUI that runs
the same model. It compares processor arrangements (two CCXs or one, planar or stacked L3,
a side-by-side cache die, one die or two) on identical memory traces, changing one
parameter at a time.

**This is a model, not AMD hardware.** It does not reproduce AMD's replacement policy,
prefetchers, AMD's actual L3 fill policy, physical address mapping, pipeline or 3D thermal
effects. Use it for differences between configurations, and label every result in the
paper as a model output.

## Files

| Path | What it is |
|---|---|
| `src/cachesim.cpp` | The simulator (C++17, one file, no dependencies) |
| `gui/index.html` | The GUI. Open it in a browser (loads Chart.js from a CDN) |
| `gui/index-offline.html` | The same GUI with Chart.js built in; works without internet |
| `gui/sim-core.js` | The JavaScript port of the simulator used by the GUI |
| `gui/template.html`, `gui/build.py` | Source of the GUI pages and the script that builds them |
| `experiments.json` | The ready-made experiments, extracted from the GUI by `build.py` |
| `run_experiments.py` | Runs those experiments with the C++ binary; writes CSV and PNG |
| `test/crosscheck.js` | Checks that C++ and JavaScript give identical results |
| `test/check_golden.py` | Checks the C++ binary against the JavaScript results stored in `test/crosscheck-golden.json`, for machines without Node.js (`python3 test/check_golden.py ./cachesim`). Regenerate the file with `node test/crosscheck.js ./cachesim --write-golden` whenever `gui/sim-core.js` changes; the script warns if it has. |
| `test/experiments.js` | Runs every GUI experiment in Node and prints the numbers |

## Build and run (WSL or Linux)

```bash
cd tools/cachesim
make                         # builds ./cachesim
make test                    # self-test, then C++ vs JavaScript cross-check (needs node)
python3 run_experiments.py   # all experiments -> results/*.csv (+ PNG if matplotlib is installed)
python3 run_experiments.py e1 v1 c1 --accesses 1000000 --out ../../research/measurements/cachesim
```

One run:

```bash
./cachesim --preset zen2_2ccx --set kind=random --set ws_mb=24 --set accesses=1000000
./cachesim --preset vcache --set l3_lat=55 --set clock_ghz=4.8 --set kind=graph --set threads=8
```

A real program, through Valgrind:

```bash
sudo apt install valgrind
valgrind --tool=lackey --trace-mem=yes ./myprog 2>&1 >/dev/null | ./cachesim --preset zen3_1ccx --trace -
```

The output is one JSON object (hit counts per level, hit rates, average access time,
DRAM reads and writes, transfers between groups, estimated time and the limit that binds
it, bandwidth, energy, and misses per thousand instructions for Lackey traces).

In the GUI, the **Experiments** tab runs the same experiments with one click. The
**Compare** tab highlights exactly which settings differ between A and B, so you can
keep a comparison to one changed factor.

## The model

- **Caches.** Each core has a private L1D and a private L2 that contains everything in its
  L1. Cores are split evenly into L3 groups (a CCX or a CCD), each sharing one L3. The L3
  is filled on every miss (the sources used in the paper do not state how Zen's L3 is filled).
  An optional L4 is shared by all groups (a side-by-side cache die). By default it is also filled
  on every miss, so it holds copies of L3 data; `l4_victim=1` makes it an exclusive victim cache
  that takes every L3 eviction instead. Replacement: LRU, FIFO, random or tree pseudo-LRU.
  A working set occupies contiguous line numbers, so it spreads evenly over the sets and has
  no conflict misses below capacity (real 4 KB pages are scattered over physical memory).
- **Coherence.** A directory records which cores hold each line. A write invalidates all
  other copies; a write to a line held by another core adds one L3 latency, plus the hop if a
  holder is in another group. A read of a line another core has modified is served core to core.
- **Latency.** Each access is charged the latency of the level that served it:
  L1, L2, L3; another group's L3 or core costs `2 × L3 + hop`; an L4 hit costs `L3 + L4`;
  DRAM costs `L3 + mem_ns × clock`, plus the hop when `dram_hop=1` (set in the `twoccd`
  preset: every memory access crosses to the I/O die). The overlap setting scales the part
  beyond an L2 hit (1 = no overlap). The paper's study uses 0.335, which makes a removed
  miss save about 103 cycles gross (about 101 once the stacked L3's four extra cycles on that
  workload's hits, also overlapped, are taken off), the self-consistent reading of Lam's libx264
  measurement.
- **Two latency outputs.** `amat_ns` / `amat_cycles` are the raw average latency, with no
  overlap applied, as a latency sweep measures. `exposed_ns` / `exposed_cycles` are the
  average latency after the overlap factor, the part the core actually waits for.
- **Time.** The largest of: the slowest core's latency-bound time; L3 bytes over L3
  bandwidth; DRAM bytes over DRAM bandwidth; link bytes over link bandwidth. The link
  limit is off by default (`link_gbs=0`); set `link_gbs=55` to enable it.
- **Energy.** Per-event dynamic energy. The cache and DRAM defaults are placeholders, not
  measurements. The link default (2 pJ/bit) is AMD's figure for the Zen 1 die-to-die link.
- **Warm-up.** Random and hot/cold workloads first touch the working set in order (up to
  the cache capacity), then run a separate random stream; sequential, stride and graph
  workloads run their own loop first. Statistics are reset before measurement. Ping-pong runs
  have no separate warm-up; they skip their first 40 accesses.
- **Hot/cold workload.** `hot_prob` of the accesses go to the first `hot_frac` of the working
  set and the rest to the whole set; optionally `far_prob` of them go to a separate `far_mb`
  region beyond it. Probabilities have a resolution of one in a million.

## Default values and where they come from

| Value | Source |
|---|---|
| L1 4, L2 12, L3 47 cycles; DRAM 47 cycles + 74 ns; 32 KB 8-way L1D, 512 KB 8-way L2, 16-way L3 | 7-cpu.com, Zen 3 Ryzen 5 5600G |
| Zen 2 style L3 at 39 cycles | 47 minus the 7–8 cycles that unifying the L3 added (Chips and Cheese); derived |
| Stacked 96 MB L3 at 51 cycles | AMD ISSCC 2022 (+4 cycles), confirmed on three generations |
| Planar 96 MB at 59 cycles | Assumption; sweep `l3_lat` to test it |
| L4 22 ns | Chosen so an L4 hit totals ~34 ns, in line with the more than 30 ns Lam measured for Broadwell's eDRAM |
| Hop 9 ns | Rome CCD–IOD round trip under 9 ns (Naffziger et al. 2020); its use for CCX-to-CCX is an assumption |
| 32 B/cycle per core L3 bandwidth | AMD ISSCC 2022, slide 20 |
| 51.2 GB/s DRAM; link limit off (55 GB/s if enabled) | Two DDR4-3200 channels; Naffziger et al.'s effective Rome link figure |
| 8 cores, 4 GHz, 32 MB L3 as 2 × 16 MB or 1 × 32 MB | The group's experiment plan (Zen 2 and Zen 3 style) |

## Presets

`zen2_2ccx`, `zen3_1ccx`, `vcache`, `planar96`, `sidecar`, `twoccd`, `mono16`.
See `PRESETS` in `src/cachesim.cpp` or `gui/sim-core.js`.
