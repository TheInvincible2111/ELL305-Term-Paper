---
draft: 1
date: 2026-08-24
status: implemented
tags: [draft-1, latex, single-file, validation]
---

# Phase 5 single-file validation

The modular project remains the authoritative editing form. A validation-only workflow generates one consolidated LaTeX source under `../../../build/single-file-validation/` and compiles it independently with bibliography, glossary, index, TikZ figures, and project-local image assets.

The validation command is `../../../scripts/validate-single-file.ps1`.

This workflow does not write to the tracked submission package, does not create a ZIP, and does not publish anything. The actual submission package remains gated until explicitly requested.
