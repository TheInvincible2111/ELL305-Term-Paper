// ELL305 cache-hierarchy simulator (C++17).
//
// A trace-driven, functional model of a multi-core cache hierarchy: private L1D and
// inclusive private L2 per core, cores split into L3 groups (a CCX or a CCD) that each
// share one L3, an optional shared L4 (a side-by-side cache die), a directory for
// coherence, and DRAM. Latency is charged per access from the level that served it;
// execution time, bandwidth and energy are estimated afterwards.
//
// gui/sim-core.js is a line-for-line port of this file. Both use the same random number
// generator, cache model and workloads, so the same configuration gives identical counts
// (checked by test/crosscheck.js).
//
// Build:  g++ -O2 -std=c++17 -o cachesim src/cachesim.cpp
// Usage:  ./cachesim --preset zen3_1ccx --set kind=random --set ws_mb=24 --set accesses=1000000
//         valgrind --tool=lackey --trace-mem=yes ./prog 2>&1 >/dev/null | ./cachesim --trace - --preset vcache
//         ./cachesim --selftest
// Output: one JSON object with all counters and derived metrics.

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <functional>
#include <iostream>
#include <limits>
#include <map>
#include <memory>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

using u32 = uint32_t;
using u64 = uint64_t;

// ---------- deterministic random numbers (mulberry32, identical to the JS core) ----------
struct Rng {
  u32 a;
  explicit Rng(u32 seed) : a(seed) {}
  u32 next() {
    a += 0x6D2B79F5u;
    u32 t = a;
    t = (t ^ (t >> 15)) * (t | 1u);
    t = t ^ (t + (t ^ (t >> 7)) * (t | 61u));
    return t ^ (t >> 14);
  }
};
static u32 mix32(u32 x) {
  x = (x ^ (x >> 16)) * 0x85EBCA6Bu;
  x = (x ^ (x >> 13)) * 0xC2B2AE35u;
  return x ^ (x >> 16);
}

// ---------- configuration ----------
struct Config {
  double cores = 8, groups = 1, clock_ghz = 4.0, line = 64;
  double l1_kb = 32, l1_ways = 8, l1_lat = 4;
  double l2_kb = 512, l2_ways = 8, l2_lat = 12;
  double l3_mb = 32, l3_ways = 16, l3_lat = 47;
  double l4_mb = 0, l4_ways = 16, l4_lat_ns = 22;
  double mem_ns = 74, hop_ns = 9, dram_hop = 0, l4_victim = 0;
  std::string policy = "lru";
  double seed = 1;
  double overlap = 1.0, work_cycles = 1;
  double l3_bw_bpc = 32, mem_bw_gbs = 51.2, link_gbs = 0;
  double e_l1_pj = 5, e_l2_pj = 20, e_l3_pj = 100, e_l4_pj = 300, e_dram_pj = 2000, e_link_pj_bit = 2;
  bool set(const std::string& k, const std::string& v) {
    if (k == "policy") { policy = v; return true; }
    std::map<std::string, double*> m = {
      {"cores", &cores}, {"groups", &groups}, {"clock_ghz", &clock_ghz}, {"line", &line},
      {"l1_kb", &l1_kb}, {"l1_ways", &l1_ways}, {"l1_lat", &l1_lat},
      {"l2_kb", &l2_kb}, {"l2_ways", &l2_ways}, {"l2_lat", &l2_lat},
      {"l3_mb", &l3_mb}, {"l3_ways", &l3_ways}, {"l3_lat", &l3_lat},
      {"l4_mb", &l4_mb}, {"l4_ways", &l4_ways}, {"l4_lat_ns", &l4_lat_ns},
      {"mem_ns", &mem_ns}, {"hop_ns", &hop_ns}, {"dram_hop", &dram_hop}, {"l4_victim", &l4_victim}, {"seed", &seed},
      {"overlap", &overlap}, {"work_cycles", &work_cycles},
      {"l3_bw_bpc", &l3_bw_bpc}, {"mem_bw_gbs", &mem_bw_gbs}, {"link_gbs", &link_gbs},
      {"e_l1_pj", &e_l1_pj}, {"e_l2_pj", &e_l2_pj}, {"e_l3_pj", &e_l3_pj}, {"e_l4_pj", &e_l4_pj},
      {"e_dram_pj", &e_dram_pj}, {"e_link_pj_bit", &e_link_pj_bit}};
    auto it = m.find(k);
    if (it == m.end()) return false;
    *it->second = std::stod(v);
    return true;
  }
};

struct Workload {
  std::string kind = "random";
  double ws_mb = 16, accesses = 1000000, warmup = -1, write_frac = 0, shared = 0, threads = 1;
  double stride = 4096, hot_frac = 0.1, hot_prob = 0.9, far_mb = 0, far_prob = 0, n = 128, block = 0, degree = 8;
  double pp_a = 0, pp_b = 1, iters = 2000;
  std::vector<std::array<u64, 3>>* trace = nullptr;
  double instructions = 0;
  bool set(const std::string& k, const std::string& v) {
    if (k == "kind") { kind = v; return true; }
    std::map<std::string, double*> m = {
      {"ws_mb", &ws_mb}, {"accesses", &accesses}, {"warmup", &warmup}, {"write_frac", &write_frac},
      {"shared", &shared}, {"threads", &threads}, {"stride", &stride}, {"hot_frac", &hot_frac},
      {"hot_prob", &hot_prob}, {"far_mb", &far_mb}, {"far_prob", &far_prob}, {"n", &n}, {"block", &block}, {"degree", &degree},
      {"pp_a", &pp_a}, {"pp_b", &pp_b}, {"iters", &iters}};
    auto it = m.find(k);
    if (it == m.end()) return false;
    *it->second = std::stod(v);
    return true;
  }
};

