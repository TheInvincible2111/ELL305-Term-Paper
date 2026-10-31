#!/usr/bin/env bash
# One-time (idempotent) setup of the TeX add-ons needed to build the report in
# Claude's Linux workspace on Ishan's computer. Windows builds use MiKTeX via
# build.ps1 and do not need this.
#
# The workspace ships TeX Live 2022, which lacks biblatex/biber and the newtx
# fonts. This downloads only those packages from a fixed CTAN mirror into
# tmp/texlive/ (gitignored), so they persist between sessions.
# Requires network access to mirrors.mit.edu (Claude Settings > Capabilities).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
T="$ROOT/tmp/texlive"
MIRROR="https://mirrors.mit.edu/CTAN/systems/texlive/tlnet/archive"
PKGS=(biblatex biblatex-ieee newtx txfonts logreq)
BINPKGS=(biber.x86_64-linux)
mkdir -p "$T/dl" "$T/texmf"
for p in "${PKGS[@]}" "${BINPKGS[@]}"; do
  if [[ ! -s "$T/dl/$p.tar.xz" ]]; then
    echo "Downloading $p"
    curl -fsS -m 170 -o "$T/dl/$p.tar.xz" "$MIRROR/$p.tar.xz"
  fi
done
# Extract each archive once; a marker avoids overwriting (which the shared
# folder refuses without delete permission).
for p in "${PKGS[@]}"; do
  [[ -f "$T/dl/$p.extracted" ]] || { tar -xJf "$T/dl/$p.tar.xz" -C "$T/texmf" && touch "$T/dl/$p.extracted"; }
done
for p in "${BINPKGS[@]}"; do
  [[ -f "$T/dl/$p.extracted" ]] || { tar -xJf "$T/dl/$p.tar.xz" -C "$T" && touch "$T/dl/$p.extracted"; }
done
"$T/bin/x86_64-linux/biber" --version
echo "TeX add-ons ready in tmp/texlive. Run scripts/build-linux.sh next."
