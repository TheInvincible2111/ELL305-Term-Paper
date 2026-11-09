# Optional: cache miss rates with AMD uProf on Windows (about 10 minutes)

This step gives real L1/L2/L3 miss rates and IPC. It runs on Windows, not in WSL.

1. Install AMD uProf for Windows from AMD's website (free).
2. Open an administrator Command Prompt in the uProf `bin` folder.
3. Check what your version supports: `AMDuProfPcm -h`
   (Lawenda et al. used AMDuProfPcm with the metric groups ipc, l1, l2, l3, tlb.)
4. Install 7-Zip if needed, then run its benchmark under uProf, single-threaded, for example:
   `AMDuProfPcm -m ipc,l1,l2,l3 -c core=0 -o C:\ELL305\uprof-7zip.csv -- "C:\Program Files\7-Zip\7z.exe" b -mmt1`
   The exact flags differ between versions: follow `-h`, and write the command you used in notes.md.
5. Put the CSV into the results folder before zipping.