static long jsround(double x) { return (long)std::floor(x + 0.5); }  // Math.round for x >= 0

// ---------- one set-associative cache ----------
struct Cache {
  u64 ways, sets;
  std::vector<int64_t> tag;     // -1 = invalid; otherwise the line number
  std::vector<uint8_t> dirty;
  std::vector<double> stamp;
  double clock = 0;
  int pol;                      // 0 lru, 1 fifo, 2 random, 3 tree-PLRU
  std::vector<uint8_t> plru;
  Rng rng;
  bool evDirty = false;
  u64 lastIdx = 0;

  Cache(double sizeBytes, double waysIn, double line, const std::string& policy, u32 seed) : rng(seed) {
    u64 nlines = std::max<u64>(1, (u64)std::floor(sizeBytes / line));
    ways = std::max<u64>(1, std::min<u64>((u64)waysIn, nlines));
    sets = std::max<u64>(1, nlines / ways);
    u64 n = sets * ways;
    tag.assign(n, -1); dirty.assign(n, 0); stamp.assign(n, 0);
    pol = policy == "fifo" ? 1 : policy == "random" ? 2 : policy == "plru" ? 3 : 0;
    if (pol == 3 && (ways & (ways - 1)) != 0) pol = 0;
    if (pol == 3) plru.assign(sets * std::max<u64>(1, ways - 1), 0);
  }
  int64_t lookup(u64 ln) const {
    u64 base = (ln % sets) * ways;
    for (u64 w = 0; w < ways; w++) if (tag[base + w] == (int64_t)ln) return (int64_t)(base + w);
    return -1;
  }
  void plruTouch(u64 set, u64 way) {
    u64 lo = 0, hi = ways, node = 0, b = set * (ways - 1);
    while (hi - lo > 1) {
      u64 mid = (lo + hi) >> 1;
      if (way < mid) { plru[b + node] = 1; node = 2 * node + 1; hi = mid; }
      else { plru[b + node] = 0; node = 2 * node + 2; lo = mid; }
    }
  }
  void touch(u64 idx) {
    if (pol == 0) stamp[idx] = ++clock;
    else if (pol == 3) plruTouch(idx / ways, idx % ways);
  }
  int64_t insert(u64 ln, bool d) {
    u64 set = ln % sets, base = set * ways;
    int64_t v = -1;
    for (u64 w = 0; w < ways; w++) if (tag[base + w] == -1) { v = (int64_t)w; break; }
    if (v < 0) {
      if (pol == 2) v = (int64_t)(rng.next() % (u32)ways);
      else if (pol == 3) {
        u64 lo = 0, hi = ways, node = 0, b = set * (ways - 1);
        while (hi - lo > 1) {
          u64 mid = (lo + hi) >> 1;
          if (plru[b + node] == 0) { node = 2 * node + 1; hi = mid; } else { node = 2 * node + 2; lo = mid; }
        }
        v = (int64_t)lo;
      } else {
        double best = std::numeric_limits<double>::infinity();
        for (u64 w = 0; w < ways; w++) if (stamp[base + w] < best) { best = stamp[base + w]; v = (int64_t)w; }
      }
    }
    u64 idx = base + (u64)v;
    int64_t ev = tag[idx];
    evDirty = ev != -1 && dirty[idx] == 1;
    tag[idx] = (int64_t)ln; dirty[idx] = d ? 1 : 0;
    stamp[idx] = ++clock;
    if (pol == 3) plruTouch(set, (u64)v);
    lastIdx = idx;
    return ev;
  }
  int invalidate(u64 ln) {
    int64_t i = lookup(ln);
    if (i < 0) return -1;
    int d = dirty[i];
    tag[i] = -1; dirty[i] = 0; stamp[i] = 0;
    return d;
  }
};

// ---------- statistics ----------
struct Stats {
  double accesses = 0, reads = 0, writes = 0, instructions = 0;
  double l1_hit = 0, l2_hit = 0, l3_hit = 0, l3_remote = 0, c2c_local = 0, c2c_remote = 0;
  double l4_hit = 0, dram_reads = 0, dram_writes = 0, inv_local = 0, inv_remote = 0, lat_cycles = 0, exp_cycles = 0;
};

// ---------- the hierarchy ----------
struct Sim {
  Config c;
  int cores, groups;
  double hopC, memC, l4C;
  std::vector<std::unique_ptr<Cache>> l1, l2, l3;
  std::unique_ptr<Cache> l4;
  std::vector<int> grp;
  bool useDir;
  std::unordered_map<u64, u32> dir;
  Stats s;
  std::vector<double> coreCycles, coreAcc, l3Bytes, linkBytes, dramBytesG;
  std::vector<uint8_t> activeCore;

