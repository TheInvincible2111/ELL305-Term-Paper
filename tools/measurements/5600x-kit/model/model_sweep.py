#!/usr/bin/env python3
"""Runs the paper's cache model with Ryzen 5 5600X parameters, so its prediction can be put
next to the measured latency sweep.

    python3 model/model_sweep.py --bin model/cachesim --ghz 4.6 --out results/model-latency.csv

The model uses its default (7-cpu.com) latencies: L1 4, L2 12, L3 47 cycles, memory L3 + 74 ns.
--mem-ns lets you replace the 74 ns with the value measured on this machine.

It reports the model's raw average latency (amat_cycles, overlap 1), which is what a latency sweep
measures. The model maps each working set to consecutive cache lines, so it has no conflict misses
and stays flat until a cache is completely full; the measured curve will rise earlier (paper, S0).
The model source is the same as tools/cachesim/src/cachesim.cpp in the paper repository (8 Nov 2026).
"""
import argparse, csv, json, subprocess, statistics
ap = argparse.ArgumentParser()
ap.add_argument("--bin", default="model/cachesim")
ap.add_argument("--ghz", type=float, required=True)
ap.add_argument("--mem-ns", type=float, default=74)
ap.add_argument("--out", required=True)
a = ap.parse_args()
sizes_kib = [16, 32, 48, 64, 128, 256, 384, 512, 768, 1024, 2048, 4096, 8192, 16384, 24576, 32768,
             40960, 49152, 65536, 98304, 131072, 262144, 524288, 1048576]
with open(a.out, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["size_kib", "model_cycles", "model_ns", "clock_ghz", "mem_ns"])
    for s in sizes_kib:
        vals = []
        for seed in (1, 2, 3):
            cmd = [a.bin, "--preset", "zen3_1ccx", "--set", "cores=6", "--set", f"clock_ghz={a.ghz}",
                   "--set", f"mem_ns={a.mem_ns}", "--set", "kind=random", "--set", f"ws_mb={s/1024}",
                   "--set", "threads=1", "--set", "overlap=1", "--set", "accesses=400000", "--set", f"seed={seed}"]
            vals.append(json.loads(subprocess.run(cmd, check=True, capture_output=True, text=True).stdout)["amat_cycles"])
        c = statistics.mean(vals)
        w.writerow([s, round(c, 3), round(c / a.ghz, 3), a.ghz, a.mem_ns])
print("wrote", a.out)
