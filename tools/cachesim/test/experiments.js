// Runs every ready-made experiment from gui/template.html in Node and prints the results,
// so the "what to look for" text can be checked against what the model actually does.
"use strict";
const fs = require("fs"), path = require("path");
const SIM = require(path.join(__dirname, "..", "gui", "sim-core.js"));
const html = fs.readFileSync(path.join(__dirname, "..", "gui", "template.html"), "utf8");
const exSrc = html.slice(html.indexOf("const EXPERIMENTS = ["), html.indexOf("function buildExperiments"));
const baseSrc = html.slice(html.indexOf("const WL_BASE"), html.indexOf("function exSeries"));
const metSrc = html.slice(html.indexOf("const METRICS = {"), html.indexOf("const SWEEP_PARAMS"));
const P = SIM.PRESETS;
function presetCfg(name, extra) { return Object.assign({}, SIM.DEFAULTS, P[name].cfg, extra || {}); }
const EXPERIMENTS = eval(exSrc + "; EXPERIMENTS");
const WL_BASE = eval(baseSrc + "; WL_BASE");
const METRICS = eval(metSrc + "; METRICS");
const acc = Number(process.argv[3] || 150000), only = process.argv[2] && process.argv[2] !== "all" ? process.argv[2].split(",") : null;
for (const ex of EXPERIMENTS) {
  if (only && !only.includes(ex.id)) continue;
  const t0 = Date.now();
  const series = ex.series.map(s => { const wl = Object.assign({}, WL_BASE, ex.wl, s.wl || {}); wl.accesses = ex.perThread ? acc : Math.max(20000, Math.round(acc / Math.max(1, wl.threads))); return { name: s.name, cfg: presetCfg(s.preset, s.extra), sweep: s.sweep, wl }; });
  const res = series.map(s => ex.values.map(v => { const cfg = Object.assign({}, s.cfg), wl = Object.assign({}, s.wl); if (s.sweep !== false) { const [w, k] = ex.param.split("."); (w === "cfg" ? cfg : wl)[k] = v; } return SIM.run(cfg, wl); }));
  console.log(`\n== ${ex.id}: ${ex.title}  (${((Date.now() - t0) / 1000).toFixed(1)} s)`);
  for (const mk of ex.metrics) {
    const m = METRICS[mk];
    console.log(`  ${m.label} (${m.unit})   x = ${ex.values.join(" | ")}`);
    series.forEach((s, j) => { let ys = res[j].map(r => m.f(r)); if (m.relative) ys = ys.map(y => y / (ys[0] || 1)); console.log(`    ${s.name.padEnd(36)} ${ys.map(y => y.toFixed(2)).join(" | ")}`); });
  }
}
