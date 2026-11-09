#!/usr/bin/env python3
"""Compares the group's Ryzen 5 5600X measurements with the paper's cache model and writes the
paper's figure and tables for them.

    python3 compare_5600x.py --bin tools/cachesim/cachesim \
        --results research/measurements/5600X/results-20261108-0724 \
        --csv research/measurements/5600X/model-comparison.csv --figures initial-draft-2/figures

Measured values are the median of the kit's three runs. The model is run twice at the measured
clock: with its default inputs (L3 47 cycles, memory L3 + 74 ns, from 7-cpu.com) and with two
inputs refitted to this machine (L3 54 cycles, the measured 2 MB-page plateau at 8-16 MB;
memory 90 ns, so that the 1 GB value matches). Random accesses, no overlap, three seeds."""
import argparse, csv, json, pathlib, statistics as st, subprocess
ap = argparse.ArgumentParser()
ap.add_argument("--bin", required=True); ap.add_argument("--results", required=True)
ap.add_argument("--csv", required=True); ap.add_argument("--figures", required=True)
a = ap.parse_args()
R = pathlib.Path(a.results); F = pathlib.Path(a.figures)
GHZ = float(list(csv.DictReader(open(R / "clock-after.csv")))[-1]["estimated_ghz"])
REFIT = {"l3_lat": 54, "mem_ns": 90}

def median_runs(kind):
    runs = [list(csv.DictReader(open(R / f"latency-{kind}-run{i}.csv"))) for i in (1, 2, 3)]
    return [(float(r[0]["size_kib"]), st.median(float(x["ns_per_load"]) for x in r)) for r in zip(*runs)]
m4k, m2m = median_runs("4k"), median_runs("2m")

def model(kib, **extra):
    vals = []
    for seed in (1, 2, 3):
        kv = dict(cores=6, clock_ghz=GHZ, kind="random", ws_mb=kib / 1024, threads=1, overlap=1,
                  accesses=400000, seed=seed); kv.update(extra)
        cmd = [a.bin, "--preset", "zen3_1ccx"] + sum((["--set", f"{k}={v}"] for k, v in kv.items()), [])
        vals.append(json.loads(subprocess.run(cmd, check=True, capture_output=True, text=True).stdout)["amat_ns"])
    return st.mean(vals)

rows = []
for (s, y2), (_, y4) in zip(m2m, m4k):
    rows.append([round(s, 1), round(y2, 3), round(y4, 3), round(model(s), 3), round(model(s, **REFIT), 3)])
with open(a.csv, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["size_kib", "measured_2m_ns", "measured_4k_ns", "model_default_ns", "model_refit_ns", ])
    w.writerows(rows)
print("wrote", a.csv)

def coords(col):
    return " ".join(f"({r[0] / 1024:.4g},{r[col]:.4g})" for r in rows)
(F / "m5600x-latency.tex").write_text(rf"""\begin{{figure}}[htbp]
\centering
\begin{{tikzpicture}}
\begin{{axis}}[
  width=0.9\textwidth, height=7.2cm,
  xmode=log, log basis x=2, xmin=0.00390625, xmax=1024, ymode=log, ymin=0.6, ymax=160,
  ytick={{1,2,5,10,20,50,100}}, yticklabels={{1,2,5,10,20,50,100}},
  xtick={{0.00390625,0.03125,0.25,2,16,128,1024}}, xticklabels={{4\,KB,32\,KB,256\,KB,2\,MB,16\,MB,128\,MB,1\,GB}},
  xlabel={{Size of the data region (log scale)}}, ylabel={{Time per dependent load (ns, log scale)}},
  legend pos=north west, legend style={{font=\scriptsize}}, legend cell align=left,
  grid=major, grid style={{draftgray!20}}]
\addplot[mmred,very thick] coordinates {{{coords(1)}}};
\addlegendentry{{Measured, 2\,MB pages}}
\addplot[mmamber,thick,dashed] coordinates {{{coords(2)}}};
\addlegendentry{{Measured, 4\,KB pages}}
\addplot[draftgray,thick,dotted] coordinates {{{coords(3)}}};
\addlegendentry{{Model, default inputs (not fitted)}}
\addplot[draftblue,thick] coordinates {{{coords(4)}}};
\addlegendentry{{Model, L3 and memory latency fitted to this machine}}
\addplot[draftgray,thin,forget plot] coordinates {{(32,0.6) (32,160)}};
\node[font=\scriptsize,text=draftgray,anchor=south west,rotate=90] at (axis cs:32,1.2) {{32\,MB L3}};
\end{{axis}}
\end{{tikzpicture}}
\caption{{The group's Ryzen~5 5600X (one CCD, 32\,MB L3, {GHZ:.2f}\,GHz) against the model of \cref{{sec:sim-study}}: pointer-chasing latency, median of three runs, under WSL2 (\cref{{app:5600x}}). With its default inputs (dotted), the model's plateaus are the published latencies of another Zen~3 chip, which it takes as inputs; L1 and L2 agree with this machine's, and L3 and memory are within about 20\%. Its own behaviour shows only between the plateaus. Fitting those two latencies to this machine (54 cycles, and 90\,ns beyond the L3; solid blue) is a calibration that aligns the plateaus and the 1\,GB value by construction. Two differences remain after it. Just above each capacity the measured latency is higher, partly because a pointer chase visits its lines in a fixed cycle, which the model's random accesses do not reproduce (\cref{{tab:sim-policy}}); and the measured L3 begins to slow down at about 16--20\,MB, before it is full. 4\,KB pages add the TLB misses of \cref{{tab:tlb-reach}}.}}
\label{{fig:m5600x-latency}}
\end{{figure}}
""")
print("wrote m5600x-latency.tex")

# overlap of independent misses
mlp = list(csv.DictReader(open(R / "mlp.csv")))
def med(size, k): return st.median(float(r["ns_per_load"]) for r in mlp if r["size_mib"] == size and r["chains"] == str(k))
body = ""
for k in (1, 2, 3, 4, 6, 8, 10, 16):
    body += f"    {k} & {med('1024', k):.1f} & {med('1024', k) / med('1024', 1):.3f} & {med('16', k):.2f} & {med('16', k) / med('16', 1):.3f} \\\\\n"
(F / "m5600x-table-mlp.tex").write_text(rf"""\begin{{table}}[htbp]
  \centering
  \caption{{Overlap of independent misses on the group's Ryzen~5 5600X: time per load when the core follows $k$ independent pointer chains through memory (1\,GB) or through the L3 (16\,MB), and that time as a fraction of the single-chain latency (median of three runs; \cref{{app:5600x}}). The fraction is what the model's overlap factor stands for.}}
  \label{{tab:m5600x-mlp}}
  \small
  \begin{{tabular}}{{@{{}}ccccc@{{}}}}
    \toprule
    \textbf{{Chains $k$}} & \textbf{{Memory (ns/load)}} & \textbf{{Fraction}} & \textbf{{L3 (ns/load)}} & \textbf{{Fraction}} \\
    \midrule
{body}    \bottomrule
  \end{{tabular}}
\end{{table}}
""")
print("wrote m5600x-table-mlp.tex")
