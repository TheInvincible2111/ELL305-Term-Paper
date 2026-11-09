#!/usr/bin/env python3
"""Turns the CSVs in a results folder into pgfplots figures and tables for the paper (figures/sim-*.tex).

    python3 make_figures.py RESULTS_DIR FIGURES_DIR

Every simulated value comes from a CSV. The only values typed here are the measured Milan and
Milan-X latency points of fig:sim-latency, read from the paper's fig:milanx-latency, and
Reguly's measured ratio (265 / 58.6 ns) in fig:sim-pingpong."""
import csv, pathlib, sys
R = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "results")
F = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "figures"); F.mkdir(exist_ok=True)

def rows(name):
    with open(R / f"{name}.csv") as f:
        return list(csv.DictReader(f))

def coords(pts):
    return " ".join(f"({x:g},{y:.4g})" for x, y in pts)

def save(name, body):
    (F / f"{name}.tex").write_text(body)
    print("wrote", name)

# ---- S0: latency sweep, model against Chips and Cheese -----------------------------------
s0 = rows("s0_latency_sweep")
m32 = [(float(r["ws_mb"]) * 1024, float(r["amat_cycles_mean"])) for r in s0 if r["l3"] == "32MB"]
m96 = [(float(r["ws_mb"]) * 1024, float(r["amat_cycles_mean"])) for r in s0 if r["l3"] == "96MB"]
milan = "(32,4) (48,12) (256,12) (512,17) (1024,40) (2048,48) (16384,47.5) (32768,52) (65536,240) (131072,290) (1048576,342)"
milanx = "(32,4) (48,12) (256,12) (512,16) (1024,42) (2048,51) (65536,51) (98304,65) (131072,150) (262144,260) (1048576,313)"
save("sim-latency", rf"""\begin{{figure}}[htbp]
\centering
\begin{{tikzpicture}}
\begin{{axis}}[
  width=0.94\textwidth, height=6.6cm,
  xmode=log, log basis x=2, ymode=log, log basis y=2,
  xmin=16, xmax=1048576, ymin=2, ymax=512,
  xtick={{32,512,8192,32768,98304,1048576}}, xticklabels={{32\,KB,512\,KB,8\,MB,32\,MB,96\,MB,1\,GB}},
  ytick={{4,8,16,32,64,128,256}}, yticklabels={{4,8,16,32,64,128,256}},
  xlabel={{Size of the data region accessed (log scale)}}, ylabel={{Average latency (cycles)}},
  legend pos=north west, legend style={{font=\scriptsize}}, legend cell align=left,
  grid=major, grid style={{draftgray!20}}]
\addplot[draftgray,thick] coordinates {{{coords(m32)}}};
\addlegendentry{{Model, 32\,MB L3 (47 cycles)}}
\addplot[draftblue,very thick] coordinates {{{coords(m96)}}};
\addlegendentry{{Model, 96\,MB L3 (51 cycles)}}
\addplot[draftgray,only marks,mark=o,mark size=1.8pt] coordinates {{{milan}}};
\addlegendentry{{Measured, Milan (Chips and Cheese)}}
\addplot[draftblue,only marks,mark=*,mark size=1.6pt] coordinates {{{milanx}}};
\addlegendentry{{Measured, Milan-X (Chips and Cheese)}}
\end{{axis}}
\end{{tikzpicture}}
\caption{{S0: the model's raw average latency (no overlap) for random accesses to a region of growing size (lines; mean of five seeds, spread smaller than the line width) against the latency sweep Chips and Cheese measured on Milan and Milan-X (points, read from \cref{{fig:milanx-latency}}) \cite{{cozmaAMDsVCacheTested2022}}. The level latencies are inputs, so their match is expected. The shape between them is not: the model's L3 stays flat up to its full capacity, whereas the measured curves rise earlier.}}
\label{{fig:sim-latency}}
\end{{figure}}
""")

# ---- S1: working-set sweep ---------------------------------------------------------------
s1 = rows("s1_working_set")
def s1pts(kind, col):
    return [(float(r["ws_mb"]), float(r[col])) for r in s1 if r["kind"] == kind]
