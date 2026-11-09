#!/usr/bin/env python3
"""Builds the self-contained GUI pages from template.html and sim-core.js.

    python3 gui/build.py            # writes gui/index.html (Chart.js from a CDN)
                                    # and gui/index-offline.html (Chart.js inlined, works without internet)

Needs Node.js to compute the example results shown when the page opens, and, for the offline page,
gui/vendor/chart.umd.js (Chart.js 4.4.1, from `npm pack chart.js@4.4.1`).
"""
import json, pathlib, subprocess, sys

here = pathlib.Path(__file__).resolve().parent
core = (here / "sim-core.js").read_text()
tpl = (here / "template.html").read_text()

example_js = r"""
const S = require(process.argv[1]);
const A = Object.assign({}, S.DEFAULTS, S.PRESETS.zen2_2ccx.cfg), B = Object.assign({}, S.DEFAULTS, S.PRESETS.zen3_1ccx.cfg);
const wl = { kind: "random", ws_mb: 24, threads: 1, shared: 0, write_frac: 0, stride: 4096, n: 128, block: 0, degree: 8, pp_a: 0, pp_b: 4, iters: 2000, accesses: 400000 };
console.log(JSON.stringify({ A: S.run(A, wl), B: S.run(B, wl) }));
"""
example = subprocess.run(["node", "-e", example_js, str(here / "sim-core.js")], check=True, capture_output=True, text=True).stdout.strip()
page = tpl.replace("/*@@SIMCORE@@*/", core).replace("/*@@EXAMPLE@@*/", "const EXAMPLE = " + example + ";")

cdn = '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.js"></script>'
(here / "index.html").write_text(page.replace("<!--@@CHARTJS@@-->", cdn))
vendor = here / "vendor" / "chart.umd.js"
if vendor.exists():
    inline = "<script>" + vendor.read_text().replace("</script", "<\\/script") + "</script>"
    full = "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
    body = page.replace("<!--@@CHARTJS@@-->", inline)
    (here / "index-offline.html").write_text(full + body.replace("<div class=\"wrap\">", "</head>\n<body>\n<div class=\"wrap\">", 1) + "\n</body>\n</html>\n")
    print("wrote index.html and index-offline.html")
else:
    print("wrote index.html (no vendor/chart.umd.js, so no offline page)")

# experiments.json: the ready-made experiments, read from template.html so the command-line
# runner (run_experiments.py) and the GUI always use the same definitions
dump = r"""
const fs = require("fs");
const html = fs.readFileSync(process.argv[1], "utf8");
const src = html.slice(html.indexOf("const EXPERIMENTS = ["), html.indexOf("function buildExperiments"));
const base = html.slice(html.indexOf("const WL_BASE"), html.indexOf("function exSeries"));
console.log(JSON.stringify({ wl_base: eval(base + "; WL_BASE"), experiments: eval(src + "; EXPERIMENTS") }, null, 1));
"""
out = subprocess.run(["node", "-e", dump, str(here / "template.html")], check=True, capture_output=True, text=True).stdout
(here.parent / "experiments.json").write_text(out)
print("wrote experiments.json")
