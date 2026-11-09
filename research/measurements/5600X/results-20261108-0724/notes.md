# Notes for this measurement run

- Date and time: 8 November 2026; run started 07:24 UTC (12:54 IST), finished 07:33 UTC
- Who ran it: the group (on the 5600X PC; host name IshanKaPC)
- Machine: Ryzen 5 5600X; motherboard: MSI B550 Gaming Edge WiFi
- BIOS: PBO enabled; no Curve Optimizer and no other overclock
- RAM: DDR4-3200 (1600 MHz memory clock); timings as reported: "1:16, 16, 20, 20, 40, 73, 1T"
  (read as CL16-20-20-40, tRC 73, command rate 1T; the "1:16" entry is recorded as given); size: 32 GB DDR4
- Infinity Fabric clock (FCLK): 1600 MHz (1:1 with the memory clock)
- Windows power plan: High performance
- Cooler: DeepCool AS500
- Running under WSL2 or native Linux: WSL2 (kernel 6.6.114.1-microsoft-standard-WSL2; transparent huge pages = madvise)
- Anything else running at the time: nothing deliberately; possibly ordinary Windows background processes
- Core clock seen in Task Manager during the latency runs: 4.6 GHz (the kit's estimate: 4.614 GHz before and after)
- Anything unusual: 2 MB-page latency run 3 is slower than runs 1–2 from about 19 MB upwards (huge pages
  probably only partly granted); medians of the three runs are used. 12-thread bandwidth values below
  about 32 MB are erratic (see ANALYSIS.md).