save("sim-working-set", rf"""\begin{{figure}}[htbp]
\centering
\begin{{tikzpicture}}
\begin{{axis}}[
  name=hit, width=0.42\textwidth, height=5.8cm,
  xmode=log, log basis x=2, xmin=2, xmax=256, ymin=0, ymax=105,
  xtick={{2,8,32,96,256}}, xticklabels={{2,8,32,96,256}},
  xlabel={{Working set (MB, log scale)}}, ylabel={{L3 hit rate (\%)}},
  title={{\small (a) L3 hit rate}}, legend style={{font=\scriptsize,at={{(0.03,0.03)}},anchor=south west}},
  grid=major, grid style={{draftgray!20}}]
\addplot[draftgray,thick] coordinates {{{coords(s1pts("random", "p32_l3_hit_pct_mean"))}}};
\addlegendentry{{32\,MB, random}}
\addplot[draftblue,very thick] coordinates {{{coords(s1pts("random", "s96_l3_hit_pct_mean"))}}};
\addlegendentry{{96\,MB, random}}
\addplot[draftgray,thick,dashed] coordinates {{{coords(s1pts("hotcold", "p32_l3_hit_pct_mean"))}}};
\addlegendentry{{32\,MB, hot/cold}}
\addplot[draftblue,very thick,dashed] coordinates {{{coords(s1pts("hotcold", "s96_l3_hit_pct_mean"))}}};
\addlegendentry{{96\,MB, hot/cold}}
\end{{axis}}
\begin{{axis}}[
  at={{(hit.east)}}, anchor=west, xshift=2.3cm, width=0.42\textwidth, height=5.8cm,
  xmode=log, log basis x=2, xmin=2, xmax=256, ymin=0.9, ymax=4.6,
  xtick={{2,8,32,96,256}}, xticklabels={{2,8,32,96,256}},
  xlabel={{Working set (MB, log scale)}}, ylabel={{Speed-up, 96 over 32\,MB}},
  title={{\small (b) Speed-up of the memory system}}, legend style={{font=\scriptsize,at={{(0.03,0.97)}},anchor=north west}},
  grid=major, grid style={{draftgray!20}}]
\fill[draftblue!8] (axis cs:32,0.9) rectangle (axis cs:96,4.6);
\addplot[draftblue,very thick] coordinates {{{coords(s1pts("random", "mem_speedup_96_over_32"))}}};
\addlegendentry{{random}}
\addplot[draftblue,very thick,dashed] coordinates {{{coords(s1pts("hotcold", "mem_speedup_96_over_32"))}}};
\addlegendentry{{hot/cold}}
\addplot[draftgray,thin] coordinates {{(2,1) (256,1)}};
\end{{axis}}
\end{{tikzpicture}}
\caption{{S1: the effect of tripling the L3 against the size of the working set, all else equal (one thread; overlap factor 0.335; mean of five seeds). (a) The L3 hit rate. (b) The model's memory-system time (exposed latency plus one cycle of other work per access) with 32\,MB divided by that with 96\,MB; values below 1 are the four extra cycles. The gain is confined to working sets between the two capacities (shaded) and fades beyond 96\,MB, the three regimes of \cref{{fig:working-set}}. Because almost every access in these synthetic workloads reaches the L3 or memory once the working set is well above the L2, the speed-ups are those of the memory system, not of a program.}}
\label{{fig:sim-working-set}}
\end{{figure}}
""")

# ---- S2: four designs ------------------------------------------------------------------------
s2 = rows("s2_designs")
styles = {"32MB baseline": "draftgray,thick", "96MB stacked 51c": "draftblue,very thick",
          "96MB planar 59c": "mmamber,thick,dashed", "32MB + 64MB L4 inclusive": "mmteal,thick,dash dot",
          "32MB + 64MB L4 victim": "mmpurple,thick,dotted"}
labels = {"32MB baseline": "32\\,MB L3 (baseline)", "96MB stacked 51c": "96\\,MB stacked, 51 cycles",
          "96MB planar 59c": "96\\,MB planar, 59 cycles (assumed)", "32MB + 64MB L4 inclusive": "32\\,MB L3 + 64\\,MB side die, inclusive",
          "32MB + 64MB L4 victim": "32\\,MB L3 + 64\\,MB side die, victim"}
plots = ""
for d in styles:
    pts = [(float(r["ws_mb"]), float(r["exposed_ns_mean"])) for r in s2 if r["design"] == d]
    plots += f"\\addplot[{styles[d]}] coordinates {{{coords(pts)}}};\n\\addlegendentry{{{labels[d]}}}\n"
