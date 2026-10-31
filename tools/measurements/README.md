# 5600X measurements (optional original data for the term paper)

Two measurements on Ishan's Ryzen 5 5600X (Zen 3, one CCD, 6 cores, 32 MB L3).
Save every output into `research/measurements/` exactly as produced — do not edit numbers by hand.
Before each run: plug in / normal power plan, close games, browsers and other heavy programs.

## 1. Latency sweep (WSL, about 2 minutes per run)

In a WSL Ubuntu terminal, from the project folder:

```bash
sudo apt install -y build-essential             # once
cd /mnt/c/Users/ishan/Documents/ELL305-Term-Paper
mkdir -p research/measurements
gcc -O2 -o /tmp/latency tools/measurements/latency.c
lscpu > research/measurements/5600X-lscpu.txt
/tmp/latency        > research/measurements/5600X-latency-4k.csv
/tmp/latency --huge > research/measurements/5600X-latency-2m.csv
```

While a run is going, note the CPU speed shown in Task Manager → Performance → CPU
(or HWiNFO "Core 0 clock") in `research/measurements/notes.md`, together with the date,
RAM speed and timings (shown in Task Manager → Memory, or CPU-Z → Memory).
The clock lets us convert nanoseconds to cycles.

What it shows: steps at 32 KB (L1), 512 KB (L2) and 32 MB (L3), then main memory.
The `--huge` run reduces TLB effects so the cache steps are cleaner.
Caveat to state in the paper: WSL2 is a lightweight virtual machine, which can add a little
to memory latency; the cache levels themselves are unaffected.

## 2. Cache miss rates with AMD uProf (Windows, about 10 minutes)

1. Install **AMD uProf** for Windows from AMD's website (free).
2. Open an *administrator* Command Prompt in the uProf `bin` folder.
3. Check the options your version supports: `AMDuProfPcm -h`
   (Lawenda et al. used AMDuProfPcm with the metric groups `ipc, l1, l2, l3, tlb`.)
4. Run the 7-Zip benchmark under it, single-threaded, for example
   `AMDuProfPcm -m ipc,l1,l2,l3 -c core=0 -o C:\Users\ishan\Documents\ELL305-Term-Paper\research\measurements\5600X-uprof-7zip.csv -- "C:\Program Files\7-Zip\7z.exe" b -mmt1`
   The exact flags may differ by version — follow `-h`, and save the command you actually used in `notes.md`.

This gives real L1/L2/L3 miss rates and IPC to replace the assumed 5% / 30% / 40% in the
Part II worked example, and a 7-Zip result to compare with Lam's 7950X3D measurements.
