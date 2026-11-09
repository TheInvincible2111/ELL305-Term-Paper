// Runs the same configurations through the C++ binary and the JavaScript core and
// compares every numeric result. Usage: node test/crosscheck.js [path/to/cachesim] [--write-golden]
// --write-golden also saves the JavaScript results to test/crosscheck-golden.json, so that
// test/check_golden.py can compare the C++ binary with them on a machine without Node.js.
"use strict";
const { execFileSync } = require("child_process");
const path = require("path");
const SIM = require(path.join(__dirname, "..", "gui", "sim-core.js"));
const argv = process.argv.slice(2);
const writeGolden = argv.includes("--write-golden");
const bin = argv.filter(a => a !== "--write-golden")[0] || path.join(__dirname, "..", "cachesim");
const golden = [];

const cases = [
  ["zen3_1ccx", { kind: "random", ws_mb: 24, accesses: 200000 }],
  ["zen2_2ccx", { kind: "random", ws_mb: 24, accesses: 200000 }],
  ["vcache", { kind: "random", ws_mb: 64, accesses: 200000, write_frac: 0.2 }],
  ["sidecar", { kind: "random", ws_mb: 80, accesses: 200000, write_frac: 0.3 }],
  ["zen2_2ccx", { kind: "random", ws_mb: 12, accesses: 50000, threads: 8, shared: 1, write_frac: 0.1 }],
  ["twoccd", { kind: "hotcold", ws_mb: 96, accesses: 30000, threads: 16, shared: 1, write_frac: 0.05 }],
  ["zen3_1ccx", { kind: "sequential", ws_mb: 40, accesses: 200000 }, { policy: "random" }],
  ["zen3_1ccx", { kind: "stride", ws_mb: 8, stride: 4096, accesses: 100000 }, { policy: "plru", l1_ways: 4 }],
  ["zen3_1ccx", { kind: "matmul", n: 96, block: 16, threads: 8 }],
  ["zen2_2ccx", { kind: "graph", ws_mb: 16, accesses: 100000, threads: 8 }, { link_gbs: 55 }],
  ["zen2_2ccx", { kind: "pingpong", pp_a: 0, pp_b: 4, iters: 500 }],
  ["zen3_1ccx", { kind: "random", ws_mb: 48, accesses: 100000 }, { policy: "fifo", overlap: 0.4, clock_ghz: 4.8 }],
  ["twoccd", { kind: "random", ws_mb: 8, accesses: 30000, threads: 16, shared: 0 }, { dram_hop: 1, hop_ns: 37 }],
  ["sidecar", { kind: "random", ws_mb: 80, accesses: 150000, write_frac: 0.2 }, { l4_victim: 1, l4_lat_ns: 8 }],
  ["vcache", { kind: "hotcold", ws_mb: 40, hot_frac: 0.0004, hot_prob: 0.98845, far_mb: 512, far_prob: 0.004, accesses: 150000 },
   { l1_lat: 1, work_cycles: 0.31, overlap: 0.335 }],
];

let fails = 0;
for (const [preset, wl, extra] of cases) {
  const cfg = Object.assign({}, SIM.PRESETS[preset].cfg, extra || {});
  const args = ["--preset", preset];
  for (const [k, v] of Object.entries(extra || {})) args.push("--set", `${k}=${v}`);
  for (const [k, v] of Object.entries(wl)) args.push("--set", `${k}=${v}`);
  const cpp = JSON.parse(execFileSync(bin, args, { encoding: "utf8" }));
  const js = SIM.run(cfg, wl);
  golden.push({ args, js });
  const bad = [];
  for (const [k, v] of Object.entries(cpp)) {
    if (typeof v !== "number") { if (js[k] !== v) bad.push(`${k}: ${v} vs ${js[k]}`); continue; }
    const w = js[k];
    if (typeof w !== "number") { bad.push(`${k}: missing in JS`); continue; }
    if (Math.abs(v - w) > 1e-9 * Math.max(1, Math.abs(v))) bad.push(`${k}: C++ ${v} vs JS ${w}`);
  }
  const label = `${preset} ${wl.kind} ${JSON.stringify(extra || {})}`;
  if (bad.length) { fails++; console.log("FAIL", label, bad.slice(0, 5).join("; ")); }
  else console.log("PASS", label, `l3_hit_rate=${cpp.l3_hit_rate.toFixed(4)} amat_ns=${cpp.amat_ns.toFixed(2)}`);
}
console.log(fails ? `${fails} case(s) differ` : "C++ and JavaScript results identical");
if (writeGolden && !fails) {
  const crypto = require("crypto"), fs = require("fs");
  const coreFile = path.join(__dirname, "..", "gui", "sim-core.js");
  const sha = crypto.createHash("sha256").update(fs.readFileSync(coreFile)).digest("hex");
  const out = { written: new Date().toISOString(), node: process.version, sim_core_sha256: sha, cases: golden };
  fs.writeFileSync(path.join(__dirname, "crosscheck-golden.json"), JSON.stringify(out, null, 1) + "\n");
  console.log("wrote test/crosscheck-golden.json");
}
process.exit(fails ? 1 : 0);
