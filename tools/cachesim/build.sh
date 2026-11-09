#!/usr/bin/env bash
# Build and test the cache simulator.  Usage: ./build.sh [test|gui]
set -euo pipefail
cd "$(dirname "$0")"
g++ -O2 -std=c++17 -Wall -Wextra -o cachesim src/cachesim.cpp
echo "built ./cachesim"
case "${1:-}" in
  test) ./cachesim --selftest; node test/crosscheck.js ./cachesim ;;
  gui)  python3 gui/build.py ;;
esac
