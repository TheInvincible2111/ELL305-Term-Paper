// ELL305 cache-hierarchy simulator: JavaScript core.
// This file is a line-for-line port of src/cachesim.cpp. Both use the same random
// number generator, the same cache model and the same workloads, so for the same
// configuration they produce identical counts (checked by test/crosscheck.js).
//
// Model in one paragraph: a trace-driven, functional simulator. Each core has a
// private L1D and an inclusive private L2. Cores are split into L3 groups (a CCX or a
// CCD); each group shares one L3. An optional L4 is shared by all groups (a
// side-by-side cache die). A directory tracks which cores hold each line in their
// L2, so writes invalidate other copies and reads of a line another core has
// modified are served core-to-core. Latency is charged per access from the level
// that served it; time, bandwidth and energy are estimated afterwards.

"use strict";

var SIM = (function () {

  // ---------- deterministic random numbers (mulberry32, 32-bit) ----------
  function Rng(seed) { this.a = seed >>> 0; }
  Rng.prototype.next = function () {
    this.a = (this.a + 0x6D2B79F5) >>> 0;
    var t = this.a;
    t = Math.imul(t ^ (t >>> 15), t | 1) >>> 0;
    t = (t ^ (t + Math.imul(t ^ (t >>> 7), t | 61))) >>> 0;
    return (t ^ (t >>> 14)) >>> 0;
  };
  function mix32(x) { // murmur3 finalizer, used as a fixed hash
    x = x >>> 0;
    x = Math.imul(x ^ (x >>> 16), 0x85EBCA6B) >>> 0;
    x = Math.imul(x ^ (x >>> 13), 0xC2B2AE35) >>> 0;
    return (x ^ (x >>> 16)) >>> 0;
  }

  // ---------- default configuration ----------
  var DEFAULTS = {
    cores: 8, groups: 1, clock_ghz: 4.0, line: 64,
    l1_kb: 32, l1_ways: 8, l1_lat: 4,
    l2_kb: 512, l2_ways: 8, l2_lat: 12,
    l3_mb: 32, l3_ways: 16, l3_lat: 47,
    l4_mb: 0, l4_ways: 16, l4_lat_ns: 22,
    mem_ns: 74, hop_ns: 9, dram_hop: 0, l4_victim: 0,
    policy: "lru", seed: 1,
    overlap: 1.0, work_cycles: 1,
    l3_bw_bpc: 32, mem_bw_gbs: 51.2, link_gbs: 0,
    e_l1_pj: 5, e_l2_pj: 20, e_l3_pj: 100, e_l4_pj: 300, e_dram_pj: 2000, e_link_pj_bit: 2
  };

  // ---------- one set-associative cache ----------
  var POLICIES = { lru: 0, fifo: 1, random: 2, plru: 3 };

  function Cache(sizeBytes, ways, line, policy, seed) {
    var nlines = Math.max(1, Math.floor(sizeBytes / line));
    ways = Math.max(1, Math.min(ways, nlines));
    this.ways = ways;
    this.sets = Math.max(1, Math.floor(nlines / ways));
    var n = this.sets * ways;
    this.tag = new Float64Array(n).fill(-1);
    this.dirty = new Uint8Array(n);
    this.stamp = new Float64Array(n);
    this.clock = 0;
    var pol = POLICIES[policy] === undefined ? 0 : POLICIES[policy];
    if (pol === 3 && (ways & (ways - 1)) !== 0) pol = 0; // tree PLRU needs a power-of-two way count
    this.pol = pol;
    this.plru = pol === 3 ? new Uint8Array(this.sets * Math.max(1, ways - 1)) : null;
    this.rng = new Rng(seed);
  }
  Cache.prototype.lookup = function (ln) {
    var base = (ln % this.sets) * this.ways;
    for (var w = 0; w < this.ways; w++) if (this.tag[base + w] === ln) return base + w;
    return -1;
  };
  Cache.prototype.plruTouch = function (set, way) {
    var lo = 0, hi = this.ways, node = 0, b = set * (this.ways - 1);
    while (hi - lo > 1) {
      var mid = (lo + hi) >> 1;
      if (way < mid) { this.plru[b + node] = 1; node = 2 * node + 1; hi = mid; }
      else { this.plru[b + node] = 0; node = 2 * node + 2; lo = mid; }
    }
  };
  Cache.prototype.touch = function (idx) {
    if (this.pol === 0) this.stamp[idx] = ++this.clock;
    else if (this.pol === 3) this.plruTouch(Math.floor(idx / this.ways), idx % this.ways);
  };
  // insert a line; returns evicted line (or -1) and sets this.evDirty
  Cache.prototype.insert = function (ln, dirty) {
    var set = ln % this.sets, base = set * this.ways, v = -1, w;
    for (w = 0; w < this.ways; w++) if (this.tag[base + w] === -1) { v = w; break; }
    if (v < 0) {
      if (this.pol === 2) v = this.rng.next() % this.ways;
      else if (this.pol === 3) {
        var lo = 0, hi = this.ways, node = 0, b = set * (this.ways - 1);
        while (hi - lo > 1) {
          var mid = (lo + hi) >> 1;
          if (this.plru[b + node] === 0) { node = 2 * node + 1; hi = mid; } else { node = 2 * node + 2; lo = mid; }
        }
        v = lo;
      } else {
        var best = Infinity;
        for (w = 0; w < this.ways; w++) if (this.stamp[base + w] < best) { best = this.stamp[base + w]; v = w; }
      }
    }
    var idx = base + v, ev = this.tag[idx];
    this.evDirty = ev !== -1 && this.dirty[idx] === 1;
    this.tag[idx] = ln; this.dirty[idx] = dirty ? 1 : 0;
    this.stamp[idx] = ++this.clock;
    if (this.pol === 3) this.plruTouch(set, v);
    this.lastIdx = idx;
    return ev;
  };
  Cache.prototype.invalidate = function (ln) { // returns -1 if absent, else 0/1 = was dirty
    var i = this.lookup(ln);
    if (i < 0) return -1;
    var d = this.dirty[i];
    this.tag[i] = -1; this.dirty[i] = 0; this.stamp[i] = 0;
    return d;
  };

  // ---------- the hierarchy ----------
  function Sim(cfgIn, coherence) {
    var c = {}, k;
    for (k in DEFAULTS) c[k] = DEFAULTS[k];
    for (k in cfgIn) if (cfgIn[k] !== undefined) c[k] = cfgIn[k];
    c.cores = Math.max(1, Math.min(16, Math.round(c.cores)));
    c.groups = Math.max(1, Math.min(c.cores, Math.round(c.groups)));
    this.c = c;
    var f = c.clock_ghz;
    this.hopC = c.hop_ns * f; this.memC = c.mem_ns * f; this.l4C = c.l4_lat_ns * f;
    this.l1 = []; this.l2 = []; this.l3 = []; this.grp = [];
    for (var i = 0; i < c.cores; i++) {
      this.l1.push(new Cache(c.l1_kb * 1024, c.l1_ways, c.line, c.policy, (c.seed * 977 + i * 31 + 1) >>> 0));
      this.l2.push(new Cache(c.l2_kb * 1024, c.l2_ways, c.line, c.policy, (c.seed * 977 + i * 31 + 2) >>> 0));
      this.grp.push(Math.floor(i * c.groups / c.cores));
    }
    for (var g = 0; g < c.groups; g++)
      this.l3.push(new Cache(c.l3_mb * 1048576, c.l3_ways, c.line, c.policy, (c.seed * 977 + 500 + g) >>> 0));
    this.l4 = c.l4_mb > 0 ? new Cache(c.l4_mb * 1048576, c.l4_ways, c.line, c.policy, (c.seed * 977 + 900) >>> 0) : null;
    this.dir = (c.cores > 1 && coherence !== false) ? new Map() : null;
    this.coresInGroup = new Array(c.groups).fill(0);
    for (i = 0; i < c.cores; i++) this.coresInGroup[this.grp[i]]++;
    this.reset();
  }
  Sim.prototype.reset = function () {
    var c = this.c;
    this.s = {
      accesses: 0, reads: 0, writes: 0, instructions: 0,
      l1_hit: 0, l2_hit: 0, l3_hit: 0, l3_remote: 0, c2c_local: 0, c2c_remote: 0,
      l4_hit: 0, dram_reads: 0, dram_writes: 0, inv_local: 0, inv_remote: 0,
      lat_cycles: 0, exp_cycles: 0
    };
    this.coreCycles = new Float64Array(c.cores);
    this.coreAcc = new Float64Array(c.cores);
    this.activeCore = new Uint8Array(c.cores);
    this.l3Bytes = new Float64Array(c.groups);
    this.linkBytes = new Float64Array(c.groups);
    this.dramBytesG = new Float64Array(c.groups);
  };
  Sim.prototype.dirAdd = function (ln, core) {
    if (!this.dir) return;
    this.dir.set(ln, (this.dir.get(ln) || 0) | (1 << core));
  };
  Sim.prototype.dirRemove = function (ln, core) {
    if (!this.dir) return;
    var m = (this.dir.get(ln) || 0) & ~(1 << core);
    if (m) this.dir.set(ln, m); else this.dir.delete(ln);
  };
  Sim.prototype.l3Insert = function (g, ln, dirty) {
    var L3 = this.l3[g];
    var i = L3.lookup(ln);
    if (i >= 0) { if (dirty) L3.dirty[i] = 1; return; }
    var ev = L3.insert(ln, dirty);
    if (ev !== -1 && this.l4 && this.c.l4_victim > 0) { this.l4Insert(ev, L3.evDirty); return; }  // victim L4 takes every L3 eviction
    if (ev !== -1 && L3.evDirty) {
      if (this.l4) this.l4Insert(ev, true);
      else { this.s.dram_writes++; this.dramBytesG[g] += this.c.line; if (this.c.link_gbs > 0) this.linkBytes[g] += this.c.line; }
    }
  };
  Sim.prototype.l4Insert = function (ln, dirty) {
    var i = this.l4.lookup(ln);
    if (i >= 0) { if (dirty) this.l4.dirty[i] = 1; return; }
    var ev = this.l4.insert(ln, dirty);
    if (ev !== -1 && this.l4.evDirty) { this.s.dram_writes++; this.dramBytesG[0] += this.c.line; }
  };
  Sim.prototype.l2Fill = function (core, ln, dirty) {
    var L2 = this.l2[core];
    var ev = L2.insert(ln, dirty);
    var idx = L2.lastIdx;
    if (ev !== -1) {
      var evd = L2.evDirty;
      this.l1[core].invalidate(ev);          // L1 is inclusive in L2
      this.dirRemove(ev, core);
      if (evd) this.l3Insert(this.grp[core], ev, true);
    }
    this.dirAdd(ln, core);
    return idx;
  };
  // serve a private (L1+L2) miss; returns latency in cycles
  Sim.prototype.fetch = function (core, g, ln, isWrite) {
    var c = this.c, s = this.s, L = c.line;
    if (this.dir) {
      var holders = (this.dir.get(ln) || 0) & ~(1 << core);
      if (holders) {
        var owner = -1, sameGroup = -1, otherGroup = -1, o;
        for (o = 0; o < c.cores; o++) {
          if (!(holders & (1 << o))) continue;
          var i2 = this.l2[o].lookup(ln);
          if (i2 >= 0 && this.l2[o].dirty[i2]) { owner = o; }
          if (this.grp[o] === g) { if (sameGroup < 0) sameGroup = o; } else if (otherGroup < 0) otherGroup = o;
        }
        if (owner >= 0) {
          var og = this.grp[owner];
          if (!isWrite) { // downgrade: owner keeps a clean copy, data written back to its L3
            var j = this.l2[owner].lookup(ln); this.l2[owner].dirty[j] = 0;
            this.l3Insert(og, ln, true);
          }
          if (og === g) { s.c2c_local++; this.l3Bytes[g] += L; return c.l3_lat; }
          s.c2c_remote++; this.linkBytes[g] += L; this.linkBytes[og] += L;
          if (!isWrite) this.l3Insert(g, ln, false);
          return c.l3_lat + this.hopC + c.l3_lat;
        }
        if (sameGroup >= 0) { s.c2c_local++; this.l3Bytes[g] += L; return c.l3_lat; }
        // only clean copies in other groups: fall through to the L3 checks below
      }
    }
    var L3 = this.l3[g];
    var i3 = L3.lookup(ln);
    if (i3 >= 0) { L3.touch(i3); s.l3_hit++; this.l3Bytes[g] += L; return c.l3_lat; }
    if (c.groups > 1) {
      for (var gg = 0; gg < c.groups; gg++) {
        if (gg === g) continue;
        var r = this.l3[gg].lookup(ln);
        if (r >= 0) {
          this.l3[gg].touch(r);
          s.l3_remote++; this.linkBytes[g] += L; this.linkBytes[gg] += L;
          this.l3Insert(g, ln, false);
          return c.l3_lat + this.hopC + c.l3_lat;
        }
      }
      if (this.dir) {
        var h2 = (this.dir.get(ln) || 0) & ~(1 << core);
        if (h2) { // clean copy in another group's private cache
          for (var q = 0; q < c.cores; q++) if (h2 & (1 << q)) { var qg = this.grp[q]; this.linkBytes[qg] += L; break; }
          s.c2c_remote++; this.linkBytes[g] += L;
          this.l3Insert(g, ln, false);
          return c.l3_lat + this.hopC + c.l3_lat;
        }
      }
    }
    if (this.l4) {
      var i4 = this.l4.lookup(ln);
      if (i4 >= 0) {
        s.l4_hit++;
        if (c.l4_victim > 0) { var d4 = this.l4.dirty[i4] !== 0; this.l4.invalidate(ln); this.l3Insert(g, ln, d4); }  // exclusive: move up
        else { this.l4.touch(i4); this.l3Insert(g, ln, false); }
        return c.l3_lat + this.l4C;
      }
    }
    s.dram_reads++; this.dramBytesG[g] += L; if (c.link_gbs > 0) this.linkBytes[g] += L;
    if (this.l4 && !(c.l4_victim > 0)) this.l4Insert(ln, false);
    this.l3Insert(g, ln, false);
    return c.l3_lat + this.memC + (c.dram_hop > 0 ? this.hopC : 0);  // dram_hop: every memory access crosses to the I/O die
  };
  // one access by one core; returns the latency charged (cycles)
  Sim.prototype.access = function (core, ln, isWrite) {
    var c = this.c, s = this.s, g = this.grp[core];
    var L1 = this.l1[core], L2 = this.l2[core];
    var lat, privHit = false, i2;
    var i1 = L1.lookup(ln);
    if (i1 >= 0) { L1.touch(i1); s.l1_hit++; lat = c.l1_lat; privHit = true; i2 = L2.lookup(ln); }
    else {
      i2 = L2.lookup(ln);
      if (i2 >= 0) { L2.touch(i2); s.l2_hit++; lat = c.l2_lat; privHit = true; L1.insert(ln, false); }
      else {
        lat = this.fetch(core, g, ln, isWrite);
        i2 = this.l2Fill(core, ln, false);
        L1.insert(ln, false);
      }
    }
    if (isWrite) {
      if (this.dir) {
        var others = (this.dir.get(ln) || 0) & ~(1 << core);
        if (others) {
          var remote = false;
          for (var o = 0; o < c.cores; o++) {
            if (!(others & (1 << o))) continue;
            this.l1[o].invalidate(ln);
            this.l2[o].invalidate(ln);
            if (this.grp[o] === g) s.inv_local++; else { s.inv_remote++; remote = true; }
          }
          this.dir.set(ln, 1 << core);
          if (privHit) lat += c.l3_lat;
          if (remote) lat += this.hopC;
        }
      }
      for (var gg = 0; gg < c.groups; gg++) if (gg !== g) this.l3[gg].invalidate(ln);
      L2.dirty[i2] = 1;
      s.writes++;
    } else s.reads++;
    s.accesses++;
    var exposed = lat <= c.l2_lat ? lat : c.l2_lat + c.overlap * (lat - c.l2_lat);
    this.coreCycles[core] += exposed + c.work_cycles;
    s.exp_cycles += exposed;
    this.coreAcc[core]++;
    this.activeCore[core] = 1;
    s.lat_cycles += lat;
    return lat;
  };

  // ---------- workloads ----------
  // Each workload returns an object with next(out) -> false when finished;
  // out = {core, line, write}. Addresses are byte addresses; lines = addr / line size.
  var PRIV = 68719476736; // 2^36 bytes between private regions

  function perCore(cfg, wl, makeGen) {
    var cores = Math.max(1, Math.min(cfg.cores, wl.threads || cfg.cores));
    var gens = [], i;
    for (i = 0; i < cores; i++) gens.push(makeGen(i, cores));
    var turn = 0, alive = cores, done = new Uint8Array(cores);
    return {
      next: function (out) {
        while (alive > 0) {
          var t = turn; turn = (turn + 1) % cores;
          if (done[t]) continue;
          if (gens[t](out)) { out.core = t; return true; }
          done[t] = 1; alive--;
        }
        return false;
      }
    };
  }

  function makeWorkload(cfg, wlIn, salt) {
    salt = salt || 0;
    var wl = {};
    var WLD = { kind: "random", ws_mb: 16, accesses: 1000000, warmup: -1, write_frac: 0, shared: 0, threads: 1,
      stride: 4096, hot_frac: 0.1, hot_prob: 0.9, far_mb: 0, far_prob: 0, n: 128, block: 0, degree: 8, pp_a: 0, pp_b: 1, iters: 2000 };
    for (var k in WLD) wl[k] = WLD[k];
    for (k in wlIn) if (wlIn[k] !== undefined) wl[k] = wlIn[k];
    var L = cfg.line;
    var kind = wl.kind;

    if (kind === "random" || kind === "sequential" || kind === "stride" || kind === "hotcold") {
      var wsBytes = Math.max(L, Math.round(wl.ws_mb * 1048576));
      var nl = Math.max(1, Math.floor(wsBytes / L));
      var wf = Math.round(wl.write_frac * 1000);
      var hp = Math.round(wl.hot_prob * 1000000), fp = Math.round(wl.far_prob * 1000000);  // resolution 1e-6
      var farN = Math.floor(Math.max(0, Math.round(wl.far_mb * 1048576)) / L);
      return perCore(cfg, wl, function (core, cores) {
        var rng = new Rng((cfg.seed * 7919 + core * 104729 + 17 + salt * 1000003) >>> 0);
        var base = wl.shared ? 0 : (core + 1) * PRIV / L;
        var pos = 0, left = wl.accesses, hotN = Math.max(1, Math.floor(nl * wl.hot_frac));
        var sl = Math.max(1, Math.round(wl.stride / L));
        return function (out) {
          if (left <= 0) return false;
          left--;
          var idx;
          if (kind === "random") idx = rng.next() % nl;
          else if (kind === "sequential") { idx = pos; pos = (pos + 1) % nl; }
          else if (kind === "stride") { idx = (pos * sl) % nl; pos++; }
          else {
            var r = rng.next() % 1000000;
            if (r < hp) idx = rng.next() % hotN;
            else if (farN > 0 && r < hp + fp) idx = nl + rng.next() % farN;  // far region beyond the working set
            else idx = rng.next() % nl;
          }
          out.line = base + idx;
          out.write = wf > 0 && (rng.next() % 1000) < wf;
          return true;
        };
      });
    }

    if (kind === "matmul") {
      var n = Math.max(2, Math.round(wl.n)), b = wl.block > 0 ? Math.min(n, Math.round(wl.block)) : n;
      var A = 0, B = n * n * 8, C = 2 * n * n * 8;
      return perCore(cfg, wl, function (core, cores) {
        var r0 = Math.floor(core * n / cores), r1 = Math.floor((core + 1) * n / cores);
        var ii = r0, jj = 0, kk = 0, i = r0, j = 0, kx = 0, phase = 0, sub = 0, done = r0 >= r1;
        return function (out) {
          if (done) return false;
          var addr, wr = false;
          if (phase === 0) { phase = 1; kx = kk; sub = 0; addr = C + (i * n + j) * 8; }
          else if (phase === 1) {
            if (sub === 0) { sub = 1; addr = A + (i * n + kx) * 8; }
            else { sub = 0; addr = B + (kx * n + j) * 8; kx++; if (kx >= Math.min(kk + b, n)) phase = 2; }
          } else {
            phase = 0; addr = C + (i * n + j) * 8; wr = true;
            j++;
            if (j >= Math.min(jj + b, n)) {
              j = jj; i++;
              if (i >= Math.min(ii + b, r1)) {
                i = ii; kk += b;
                if (kk >= n) {
                  kk = 0; jj += b;
                  if (jj >= n) { jj = 0; ii += b; if (ii >= r1) done = true; }
                  j = jj;
                }
                i = ii;
              }
            }
          }
          out.line = Math.floor(addr / L); out.write = wr;
          return true;
        };
      });
    }

    if (kind === "graph") {
      var V = Math.max(16, Math.floor(wl.ws_mb * 1048576 / 8)), d = Math.max(1, Math.round(wl.degree));
      var OFF = 0, EDGE = V * 8, PROP = V * 8 + V * d * 4;
      return perCore(cfg, wl, function (core, cores) {
        var v0 = Math.floor(core * V / cores), v1 = Math.floor((core + 1) * V / cores);
        var v = v0, e = 0, phase = 0, left = wl.accesses;
        return function (out) {
          if (left <= 0 || v0 >= v1) return false;
          left--;
          var addr, wr = false;
          if (phase === 0) { addr = OFF + v * 8; phase = 1; e = 0; }
          else if (phase === 1) { addr = EDGE + (v * d + e) * 4; phase = 2; }
          else if (phase === 2) {
            var nb = mix32((v * d + e) >>> 0) % V; addr = PROP + nb * 8; e++;
            phase = e < d ? 1 : 3;
          } else { addr = PROP + v * 8; wr = true; phase = 0; v++; if (v >= v1) v = v0; }
          out.line = Math.floor(addr / L); out.write = wr;
          return true;
        };
      });
    }

    if (kind === "pingpong") {
      var a = Math.min(cfg.cores - 1, Math.round(wl.pp_a)), bb = Math.min(cfg.cores - 1, Math.round(wl.pp_b));
      var X = 1000003, Y = 2000003, step = 0, it = 0;
      return {
        next: function (out) {
          if (it >= wl.iters) return false;
          if (step === 0) { out.core = a; out.line = X; out.write = true; }
          else if (step === 1) { out.core = bb; out.line = X; out.write = false; }
          else if (step === 2) { out.core = bb; out.line = Y; out.write = true; }
          else { out.core = a; out.line = Y; out.write = false; }
          step++; if (step === 4) { step = 0; it++; }
          return true;
        }, pingpong: true
      };
    }

    if (kind === "trace") {
      var tr = wl.trace || []; var p = 0;
      return { next: function (out) {
        if (p >= tr.length) return false;
        var e2 = tr[p++]; out.core = Math.min(cfg.cores - 1, e2[0]); out.line = e2[1]; out.write = !!e2[2]; return true; } };
    }
    throw new Error("unknown workload: " + kind);
  }

  // ---------- run one experiment ----------
  function run(cfgIn, wlIn, progress) {
    var wl = {}; for (var k in wlIn) wl[k] = wlIn[k];
    var multi = wl.kind === "pingpong" || wl.kind === "trace" || (wl.threads || 1) > 1;
    var sim = new Sim(cfgIn, multi), c = sim.c;
    var out = { core: 0, line: 0, write: false };
    // warm-up. Random and hot/cold: each thread first touches its working set in order, up to
    // the total cache capacity, then a separate random stream of half the cache capacity settles
    // the replacement state. Sequential and stride: the loop runs once over the working set
    // (or until the caches are full) and measurement continues from where it stopped. Graph traversal
    // warms up for three times the cache capacity in lines (at least as many accesses as it measures). Stats reset after warm-up.
    var threads = Math.max(1, Math.min(c.cores, wl.threads || 1));
    var totalLines = Math.floor((c.l3_mb * c.groups + c.l4_mb) * 1048576 / c.line);
    var nlw = Math.max(1, Math.floor(Math.max(c.line, Math.round((wl.ws_mb || 16) * 1048576)) / c.line));
    var gen;
    if (wl.kind === "random" || wl.kind === "hotcold") {
      var warm = wl.warmup;
      if (warm === undefined || warm < 0) {
        var pre = Math.min(nlw, totalLines, 8000000);
        for (var t = 0; t < threads; t++) {
          var base0 = wl.shared ? 0 : (t + 1) * PRIV / c.line;
          for (var q = 0; q < pre; q++) sim.access(t, base0 + q, false);
          if (wl.shared) break;
        }
        warm = Math.min(Math.floor(totalLines / 2), 4000000);
      }
      if (warm > 0) {
        var wgen = makeWorkload(c, Object.assign({}, wl, { accesses: Math.ceil(warm / threads) }), 1);
        while (wgen.next(out)) sim.access(out.core, out.line, out.write);
      }
      sim.reset();
      gen = makeWorkload(c, wl);
    } else if (wl.kind === "sequential" || wl.kind === "stride" || wl.kind === "graph") {
      var wpt = (wl.warmup === undefined || wl.warmup < 0)
        ? (wl.kind === "graph" ? Math.max(wl.accesses, Math.ceil(Math.min(3 * totalLines, 8000000) / threads)) : Math.min(nlw, Math.max(4096, Math.ceil(totalLines / threads)), 4000000))
        : Math.ceil(wl.warmup / threads);
      gen = makeWorkload(c, Object.assign({}, wl, { accesses: wpt + wl.accesses }));
      for (var w2 = 0; w2 < wpt * threads && gen.next(out); w2++) sim.access(out.core, out.line, out.write);
      sim.reset();
    } else gen = makeWorkload(c, wl);
    var n = 0, total = wl.kind === "pingpong" ? (wl.iters || 2000) * 4 : (wl.accesses || 0) * Math.max(1, Math.min(c.cores, wl.threads || 1));
    var ppSkip = wl.kind === "pingpong" ? 40 : 0, ppCycles = 0, ppCount = 0;
    while (gen.next(out)) {
      var lat = sim.access(out.core, out.line, out.write);
      if (gen.pingpong) { if (n >= ppSkip) { ppCycles += lat; ppCount++; } }
      n++;
      if (progress && (n & 262143) === 0 && total > 0) progress(n / total);
    }
    var r = summarize(sim);
    if (gen.pingpong) { r.pp_roundtrip_cycles = ppCount ? ppCycles / (ppCount / 4) : 0; r.pp_roundtrip_ns = r.pp_roundtrip_cycles / c.clock_ghz; }
    if (wl.instructions) r.instructions = wl.instructions;
    return r;
  }

  function summarize(sim) {
    var c = sim.c, s = sim.s, f = c.clock_ghz, L = c.line, r = {}, k;
    for (k in s) r[k] = s[k];
    var A = Math.max(1, s.accesses);
    var l1m = s.accesses - s.l1_hit, l2m = l1m - s.l2_hit;
    r.l1_hit_rate = s.l1_hit / A;
    r.l2_hit_rate = l1m > 0 ? s.l2_hit / l1m : 0;
    r.l3_lookups = l2m;
    r.l3_hit_rate = l2m > 0 ? (s.l3_hit + s.c2c_local) / l2m : 0;
    r.l3_miss_rate = l2m > 0 ? 1 - r.l3_hit_rate : 0;
    r.amat_cycles = s.lat_cycles / A;
    r.amat_ns = r.amat_cycles / f;
    r.exposed_cycles = s.exp_cycles / A;
    r.exposed_ns = r.exposed_cycles / f;
    r.dram_per_kacc = 1000 * s.dram_reads / A;
    // time model: the slowest of latency, L3 bandwidth, DRAM bandwidth and link bandwidth
    var tLat = 0, active = 0, i, g;
    for (i = 0; i < c.cores; i++) { if (sim.coreCycles[i] / f > tLat) tLat = sim.coreCycles[i] / f; if (sim.activeCore[i]) active++; }
    var dramBytes = (s.dram_reads + s.dram_writes) * L;
    var tDram = dramBytes / c.mem_bw_gbs;
    var tL3 = 0, tLink = 0;
    for (g = 0; g < c.groups; g++) {
      var act = 0;
      for (i = 0; i < c.cores; i++) if (sim.grp[i] === g && sim.activeCore[i]) act++;
      var bw = Math.max(1, act) * c.l3_bw_bpc * f;
      if (sim.l3Bytes[g] / bw > tL3) tL3 = sim.l3Bytes[g] / bw;
      if (c.link_gbs > 0 && sim.linkBytes[g] / c.link_gbs > tLink) tLink = sim.linkBytes[g] / c.link_gbs;
    }
    var t = Math.max(tLat, tDram, tL3, tLink);
    r.time_ns = t; r.t_latency_ns = tLat; r.t_dram_ns = tDram; r.t_l3_ns = tL3; r.t_link_ns = tLink;
    r.bottleneck = t === tLat ? "latency" : t === tDram ? "DRAM bandwidth" : t === tL3 ? "L3 bandwidth" : "die-to-die link";
    r.active_cores = active;
    r.dram_bw_gbs = t > 0 ? dramBytes / t : 0;
    var l3b = 0, lb = 0; for (g = 0; g < c.groups; g++) { l3b += sim.l3Bytes[g]; lb += sim.linkBytes[g]; }
    r.l3_bw_gbs = t > 0 ? l3b / t : 0;
    r.link_bytes = lb;
    r.throughput_gaps = t > 0 ? s.accesses / t : 0; // accesses per ns = G accesses/s
    // energy (dynamic, illustrative per-event values)
    var e = s.accesses * c.e_l1_pj + l1m * c.e_l2_pj + l2m * c.e_l3_pj +
            (s.l3_remote + s.c2c_remote) * c.e_l3_pj +
            (c.l4_mb > 0 ? (l2m - s.l3_hit - s.c2c_local - s.l3_remote - s.c2c_remote) * c.e_l4_pj : 0) +
            (s.dram_reads + s.dram_writes) * c.e_dram_pj + lb * 8 * c.e_link_pj_bit;
    r.energy_nj = e / 1000; r.energy_pj_per_access = e / A;
    // where accesses were served (fractions of all accesses)
    r.served = {
      L1: s.l1_hit / A, L2: s.l2_hit / A, "L3 (own)": (s.l3_hit + s.c2c_local) / A,
      "Other die / CCX": (s.l3_remote + s.c2c_remote) / A, L4: s.l4_hit / A, DRAM: s.dram_reads / A
    };
    return r;
  }

  // ---------- trace parsing (Valgrind Lackey or "core R|W hexaddr") ----------
  function parseTrace(text, line) {
    var out = [], instr = 0, lines = text.split(/\r?\n/);
    for (var i = 0; i < lines.length; i++) {
      var s = lines[i]; if (!s) continue;
      var m = /^\s*([ILSM])\s+([0-9a-fA-F]+),(\d+)/.exec(s);
      if (m) {
        if (m[1] === "I") { instr++; continue; }
        var addr = parseInt(m[2], 16), size = parseInt(m[3], 10);
        var a0 = Math.floor(addr / line), a1 = Math.floor((addr + Math.max(1, size) - 1) / line);
        for (var ln = a0; ln <= a1; ln++) {
          if (m[1] === "L") out.push([0, ln, 0]);
          else if (m[1] === "S") out.push([0, ln, 1]);
          else { out.push([0, ln, 0]); out.push([0, ln, 1]); }
        }
        continue;
      }
      var m2 = /^\s*(\d+)\s+([RW])\s+(?:0x)?([0-9a-fA-F]+)/.exec(s);
      if (m2) out.push([parseInt(m2[1], 10), Math.floor(parseInt(m2[3], 16) / line), m2[2] === "W" ? 1 : 0]);
    }
    return { trace: out, instructions: instr };
  }

  // ---------- presets (sources in tools/cachesim/README.md) ----------
  var PRESETS = {
    zen2_2ccx: { label: "Zen 2 style: two CCXs, 16 MB L3 each", cfg: { cores: 8, groups: 2, l3_mb: 16, l3_lat: 39 } },
    zen3_1ccx: { label: "Zen 3 style: one CCX, 32 MB L3", cfg: { cores: 8, groups: 1, l3_mb: 32, l3_lat: 47 } },
    vcache: { label: "Zen 3 + 3D V-Cache: 96 MB stacked L3", cfg: { cores: 8, groups: 1, l3_mb: 96, l3_lat: 51 } },
    planar96: { label: "Hypothetical planar 96 MB L3 (assumed +12 cycles)", cfg: { cores: 8, groups: 1, l3_mb: 96, l3_lat: 59 } },
    sidecar: { label: "Side-by-side cache die: 32 MB L3 + 64 MB L4", cfg: { cores: 8, groups: 1, l3_mb: 32, l3_lat: 47, l4_mb: 64, l4_lat_ns: 22 } },
    twoccd: { label: "Two chiplets: 2 x 8 cores, 32 MB L3 each", cfg: { cores: 16, groups: 2, l3_mb: 32, l3_lat: 47, hop_ns: 9, dram_hop: 1 } },
    mono16: { label: "Hypothetical monolithic 16 cores, one 64 MB L3", cfg: { cores: 16, groups: 1, l3_mb: 64, l3_lat: 47 } }
  };

  return { DEFAULTS: DEFAULTS, PRESETS: PRESETS, Cache: Cache, Sim: Sim, Rng: Rng, mix32: mix32,
           makeWorkload: makeWorkload, run: run, parseTrace: parseTrace };
})();

if (typeof module !== "undefined") module.exports = SIM;