  Sim(const Config& cfg, bool coherence) : c(cfg) {
    cores = (int)std::max(1L, std::min(16L, jsround(c.cores)));
    groups = (int)std::max(1L, std::min((long)cores, jsround(c.groups)));
    c.cores = cores; c.groups = groups;
    double f = c.clock_ghz;
    hopC = c.hop_ns * f; memC = c.mem_ns * f; l4C = c.l4_lat_ns * f;
    u32 sd = (u32)(u64)c.seed;
    for (int i = 0; i < cores; i++) {
      l1.emplace_back(new Cache(c.l1_kb * 1024, c.l1_ways, c.line, c.policy, sd * 977u + (u32)i * 31u + 1u));
      l2.emplace_back(new Cache(c.l2_kb * 1024, c.l2_ways, c.line, c.policy, sd * 977u + (u32)i * 31u + 2u));
      grp.push_back((int)std::floor((double)i * groups / cores));
    }
    for (int g = 0; g < groups; g++)
      l3.emplace_back(new Cache(c.l3_mb * 1048576, c.l3_ways, c.line, c.policy, sd * 977u + 500u + (u32)g));
    if (c.l4_mb > 0) l4.reset(new Cache(c.l4_mb * 1048576, c.l4_ways, c.line, c.policy, sd * 977u + 900u));
    useDir = cores > 1 && coherence;
    reset();
  }
  void reset() {
    s = Stats();
    coreCycles.assign(cores, 0); coreAcc.assign(cores, 0); activeCore.assign(cores, 0);
    l3Bytes.assign(groups, 0); linkBytes.assign(groups, 0); dramBytesG.assign(groups, 0);
  }
  u32 dirGet(u64 ln) const { auto it = dir.find(ln); return it == dir.end() ? 0 : it->second; }
  void dirAdd(u64 ln, int core) { if (useDir) dir[ln] |= (1u << core); }
  void dirRemove(u64 ln, int core) {
    if (!useDir) return;
    auto it = dir.find(ln);
    if (it == dir.end()) return;
    it->second &= ~(1u << core);
    if (!it->second) dir.erase(it);
  }
  void l4Insert(u64 ln, bool d) {
    int64_t i = l4->lookup(ln);
    if (i >= 0) { if (d) l4->dirty[i] = 1; return; }
    int64_t ev = l4->insert(ln, d);
    if (ev != -1 && l4->evDirty) { s.dram_writes++; dramBytesG[0] += c.line; }
  }
  void l3Insert(int g, u64 ln, bool d) {
    Cache& L3 = *l3[g];
    int64_t i = L3.lookup(ln);
    if (i >= 0) { if (d) L3.dirty[i] = 1; return; }
    int64_t ev = L3.insert(ln, d);
    if (ev != -1 && l4 && c.l4_victim > 0) { l4Insert((u64)ev, L3.evDirty); return; }   // victim L4 takes every L3 eviction
    if (ev != -1 && L3.evDirty) {
      if (l4) l4Insert((u64)ev, true);
      else { s.dram_writes++; dramBytesG[g] += c.line; if (c.link_gbs > 0) linkBytes[g] += c.line; }
    }
  }
  u64 l2Fill(int core, u64 ln, bool d) {
    Cache& L2 = *l2[core];
    int64_t ev = L2.insert(ln, d);
    u64 idx = L2.lastIdx;
    if (ev != -1) {
      bool evd = L2.evDirty;
      l1[core]->invalidate((u64)ev);
      dirRemove((u64)ev, core);
      if (evd) l3Insert(grp[core], (u64)ev, true);
    }
    dirAdd(ln, core);
    return idx;
  }
  double fetch(int core, int g, u64 ln, bool isWrite) {
    double L = c.line;
    if (useDir) {
      u32 holders = dirGet(ln) & ~(1u << core);
      if (holders) {
        int owner = -1, sameGroup = -1, otherGroup = -1;
        for (int o = 0; o < cores; o++) {
          if (!(holders & (1u << o))) continue;
          int64_t i2 = l2[o]->lookup(ln);
          if (i2 >= 0 && l2[o]->dirty[i2]) owner = o;
          if (grp[o] == g) { if (sameGroup < 0) sameGroup = o; } else if (otherGroup < 0) otherGroup = o;
        }
        if (owner >= 0) {
          int og = grp[owner];
          if (!isWrite) {
            int64_t j = l2[owner]->lookup(ln); l2[owner]->dirty[j] = 0;
            l3Insert(og, ln, true);
          }
          if (og == g) { s.c2c_local++; l3Bytes[g] += L; return c.l3_lat; }
          s.c2c_remote++; linkBytes[g] += L; linkBytes[og] += L;
          if (!isWrite) l3Insert(g, ln, false);
          return c.l3_lat + hopC + c.l3_lat;
        }
        if (sameGroup >= 0) { s.c2c_local++; l3Bytes[g] += L; return c.l3_lat; }
      }
    }
    Cache& L3 = *l3[g];
    int64_t i3 = L3.lookup(ln);
    if (i3 >= 0) { L3.touch((u64)i3); s.l3_hit++; l3Bytes[g] += L; return c.l3_lat; }
    if (groups > 1) {
      for (int gg = 0; gg < groups; gg++) {
        if (gg == g) continue;
        int64_t r = l3[gg]->lookup(ln);
        if (r >= 0) {
          l3[gg]->touch((u64)r);
          s.l3_remote++; linkBytes[g] += L; linkBytes[gg] += L;
          l3Insert(g, ln, false);
          return c.l3_lat + hopC + c.l3_lat;
        }
      }
      if (useDir) {
        u32 h2 = dirGet(ln) & ~(1u << core);
        if (h2) {
          for (int q = 0; q < cores; q++) if (h2 & (1u << q)) { linkBytes[grp[q]] += L; break; }
          s.c2c_remote++; linkBytes[g] += L;
          l3Insert(g, ln, false);
          return c.l3_lat + hopC + c.l3_lat;
        }
      }
    }
    if (l4) {
      int64_t i4 = l4->lookup(ln);
      if (i4 >= 0) {
        s.l4_hit++;
        if (c.l4_victim > 0) { bool d4 = l4->dirty[i4] != 0; l4->invalidate(ln); l3Insert(g, ln, d4); }  // exclusive: move up
        else { l4->touch((u64)i4); l3Insert(g, ln, false); }
        return c.l3_lat + l4C;
      }
    }
    s.dram_reads++; dramBytesG[g] += L; if (c.link_gbs > 0) linkBytes[g] += L;
    if (l4 && !(c.l4_victim > 0)) l4Insert(ln, false);
    l3Insert(g, ln, false);
    return c.l3_lat + memC + (c.dram_hop > 0 ? hopC : 0);   // dram_hop: every memory access crosses to the I/O die
  }
  double access(int core, u64 ln, bool isWrite) {
    int g = grp[core];
    Cache& L1 = *l1[core];
    Cache& L2 = *l2[core];
    double lat; bool privHit = false; int64_t i2;
    int64_t i1 = L1.lookup(ln);
    if (i1 >= 0) { L1.touch((u64)i1); s.l1_hit++; lat = c.l1_lat; privHit = true; i2 = L2.lookup(ln); }
    else {
      i2 = L2.lookup(ln);
      if (i2 >= 0) { L2.touch((u64)i2); s.l2_hit++; lat = c.l2_lat; privHit = true; L1.insert(ln, false); }
      else {
        lat = fetch(core, g, ln, isWrite);
        i2 = (int64_t)l2Fill(core, ln, false);
        L1.insert(ln, false);
      }
    }
    if (isWrite) {
      if (useDir) {
        u32 others = dirGet(ln) & ~(1u << core);
        if (others) {
          bool remote = false;
          for (int o = 0; o < cores; o++) {
            if (!(others & (1u << o))) continue;
            l1[o]->invalidate(ln);
            l2[o]->invalidate(ln);
            if (grp[o] == g) s.inv_local++; else { s.inv_remote++; remote = true; }
          }
          dir[ln] = 1u << core;
          if (privHit) lat += c.l3_lat;
          if (remote) lat += hopC;
        }
      }
      for (int gg = 0; gg < groups; gg++) if (gg != g) l3[gg]->invalidate(ln);
      L2.dirty[(u64)i2] = 1;
      s.writes++;
    } else s.reads++;
    s.accesses++;
    double exposed = lat <= c.l2_lat ? lat : c.l2_lat + c.overlap * (lat - c.l2_lat);
    coreCycles[core] += exposed + c.work_cycles;
    s.exp_cycles += exposed;
    coreAcc[core]++;
    activeCore[core] = 1;
    s.lat_cycles += lat;
    return lat;
  }
};

