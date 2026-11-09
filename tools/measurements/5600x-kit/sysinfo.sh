#!/usr/bin/env bash
# Records the machine, OS and memory settings that every result depends on.
out="$1"
{
  echo "date: $(date -Is)"
  echo "uname: $(uname -a)"
  echo "wsl: $(grep -qi microsoft /proc/version && echo yes || echo no)"
  echo "transparent_hugepage: $(cat /sys/kernel/mm/transparent_hugepage/enabled 2>/dev/null)"
  echo "nproc: $(nproc)"
  echo; echo "== lscpu =="; lscpu
  echo; echo "== address sizes =="; grep -m1 "address sizes" /proc/cpuinfo
  echo; echo "== memory =="; free -h
  echo; echo "== compiler =="; gcc --version | head -1
} > "$out" 2>&1
