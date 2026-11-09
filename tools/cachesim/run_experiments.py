#!/usr/bin/env python3
"""Runs the ready-made experiments with the C++ simulator and writes CSV files (and PNG plots
if matplotlib is installed). The experiment definitions come from experiments.json, which
gui/build.py extracts from the GUI, so both always run the same experiments.

    ./build.sh                             # builds ./cachesim
    python3 run_experiments.py             # all experiments, 400 000 accesses per point
    python3 run_experiments.py e1 v1 c1    # selected experiments
    python3 run_experiments.py --accesses 1000000 --out ../../research/measurements/cachesim
"""
import argparse, concurrent.futures as cf, csv, json, os, pathlib, subprocess, sys

here = pathlib.Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("ids", nargs="*", help="experiment ids (default: all)")
ap.add_argument("--accesses", type=int, default=400000, help="measured accesses per point, split across threads")
ap.add_argument("--out", default=str(here / "results"), help="output folder")
ap.add_argument("--bin", default=str(here / "cachesim"))
ap.add_argument("--jobs", type=int, default=os.cpu_count() or 2)
args = ap.parse_args()

spec = json.loads((here / "experiments.json").read_text())
base, exps = spec["wl_base"], spec["experiments"]
if args.ids:
    exps = [e for e in exps if e["id"] in args.ids]
out = pathlib.Path(args.out); out.mkdir(parents=True, exist_ok=True)

METRICS = {  # same definitions as the GUI
    "l3_hit_rate": ("L3 hit rate (%)", lambda r: 100 * r["l3_hit_rate"]),
    "l3_miss_rate": ("L3 miss rate (%)", lambda r: 100 * r["l3_miss_rate"]),
    "amat_ns": ("Average access time (ns)", lambda r: r["amat_ns"]),
    "amat_cycles": ("Average access time (cycles)", lambda r: r["amat_cycles"]),
    "dram_per_kacc": ("DRAM reads per 1000 accesses", lambda r: r["dram_per_kacc"]),
    "cross_per_kacc": ("Transfers between groups per 1000 accesses", lambda r: 1000 * (r["l3_remote"] + r["c2c_remote"]) / max(1, r["accesses"])),
    "l1_hit_rate": ("L1 hit rate (%)", lambda r: 100 * r["l1_hit_rate"]),
    "l2_hit_rate": ("L2 hit rate (%)", lambda r: 100 * r["l2_hit_rate"]),
    "time_us": ("Estimated time (us)", lambda r: r["time_ns"] / 1000),
    "throughput": ("Throughput (G accesses/s)", lambda r: r["throughput_gaps"]),
    "speedup": ("Throughput relative to first point", lambda r: r["throughput_gaps"]),
    "dram_bw": ("DRAM bandwidth used (GB/s)", lambda r: r["dram_bw_gbs"]),
    "energy": ("Energy per access (pJ)", lambda r: r["energy_pj_per_access"]),
    "roundtrip": ("Ping-pong round trip (ns)", lambda r: r.get("pp_roundtrip_ns", 0)),
}

def run_point(preset, extra, wl):
    cmd = [args.bin, "--preset", preset]
    for k, v in {**(extra or {}), **wl}.items():
        cmd += ["--set", f"{k}={v}"]
    return json.loads(subprocess.run(cmd, check=True, capture_output=True, text=True).stdout)

try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
except ImportError:
    plt = None

for ex in exps:
    pkey, pname = ex["param"].split(".")
    jobs = []
    for s in ex["series"]:
        for v in ex["values"]:
            wl = {**base, **ex["wl"], **s.get("wl", {})}
            wl["accesses"] = args.accesses if ex.get("perThread") else max(20000, round(args.accesses / max(1, wl["threads"])))
            extra = dict(s.get("extra", {}))
            if s.get("sweep", True) is not False:
                (extra if pkey == "cfg" else wl)[pname] = v
            jobs.append((s["name"], v, s["preset"], extra, wl))
    print(f"{ex['id']}: {ex['title']} ({len(jobs)} runs)", flush=True)
    with cf.ThreadPoolExecutor(args.jobs) as pool:
        results = list(pool.map(lambda j: run_point(j[2], j[3], j[4]), jobs))
    rows = []
    for (name, v, *_), r in zip(jobs, results):
        rows.append({"series": name, ex["param"]: v, **{k: r[k] for k in r}})
    with open(out / f"{ex['id']}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    if plt:
        for mk in ex["metrics"]:
            label, fn = METRICS[mk]
            fig, ax = plt.subplots(figsize=(7, 4))
            for s in ex["series"]:
                ys = [fn(r) for (name, *_), r in zip(jobs, results) if name == s["name"]]
                if mk == "speedup" and ys and ys[0]: ys = [y / ys[0] for y in ys]
                xs = [str(v) for v in ex["values"]] if isinstance(ex["values"][0], str) else ex["values"]
                ax.plot(xs, ys, marker="o", linestyle="--" if s.get("dash") else "-", label=s["name"])
            ax.set_xlabel(ex["param"].split(".")[1]); ax.set_ylabel(label); ax.set_title(ex["title"], fontsize=10)
            ax.grid(alpha=.3); ax.legend(fontsize=8); fig.tight_layout()
            fig.savefig(out / f"{ex['id']}-{mk}.png", dpi=150); plt.close(fig)
print(f"results in {out}")