// ---------- workloads ----------
struct Access { int core = 0; u64 line = 0; bool write = false; };
using Gen = std::function<bool(Access&)>;
static const double PRIV = 68719476736.0;  // 2^36 bytes between private regions

struct WorkloadGen {
  Gen next;
  bool pingpong = false;
};

static WorkloadGen perCore(const Config& cfg, const Workload& wl,
                           std::function<std::function<bool(Access&)>(int, int)> makeGen) {
  int cores = (int)std::max(1.0, std::min(cfg.cores, wl.threads > 0 ? wl.threads : cfg.cores));
  auto gens = std::make_shared<std::vector<std::function<bool(Access&)>>>();
  for (int i = 0; i < cores; i++) gens->push_back(makeGen(i, cores));
  auto turn = std::make_shared<int>(0), alive = std::make_shared<int>(cores);
  auto done = std::make_shared<std::vector<uint8_t>>(cores, 0);
  WorkloadGen w;
  w.next = [=](Access& out) {
    while (*alive > 0) {
      int t = *turn; *turn = (*turn + 1) % cores;
      if ((*done)[t]) continue;
      if ((*gens)[t](out)) { out.core = t; return true; }
      (*done)[t] = 1; (*alive)--;
    }
    return false;
  };
  return w;
}

static WorkloadGen makeWorkload(const Config& cfg, const Workload& wl, u32 salt = 0) {
  double L = cfg.line;
  const std::string kind = wl.kind;
  if (kind == "random" || kind == "sequential" || kind == "stride" || kind == "hotcold") {
    double wsBytes = std::max(L, (double)jsround(wl.ws_mb * 1048576));
    u64 nl = std::max<u64>(1, (u64)std::floor(wsBytes / L));
    long wf = jsround(wl.write_frac * 1000);
    long hp = jsround(wl.hot_prob * 1000000), fp = jsround(wl.far_prob * 1000000);   // resolution 1e-6
    u64 farN = (u64)std::floor(std::max(0.0, (double)jsround(wl.far_mb * 1048576)) / L);
    return perCore(cfg, wl, [=](int core, int) {
      auto rng = std::make_shared<Rng>((u32)((u32)(u64)cfg.seed * 7919u + (u32)core * 104729u + 17u + salt * 1000003u));
      u64 base = wl.shared ? 0 : (u64)((core + 1) * PRIV / L);
      auto pos = std::make_shared<u64>(0);
      auto left = std::make_shared<double>(wl.accesses);
      u64 hotN = std::max<u64>(1, (u64)std::floor(nl * wl.hot_frac));
      u64 sl = std::max<u64>(1, (u64)jsround(wl.stride / L));
      bool rnd = kind == "random", seq = kind == "sequential", str = kind == "stride";
      return std::function<bool(Access&)>([=](Access& out) {
        if (*left <= 0) return false;
        (*left)--;
        u64 idx;
        if (rnd) idx = rng->next() % nl;
        else if (seq) { idx = *pos; *pos = (*pos + 1) % nl; }
        else if (str) { idx = (*pos * sl) % nl; (*pos)++; }
        else {
          u32 r = rng->next() % 1000000;
          if ((long)r < hp) idx = rng->next() % hotN;
          else if (farN > 0 && (long)r < hp + fp) idx = nl + rng->next() % farN;   // far region beyond the working set
          else idx = rng->next() % nl;
        }
        out.line = base + idx;
        out.write = wf > 0 && (long)(rng->next() % 1000) < wf;
        return true;
      });
    });
  }
  if (kind == "matmul") {
    long n = std::max(2L, jsround(wl.n));
    long b = wl.block > 0 ? std::min(n, jsround(wl.block)) : n;
    u64 A = 0, B = (u64)n * n * 8, C = 2 * (u64)n * n * 8;
    return perCore(cfg, wl, [=](int core, int cores) {
      long r0 = (long)std::floor((double)core * n / cores), r1 = (long)std::floor((double)(core + 1) * n / cores);
      struct St { long ii, jj, kk, i, j, kx; int phase, sub; bool done; };
      auto st = std::make_shared<St>(St{r0, 0, 0, r0, 0, 0, 0, 0, r0 >= r1});
      return std::function<bool(Access&)>([=](Access& out) {
        St& q = *st;
        if (q.done) return false;
        u64 addr; bool wr = false;
        if (q.phase == 0) { q.phase = 1; q.kx = q.kk; q.sub = 0; addr = C + (u64)(q.i * n + q.j) * 8; }
        else if (q.phase == 1) {
          if (q.sub == 0) { q.sub = 1; addr = A + (u64)(q.i * n + q.kx) * 8; }
          else { q.sub = 0; addr = B + (u64)(q.kx * n + q.j) * 8; q.kx++; if (q.kx >= std::min(q.kk + b, n)) q.phase = 2; }
        } else {
          q.phase = 0; addr = C + (u64)(q.i * n + q.j) * 8; wr = true;
          q.j++;
          if (q.j >= std::min(q.jj + b, n)) {
            q.j = q.jj; q.i++;
            if (q.i >= std::min(q.ii + b, r1)) {
              q.i = q.ii; q.kk += b;
              if (q.kk >= n) {
                q.kk = 0; q.jj += b;
                if (q.jj >= n) { q.jj = 0; q.ii += b; if (q.ii >= r1) q.done = true; }
                q.j = q.jj;
              }
              q.i = q.ii;
            }
          }
        }
        out.line = (u64)std::floor(addr / L); out.write = wr;
        return true;
      });
    });
  }
  if (kind == "graph") {
    u64 V = std::max<u64>(16, (u64)std::floor(wl.ws_mb * 1048576 / 8));
    u64 d = (u64)std::max(1L, jsround(wl.degree));
    u64 OFF = 0, EDGE = V * 8, PROP = V * 8 + V * d * 4;
    return perCore(cfg, wl, [=](int core, int cores) {
      u64 v0 = (u64)std::floor((double)core * V / cores), v1 = (u64)std::floor((double)(core + 1) * V / cores);
      struct St { u64 v, e; int phase; double left; };
      auto st = std::make_shared<St>(St{v0, 0, 0, wl.accesses});
      return std::function<bool(Access&)>([=](Access& out) {
        St& q = *st;
        if (q.left <= 0 || v0 >= v1) return false;
        q.left--;
        u64 addr; bool wr = false;
        if (q.phase == 0) { addr = OFF + q.v * 8; q.phase = 1; q.e = 0; }
        else if (q.phase == 1) { addr = EDGE + (q.v * d + q.e) * 4; q.phase = 2; }
        else if (q.phase == 2) {
          u64 nb = mix32((u32)(q.v * d + q.e)) % V; addr = PROP + nb * 8; q.e++;
          q.phase = q.e < d ? 1 : 3;
        } else { addr = PROP + q.v * 8; wr = true; q.phase = 0; q.v++; if (q.v >= v1) q.v = v0; }
        out.line = (u64)std::floor((double)addr / L); out.write = wr;
        return true;
      });
    });
  }
  if (kind == "pingpong") {
    int a = (int)std::min((long)cfg.cores - 1, jsround(wl.pp_a)), bb = (int)std::min((long)cfg.cores - 1, jsround(wl.pp_b));
    auto step = std::make_shared<int>(0); auto it = std::make_shared<double>(0);
    double iters = wl.iters;
    WorkloadGen w; w.pingpong = true;
    w.next = [=](Access& out) {
      if (*it >= iters) return false;
      const u64 X = 1000003, Y = 2000003;
      if (*step == 0) { out.core = a; out.line = X; out.write = true; }
      else if (*step == 1) { out.core = bb; out.line = X; out.write = false; }
      else if (*step == 2) { out.core = bb; out.line = Y; out.write = true; }
      else { out.core = a; out.line = Y; out.write = false; }
      (*step)++; if (*step == 4) { *step = 0; (*it)++; }
      return true;
    };
    return w;
  }
  if (kind == "trace") {
    auto tr = wl.trace; auto p = std::make_shared<size_t>(0);
    int maxc = (int)cfg.cores - 1;
    WorkloadGen w;
    w.next = [=](Access& out) {
      if (!tr || *p >= tr->size()) return false;
      auto& e = (*tr)[(*p)++];
      out.core = std::min(maxc, (int)e[0]); out.line = e[1]; out.write = e[2] != 0;
      return true;
    };
    return w;
  }
  throw std::runtime_error("unknown workload: " + kind);
}

