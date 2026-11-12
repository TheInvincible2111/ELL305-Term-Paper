#!/usr/bin/env python3
"""Flatten the modular initial-draft-2 sources into one self-contained .tex for submission.

Course rule: exactly two files (one .tex, one PDF). Every \\input is inlined, the
bibliography is embedded with filecontents*, and full-line comments are dropped
(except inside filecontents* blocks, whose content must stay byte-for-byte).
Usage: python3 scripts/flatten-initial-draft-2.py OUT.tex
Edit the modular files as usual; rerun this script to regenerate the submission file.
"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
PAPER = ROOT / 'paper'
BIBNAME = 'ELL305-term-paper-references.bib'
INPUT = re.compile(r'\\input\{"?([^"}]+?)"?\}')

def resolve(name):
    p = (PAPER / name)
    if not p.suffix: p = p.with_suffix('.tex')
    return p.resolve()

def expand(path, seen=()):
    text = path.read_text(encoding='utf-8')
    out = []
    in_fc = False
    for line in text.splitlines():
        if line.lstrip().startswith('\\begin{filecontents'): in_fc = True
        if in_fc:
            out.append(line)
            if line.lstrip().startswith('\\end{filecontents'): in_fc = False
            continue
        if line.lstrip().startswith('%'):
            continue
        m = INPUT.search(line)
        if m and not line.lstrip().startswith('%'):
            target = resolve(m.group(1))
            if target in seen: raise SystemExit(f'cycle at {target}')
            before, after = line[:m.start()], line[m.end():]
            if before.strip(): out.append(before)
            out.append(expand(target, seen + (target,)))
            if after.strip(): out.append(after)
            continue
        out.append(line)
    return '\n'.join(out)

body = expand(PAPER / 'main-initial-draft-2.tex')
body = body.replace('\\addbibresource{../references/references.bib}', '\\addbibresource{' + BIBNAME + '}')
assert BIBNAME in body, 'bibliography resource not found'
bib = (ROOT / 'references' / 'references.bib').read_text(encoding='utf-8')
head = ('% ELL305 Computer Architecture term paper: single self-contained source.\n'
        '% Compile: pdflatex, biber, makeglossaries, pdflatex x2, makeglossaries, makeindex, pdflatex x2;\n'
        '% Overleaf and latexmk do this automatically.\n'
        '\\begin{filecontents*}[overwrite]{' + BIBNAME + '}\n' + bib.rstrip('\n') + '\n\\end{filecontents*}\n')
out = head + body + '\n'
left = INPUT.findall(out)
assert not left, f'unexpanded inputs: {left}'
pathlib.Path(sys.argv[1]).write_text(out, encoding='utf-8', newline='\n')
print(f'wrote {sys.argv[1]} ({len(out)//1024} KB)')