save("sim-designs", rf"""\begin{{figure}}[htbp]
\centering
\begin{{tikzpicture}}
\begin{{axis}}[
  width=0.9\textwidth, height=6.4cm,
  xmode=log, log basis x=2, xmin=8, xmax=192, ymin=0,
  xtick={{8,16,32,64,96,192}}, xticklabels={{8,16,32,64,96,192}},
  xlabel={{Working set (MB, log scale)}}, ylabel={{Exposed latency per access (ns)}},
  legend pos=north west, legend style={{font=\scriptsize}}, legend cell align=left,
  grid=major, grid style={{draftgray!20}}]
{plots}\end{{axis}}
\end{{tikzpicture}}
\caption{{S2: ways to provide about 96\,MB of last-level cache, compared on the same random-access workload (one thread at 4\,GHz; average latency after the overlap factor of 0.335; mean of five seeds). The planar latency of 59 cycles is an assumption that \cref{{tab:sim-planar}} varies. The side die is a 64\,MB L4 at 22\,ns, either filled on every miss (inclusive) or filled by L3 evictions (victim); \cref{{tab:sim-side-die}} varies its latency.}}
\label{{fig:sim-designs}}
\end{{figure}}
""")

# ---- S3: cache against clock -----------------------------------------------------------------
s3 = rows("s3_cache_vs_clock")
gstyle = {"0": "draftblue,very thick", "4": "mmteal,thick", "7.3": "mmamber,thick,dashed", "10": "mmred,thick,dash dot"}
plots = ""
for g, st in gstyle.items():
    pts = sorted((float(r["misses_removed_per_kinstr"]), float(r["speedup_stacked_over_plain"]))
                 for r in s3 if r["clock_gap_pct"] == g and float(r["ws_mb"]) <= 96)   # within the stacked capacity
    plots += f"\\addplot[{st},mark=*,mark size=1.2pt] coordinates {{{coords(pts)}}};\n\\addlegendentry{{clock gap {g}\\%}}\n"
save("sim-cache-clock", rf"""\begin{{figure}}[htbp]
\centering
\begin{{tikzpicture}}
\begin{{axis}}[
  width=0.9\textwidth, height=6.6cm,
  xmin=0, xmax=1.8, ymin=0.88, ymax=1.34,
  xlabel={{Misses removed by the larger L3 (per 1000 instructions)}}, ylabel={{Speed-up, stacked over plain}},
  legend pos=north west, legend style={{font=\scriptsize}}, legend cell align=left,
  grid=major, grid style={{draftgray!20}}]
\addplot[draftgray,thin,forget plot] coordinates {{(0,1) (1.8,1)}};
{plots}\end{{axis}}
\end{{tikzpicture}}
\caption{{S3: the V-Cache CCD (96\,MB, 51 cycles) at a lower clock against the plain CCD (32\,MB, 47 cycles) at 5.15\,GHz, as the working set grows and the larger cache removes more misses. The access mix is calibrated to Lam's libx264 run (about 3.8 L3 accesses per 1000 instructions, of which about 1.04 per 1000 instructions miss even in the larger cache); the overlap factor is 0.335. A 7.3\% gap is the 4.8 against 5.15\,GHz Lam measured on the 7950X3D. Each curve crosses 1 at the break-even of that clock gap; \cref{{tab:sim-breakeven}} compares the crossings with the analytical model of \cref{{sec:cache-clock-model}}.}}
\label{{fig:sim-cache-clock}}
\end{{figure}}
""")