// ---------- results ----------
struct Result { std::vector<std::pair<std::string, double>> num; std::string bottleneck; };

static Result summarize(Sim& sim) {
  const Config& c = sim.c; const Stats& s = sim.s;
  double f = c.clock_ghz, L = c.line;
  Result r;
  auto put = [&](const std::string& k, double v) { r.num.push_back({k, v}); };
  put("accesses", s.accesses); put("reads", s.reads); put("writes", s.writes);
  put("l1_hit", s.l1_hit); put("l2_hit", s.l2_hit); put("l3_hit", s.l3_hit); put("l3_remote", s.l3_remote);
  put("c2c_local", s.c2c_local); put("c2c_remote", s.c2c_remote); put("l4_hit", s.l4_hit);
  put("dram_reads", s.dram_reads); put("dram_writes", s.dram_writes);
  put("inv_local", s.inv_local); put("inv_remote", s.inv_remote); put("lat_cycles", s.lat_cycles);
  double A = std::max(1.0, s.accesses);
  double l1m = s.accesses - s.l1_hit, l2m = l1m - s.l2_hit;
  put("l1_hit_rate", s.l1_hit / A);
  put("l2_hit_rate", l1m > 0 ? s.l2_hit / l1m : 0);
  put("l3_lookups", l2m);
  double l3hr = l2m > 0 ? (s.l3_hit + s.c2c_local) / l2m : 0;
  put("l3_hit_rate", l3hr);
  put("l3_miss_rate", l2m > 0 ? 1 - l3hr : 0);
  put("amat_cycles", s.lat_cycles / A);
  put("amat_ns", s.lat_cycles / A / f);
  put("exposed_cycles", s.exp_cycles / A);
  put("exposed_ns", s.exp_cycles / A / f);
  put("dram_per_kacc", 1000 * s.dram_reads / A);
  double tLat = 0; int active = 0;
  for (int i = 0; i < sim.cores; i++) { if (sim.coreCycles[i] / f > tLat) tLat = sim.coreCycles[i] / f; if (sim.activeCore[i]) active++; }
  double dramBytes = (s.dram_reads + s.dram_writes) * L;
  double tDram = dramBytes / c.mem_bw_gbs, tL3 = 0, tLink = 0;
  for (int g = 0; g < sim.groups; g++) {
    int act = 0;
    for (int i = 0; i < sim.cores; i++) if (sim.grp[i] == g && sim.activeCore[i]) act++;
    double bw = std::max(1, act) * c.l3_bw_bpc * f;
    if (sim.l3Bytes[g] / bw > tL3) tL3 = sim.l3Bytes[g] / bw;
    if (c.link_gbs > 0 && sim.linkBytes[g] / c.link_gbs > tLink) tLink = sim.linkBytes[g] / c.link_gbs;
  }
  double t = std::max(std::max(tLat, tDram), std::max(tL3, tLink));
  put("time_ns", t); put("t_latency_ns", tLat); put("t_dram_ns", tDram); put("t_l3_ns", tL3); put("t_link_ns", tLink);
  r.bottleneck = t == tLat ? "latency" : t == tDram ? "DRAM bandwidth" : t == tL3 ? "L3 bandwidth" : "die-to-die link";
  put("active_cores", active);
  put("dram_bw_gbs", t > 0 ? dramBytes / t : 0);
  double l3b = 0, lb = 0;
  for (int g = 0; g < sim.groups; g++) { l3b += sim.l3Bytes[g]; lb += sim.linkBytes[g]; }
  put("l3_bw_gbs", t > 0 ? l3b / t : 0);
  put("link_bytes", lb);
  put("throughput_gaps", t > 0 ? s.accesses / t : 0);
  double e = s.accesses * c.e_l1_pj + l1m * c.e_l2_pj + l2m * c.e_l3_pj +
             (s.l3_remote + s.c2c_remote) * c.e_l3_pj +
             (c.l4_mb > 0 ? (l2m - s.l3_hit - s.c2c_local - s.l3_remote - s.c2c_remote) * c.e_l4_pj : 0) +
             (s.dram_reads + s.dram_writes) * c.e_dram_pj + lb * 8 * c.e_link_pj_bit;
  put("energy_nj", e / 1000); put("energy_pj_per_access", e / A);
  return r;
}

