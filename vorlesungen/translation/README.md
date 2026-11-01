# Help translate Gordan's *Vorlesungen über Invariantentheorie* with your own Claude

Most of Gordan's lectures (vol. I from p. 29, and all of vol. II) exist here only in German. If you have Claude credits
you are not using, one part of about 20 printed pages can be translated into English with a single prompt: Claude
downloads the German LaTeX and the material it needs from this repository, translates, checks its work against the
scans of the printed book, and gives you a zip with the English LaTeX to send back. You do not need to do anything
else.

## What to do

1. Open Claude Code in an empty folder (best: it can download, run its checks and make the zip), or a new chat on
   claude.ai. Choose the most capable model and the highest effort setting.
2. Paste the prompt below. Replace the part name if you were given a different one; [STATUS.md](STATUS.md) lists all
   parts.
3. When Claude is done, send the zip it made to the person who sent you here (WhatsApp is fine).

If Claude Code asks for permission to download or run something, you can answer "Yes, and don't ask again": the
prompt allows downloads from github.com, gdz.sub.uni-goettingen.de, archive.org and gutenberg.org, and running Python
and LaTeX on the downloaded files.

## The prompt

```text
Please translate one part of Paul Gordan's "Vorlesungen über Invariantentheorie" (1885/1887, public domain) from
German into English LaTeX for the open edition at https://github.com/KokunoYumeto/paul-gordan.

Your part: band2_de_001_020.tex (vol. II, printed pages 1-20).

Read and follow the instructions at
https://raw.githubusercontent.com/KokunoYumeto/paul-gordan/main/vorlesungen/translation/INSTRUCTIONS.md
They give the German source, the glossary, earlier English parts as a style model, standard English books on the
subject to compare terminology with, the scans of the printed book for spot checks, the checks to run and the
deliverable.

I allow you to download every file linked in those instructions and to create files, run Python, LaTeX and zip in
this folder, without asking me each time. Use your highest effort setting. Work through to the end on your own; when
you are done, give me one zip file with the English LaTeX and your notes, and tell me where it is. Open a GitHub pull
request only if GitHub is already set up on this computer; otherwise the zip is all I need.
```

## Credit and licence

Helpers are credited by the name they choose (a person, a company, or nothing) in the main README, for example:
"English of vol. II, pp. 1–20: AI-translated by Claude (Anthropic), run by …". The translations are released with the
rest of this repository under [CC0 1.0](../../LICENSE).

## Files

- [INSTRUCTIONS.md](INSTRUCTIONS.md): the instructions Claude follows.
- [GLOSSARY.md](GLOSSARY.md): English terms of classical invariant theory used throughout.
- [STATUS.md](STATUS.md): the parts and who is working on them.
- [de/](de): the German parts (vol. I from p. 29 in 20-page parts, vol. II in 20-page parts), cut from the full
  sources in [../tex](../tex).
- [chunks.py](chunks.py): `python chunks.py check DE_PART EN_PART` compares the formulas, page marks and braces of a
  translation with its German part.
- `en/`: finished English parts, before they are joined into the full volumes.
