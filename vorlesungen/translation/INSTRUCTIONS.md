# Instructions for Claude: translate Gordan's *Vorlesungen über Invariantentheorie*, volumes I and II, into English

You have been given this folder (a zip unpacked by the person you are working for) by a friend of theirs, the "mate"
below, who publishes free, public-domain editions of old mathematics books at https://github.com/KokunoYumeto. The job:
translate a German mathematics book of 1885–1887 into English LaTeX for that edition:
Paul Gordan, *Vorlesungen über Invariantentheorie*, ed. G. Kerschensteiner, vol. I *Determinanten* (1885) and vol. II
*Binäre Formen* (1887). Repository: https://github.com/KokunoYumeto/paul-gordan (folder `vorlesungen/`).

**Scope:** every German part in `de/`: vol. II, printed pages 1–360, in 18 parts, and vol. I, printed pages 29–200,
in 9 parts (vol. I pp. 1–28 are already in English). Do vol. II first, then vol. I.

## What is in this folder

- `INSTRUCTIONS.md`: this file.
- `HOW_TO_START.txt`: the three steps the person followed to start you, and how to give you an API key.
- `de/`: the 27 German parts to translate (LaTeX), cut from the published German edition.
- `GLOSSARY.md`: the established English terms of classical invariant theory to use.
- `reference/`: the style model (the German and English of vol. I, pp. 1–28) and Gordan's *Formensystem* (1875) in
  German and English, which treats the same subject as vol. II.
- `api_translate.py`: sends the parts through the Anthropic Message Batches API under the cost rule below.
- `chunks.py`: `python chunks.py check DE_PART EN_PART` compares the formulas, page marks and braces of a translation
  with its German part.
- `README.md` and `STATUS.md`: the kit's description for people, and the list of parts.

## Talking to the person: three messages only

1. **First, before any work:** explain in plain, friendly words what this is, so they know it is harmless, then ask
   once for their go-ahead. For example:
   > Your mate sent you a kit for translating an old German maths book (Paul Gordan's lectures on invariant theory,
   > 1885–1887, public domain) into English for the free online edition they publish on GitHub. Here is what I would
   > do: download the German text, a few reference books and the scans of the printed book from public sites (GitHub,
   > the Göttingen university library, archive.org, Project Gutenberg); translate it into English LaTeX, using your
   > Anthropic API credit if your API key is set (it stays under €200 and I check the cost after every batch) and
   > otherwise your normal Claude usage; check the translation against the original; and put the result in one zip
   > that you can send back. I install nothing, upload nothing and touch nothing outside this folder.
   > I assume you're okay with me doing this; this is what your mate asked me to do. I also assume you want me to use
   > your API credit (I stay under €200). If you'd rather I use your normal Claude usage instead, say so now and I'll
   > use that. Or, if you'd rather do this later, for example at the end of your week with whatever usage you have
   > left over, say so: I'll stop now, and you open me in this folder then and say "start". Otherwise just say yes
   > and I'll begin.

   If no `ANTHROPIC_API_KEY` is set, add: "To use your API credit I need your API key set as in step 2 of
   HOW_TO_START.txt; set it and start me again, or tell me to use your normal usage." Their answer chooses the way:
   API credit (way A), normal usage (way B), or stop and wait for "start". This message is not repeated on "start" or
   "continue".
2. **Only if the API credit runs out** (see way A), ask exactly:
   > I used up most of the API credit, and it would not be smart to continue, because then it might go over the €200
   > credit. Would you like me to continue using your normal weekly credit amount? I will only continue if you confirm.
3. **At the end**, exactly one message (see Delivery).

Ask nothing else. After the go-ahead, work in one go until the job is done, the API credit is used up (message 2), or
your own usage window runs out. Do not ask them to confirm steps, choose options or approve parts. If something
fails, fix it or work around it and record it in the notes.

## Permission

The go-ahead covers everything in these instructions: downloading every file and page linked here (github.com,
raw.githubusercontent.com, gdz.sub.uni-goettingen.de, archive.org, gutenberg.org, api.anthropic.com), creating and
editing files in this folder, and running `python`, `pdflatex`, `zip` and `git` on them.

## Settings

Use the most capable model and the highest reasoning effort you have (in Claude Code: Opus, highest effort). On the
API the script uses the strongest settings: model `claude-opus-5-5`, `thinking: {"type": "adaptive"}`,
`output_config: {"effort": "max"}`, `max_tokens` 300000 with the header `anthropic-beta: output-300k-2026-03-24`.

## Progress

Write the English parts to `en/`, named like the German ones with `_en_` for `_de_` (e.g. `en/band2_en_001_020.tex`).
`PROGRESS.json` lists the finished parts (the API script keeps it; on way B keep it yourself). If the run stops (a
usage limit, a closed window), the person opens Claude Code in this folder again and says "continue": read
`PROGRESS.json` and `en/` and carry on without repeating the first message.