# ---- S4: ping-pong calibration -------------------------------------------------------------
s4 = rows("s4_pingpong")
pts = [(float(r["hop_ns"]), float(r["ratio"])) for r in s4]
save("sim-pingpong", rf"""\begin{{figure}}[htbp]
\centering
\begin{{tikzpicture}}
\begin{{axis}}[
  width=0.82\textwidth, height=6.0cm,
  xmin=0, xmax=250, ymin=0, ymax=22,
  xlabel={{Cost of one die-to-die hop in the model (ns)}}, ylabel={{Round trip, other CCD $\div$ same CCD}},
  legend columns=2, legend style={{font=\scriptsize,at={{(0.5,-0.34)}},anchor=north}}, legend cell align=left,
  grid=major, grid style={{draftgray!20}}]
\addplot[draftblue,very thick,mark=*,mark size=1.3pt] coordinates {{{coords(pts)}}};
\addlegendentry{{Model (ping-pong on one cache line)}}
\addplot[mmred,thick,dashed] coordinates {{(0,4.52) (250,4.52)}};
\addlegendentry{{Measured on Milan-X: 265 $\div$ 58.6\,ns (Reguly)}}
\addplot[draftgray,thick,dotted] coordinates {{(9,0) (9,11)}};
\addlegendentry{{AMD's CCD--IOD round trip, 9\,ns}}
\addplot[draftgray,thick,dashdotted] coordinates {{(18,0) (18,11)}};
\addlegendentry{{Two such round trips, 18\,ns}}
\end{{axis}}
\end{{tikzpicture}}
\caption{{S4: the model's ratio of cross-CCD to same-CCD ping-pong time as the cost of a hop grows (planar Zen~3 CCDs at 4\,GHz). Only the ratio is compared with Reguly's measurement \cite{{regulyComparativeEvaluationBandwidthbound2023}}, because Reguly's test times one message while the model's round trip contains two messages and two write upgrades. One transfer between two different CCDs, a request and its reply, crosses the CCD--IOD link four times, two of AMD's 9\,ns round trips. With a 9\,ns hop the model gives 2.2$\times$ and with 18\,ns 2.9$\times$; matching the measured 4.5$\times$ needs a hop of about 37\,ns. That value is fitted to the ratio only: the model's exchanges are about 2.4 times faster than the measured ones, so 37\,ns is not the real cost of a transfer, which \cref{{sec:cross-ccd}} puts at about 206\,ns.}}
\label{{fig:sim-pingpong}}
\end{{figure}}
""")

# ---- S5: Zen 2 -> Zen 3 --------------------------------------------------------------------
s5 = rows("s5_zen2_zen3")
dst = {"2x16MB, 39c": ("draftgray,thick", "2 $\\times$ 16\\,MB, 39 cycles (Zen~2)"),
       "2x16MB, 47c": ("mmamber,thick,dashed", "2 $\\times$ 16\\,MB, 47 cycles"),
       "1x32MB, 47c": ("draftblue,very thick", "1 $\\times$ 32\\,MB, 47 cycles (Zen~3)")}
def panel(th, title, name, at="", legend=True):
    p = ""
    for d, (st, lab) in dst.items():
        pts = [(float(r["ws_mb"]), float(r["exposed_ns_mean"])) for r in s5 if r["threads"] == th and r["design"] == d]
        p += (f"\\addplot[{st}] coordinates {{{coords(pts)}}};\n\\addlegendentry{{{lab}}}\n" if legend
              else f"\\addplot[{st},forget plot] coordinates {{{coords(pts)}}};\n")
    leg = (" legend columns=3, legend style={font=\\scriptsize,at={(1.12,-0.30)},anchor=north,column sep=6pt}, legend cell align=left,"
           if legend else "")
    return rf"""\begin{{axis}}[
  name={name}, {at} width=0.42\textwidth, height=5.8cm, xmin=4, xmax=40, ymin=0,
  xlabel={{Working set (MB)}}, ylabel={{Exposed latency per access (ns)}}, title={{\small {title}}},{leg}
  grid=major, grid style={{draftgray!20}}]
{p}\end{{axis}}
"""
save("sim-zen2-zen3", rf"""\begin{{figure}}[htbp]
\centering
\begin{{tikzpicture}}
{panel("1t", "(a) One thread", "one")}{panel("8t-shared", "(b) Eight threads, shared data", "eight", "at={(one.east)}, anchor=west, xshift=2.3cm,", legend=False)}\end{{tikzpicture}}
\caption{{S5: the Zen~2 to Zen~3 change of L3 organisation, separated from the latency change (random accesses; average latency after the overlap factor of 0.335; mean of five seeds). Comparing the dashed line with the thick one isolates the unification itself, since both have a 47-cycle L3; comparing the thin solid line with the dashed one isolates the latency change.}}
\label{{fig:sim-zen2-zen3}}
\end{{figure}}
""")

