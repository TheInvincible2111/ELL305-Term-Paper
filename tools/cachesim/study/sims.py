#!/usr/bin/env python3
"""Simulation study for the ELL305 term paper (Part V, sec:sim-study; Appendix E).

Runs the Cache Hierarchy Lab simulator (tools/cachesim) for experiments S0-S6 and the
sensitivity checks, and writes one CSV per experiment into the output folder.
Every point is run with five random seeds; CSVs give the mean, minimum and maximum.

    python3 sims.py --bin ../cachesim --out results            # everything (about 7 minutes on 16 threads)
    python3 sims.py --bin ../cachesim --out check --only s0 s4  # a subset

Metrics. `exposed_ns` is the average latency the core waits for after the overlap factor;
`amat_ns` is the raw average latency with no overlap (what a latency sweep measures);
`time_us` is the model's run time, which adds `work_cycles` of other work per access.
"""
import argparse, concurrent.futures as cf, csv, json, os, pathlib, statistics, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("--bin", default="./cachesim")
ap.add_argument("--out", default="results")
ap.add_argument("--accesses", type=int, default=1_000_000)
ap.add_argument("--seeds", type=int, default=5)
ap.add_argument("--jobs", type=int, default=os.cpu_count() or 2)
ap.add_argument("--only", nargs="*", default=None)
args = ap.parse_args()
OUT = pathlib.Path(args.out); OUT.mkdir(parents=True, exist_ok=True)
SEEDS = list(range(1, args.seeds + 1))

# ---- calibration constants (derived in S0b; see Appendix E) ----
# Lam's 7950X3D measurements, both CCDs at 4.2 GHz: per 1000 instructions, L3 accesses A, misses
# removed dM, and cycles saved net of the four extra L3 cycles. The overlap factor h is the value at
# which the model reproduces that net saving when it also overlaps the four extra cycles:
#     dM * h * (L3 + mem - L3_stacked) - A * 4 * h = net saving.
F_CAL, L3, L3S, MEM_NS = 4.2, 47, 51, 74
LAM = {"libx264": (3.85, 0.40, 36.0), "Cyberpunk 2077": (9.3, 1.64, 94.0), "GHPC": (13.3, 2.57, 77.0)}
def h_of(A, dM, net):
    return net / (dM * (L3 + MEM_NS * F_CAL - L3S) - A * 4)
CAL = {k: h_of(*v) for k, v in LAM.items()}
CAL_OVERLAP = round(CAL["libx264"], 3)          # 0.335
H_LOW, H_MID = round(CAL["GHPC"], 3), round(CAL["Cyberpunk 2077"], 3)

def run(preset, **kv):
    cmd = [args.bin, "--preset", preset]
    kv.setdefault("accesses", args.accesses)
    for k, v in kv.items():
        cmd += ["--set", f"{k}={v}"]
    r = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(r.stdout)

POOL = cf.ThreadPoolExecutor(args.jobs)

def runseeds(preset, metric_fns, **kv):
    """Run one point over all seeds; return ({metric: (mean, min, max)}, raw results)."""
    futs = [POOL.submit(run, preset, seed=s, **kv) for s in SEEDS]
    res = [f.result() for f in futs]
    out = {}
    for name, fn in metric_fns.items():
        vals = [fn(r) for r in res]
        out[name] = (statistics.mean(vals), min(vals), max(vals))
    return out, res