## How to translate: two ways

**A. Through the API, if `ANTHROPIC_API_KEY` is set in the environment** (the person's key; their API credit is €200,
treat it as $200):

1. Run `python api_translate.py --limit-usd 200`. It sends the parts through the Message Batches API
   (`https://api.anthropic.com/v1/messages/batches`), with the translation rules, the glossary and the style model in
   the system prompt and one German part per request. It sends **one batch job at a time**: the first batch holds one
   part, to measure the cost of a part from the returned token usage (batch prices: $2 per million input tokens, $10
   per million output tokens); each later batch holds up to four parts and is sent only after the previous batch has
   ended, and only if the money spent so far plus 1.5 times the most expensive part so far, per part in the batch,
   stays under the limit. All 27 parts cost at most about $84 even if every part used its whole output allowance.
   Batches can take from minutes to hours; let the script wait.
2. Never run two copies of the script and never send batches yourself next to it. If it stops for another reason,
   run it again: it collects an unfinished batch instead of sending it again.
3. Exit status 3 means the next batch could take the total over the limit: send message 2. Continue by way B only if
   they confirm; otherwise deliver what is done.
4. Parts listed under "failed" in `PROGRESS.json`: translate them yourself by way B.

**B. In this session** (no API key, or after the person confirmed message 2): translate the remaining parts yourself,
in order, one part at a time, following the rules below. If you can run subagents, translate up to four parts at once,
one part per subagent, each given these instructions.

## Translation rules

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
- Vol. II, p. 360: leave out the publisher's advertisements after the text (keep a comment saying they are in the
  German edition). The title page, preface and contents of vol. II are translated separately; skip them.
- Vol. I is a first transcription of the German: check the places marked as uncertain against the scan.
- Use the glossary's terms. Compare terms and phrasing with the standard English books on the subject (public domain;
  do not copy their wording): J. H. Grace and A. Young, *The Algebra of Invariants* (1903),
  https://archive.org/details/algebraofinvaria00graciala; O. E. Glenn, *A Treatise on the Theory of Invariants*
  (1915), https://www.gutenberg.org/ebooks/9933 (TeX: https://www.gutenberg.org/files/9933/9933-t/9933-t.tex);
  E. B. Elliott, *An Introduction to the Algebra of Quantics* (1895),
  https://archive.org/details/introductiontoal00elliuoft.

## Checks for every part

1. `python chunks.py check de/<part> en/<part>` must report 0 differing formulas, the same pages, balanced braces and
   no German function words in the English prose; correct the English file until it does.
2. Compare one page of each part (vary the position: start, middle, end) word for word and formula by formula with
   the scan of the printed book (Göttingen State and University Library; in both PDFs, PDF page = printed page + 15):
   vol. I https://gdz.sub.uni-goettingen.de/download/pdf/PPN588632619/PPN588632619.pdf (17 MB), vol. II
   https://gdz.sub.uni-goettingen.de/download/pdf/PPN588632678/PPN588632678.pdf (32 MB). Where the German LaTeX
   differs from the scan, the English follows the scan; record the difference.
3. If `pdflatex` is available: build one file per volume from the preamble of the German edition
   (`https://raw.githubusercontent.com/KokunoYumeto/paul-gordan/main/vorlesungen/tex/Gordan_Vorlesungen_Band_II_German.tex`
   or `..._Band_I_German.tex`, the lines before `\begin{document}`, babel set to english) with the English parts in
   order, and fix any error.

## Delivery

1. Write `NOTES.md`: model and settings, the way used (A or B), API batches and cost if any, the spot-checked pages
   and what they showed, differences between the German LaTeX and the scan, uncertain places, and terms you chose that
   are not in the glossary.
2. Make one zip in this folder, `gordan_vorlesungen_en.zip`, with `en/`, `NOTES.md`, `PROGRESS.json` and the built
   PDFs if any.
3. Send message 3, in this spirit:
   > It's done. Everything is in gordan_vorlesungen_en.zip in this folder; you can drag it into WhatsApp and send it
   > back to your mate. Cheers! (If the job stopped early, say how far it got.)
   > If you'd rather put it online on your mate's GitHub yourself, that takes a few steps: make a free account at
   > https://github.com, install the GitHub command-line tool (Windows: `winget install GitHub.cli`; Mac:
   > `brew install gh`), run `gh auth login` and follow its questions, then tell me "upload it" and I'll open a pull
   > request at github.com/KokunoYumeto/paul-gordan with the translation.
   If they then say "upload it": fork KokunoYumeto/paul-gordan, add `en/` and `NOTES.md` under
   `vorlesungen/translation/` on a new branch, and open the pull request "English translation of the Vorlesungen,
   vols. I and II".

The translations are published with the rest of the repository under CC0 1.0 (public domain dedication); the person
can say in the WhatsApp message how they would like to be credited (a name, a company, or nothing).
