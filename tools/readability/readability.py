"""Readability indices for the main text of an ELL305 draft.

Usage:  python readability.py <draft-folder> [--dump plain.txt]

Reads sections/part*.tex in order, strips LaTeX to running prose and prints
the indices computed by the textstat library (version pinned in
requirements.txt). What is removed:

  * comments, \\input lines, headings, labels, index entries, citations and
    cross-references;
  * floats and display material (table, figure, tabular(x), equation, align,
    tikzpicture, lstlisting): their text is not running prose;
  * inline math, which is replaced by the single word "value" so that the
    sentence around it stays intact.

Formatting commands (\\emph, \\textbf, \\gls, ...) keep their text. List items
that do not end in punctuation are closed with a full stop so that they are
counted as sentences rather than merged into the next one.
"""
import glob
import os
import re
import statistics
import sys

import textstat

DROP_ENVS = r"table|table\*|figure|figure\*|tabular|tabularx|equation|equation\*|align|align\*|tikzpicture|lstlisting"


def strip_latex(t: str) -> str:
    t = re.sub(r"(?<!\\)%.*", "", t)                                   # comments
    t = re.sub(r"\\begin\{(" + DROP_ENVS + r")\}.*?\\end\{\1\}", " ", t, flags=re.S)
    t = re.sub(r"\\\[.*?\\\]", " ", t, flags=re.S)                     # display math
    t = re.sub(r"\$[^$]*\$", "value", t)                               # inline math
    t = re.sub(r"\\(input|label|index|clearpage|phantomsection|noindent)\b(\{[^}]*\})?", " ", t)
    t = re.sub(r"\\(part|section|subsection|subsubsection|paragraph)\*?\{[^}]*\}", " ", t)
    t = re.sub(r"\\[cC]ref\{[^}]*\}", "it", t)
    t = re.sub(r"\\(cite|ref|eqref|autoref|pageref)(\[[^\]]*\])*\{[^}]*\}", "", t)
    t = re.sub(r"\\(href)\{[^}]*\}", "", t)
    t = re.sub(r"\\(gls|glspl|Gls|Glspl)\{([^}]*)\}", lambda m: m.group(2).replace("-", " "), t)
    t = re.sub(r"\\item\[([^\]]*)\]", r"\n\1. ", t)
    t = re.sub(r"\\item\b", "\n", t)
    t = re.sub(r"\\(begin|end)\{[^}]*\}(\[[^\]]*\])*", "\n", t)
    t = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", t)                 # remaining commands
    t = t.replace("~", " ").replace("\\,", " ").replace("``", '"').replace("''", '"')
    t = re.sub(r"[{}\\]", " ", t)
    t = t.replace("et al.", "et al").replace("e.g.", "eg").replace("i.e.", "ie")
    # close list items / lines that end without punctuation so they count as sentences
    lines = []
    for para in re.split(r"\n\s*\n|\n(?=\s*\S)", t):
        p = " ".join(para.split())
        if p and len(p.split()) > 3 and p[-1] not in ".?!:;":
            p += "."
        if p:
            lines.append(p)
    return "\n".join(lines)


def main() -> None:
    draft = sys.argv[1]
    files = sorted(glob.glob(os.path.join(draft, "sections", "part*.tex")))
    text = "\n".join(strip_latex(open(f, encoding="utf8").read()) for f in files)
    if "--dump" in sys.argv:
        open(sys.argv[sys.argv.index("--dump") + 1], "w", encoding="utf8").write(text)
    grades = {
        "Gunning Fog": textstat.gunning_fog(text),
        "Flesch--Kincaid Grade Level": textstat.flesch_kincaid_grade(text),
        "SMOG": textstat.smog_index(text),
        "Coleman--Liau": textstat.coleman_liau_index(text),
        "Automated Readability Index": textstat.automated_readability_index(text),
    }
    print("files:", ", ".join(os.path.basename(f) for f in files))
    print("words:", textstat.lexicon_count(text), " sentences:", textstat.sentence_count(text))
    print("Flesch Reading Ease:", textstat.flesch_reading_ease(text))
    for k, v in grades.items():
        print(f"{k}: {v:.2f}")
    vals = list(grades.values())
    print(f"Average grade level: {statistics.mean(vals):.2f}")
    print(f"Median grade level: {statistics.median(vals):.2f}")


if __name__ == "__main__":
    main()