def write(name, header, rows):
    with open(OUT / f"{name}.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
    print(f"wrote {name}.csv ({len(rows)} rows)", flush=True)

def flat(d, keys):
    row = []
    for k in keys:
        row += [round(x, 6) for x in d[k]]
    return row

def mhdr(keys):
    h = []
    for k in keys:
        h += [f"{k}_mean", f"{k}_min", f"{k}_max"]
    return h

M = {
    "amat_cycles": lambda r: r["amat_cycles"],
    "amat_ns": lambda r: r["amat_ns"],
    "exposed_ns": lambda r: r["exposed_ns"],
    "l3_hit_pct": lambda r: 100 * r["l3_hit_rate"],
    "dram_per_kacc": lambda r: r["dram_per_kacc"],
    "time_us": lambda r: r["time_ns"] / 1000,
    "cross_per_kacc": lambda r: 1000 * (r["l3_remote"] + r["c2c_remote"]) / max(1, r["accesses"]),
    "dram_bw_gbs": lambda r: r["dram_bw_gbs"],
    "rt_ns": lambda r: r.get("pp_roundtrip_ns", 0),
}
def pick(*names): return {n: M[n] for n in names}
def want(tag): return args.only is None or tag in args.only

# ---------------- S0a: latency sweep against Chips and Cheese's Milan / Milan-X curve ----------
if want("s0"):
    sizes = [0.016, 0.032, 0.064, 0.128, 0.256, 0.512, 1, 2, 4, 8, 16, 24, 32, 40, 48, 64, 80, 96,
             112, 128, 192, 256, 512, 1024]
    rows = []
    for preset, label in [("zen3_1ccx", "32MB"), ("vcache", "96MB")]:
        for ws in sizes:
            d, _ = runseeds(preset, pick("amat_cycles", "l3_hit_pct"), kind="random", ws_mb=ws, threads=1, overlap=1)
            rows.append([label, ws] + flat(d, ["amat_cycles", "l3_hit_pct"]))
    write("s0_latency_sweep", ["l3", "ws_mb"] + mhdr(["amat_cycles", "l3_hit_pct"]), rows)

# ---------------- S0b: calibration of the overlap factor ------------------------------------
# For each of Lam's three workloads with a stated MPKI: the self-consistent overlap factor, and
# the gross cycles a removed miss saves in the model at that factor (64 MB random set, 4.2 GHz).
if want("s0"):
    rows = []
    cases = [(n, round(CAL[n], 3)) for n in ("GHPC", "Cyberpunk 2077", "libx264")] + [("no overlap", 1.0)]
    for name, h in cases:
        kv = dict(kind="random", ws_mb=64, threads=1, overlap=h, clock_ghz=F_CAL)
        a, ra = runseeds("zen3_1ccx", pick("dram_per_kacc"), **kv)
        b, rb = runseeds("vcache", pick("dram_per_kacc"), **kv)
        dc = [(x["t_latency_ns"] - y["t_latency_ns"]) * F_CAL / x["accesses"] for x, y in zip(ra, rb)]
        dm = [(x["dram_reads"] - y["dram_reads"]) / x["accesses"] for x, y in zip(ra, rb)]
        per = [c / m for c, m in zip(dc, dm)]
        A, dM, net = LAM.get(name, (0, 0, 0))
        rows.append([name, h, round(statistics.mean(per), 2), round(min(per), 2), round(max(per), 2),
                     A, dM, net, round(h * (L3 + MEM_NS * F_CAL - L3S), 1)])
    write("s0_calibration", ["workload", "overlap", "model_saved_per_removed_miss_mean", "min", "max",
                             "lam_l3_acc_per_kinstr", "lam_removed_per_kinstr", "lam_net_saved_per_kinstr",
                             "analytic_gross_per_removed_miss"], rows)

# ---------------- S1: working-set sweep, 32 vs 96 MB ----------------------------------------
if want("s1"):
    sizes = [2, 4, 8, 16, 24, 32, 40, 48, 64, 80, 96, 128, 192, 256]
    rows = []
    for kind in ["random", "hotcold"]:
        for ws in sizes:
            res = {}
            for preset in ["zen3_1ccx", "vcache"]:
                res[preset], _ = runseeds(preset, pick("l3_hit_pct", "exposed_ns", "dram_per_kacc", "time_us"),
                                          kind=kind, ws_mb=ws, threads=1, overlap=CAL_OVERLAP)
            sp = res["zen3_1ccx"]["time_us"][0] / res["vcache"]["time_us"][0]
            rows.append([kind, ws] + flat(res["zen3_1ccx"], ["l3_hit_pct", "exposed_ns", "dram_per_kacc"])
                        + flat(res["vcache"], ["l3_hit_pct", "exposed_ns", "dram_per_kacc"]) + [round(sp, 4)])
    hdr = ["kind", "ws_mb"] + [f"p32_{h}" for h in mhdr(["l3_hit_pct", "exposed_ns", "dram_per_kacc"])] \
          + [f"s96_{h}" for h in mhdr(["l3_hit_pct", "exposed_ns", "dram_per_kacc"])] + ["mem_speedup_96_over_32"]
    write("s1_working_set", hdr, rows)

# ---------------- S2: four ways to 96 MB; planar break-even; the side die -------------------
if want("s2"):
    sizes = [8, 16, 24, 32, 48, 64, 80, 96, 128, 192]
    designs = [("zen3_1ccx", {}, "32MB baseline"), ("vcache", {}, "96MB stacked 51c"),
               ("planar96", {}, "96MB planar 59c"), ("sidecar", {}, "32MB + 64MB L4 inclusive"),
               ("sidecar", {"l4_victim": 1}, "32MB + 64MB L4 victim")]
    rows = []
    for preset, extra, label in designs:
        for ws in sizes:
            d, _ = runseeds(preset, pick("exposed_ns", "amat_ns", "l3_hit_pct"), kind="random", ws_mb=ws, threads=1,
                            overlap=CAL_OVERLAP, **extra)
            rows.append([label, ws] + flat(d, ["exposed_ns", "amat_ns", "l3_hit_pct"]))
    write("s2_designs", ["design", "ws_mb"] + mhdr(["exposed_ns", "amat_ns", "l3_hit_pct"]), rows)
    # break-even planar latency against the 32 MB baseline (exposed latency)
    rows = []
    for ws in [24, 40, 48, 64, 80, 96]:
        base, _ = runseeds("zen3_1ccx", pick("exposed_ns"), kind="random", ws_mb=ws, threads=1, overlap=CAL_OVERLAP)
        lo, hi = 47, 600
        for _ in range(14):
            mid = (lo + hi) / 2
            d, _ = runseeds("planar96", pick("exposed_ns"), kind="random", ws_mb=ws, threads=1,
                            overlap=CAL_OVERLAP, l3_lat=round(mid, 2))
            if d["exposed_ns"][0] < base["exposed_ns"][0]: lo = mid
            else: hi = mid
        rows.append([ws, round((lo + hi) / 2, 1)])
    write("s2_planar_breakeven", ["ws_mb", "max_planar_l3_latency_cycles"], rows)
    # the side die: its latency swept, inclusive and victim (exclusive) organisations
    rows = []
    for ws in [48, 80]:
        st, _ = runseeds("vcache", pick("exposed_ns"), kind="random", ws_mb=ws, threads=1, overlap=CAL_OVERLAP)
        for lat in [5, 8, 12, 16, 22]:
            for org, extra in [("inclusive", {}), ("victim", {"l4_victim": 1})]:
                d, _ = runseeds("sidecar", pick("exposed_ns"), kind="random", ws_mb=ws, threads=1, overlap=CAL_OVERLAP,
                                l4_lat_ns=lat, **extra)
                rows.append([ws, lat, org, round(d["exposed_ns"][0], 4), round(st["exposed_ns"][0], 4)])
    write("s2_side_die", ["ws_mb", "l4_lat_ns", "l4_organisation", "side_exposed_ns", "stacked_exposed_ns"], rows)

# ---------------- S3: cache against clock --------------------------------------------------
# Access mix calibrated to Lam's libx264 run (Appendix E): a 16 KB hot region that stays in the L1;
# 0.799% of accesses to a cold region whose size is swept; 0.312% to a 1 GB far region that misses
# in both caches (so the stacked part keeps about 1.08 MPKI); one memory access per three
# instructions; L1 hits charged 1 cycle; 0.48 cycles of other work per access.
P_COLD, P_FAR = 0.00799, 0.00312
def mix(ws, overlap=None, **extra):
    d = dict(kind="hotcold", ws_mb=ws, hot_frac=0.016 / ws, hot_prob=round(1 - P_COLD - P_FAR, 6),
             far_mb=1024, far_prob=P_FAR, l1_lat=1, work_cycles=0.48,
             overlap=CAL_OVERLAP if overlap is None else overlap, threads=1)
    d.update(extra); return d
def per_kinstr(r, f):
    return r["t_latency_ns"] * f / r["accesses"] * 1000 / 3
def s3_curve(gaps, sizes, f_plain=5.15, **extra):
    rows = []
    for ws in sizes:
        p, rp = runseeds("zen3_1ccx", pick("time_us", "dram_per_kacc"), clock_ghz=f_plain, **mix(ws, **extra))
        cyc_p = statistics.mean(per_kinstr(r, f_plain) for r in rp)
        for g in gaps:
            fs = f_plain / (1 + g / 100)
            s, _ = runseeds("vcache", pick("time_us", "dram_per_kacc"), clock_ghz=round(fs, 4), **mix(ws, **extra))
            removed = (p["dram_per_kacc"][0] - s["dram_per_kacc"][0]) / 3
            rows.append([ws, g, round(fs, 4), round(p["dram_per_kacc"][0] / 3, 4), round(s["dram_per_kacc"][0] / 3, 4),
                         round(removed, 4), round(cyc_p, 1), round(p["time_us"][0] / s["time_us"][0], 4)])
    return rows
def breakeven(rows, g):
    pts = sorted((r[5], r[7]) for r in rows if r[1] == g)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if y0 < 1 <= y1:
            return x0 + (1 - y0) * (x1 - x0) / (y1 - y0)
    return None
S3_SIZES = [32, 33, 34, 35, 36, 37, 38, 40, 44, 48, 56, 64, 80, 96]
S3_HDR = ["ws_mb", "clock_gap_pct", "stacked_clock_ghz", "plain_mpki", "stacked_mpki", "misses_removed_per_kinstr",
          "plain_cycles_per_kinstr", "speedup_stacked_over_plain"]
if want("s3"):
    rows = s3_curve([0, 2, 4, 6, 7.3, 10], S3_SIZES)
    write("s3_cache_vs_clock", S3_HDR, rows)
    write("s3_breakeven", ["clock_gap_pct", "breakeven_misses_removed_per_kinstr"],
          [[g, round(breakeven(rows, g), 3)] for g in [0, 2, 4, 6, 7.3, 10]])
    # check of the mix at Lam's operating point: equal clocks of 4.2 GHz
    rows = []
    for ws in [36, 37, 37.5, 38, 39]:
        p, rp = runseeds("zen3_1ccx", pick("dram_per_kacc"), clock_ghz=4.2, **mix(ws))
        s, rs = runseeds("vcache", pick("dram_per_kacc"), clock_ghz=4.2, **mix(ws))
        cp = statistics.mean(per_kinstr(r, 4.2) for r in rp); cs = statistics.mean(per_kinstr(r, 4.2) for r in rs)
        acc = statistics.mean(r["l3_lookups"] / r["accesses"] * 1000 / 3 for r in rp)
        rows.append([ws, round(acc, 3), round(p["dram_per_kacc"][0] / 3, 3), round(s["dram_per_kacc"][0] / 3, 3),
                     round(cp, 1), round(cs, 1), round(100 * (cp / cs - 1), 2)])
    write("s3_validation_libx264", ["ws_mb", "plain_l3_acc_per_kinstr", "plain_mpki", "stacked_mpki",
                                    "plain_cycles_per_kinstr", "stacked_cycles_per_kinstr", "gain_pct"], rows)
if want("s3sens"):
    rows = []
    cases = [("calibrated (overlap 0.335)", {}), (f"overlap {H_MID} (Cyberpunk)", {"overlap": H_MID}),
             (f"overlap {H_LOW} (GHPC)", {"overlap": H_LOW}), ("overlap 1.0", {"overlap": 1.0}),
             ("memory 60 ns", {"mem_ns": 60}), ("memory 90 ns", {"mem_ns": 90})]
    for name, extra in cases:
        r = s3_curve([0, 7.3], S3_SIZES, **extra)
        b0, b7 = breakeven(r, 0), breakeven(r, 7.3)
        rows.append([name, round(b0, 3) if b0 is not None else "", round(b7, 3) if b7 is not None else ""])
    write("s3_sensitivity", ["case", "breakeven_equal_clock", "breakeven_gap_7.3"], rows)

# ---------------- S4: the chiplet split -----------------------------------------------------
if want("s4"):
    # ping-pong: same CCD vs other CCD, crossing cost swept; ratio compared with Reguly's 4.5x
    rows = []
    loc, _ = runseeds("twoccd", pick("rt_ns"), kind="pingpong", pp_a=0, pp_b=1, iters=2000)
    for hop in [0, 9, 18, 20, 29, 37, 40, 60, 100, 150, 241]:
        rem, _ = runseeds("twoccd", pick("rt_ns"), kind="pingpong", pp_a=0, pp_b=9, iters=2000, hop_ns=hop)
        rows.append([hop, round(loc["rt_ns"][0], 2), round(rem["rt_ns"][0], 2), round(rem["rt_ns"][0] / loc["rt_ns"][0], 3)])
    write("s4_pingpong", ["hop_ns", "same_ccd_rt_ns", "other_ccd_rt_ns", "ratio"], rows)
    # shared vs private data, two dies (hop also charged on every DRAM access) vs one die
    rows = []
    for share, wl in [("shared", dict(kind="hotcold", ws_mb=48, threads=16, shared=1, write_frac=0.05)),
                      ("private", dict(kind="random", ws_mb=8, threads=16, shared=0))]:
        mono, _ = runseeds("mono16", pick("exposed_ns", "dram_per_kacc"), overlap=CAL_OVERLAP, **wl)
        for hop in [9, 18, 37, 60]:
            two, _ = runseeds("twoccd", pick("exposed_ns", "cross_per_kacc", "dram_per_kacc"), overlap=CAL_OVERLAP,
                              hop_ns=hop, **wl)
            rows.append([share, hop] + flat(two, ["exposed_ns", "cross_per_kacc", "dram_per_kacc"])
                        + flat(mono, ["exposed_ns", "dram_per_kacc"]) + [round(two["exposed_ns"][0] / mono["exposed_ns"][0], 4)])
    write("s4_split", ["data", "hop_ns"] + [f"two_{h}" for h in mhdr(["exposed_ns", "cross_per_kacc", "dram_per_kacc"])]
          + [f"mono_{h}" for h in mhdr(["exposed_ns", "dram_per_kacc"])] + ["ratio_two_over_mono"], rows)

# ---------------- S5: Zen 2 -> Zen 3 L3 organisation ----------------------------------------
if want("s5"):
    sizes = [4, 8, 12, 16, 20, 24, 28, 32, 40]
    rows = []
    cases = [("zen2_2ccx", {}, "2x16MB, 39c"), ("zen2_2ccx", {"l3_lat": 47}, "2x16MB, 47c"),
             ("zen3_1ccx", {}, "1x32MB, 47c")]
    for threads, shared in [(1, 0), (8, 1)]:
        for preset, extra, label in cases:
            for ws in sizes:
                d, _ = runseeds(preset, pick("exposed_ns", "amat_ns", "l3_hit_pct"), kind="random", ws_mb=ws, threads=threads,
                                shared=shared, overlap=CAL_OVERLAP, **extra)
                rows.append([f"{threads}t{'-shared' if shared else ''}", label, ws] + flat(d, ["exposed_ns", "amat_ns", "l3_hit_pct"]))
    write("s5_zen2_zen3", ["threads", "design", "ws_mb"] + mhdr(["exposed_ns", "amat_ns", "l3_hit_pct"]), rows)

# ---------------- S6: all cores streaming -----------------------------------------------------
# Each thread streams through its own private region (ws_mb is per thread in the simulator).
if want("s6"):
    rows = []
    for preset, label in [("zen3_1ccx", "32MB"), ("vcache", "96MB")]:
        for ws in [8, 20]:
            for t in [1, 2, 3, 4, 5, 6, 7, 8]:
                d, res = runseeds(preset, pick("time_us", "dram_bw_gbs"), kind="sequential", ws_mb=ws, threads=t,
                                  shared=0, overlap=0.05, accesses=250000)
                thr = t * 250000 / (d["time_us"][0] * 1e-6) / 1e9     # G accesses per second, all threads
                rows.append([label, ws, t, t * ws] + flat(d, ["time_us", "dram_bw_gbs"]) + [round(thr, 4), res[0]["bottleneck"]])
    write("s6_streaming", ["l3", "ws_mb_per_thread", "threads", "ws_mb_total"] + mhdr(["time_us", "dram_bw_gbs"])
          + ["throughput_gaccess_s", "binding_limit"], rows)

# ---------------- Sensitivity: does the S1 conclusion survive the assumed inputs? -----------
if want("sens"):
    rows = []
    for name, extra in [("calibrated", {}), (f"overlap {H_LOW}", {"overlap": H_LOW}), (f"overlap {H_MID}", {"overlap": H_MID}),
                        ("overlap 1.0", {"overlap": 1.0}), ("memory 60 ns", {"mem_ns": 60}),
                        ("memory 90 ns", {"mem_ns": 90}), ("stacked L3 55 cycles", {"l3_lat_s": 55})]:
        for ws in [16, 64, 192]:
            kv = dict(kind="random", ws_mb=ws, threads=1, overlap=CAL_OVERLAP)
            e = dict(extra); lat_s = e.pop("l3_lat_s", None); kv.update(e)
            p, _ = runseeds("zen3_1ccx", pick("time_us"), **kv)
            kv2 = dict(kv)
            if lat_s: kv2["l3_lat"] = lat_s
            s, _ = runseeds("vcache", pick("time_us"), **kv2)
            rows.append([name, ws, round(p["time_us"][0] / s["time_us"][0], 4)])
    write("sensitivity", ["case", "ws_mb", "mem_speedup_96_over_32"], rows)

# ---------------- Replacement policy, on three workloads ---------------------------------------
# With uniformly random accesses every resident line is equally likely to be used next, so no
# replacement policy can change the hit rate; the policy matters only for workloads with reuse
# structure (hot/cold) or a cyclic order (sequential).
if want("policy"):
    rows = []
    for kind in ["random", "hotcold", "sequential"]:
        for pol in ["lru", "random", "plru"]:
            for ws in [16, 64, 192]:
                kv = dict(kind=kind, ws_mb=ws, threads=1, overlap=CAL_OVERLAP, policy=pol)
                if kind == "sequential": kv["shared"] = 0
                p, _ = runseeds("zen3_1ccx", pick("time_us", "exposed_ns"), **kv)
                s, _ = runseeds("vcache", pick("time_us", "exposed_ns"), **kv)
                rows.append([kind, pol, ws, round(p["exposed_ns"][0], 4), round(s["exposed_ns"][0], 4),
                             round(p["time_us"][0] / s["time_us"][0], 4)])
    write("s1_policy", ["kind", "policy", "ws_mb", "p32_exposed_ns", "s96_exposed_ns", "mem_speedup_96_over_32"], rows)

# ---------------- Seed spread of every stored quantity -----------------------------------------
if want("spread"):
    rows = []
    for f in sorted(OUT.glob("*.csv")):
        rd = list(csv.DictReader(open(f)))
        for col in (rd[0].keys() if rd else []):
            if col.endswith("_mean") and col[:-5] + "_min" in rd[0]:
                b = col[:-5]
                worst = 0
                for r in rd:
                    m, lo, hi = float(r[col]), float(r[b + "_min"]), float(r[b + "_max"])
                    if abs(m) > 1e-9: worst = max(worst, (hi - lo) / abs(m))
                rows.append([f.stem, b, round(100 * worst, 3)])
    write("seed_spread", ["file", "quantity", "max_spread_pct_of_mean"], rows)
