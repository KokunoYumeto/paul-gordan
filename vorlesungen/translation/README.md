# Help translate Gordan's *Vorlesungen über Invariantentheorie* with your own Claude

Most of Gordan's lectures (vol. I from p. 29, and all of vol. II) exist here only in German. With Claude credits you
are not using, both volumes can be translated into English in one run: Claude reads the German LaTeX in this kit,
translates it (through your Anthropic API credit, or your normal Claude usage), checks its work against the scans of
the printed book, and gives you one zip with the English LaTeX to send back.

## What to do

Follow [HOW_TO_START.txt](HOW_TO_START.txt): unpack the kit, open Claude Code in the folder, paste

```text
Read INSTRUCTIONS.md in this folder and follow it.
```

Claude then explains what it will do and asks once whether that is fine and which credit to use (your API credit,
your normal usage, or later). After that it works on its own until the zip is ready. Without the zip, start from an
empty folder with: "Download every file of https://github.com/KokunoYumeto/paul-gordan/tree/main/vorlesungen/translation
into this folder, keeping the de/ subfolder, then read INSTRUCTIONS.md and follow it."

## Credit and licence

Helpers are credited by the name they choose (a person, a company, or nothing) in the main README, for example:
"English of vols. I and II: AI-translated by Claude (Anthropic), run by …". The translations are released with the
rest of this repository under [CC0 1.0](../../LICENSE).

## Files

- [INSTRUCTIONS.md](INSTRUCTIONS.md): the instructions Claude follows.
- [HOW_TO_START.txt](HOW_TO_START.txt): the three steps for the person running it.
- [GLOSSARY.md](GLOSSARY.md): English terms of classical invariant theory used throughout.
- [STATUS.md](STATUS.md): the parts and who is working on them.
- [de/](de): the German parts (vol. I from p. 29, vol. II), 20 printed pages each, cut from the sources in [../tex](../tex).
- [api_translate.py](api_translate.py): sends the parts through the Message Batches API, one batch at a time, under a
  cost limit.
- [chunks.py](chunks.py): `python chunks.py check DE_PART EN_PART` compares the formulas, page marks and braces of a
  translation with its German part.
- `en/`: finished English parts, before they are joined into the full volumes.
