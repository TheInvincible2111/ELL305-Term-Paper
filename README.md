# ELL305 term-paper workspace

This folder is the editable home for the paper. Codex can edit, build, and inspect files here in future tasks.

## Where things go

- `paper/` - LaTeX manuscript, chapters, and figures
- `notes/` - Obsidian vault (open this folder as the vault)
- `references/references.bib` - bibliography exported from Zotero
- `research/pdfs/` - local-only research papers (shared through Zotero, not GitHub)
- `diagrams/` - editable TikZ, Mermaid, Graphviz, and WaveDrom sources
- `build/pdf/` - finished PDF
- `build/aux/` - temporary LaTeX files
- `submissions/` - verified milestone submission bundles and consolidated sources
- `imports/draft-1/` - safe landing area for the existing Draft 1 files
- `sources/` - local-only, read-only material synced from the ChatGPT project

Research papers and the course textbook are intentionally excluded from GitHub. Group members should obtain shared source material through the private Zotero group library or the course's authorized distribution channel.

## One-time setup on Windows

1. Install **MiKTeX** (recommended) or TeX Live. During MiKTeX setup, allow missing packages to be installed automatically.
2. Restart VS Code/Codex so `latexmk`, `pdflatex`, `biber`, and `bibtex` are on `PATH`.
3. In VS Code, install the **LaTeX Workshop** extension.
4. Open this whole folder in Codex/VS Code. Open `notes/` separately in Obsidian as a vault.
5. In Zotero, install Better BibTeX if desired and set an automatic export to `references/references.bib` using BibLaTeX format.

## Build

From VS Code, run **Terminal > Run Build Task**. From PowerShell:

```powershell
.\scripts\build.ps1
```

The active output is `build/pdf/ELL305-Draft-1.pdf`. Clean temporary files with:

```powershell
.\scripts\clean.ps1
```

Create the reproducible Draft 1 submission folder and ZIP with:

```powershell
.\scripts\package-draft1.ps1
```

The build uses `latexmk` when Perl is available. With a standard MiKTeX installation and no Perl, it automatically runs the equivalent `pdflatex`, `biber`, and repeat-pass sequence. After compilation, future Codex tasks can render the PDF to images and visually inspect pages for overflow, broken figures, and layout defects once Poppler (`pdftoppm`) is installed.

## Draft 1

The active milestone is stored in `Draft 1/` as independent metadata, front-matter, section, and figure modules. `paper/main.tex` is the thin build wrapper. The verified output is `build/pdf/ELL305-Draft-1.pdf`.

Future milestone versions should use sibling folders named `Draft 2/`, `Draft 3/`, and `Draft 4/`. See `DRAFTS.md` for the versioning convention.

## Collaboration and publishing

The local folder is the working copy. GitHub is the shared, published copy for the project group.

- Edit, compile, and inspect changes locally first.
- Commit and push only when Ishan explicitly says **“publish the latest version.”**
- Keep `main` in a buildable state.
- Do not commit research-paper or textbook PDFs. Share those through the private Zotero group library.
- Do not commit personal Obsidian workspace state or temporary LaTeX build files.
- The compiled milestone PDF in `build/pdf/` may be committed so group members can read it without building LaTeX.

## Useful future instructions

- “Compile the paper, fix any LaTeX errors, and inspect the changed pages.”
- “Use my notes in `notes/Papers/` to expand chapter 5, but add no unsupported claims.”
- “Import Draft 1 from `imports/draft-1/`, preserving the original files.”
- “Add these Zotero citations to the literature review and rebuild the bibliography.”