# ---- S6: streaming ---------------------------------------------------------------------------
s6 = rows("s6_streaming")
st6 = {("32MB", "8"): ("draftgray,thick", "32\\,MB L3, 8\\,MB per thread"), ("96MB", "8"): ("draftblue,very thick", "96\\,MB L3, 8\\,MB per thread"),
       ("32MB", "20"): ("draftgray,thick,dashed", "32\\,MB L3, 20\\,MB per thread"), ("96MB", "20"): ("draftblue,very thick,dashed", "96\\,MB L3, 20\\,MB per thread")}
plots = ""
for (l3, ws), (st, lab) in st6.items():
    pts = [(float(r["threads"]), float(r["throughput_gaccess_s"])) for r in s6 if r["l3"] == l3 and r["ws_mb_per_thread"] == ws]
    plots += f"\\addplot[{st},mark=*,mark size=1.2pt] coordinates {{{coords(pts)}}};\n\\addlegendentry{{{lab}}}\n"
save("sim-streaming", rf"""\begin{{figure}}[htbp]
\centering
\begin{{tikzpicture}}
\begin{{axis}}[
  width=0.82\textwidth, height=6.2cm, xmin=1, xmax=8, ymin=0, ymax=2.3,
  xlabel={{Threads, each streaming through its own data}}, ylabel={{Lines delivered (10$^9$ per second)}},
  legend pos=north west, legend style={{font=\scriptsize}}, legend cell align=left,
  grid=major, grid style={{draftgray!20}}]
\addplot[mmred,thin,dashed,forget plot] coordinates {{(1,0.8) (8,0.8)}};
\node[font=\scriptsize,mmred,anchor=south east] at (axis cs:8,0.8) {{DRAM limit: 51.2\,GB/s $\div$ 64\,B}};
{plots}\end{{axis}}
\end{{tikzpicture}}
\caption{{S6: up to eight cores streaming through private data (sequential reads; overlap 0.05, for a core whose prefetchers hide most latency; 51.2\,GB/s of DRAM bandwidth; mean of five seeds). While the combined data fits in the L3, throughput grows with the number of threads; once it does not, every configuration meets the same DRAM limit. With 8\,MB per thread, the 96\,MB L3 holds all eight threads' data and keeps scaling to 2.1 billion lines per second, while the 32\,MB L3 overflows at five threads and falls back to the DRAM limit.}}
\label{{fig:sim-streaming}}
\end{{figure}}
""")

# ====================== tables (also generated from the CSVs) ======================
def table(name, caption, label, spec, header, body, size="\\small"):
    caption = caption if caption.rstrip().endswith(".") else caption.rstrip() + "."
    save(name, "\\begin{table}[htbp]\n  \\centering\n  \\caption{" + caption + "}\n  \\label{" + label + "}\n  " + size +
         "\n  \\begin{tabular}{" + spec + "}\n    \\toprule\n    " + header + " \\\\\n    \\midrule\n" +
         "".join("    " + " & ".join(r) + " \\\\\n" for r in body) + "    \\bottomrule\n  \\end{tabular}\n\\end{table}\n")

cal = rows("s0_calibration")
table("sim-table-calibration",
      "S0: the overlap factor at which the model reproduces each of Lam's three workloads, solved so that the model's net saving per 1000 instructions, after the four extra L3 cycles are also overlapped, matches the measurement, and the gross cycles a removed miss then saves: the overlap factor times the 306.8 cycles by which a memory access at 4.2\\,GHz exceeds a stacked-L3 hit. A 64\\,MB random working set in the model reproduces these values within 1.5\\%. The per-miss values of \\cref{tab:lam-per-miss} charge the four extra cycles in full and are therefore larger",
      "tab:sim-calibration", "@{}l>{\\centering\\arraybackslash}p{3.0cm}>{\\centering\\arraybackslash}p{2.6cm}>{\\centering\\arraybackslash}p{3.4cm}@{}",
      "\\textbf{Workload (Lam)} & \\textbf{Net saving measured (cycles per 1000 instr.)} & \\textbf{Overlap factor that reproduces it} & \\textbf{Gross saving per removed miss (cycles)}",
      [[r["workload"], (f'{float(r["lam_net_saved_per_kinstr"]):.0f}' if float(r["lam_net_saved_per_kinstr"]) else "---"),
        f'{float(r["overlap"]):.3g}', f'{float(r["analytic_gross_per_removed_miss"]):.0f}'] for r in cal], size="\\footnotesize")