static Result run(const Config& cfg, Workload wl) {
  bool multi = wl.kind == "pingpong" || wl.kind == "trace" || wl.threads > 1;
  Sim sim(cfg, multi);
  const Config& c = sim.c;
  Access out;
  int threads = (int)std::max(1.0, std::min(c.cores, wl.threads > 0 ? wl.threads : 1));
  double totalLines = std::floor((c.l3_mb * c.groups + c.l4_mb) * 1048576 / c.line);
  double nlw = std::max(1.0, std::floor(std::max(c.line, (double)jsround(wl.ws_mb * 1048576)) / c.line));
  WorkloadGen gen;
  if (wl.kind == "random" || wl.kind == "hotcold") {
    double warm = wl.warmup;
    if (warm < 0) {
      double pre = std::min(std::min(nlw, totalLines), 8000000.0);
      for (int t = 0; t < threads; t++) {
        u64 base0 = wl.shared ? 0 : (u64)((t + 1) * PRIV / c.line);
        for (u64 q = 0; q < (u64)pre; q++) sim.access(t, base0 + q, false);
        if (wl.shared) break;
      }
      warm = std::min(std::floor(totalLines / 2), 4000000.0);
    }
    if (warm > 0) {
      Workload w2 = wl;
      w2.accesses = std::ceil(warm / threads);
      WorkloadGen wg = makeWorkload(c, w2, 1);
      while (wg.next(out)) sim.access(out.core, out.line, out.write);
    }
    sim.reset();
    gen = makeWorkload(c, wl, 0);
  } else if (wl.kind == "sequential" || wl.kind == "stride" || wl.kind == "graph") {
    double wpt = wl.warmup >= 0 ? std::ceil(wl.warmup / threads)
               : wl.kind == "graph" ? std::max(wl.accesses, std::ceil(std::min(3 * totalLines, 8000000.0) / threads))
               : std::min(std::min(nlw, std::max(4096.0, std::ceil(totalLines / threads))), 4000000.0);
    Workload w2 = wl; w2.accesses = wpt + wl.accesses;
    gen = makeWorkload(c, w2, 0);
    for (double k = 0; k < wpt * threads && gen.next(out); k++) sim.access(out.core, out.line, out.write);
    sim.reset();
  } else gen = makeWorkload(c, wl, 0);
  double n = 0, ppSkip = gen.pingpong ? 40 : 0, ppCycles = 0, ppCount = 0;
  while (gen.next(out)) {
    double lat = sim.access(out.core, out.line, out.write);
    if (gen.pingpong && n >= ppSkip) { ppCycles += lat; ppCount++; }
    n++;
  }
  Result r = summarize(sim);
  if (gen.pingpong) {
    double rt = ppCount ? ppCycles / (ppCount / 4) : 0;
    r.num.push_back({"pp_roundtrip_cycles", rt});
    r.num.push_back({"pp_roundtrip_ns", rt / c.clock_ghz});
  }
  if (wl.instructions > 0) {
    r.num.push_back({"instructions", wl.instructions});
    double l3m = 0, l2m = 0;
    for (auto& kv : r.num) if (kv.first == "dram_reads") l3m = kv.second;
    for (auto& kv : r.num) if (kv.first == "l3_lookups") l2m = kv.second;
    r.num.push_back({"l3_mpki", 1000 * l3m / wl.instructions});
    r.num.push_back({"l2_mpki", 1000 * l2m / wl.instructions});
  }
  return r;
}

