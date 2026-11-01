"""Gordan Band II English: split the German source into page chunks, and check an English chunk against its German.

  python chunks.py split GERMAN.tex OUTDIR A-B [A-B ...]
      writes OUTDIR/de_A_B.tex: the German body from \\weberpage{A} up to \\weberpage{B+1} (or \\end{document}).
  python chunks.py check DE_CHUNK EN_CHUNK
      compares the mathematics: the sequence of formulas ($...$, $$...$$, \\[...\\], \\(...\\), \\weq{..}{..} and display
      environments) must be identical in both, except the words inside \\text{...}/\\mbox{...}, which are translated.
      Also: the same \\weberpage marks in the same order, balanced braces, no German left outside formulas (rough check
      on frequent German function words). Prints the first differences and a summary line.
"""
import re
import sys

MATH = re.compile(
    r"\$\$.*?\$\$|\$(?:\\\$|[^$])+?\$|\\\[.*?\\\]|\\\(.*?\\\)"
    r"|\\begin\{(equation\*?|align\*?|aligned|gather\*?|multline\*?|eqnarray\*?|array|vmatrix|matrix|pmatrix|cases)\}.*?\\end\{\1\}",
    re.S)
WEQ = re.compile(r"\\weq\{([^{}]*)\}\{")
GERMAN = re.compile(r"\b(und|der|die|das|wir|ist|sind|nicht|welche|welcher|eine|einer|durch|wenn|so|auch|aber|"
                    r"oder|dass|nach|wird|werden|haben|mit|von|für|über|bei|aus|zu)\b")


def body(t):
    t = re.sub(r"(?<!\\)%[^\n]*", "", t)
    return t


def weq_blocks(t):
    """the second argument of every \\weq{label}{...} (balanced braces)"""
    out = []
    for m in WEQ.finditer(t):
        i, d = m.end(), 1
        while i < len(t) and d:
            d += {"{": 1, "}": -1}.get(t[i], 0) if t[i - 1] != "\\" else 0
            i += 1
        out.append((m.start(), "WEQ{%s}{%s}" % (m.group(1), t[m.end():i - 1])))
    return out


def formulas(t):
    t = body(t)
    items = [(m.start(), m.group(0)) for m in MATH.finditer(t)]
    items += weq_blocks(t)
    items.sort()
    out = []
    for _, f in items:
        f = re.sub(r"\\(text|mbox|textrm|textit|hbox)\s*\{[^{}]*\}", r"\\\1{}", f)
        f = re.sub(r"\s+", "", f)
        out.append(f)
    return out


def balanced(s):
    s = re.sub(r"\\[{}]", "", body(s))
    d = 0
    for ch in s:
        d += ch == "{"
        d -= ch == "}"
        if d < 0:
            return False
    return d == 0


if sys.argv[1] == "split":
    src, outdir = sys.argv[2], sys.argv[3]
    t = open(src, encoding="utf-8", newline="").read()
    for rng in sys.argv[4:]:
        a, b = (int(x) for x in rng.split("-"))
        s = t.index("\\weberpage{%d}" % a)
        s = t.rfind("\n", 0, t.rfind("% !PRINTED", 0, s) if t.rfind("% !PRINTED", 0, s) > s - 400 else s) + 1
        nxt = t.find("\\weberpage{%d}" % (b + 1))
        if nxt < 0:
            e = t.index("\\end{document}")
        else:
            p = t.rfind("% !PRINTED", 0, nxt)
            e = t.rfind("\n", 0, p if p > nxt - 400 else nxt) + 1
        open("%s/de_%03d_%03d.tex" % (outdir, a, b), "w", encoding="utf-8", newline="").write(t[s:e])
        print("de_%03d_%03d.tex" % (a, b), e - s, "chars")
elif sys.argv[1] == "check":
    de = open(sys.argv[2], encoding="utf-8").read()
    en = open(sys.argv[3], encoding="utf-8").read()
    fd, fe = formulas(de), formulas(en)
    pd = re.findall(r"\\weberpage\{(\d+)\}", de)
    pe = re.findall(r"\\weberpage\{(\d+)\}", en)
    diffs = 0
    for k in range(max(len(fd), len(fe))):
        a = fd[k] if k < len(fd) else None
        b = fe[k] if k < len(fe) else None
        if a != b:
            diffs += 1
            if diffs <= 12:
                print("formula %d differs:\n   de: %s\n   en: %s" % (k + 1, (a or "-")[:300], (b or "-")[:300]))
    prose = re.sub(MATH, " ", body(en))
    ger = GERMAN.findall(prose)
    print("formulas de %d en %d, differing %d | pages %s | braces %s | German function words in English prose: %d"
          % (len(fd), len(fe), diffs, "same" if pd == pe else "DIFFER", "ok" if balanced(en) else "UNBALANCED",
             len(ger)))