pl = rows("s2_planar_breakeven")
table("sim-table-planar",
      "S2: the longest L3 latency at which a planar 96\\,MB L3 still gives a shorter exposed latency than the 32\\,MB, 47-cycle baseline (random accesses; overlap 0.335; found by bisection on the five-seed mean). The stacked design needs 51 cycles",
      "tab:sim-planar", "@{}lcccccc@{}",
      "\\textbf{Working set (MB)} & " + " & ".join(r["ws_mb"] for r in pl),
      [["Break-even planar latency (cycles)"] + [f'{float(r["max_planar_l3_latency_cycles"]):.0f}' for r in pl]])

sd = rows("s2_side_die")
lats = []
for r in sd:
    if r["l4_lat_ns"] not in lats: lats.append(r["l4_lat_ns"])
v = {(r["ws_mb"], r["l4_lat_ns"], r["l4_organisation"]): float(r["side_exposed_ns"]) for r in sd}
st = {r["ws_mb"]: float(r["stacked_exposed_ns"]) for r in sd}
table("sim-table-side-die",
      "S2: exposed latency per access (ns) of a 64\\,MB side die beside a 32\\,MB L3, by its own latency and organisation, against the stacked 96\\,MB L3 (random accesses, one thread at 4\\,GHz, overlap 0.335). An inclusive side die is filled on every miss and holds copies of L3 data; a victim side die is filled by L3 evictions. In the model the side die is looked up after an L3 miss",
      "tab:sim-side-die", "@{}lcccc@{}",
      "& \\multicolumn{2}{c}{\\textbf{48\\,MB working set}} & \\multicolumn{2}{c}{\\textbf{80\\,MB working set}} \\\\ \\cmidrule(lr){2-3}\\cmidrule(l){4-5}\n    \\textbf{Side-die latency} & \\textbf{Inclusive} & \\textbf{Victim} & \\textbf{Inclusive} & \\textbf{Victim}",
      [[f"{l}\\,ns"] + [f'{v[(w, l, o)]:.2f}' for w in ("48", "80") for o in ("inclusive", "victim")] for l in lats]
      + [["Stacked 96\\,MB L3", f'{st["48"]:.2f}', f'{st["48"]:.2f}', f'{st["80"]:.2f}', f'{st["80"]:.2f}']])

be = {r["clock_gap_pct"]: r["breakeven_misses_removed_per_kinstr"] for r in rows("s3_breakeven")}
# Analytical model of sec:cache-clock-model (eq:cache-clock-model): C = 543 cycles, A = 3.85 L3 accesses
# per 1000 instructions, 4 extra cycles, s = 130 / 4.2 ns per removed miss, plain CCD at 5.15 GHz.
def analytic_be(g, C=543, A=3.85, s=130 / 4.2, fp=5.15):
    fv = fp / (1 + g / 100)
    return ((C + 4 * A) / fv - C / fp) / s
analytic = {g: f"{analytic_be(float(g)):.2f}" for g in be}
table("sim-table-breakeven",
      "S3: misses the larger L3 must remove per 1000 instructions for the V-Cache CCD to break even, read from \\cref{fig:sim-cache-clock} by linear interpolation, against the analytical model of \\cref{sec:cache-clock-model} at the same clocks (plain CCD at 5.15\\,GHz; the analytical equal-clock value is 0.12 at 4.2\\,GHz)",
      "tab:sim-breakeven", "@{}lcccccc@{}",
      "\\textbf{Clock gap} & " + " & ".join(f"{g}\\%" for g in be),
      [["Simulation (overlap 0.335)"] + [f"{float(x):.2f}" for x in be.values()],
       ["Analytical model, \\cref{eq:cache-clock-model}"] + [analytic.get(g, "---") for g in be]])

ss = rows("s3_sensitivity")
table("sim-table-s3-sensitivity",
      "Sensitivity of S3: the break-even (misses removed per 1000 instructions) when one input is changed. The overlap factors 0.202 and 0.105 are those that reproduce Lam's Cyberpunk~2077 and GHPC measurements (\\cref{tab:sim-calibration})",
      "tab:sim-s3-sensitivity", "@{}lcc@{}",
      "\\textbf{Changed input} & \\textbf{Equal clocks} & \\textbf{7.3\\% clock gap}",
      [[r["case"], (f'{float(r["breakeven_equal_clock"]):.2f}' if r["breakeven_equal_clock"] else "beyond range"),
        (f'{float(r["breakeven_gap_7.3"]):.2f}' if r["breakeven_gap_7.3"] else "beyond range")] for r in ss])

