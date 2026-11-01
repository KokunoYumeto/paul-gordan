# Instructions for Claude: translate one part of Gordan's *Vorlesungen über Invariantentheorie* into English

You are translating a 19th-century German mathematics book into English for a public-domain edition:
Paul Gordan, *Vorlesungen über Invariantentheorie*, ed. G. Kerschensteiner, vol. I *Determinanten* (1885) and vol. II
*Binäre Formen* (1887). Repository: https://github.com/KokunoYumeto/paul-gordan (folder `vorlesungen/`).

## Permission: work without asking

The person who gave you this task has agreed to everything in these instructions. You may, without asking first:
download every file and page linked here (from github.com, raw.githubusercontent.com, gdz.sub.uni-goettingen.de,
archive.org and gutenberg.org); create a working folder and create and edit files in it; run `python`, `pdflatex`,
`git`, `zip` and similar tools on those files. Do not ask the person to confirm each step. Ask only if something is
impossible to resolve, and at the end tell them what to send.

## Settings

Use the most capable model and the highest reasoning effort you have: in Claude Code, Opus with the highest effort
setting; through the API, the strongest model with effort "max". This is careful work on dense mathematics.

## Your part

The person tells you which part (a file in `de/`, e.g. `band2_de_001_020.tex`, printed pages 1–20 of vol. II). If they
did not, take the first part marked "open" in [STATUS.md](STATUS.md). Download it:
`https://raw.githubusercontent.com/KokunoYumeto/paul-gordan/main/vorlesungen/translation/de/<file>`

## Material to read before translating

1. **The glossary**, [GLOSSARY.md](GLOSSARY.md): the established English terms (Grace and Young). Use them consistently.
2. **Earlier English of this edition, as the style model**:
   - vol. I, pp. 1–28: `https://raw.githubusercontent.com/KokunoYumeto/paul-gordan/main/vorlesungen/tex/Gordan_Vorlesungen_Band_I_pp001-028_English.tex`
     (German counterpart: `.../vorlesungen/tex/Gordan_Vorlesungen_Band_I_pp001-028_German.tex`)
   - Gordan's *Ueber das Formensystem binaerer Formen* (1875), English and German, same subject as vol. II:
     `.../formensystem/tex/Gordan_Formensystem_English.tex` and `.../formensystem/tex/Gordan_Formensystem_German.tex`
     (prefix `https://raw.githubusercontent.com/KokunoYumeto/paul-gordan/main/`)
3. **Authoritative English books on the same subject, to compare your terms and phrasing with** (all public domain):
   - J. H. Grace and A. Young, *The Algebra of Invariants* (Cambridge, 1903), written to bring Clebsch's and Gordan's
     methods into English: https://archive.org/details/algebraofinvaria00graciala
   - O. E. Glenn, *A Treatise on the Theory of Invariants* (1915), with LaTeX source:
     https://www.gutenberg.org/ebooks/9933 (TeX: https://www.gutenberg.org/files/9933/9933-t/9933-t.tex)
   - E. B. Elliott, *An Introduction to the Algebra of Quantics* (Oxford, 1895):
     https://archive.org/details/introductiontoal00elliuoft
   Read the passages that treat the topic of your part (transvectants, the Omega process, the symbolic method,
   determinants, ...), and use their terminology where the glossary is silent. Do not copy their wording.
4. **The scans of the printed book**, for spot checks (Göttingen State and University Library):
   - vol. I: https://gdz.sub.uni-goettingen.de/id/PPN588632619 (PDF: https://gdz.sub.uni-goettingen.de/download/pdf/PPN588632619/PPN588632619.pdf, 17 MB)
   - vol. II: https://gdz.sub.uni-goettingen.de/id/PPN588632678 (PDF: https://gdz.sub.uni-goettingen.de/download/pdf/PPN588632678/PPN588632678.pdf, 32 MB)
   - In both PDFs, PDF page = printed page + 15 (e.g. printed p. 46 of vol. II is PDF page 61).

## How to translate

- Translate all German prose into clear, idiomatic English that a mathematician reads easily, faithful to the
  meaning, in the style of the earlier English parts. Do not modernise the mathematics or add explanations.
- Keep every formula, display, `\weq{..}{..}` and equation number exactly as in the German (translate only words
  inside `\text{}`, `\mbox{}`, `\hbox{}`). Notation, letters, formula numbers ((1), (I), ...) stay as printed.
- Keep every `\weberpage{n}` mark and `% !PRINTED` comment in place. Keep LaTeX comments, translating them where they
  describe the text.
- Section headings stay "§ n." with the title translated; numbered paragraphs keep their numbers; italic paragraph
  titles stay italic. "Theil" is "Part". `\gesperrt{...}` (letter-spaced emphasis) becomes `\emph{...}`.
- Misprints in formulas stay as printed, with their `[sic]` comments. For a misprinted word, translate the intended
  word and keep a short comment.
- Vol. II only: leave out the publisher's advertisements after the text of p. 360 (keep a comment saying they are in
  the German edition).
- Vol. I is a first transcription of the German: places marked as uncertain in comments must be checked against the
  scan; say what the scan shows in your notes.

## Checks before you deliver

1. If you can run Python: download [chunks.py](chunks.py) and run
   `python chunks.py check de/<german part> en/<your English part>` until it reports 0 differing formulas, the same
   pages, balanced braces and no German function words left in the English prose. If you cannot run code, compare
   the formulas one by one yourself.
2. Spot checks against the scan: compare at least three pages of your part (start, middle, end) word for word and
   formula by formula with the scan. If the German LaTeX differs from the scan, translate what the scan says and list
   the difference in your notes (these are corrections for the German edition too).
3. If you can run `pdflatex`: compile your part inside the preamble of the German file (the lines before
   `\begin{document}` in `vorlesungen/tex/Gordan_Vorlesungen_Band_II_German.tex` or `..._Band_I_German.tex`, with babel
   set to english) and fix any error.

## Deliverable

LaTeX, in two files:
- `band<1|2>_en_<first>_<last>.tex`: the English part, same structure as the German part (no preamble).
- `band<1|2>_en_<first>_<last>_NOTES.md`: model and settings used, date; the spot-checked pages and what you found;
  differences between the German LaTeX and the scan; terms you chose that are not in the glossary; anything uncertain.

Your translation is published with the rest of the repository under CC0 1.0 (public domain dedication).

## Handing it back (hands-free for the person)

- **Default:** put both files in one zip, `gordan_band<1|2>_<first>_<last>_en.zip`, tell the person where it is, and
  ask them to send that zip by WhatsApp to the person who gave them this task. That is all they need to do.
- **Only if GitHub is already set up** (`gh auth status` succeeds) **or the person says they want to set it up:** fork
  KokunoYumeto/paul-gordan, add both files under `vorlesungen/translation/en/` on a new branch, and open a pull request
  titled "English translation: Vorlesungen <I|II>, pp. <first>–<last>". Still give them the zip.
- In your last message, ask the person how they would like to be credited (a name, a company, or nothing).
