# ELL305 — Ryzen 5 5600X measurement kit

This kit measures the real cache hierarchy of a Ryzen 5 5600X (Zen 3: one CCD, 6 cores,
32 MB L3) so the term paper can check its software model against real hardware. It runs on
the 5600X machine and produces one zip file of results to bring back.

Total time: about 20 minutes, of which about 10 are unattended (the 8 November run took 9 minutes).

## What you need

- The 5600X PC with Windows 10 or 11 (or native Linux, see the end).
- About 2 GB of free RAM and 100 MB of disk space.
- Internet access once, to install the compiler.

## Before you start

- Plug in, set the Windows power plan to *Balanced* or *High performance*, and close games,
  browsers and anything else heavy. Don't use the PC while the tests run.
- Open CPU-Z (free) → *Memory* tab and note the RAM speed, timings and the fabric clock.
  You will type these into `notes.md` at the end.

## Steps

1. **Install WSL with Ubuntu** (skip if `wsl` already works). In an administrator PowerShell:
   `wsl --install -d Ubuntu` → reboot → open *Ubuntu* from the Start menu and create a user.
2. **Copy this zip** to the PC and extract it to `C:\ELL305-kit` (so this README is at
   `C:\ELL305-kit\ELL305-5600X-kit\README.md`).
3. **Open Ubuntu** and run:
   ```bash
   sudo apt update && sudo apt install -y build-essential python3 zip
   cd /mnt/c/ELL305-kit/ELL305-5600X-kit
   QUICK=1 bash run_all.sh        # 1-minute smoke test; check it ends with "Done."
   bash run_all.sh                # the real run, about 10 minutes
   ```
4. **Fill in** `results-<date>/notes.md` (open it in Notepad from `C:\ELL305-kit\...`), then
   re-zip as the last line of the run tells you.
5. **Send back** `ELL305-5600X-<date>.zip` (the one from the real run, not the QUICK one).
   On the main PC it goes into `research/measurements/5600X/` in the project folder.
6. *Optional:* `uprof-windows.md` explains a 10-minute AMD uProf run on Windows that adds real
   L1/L2/L3 miss rates. Put its CSV into the results folder before zipping.

## What the tests measure, and where they go in the paper

| Test | Output | What it shows | Used for |
|---|---|---|---|
| Clock estimate | `clock-before.csv`, `clock-after.csv` | Core clock from a chain of dependent adds | Converting ns to cycles |
| Latency sweep, 4 KB and 2 MB pages, 3 runs each | `latency-*.csv` | L1, L2, L3 and DRAM latency; TLB effect (4 KB vs 2 MB) | Comparison with the model (S0); Part II TLB-reach example |
| Memory-level parallelism, 1–16 chains | `mlp.csv` | How many misses the core overlaps, in DRAM and in L3 | Plausibility check of the fitted overlap factors (not used to fit them); Part II sec:mlp |
| Bandwidth, 1/3/6/12 threads | `bandwidth.csv` | L1/L2/L3/DRAM bandwidth by buffer size | S6 bandwidth limits |
| Core-to-core round trips, all pairs | `c2c.csv` | Sharing cost within one CCD (and between SMT siblings) | Part III sec:cross-ccd (same-CCD value) |
| Model prediction | `model-latency.csv` | The paper's model with this machine's clock | Side-by-side with the measured sweep |
| System information | `sysinfo.txt` | CPU, OS, WSL, huge-page setting, address sizes | Conditions of the measurement |

## Troubleshooting

- `$'\r': command not found` → the scripts got Windows line endings. Run
  `sed -i 's/\r$//' *.sh` in the kit folder and start again.
- `sched_setaffinity` warnings → harmless; note them in `notes.md`.
- In `sysinfo.txt`, if `transparent_hugepage` shows `[never]`, the 2 MB-page runs fall back to
  4 KB pages. That's fine; just mention it.
- WSL2 is a light virtual machine. Its nested address translation can add to the L3 and memory
  latencies, and CPU pinning inside it does not fix the physical core. Native Linux, if available,
  gives the cleanest numbers.

## Native Linux instead of WSL

Same commands, from wherever you extracted the kit:
`sudo apt install -y build-essential python3 zip && bash run_all.sh`.

## Files

`latency.c`, `bandwidth.c`, `c2c.c`, `clock.c`: the measurement programs, each with a comment
at the top explaining the method. `model/`: the paper's cache simulator and the script that runs
it with this machine's clock. `run_all.sh`: runs everything in order and zips the results.