sp = rows("s4_split")
table("sim-table-split",
      "S4: sixteen cores on two CCDs (2 $\\times$ 32\\,MB L3; the hop is charged on every transfer between CCDs and on every memory access) against a hypothetical single die with one 64\\,MB L3 at the same 47 cycles, for four hop costs (overlap 0.335; mean of five seeds). The shared data set is 48\\,MB, with 5\\% of accesses writes; the private data sets are 8\\,MB per thread, 128\\,MB in all, and overflow both organisations",
      "tab:sim-split", "@{}>{\\raggedright\\arraybackslash}p{1.4cm}c>{\\centering\\arraybackslash}p{2.3cm}>{\\centering\\arraybackslash}p{2.4cm}>{\\centering\\arraybackslash}p{2.1cm}>{\\centering\\arraybackslash}p{1.6cm}@{}",
      "\\textbf{Data} & \\textbf{Hop (ns)} & \\textbf{Transfers between CCDs per 1000 accesses} & \\textbf{Memory accesses per 1000 (two dies / one die)} & \\textbf{Exposed latency, two dies (ns)} & \\textbf{Two dies $\\div$ one die}",
      [[r["data"], r["hop_ns"], f'{float(r["two_cross_per_kacc_mean"]):.0f}',
        f'{float(r["two_dram_per_kacc_mean"]):.0f} / {float(r["mono_dram_per_kacc_mean"]):.0f}', f'{float(r["two_exposed_ns_mean"]):.2f}', f'{float(r["ratio_two_over_mono"]):.2f}$\\times$'] for r in sp], size="\\footnotesize")

se = rows("sensitivity")
cases = []
for r in se:
    if r["case"] not in cases: cases.append(r["case"])
val = {(r["case"], r["ws_mb"]): float(r["mem_speedup_96_over_32"]) for r in se}
def cname(c):
    c = c.replace("LRU -> ", "replacement: ").replace("calibrated", "none (calibrated defaults)")
    return c.replace("overlap 0.105", "overlap 0.105 (GHPC)").replace("overlap 0.202", "overlap 0.202 (Cyberpunk)")
table("sim-table-sensitivity",
      "Sensitivity of S1: the memory-system speed-up of 96 over 32\\,MB (as in \\cref{fig:sim-working-set}b, random accesses) when one assumed input is changed at a time. A 16\\,MB working set fits in both caches, 64\\,MB lies between them and 192\\,MB exceeds both",
      "tab:sim-sensitivity", "@{}lccc@{}",
      "\\textbf{Changed input} & \\textbf{16\\,MB} & \\textbf{64\\,MB} & \\textbf{192\\,MB}",
      [[cname(c)] + [f"{val[(c, w)]:.2f}" for w in ("16", "64", "192")] for c in cases])


po = rows("s1_policy")
pv = {(r["kind"], r["policy"], r["ws_mb"]): float(r["mem_speedup_96_over_32"]) for r in po}
kn = {"random": "random", "hotcold": "hot/cold", "sequential": "sequential (cyclic)"}
pn = {"lru": "LRU", "random": "random", "plru": "tree pseudo-LRU"}
table("sim-table-policy",
      "Replacement policy: the memory-system speed-up of 96 over 32\\,MB for three workloads under three policies (overlap 0.335; mean of five seeds). With random accesses every resident line is equally likely to be used next, so no policy can change the result; the policy matters for workloads with reuse or a cyclic order",
      "tab:sim-policy", "@{}llccc@{}",
      "\\textbf{Workload} & \\textbf{Policy} & \\textbf{16\\,MB} & \\textbf{64\\,MB} & \\textbf{192\\,MB}",
      [[kn[k] if p == "lru" else "", pn[p]] + [f"{pv[(k, p, w)]:.2f}" for w in ("16", "64", "192")]
       for k in ("random", "hotcold", "sequential") for p in ("lru", "random", "plru")])