// ---------- presets (same as gui/sim-core.js; sources in README.md) ----------
static std::map<std::string, std::vector<std::pair<std::string, std::string>>> PRESETS = {
  {"zen2_2ccx", {{"cores", "8"}, {"groups", "2"}, {"l3_mb", "16"}, {"l3_lat", "39"}}},
  {"zen3_1ccx", {{"cores", "8"}, {"groups", "1"}, {"l3_mb", "32"}, {"l3_lat", "47"}}},
  {"vcache", {{"cores", "8"}, {"groups", "1"}, {"l3_mb", "96"}, {"l3_lat", "51"}}},
  {"planar96", {{"cores", "8"}, {"groups", "1"}, {"l3_mb", "96"}, {"l3_lat", "59"}}},
  {"sidecar", {{"cores", "8"}, {"groups", "1"}, {"l3_mb", "32"}, {"l3_lat", "47"}, {"l4_mb", "64"}, {"l4_lat_ns", "22"}}},
  {"twoccd", {{"cores", "16"}, {"groups", "2"}, {"l3_mb", "32"}, {"l3_lat", "47"}, {"hop_ns", "9"}, {"dram_hop", "1"}}},
  {"mono16", {{"cores", "16"}, {"groups", "1"}, {"l3_mb", "64"}, {"l3_lat", "47"}}},
};

// ---------- trace parsing: Valgrind Lackey lines or "core R|W hexaddr" ----------
static void readTrace(std::istream& in, double line, std::vector<std::array<u64, 3>>& tr, double& instr) {
  std::string s;
  while (std::getline(in, s)) {
    size_t p = 0;
    while (p < s.size() && s[p] == ' ') p++;
    if (p >= s.size()) continue;
    char op = s[p];
    if ((op == 'I' || op == 'L' || op == 'S' || op == 'M') && p + 1 < s.size() && s[p + 1] == ' ') {
      if (op == 'I') { instr++; continue; }
      size_t comma = s.find(',', p);
      if (comma == std::string::npos) continue;
      u64 addr = std::stoull(s.substr(p + 1, comma - p - 1), nullptr, 16);
      u64 size = std::stoull(s.substr(comma + 1));
      u64 L = (u64)line, a0 = addr / L, a1 = (addr + std::max<u64>(1, size) - 1) / L;
      for (u64 ln = a0; ln <= a1; ln++) {
        if (op == 'L') tr.push_back({0, ln, 0});
        else if (op == 'S') tr.push_back({0, ln, 1});
        else { tr.push_back({0, ln, 0}); tr.push_back({0, ln, 1}); }
      }
      continue;
    }
    std::istringstream is(s);
    u64 core; std::string rw, hex;
    if (is >> core >> rw >> hex) {
      if (hex.rfind("0x", 0) == 0) hex = hex.substr(2);
      tr.push_back({core, std::stoull(hex, nullptr, 16) / (u64)line, (u64)(rw == "W")});
    }
  }
}

