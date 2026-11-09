#!/usr/bin/env python3
"""Checks the C++ simulator against the JavaScript results stored in crosscheck-golden.json,
for machines without Node.js.

    python3 test/check_golden.py ./cachesim

The golden file is written by `node test/crosscheck.js ./cachesim --write-golden` only when the
C++ and JavaScript results agree. It records the SHA-256 of gui/sim-core.js; if that file has
changed since, this script says so, because the stored JavaScript results may then be stale.
"""
import hashlib, json, pathlib, subprocess, sys
here = pathlib.Path(__file__).resolve().parent
binary = sys.argv[1] if len(sys.argv) > 1 else str(here.parent / "cachesim")
gold = json.loads((here / "crosscheck-golden.json").read_text())
sha = hashlib.sha256((here.parent / "gui" / "sim-core.js").read_bytes()).hexdigest()
if sha != gold["sim_core_sha256"]:
    print("WARNING: gui/sim-core.js has changed since the golden file was written; rerun crosscheck.js with Node.js.")
fails = 0
for case in gold["cases"]:
    cpp = json.loads(subprocess.run([binary] + case["args"], check=True, capture_output=True, text=True).stdout)
    js, bad = case["js"], []
    for k, v in cpp.items():
        w = js.get(k)
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            if not isinstance(w, (int, float)): bad.append(f"{k}: missing in JS")
            elif abs(v - w) > 1e-9 * max(1, abs(v)): bad.append(f"{k}: C++ {v} vs JS {w}")
        elif v != w: bad.append(f"{k}: {v} vs {w}")
    label = " ".join(case["args"])
    if bad: fails += 1; print("FAIL", label, "; ".join(bad[:5]))
    else: print("PASS", label)
print(f"{fails} case(s) differ" if fails else
      f"C++ results identical to the stored JavaScript results ({len(gold['cases'])} cases; JS run {gold['written'][:10]}, Node {gold['node']})")
sys.exit(1 if fails else 0)
