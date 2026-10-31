#!/usr/bin/env bash
# Builds the active milestone (whichever "Draft N" paper/main.tex selects) in
# Claude's Linux workspace, or the working full-paper draft (draft-initial/,
# entry point paper/main-draft-initial.tex) with --draft-initial, or the second
# working draft (initial-draft-2/, paper/main-initial-draft-2.tex) with --initial-draft-2.
# Mirrors scripts/build.ps1:
#   pdflatex -> biber -> makeglossaries -> makeindex -> pdflatex x2
#
# Usage: scripts/build-linux.sh [all|1|2|3] [--install] [--draft-initial|--initial-draft-2]
#   1 = first pass, 2 = bibliography/glossary/index, 3 = two final passes.
#   Each workspace command is capped at ~3 minutes; run the steps separately
#   if "all" would exceed that (e.g. on the first build of a session).
#   --install copies the finished PDF to build/pdf/ELL305-<draft>.pdf
#   (a tracked file); without it, output stays in tmp/linux-build/.
#   --draft-initial builds paper/main-draft-initial.tex instead of the active
#   milestone, in its own work directory, so the two never share aux files.
#
# Why the extra machinery:
# - Lookups through the shared Windows folder are very slow, so the add-ons in
#   tmp/texlive are copied to local disk ($HOME/tl-local) once per session and
#   the build runs in $HOME/linux-build; results are copied back.
# - The workspace's LaTeX core (2022) lacks \IfDocumentMetadata*, which
#   biblatex 3.21 calls. They are defined on the command line only; the
#   manuscript source is not changed. (Correct because the report never
#   declares \DocumentMetadata.)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
T="$ROOT/tmp/texlive"; L="$HOME/tl-local"; W="$HOME/linux-build"; OUT="$ROOT/tmp/linux-build"
STEP=all; INSTALL=0; TARGET=active
for a in "$@"; do case "$a" in --install) INSTALL=1;; --draft-initial) TARGET=draft-initial;; --initial-draft-2) TARGET=initial-draft-2;; all|1|2|3) STEP=$a;; *) echo "Unknown argument: $a"; exit 2;; esac; done
if [[ $TARGET == draft-initial || $TARGET == initial-draft-2 ]]; then
  JOB=main-$TARGET; DRAFT=$TARGET; W="$HOME/linux-build-$TARGET"
  [[ -f "$ROOT/paper/$JOB.tex" ]] || { echo "Missing paper/$JOB.tex"; exit 1; }
else
  JOB=main
  DRAFT="$(grep -v '^\s*%' "$ROOT/paper/main.tex" | grep -oE '\\input\{"\.\./Draft [0-9]' | head -1 | grep -oE 'Draft [0-9]')"
  [[ -n "$DRAFT" ]] || { echo "Could not find the active Draft in paper/main.tex"; exit 1; }
fi
[[ -x "$T/bin/x86_64-linux/biber" ]] || { echo "TeX add-ons missing: run scripts/setup-linux-tex.sh first"; exit 1; }

if [[ ! -f "$L/.ready" ]]; then
  echo "Preparing local TeX cache (once per session)..."
  rm -rf "$L"; mkdir -p "$L"
  cp -r "$T/texmf" "$T/bin" "$L/"
  export TEXMFHOME="$L/texmf" TEXMFVAR="$L/texmf-var" TEXMFCONFIG="$L/texmf-config"
  mktexlsr "$L/texmf" > /dev/null 2>&1
  updmap-user --quiet --nomkmap --enable Map=newtx.map > /dev/null 2>&1
  updmap-user --quiet --enable Map=txfonts.map > /dev/null 2>&1
  touch "$L/.ready"
fi
export TEXMFHOME="$L/texmf" TEXMFVAR="$L/texmf-var" TEXMFCONFIG="$L/texmf-config" PATH="$L/bin/x86_64-linux:$PATH"
mkdir -p "$W" "$OUT"; cd "$ROOT/paper"

pass() {
  pdflatex -interaction=nonstopmode -file-line-error -synctex=1 -output-directory="$W" -jobname=$JOB \
    "\providecommand\IfDocumentMetadataTF[2]{#2}\providecommand\IfDocumentMetadataT[1]{}\providecommand\IfDocumentMetadataF[1]{#1}\input{$JOB.tex}" \
    > "$W/pass.log" 2>&1 || { echo "LaTeX failed:"; grep -E '^[^:]+:[0-9]+:|^!' "$W/$JOB.log" | head -20; exit 1; }
}
if [[ $STEP == all || $STEP == 1 ]]; then pass; echo "[$DRAFT] pass 1 ok"; fi
if [[ $STEP == all || $STEP == 2 ]]; then
  biber --input-directory "$W" --output-directory "$W" $JOB > "$W/biber.out" 2>&1 || { tail -20 "$W/biber.out"; exit 1; }
  echo "biber ok"
  (cd "$W" && makeglossaries $JOB > glossaries.out 2>&1) || { tail -10 "$W/glossaries.out"; exit 1; }
  echo "glossary ok"
  (cd "$W" && makeindex $JOB.idx > index.out 2>&1) || { tail -10 "$W/index.out"; exit 1; }
  echo "index ok"
fi
if [[ $STEP == all || $STEP == 3 ]]; then
  pass; pass; echo "final passes ok"
  cp "$W/$JOB.pdf" "$OUT/ELL305-${DRAFT// /-}.pdf"
  cp "$W"/$JOB.{log,blg,glg,ilg} "$OUT"/ 2>/dev/null || true
  echo "--- log check ---"
  echo "errors: $(grep -cE '^[^:]+:[0-9]+:|^!' "$W/$JOB.log" || true)"
  grep -E 'LaTeX Warning|Package .* Warning|Overfull|Underfull|undefined' "$W/$JOB.log" | sort | uniq -c || echo "no warnings, bad boxes or undefined references"
  grep -E 'WARN|ERROR' "$W/$JOB.blg" || echo "biber: clean"
  pdfinfo "$W/$JOB.pdf" | grep -E 'Pages|Page size'
  echo "Output: tmp/linux-build/ELL305-${DRAFT// /-}.pdf"
  if [[ $INSTALL == 1 ]]; then cp "$W/$JOB.pdf" "$ROOT/build/pdf/ELL305-${DRAFT// /-}.pdf"; echo "Installed: build/pdf/ELL305-${DRAFT// /-}.pdf"; fi
fi