static void printJson(const Result& r) {
  std::printf("{");
  for (size_t i = 0; i < r.num.size(); i++) {
    double v = r.num[i].second;
    if (std::isfinite(v)) std::printf("\"%s\": %.17g, ", r.num[i].first.c_str(), v);
  }
  std::printf("\"bottleneck\": \"%s\"}\n", r.bottleneck.c_str());
}

// ---------- self-test: tiny caches with hand-checked answers ----------
static int selftest() {
  int fails = 0;
  auto check = [&](bool ok, const char* what) { std::printf("%s  %s\n", ok ? "PASS" : "FAIL", what); if (!ok) fails++; };
  { // direct-mapped, 4 lines of 64 B: lines 0 and 4 map to set 0 and evict each other
    Cache c(256, 1, 64, "lru", 1);
    c.insert(0, false); check(c.lookup(0) >= 0, "direct-mapped: line 0 present after insert");
    c.insert(4, false); check(c.lookup(0) < 0 && c.lookup(4) >= 0, "direct-mapped: line 4 evicts line 0 (same set)");
  }
  { // 2-way LRU, 1 set: A B A C -> B evicted
    Cache c(128, 2, 64, "lru", 1);
    c.insert(1, false); c.insert(2, false); c.touch(c.lookup(1)); c.insert(3, false);
    check(c.lookup(1) >= 0 && c.lookup(2) < 0, "2-way LRU: least recently used line evicted");
  }
  { // 2-way FIFO, 1 set: A B A C -> A evicted (oldest insert)
    Cache c(128, 2, 64, "fifo", 1);
    c.insert(1, false); c.insert(2, false); c.touch(c.lookup(1)); c.insert(3, false);
    check(c.lookup(1) < 0 && c.lookup(2) >= 0, "2-way FIFO: oldest inserted line evicted");
  }
  { // 4-way tree PLRU, 1 set: fill 0..3, touch 0, insert 4 -> victim is in the half not touched
    Cache c(256, 4, 64, "plru", 1);
    for (u64 i = 0; i < 4; i++) c.insert(i, false);
    c.touch(c.lookup(0)); c.insert(4, false);
    check(c.lookup(0) >= 0, "4-way PLRU: most recently used line kept");
  }
  { // LRU loop thrash: 3 lines cycled through a 2-line fully associative cache never hit
    Cache c(128, 2, 64, "lru", 1); int hits = 0;
    for (int k = 0; k < 30; k++) { u64 ln = k % 3; int64_t i = c.lookup(ln); if (i >= 0) { hits++; c.touch(i); } else c.insert(ln, false); }
    check(hits == 0, "LRU: cyclic loop one line larger than the cache never hits");
  }
  { // hierarchy: first touch goes to DRAM, second hits L1
    Config cfg; cfg.cores = 1; Sim sim(cfg, false);
    double a = sim.access(0, 12345, false), b = sim.access(0, 12345, false);
    check(a == cfg.l3_lat + cfg.mem_ns * cfg.clock_ghz && b == cfg.l1_lat, "hierarchy: miss costs L3 + DRAM, re-access costs L1");
  }
  { // coherence: core 1 reads a line core 0 has written -> core-to-core transfer; other group adds the hop
    Config cfg; cfg.cores = 8; cfg.groups = 2; Sim sim(cfg, true);
    sim.access(0, 777, true); double same = sim.access(1, 777, false);
    sim.access(0, 888, true); double other = sim.access(4, 888, false);
    check(same == cfg.l3_lat && other == 2 * cfg.l3_lat + cfg.hop_ns * cfg.clock_ghz, "coherence: same-CCX transfer vs cross-CCX transfer");
  }
  std::printf("%d failure(s)\n", fails);
  return fails ? 1 : 0;
}

int main(int argc, char** argv) {
  Config cfg; Workload wl;
  std::vector<std::array<u64, 3>> trace;
  std::string tracePath;
  auto apply = [&](const std::string& kv) {
    size_t eq = kv.find('=');
    if (eq == std::string::npos) { std::fprintf(stderr, "expected key=value: %s\n", kv.c_str()); std::exit(2); }
    std::string k = kv.substr(0, eq), v = kv.substr(eq + 1);
    if (!cfg.set(k, v) && !wl.set(k, v)) { std::fprintf(stderr, "unknown key: %s\n", k.c_str()); std::exit(2); }
  };
  for (int i = 1; i < argc; i++) {
    std::string a = argv[i];
    if (a == "--selftest") return selftest();
    else if (a == "--preset" && i + 1 < argc) {
      auto it = PRESETS.find(argv[++i]);
      if (it == PRESETS.end()) { std::fprintf(stderr, "unknown preset\n"); return 2; }
      for (auto& kv : it->second) cfg.set(kv.first, kv.second);
    } else if (a == "--config" && i + 1 < argc) {
      std::ifstream f(argv[++i]); std::string line;
      while (std::getline(f, line)) { if (line.empty() || line[0] == '#') continue; apply(line); }
    } else if (a == "--set" && i + 1 < argc) apply(argv[++i]);
    else if (a == "--trace" && i + 1 < argc) tracePath = argv[++i];
    else { std::fprintf(stderr, "usage: cachesim [--preset NAME] [--config FILE] [--set key=value]... [--trace FILE|-] [--selftest]\n"); return 2; }
  }
  if (!tracePath.empty()) {
    if (tracePath == "-") readTrace(std::cin, cfg.line, trace, wl.instructions);
    else { std::ifstream f(tracePath); readTrace(f, cfg.line, trace, wl.instructions); }
    wl.kind = "trace"; wl.trace = &trace;
  }
  printJson(run(cfg, wl));
  return 0;
}
