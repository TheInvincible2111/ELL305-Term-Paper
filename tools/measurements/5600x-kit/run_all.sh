#!/usr/bin/env bash
# ELL305 term paper - 5600X measurement kit. Runs everything and zips the results.
# Usage (in WSL Ubuntu or native Linux, from this folder):   bash run_all.sh
# Takes about 10 minutes (9 on the group's 5600X). Keep the machine plugged in and idle while it runs.
set -euo pipefail
cd "$(dirname "$0")"
# QUICK=1 bash run_all.sh  -> a 2-minute smoke test (one short run of each step; not for the paper)
QUICK=${QUICK:-0}
RUNS="1 2 3"; CHAINS="1 2 3 4 6 8 10 12 16"; THREADS="1 3 6 12"
if [ "$QUICK" = 1 ]; then RUNS="1"; CHAINS="1 4"; THREADS="1"; fi
STAMP=$(date +%Y%m%d-%H%M)
R="results-$STAMP"; mkdir -p "$R"
log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$R/run.log"; }

for t in gcc g++ python3 zip; do command -v $t >/dev/null || { echo "Missing $t. Run: sudo apt update && sudo apt install -y build-essential python3 zip"; exit 1; }; done

log "1/8 system information"
bash sysinfo.sh "$R/sysinfo.txt"

log "2/8 building"
gcc -O2 -o bin_latency latency.c
gcc -O3 -march=native -fopenmp -o bin_bandwidth bandwidth.c
gcc -O2 -pthread -o bin_c2c c2c.c
gcc -O1 -o bin_clock clock.c
g++ -O2 -std=c++17 -o model/cachesim model/cachesim.cpp

log "3/8 clock estimate (before)"
./bin_clock --cpu 0 > "$R/clock-before.csv"; cat "$R/clock-before.csv" | tee -a "$R/run.log"

log "4/8 latency sweeps: 3 runs with 4 KB pages, 3 with 2 MB pages (a few minutes)"
for i in $RUNS; do
  if [ "$QUICK" = 1 ]; then (./bin_latency --cpu 0 || true) | head -30 > "$R/latency-4k-run$i.csv" || true; continue; fi
  ./bin_latency --cpu 0        > "$R/latency-4k-run$i.csv"
  ./bin_latency --cpu 0 --huge > "$R/latency-2m-run$i.csv"
  log "   run $i done"
done

log "5/8 memory-level parallelism: independent chains in DRAM (1 GiB) and in L3 (16 MiB)"
echo "chains,size_mib,ns_per_load,ns_per_step,run" > "$R/mlp.csv"
for run in $RUNS; do
  for size in 1024 16; do
    for k in $CHAINS; do
      ./bin_latency --cpu 0 --huge --chains $k --size-mib $size | tail -1 | sed "s/$/,$run/" >> "$R/mlp.csv"
    done
  done
done

log "6/8 bandwidth with 1, 3, 6 and 12 threads"
echo "threads,kernel,bytes_per_array_kib,gb_per_s" > "$R/bandwidth.csv"
for t in $THREADS; do [ "$t" -le "$(nproc)" ] || continue; ./bin_bandwidth --threads $t | tail -n +2 >> "$R/bandwidth.csv"; log "   $t threads done"; done

log "7/8 core-to-core round trips for every pair of logical CPUs"
if [ "$QUICK" = 1 ]; then echo "skipped in QUICK mode" > "$R/c2c.csv"; else ./bin_c2c > "$R/c2c.csv"; fi

log "8/8 clock estimate (after) and model prediction"
./bin_clock --cpu 0 > "$R/clock-after.csv"; cat "$R/clock-after.csv" | tee -a "$R/run.log"
GHZ=$(tail -1 "$R/clock-after.csv" | cut -d, -f2)
python3 model/model_sweep.py --bin model/cachesim --ghz "$GHZ" --out "$R/model-latency.csv"

cp NOTES-TEMPLATE.md "$R/notes.md"
zip -qr "ELL305-5600X-$STAMP.zip" "$R"
log "Done. Fill in $R/notes.md, then re-zip with:  zip -qr ELL305-5600X-$STAMP.zip $R"
log "Send ELL305-5600X-$STAMP.zip back (or copy it into research/measurements/5600X/ in the project)."
