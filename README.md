# Paul Gordan — five works in the original language and in English

Editions of five works by Paul Gordan, one of them written with Alfred Clebsch: the text in its original language,
typeset in LaTeX from scans of the prints, and English translations.

| Work | Original | English | Status |
| --- | --- | --- | --- |
| *De linea geodetica*, dissertation (Berlin, 1862) | [Latin PDF](de-linea-geodetica/pdf/Gordan_De_linea_geodetica_Latin.pdf) | [PDF](de-linea-geodetica/pdf/Gordan_De_linea_geodetica_English.pdf) | complete, with [apparatus](de-linea-geodetica/pdf/Gordan_De_linea_geodetica_Apparatus.pdf) |
| *Ueber die Transformation der Θ-Functionen*, Habilitationsschrift (Gießen, 1863) | [German PDF](thetafunctionen/pdf/Gordan_Thetafunctionen_German.pdf) | [PDF](thetafunctionen/pdf/Gordan_Thetafunctionen_English.pdf) | complete, with [apparatus](thetafunctionen/pdf/Gordan_Thetafunctionen_Apparatus.pdf) |
| A. Clebsch and P. Gordan, *Theorie der Abelschen Functionen* (Leipzig: Teubner, 1866) | [German PDF](abelsche-functionen/pdf/Clebsch_Gordan_Abelsche_Functionen_German.pdf) | [PDF](abelsche-functionen/pdf/Clebsch_Gordan_Abelsche_Functionen_English.pdf) | complete |
| *Ueber das Formensystem binaerer Formen* (Leipzig: Teubner, 1875) | [German PDF](formensystem/pdf/Gordan_Formensystem_German.pdf) | [PDF](formensystem/pdf/Gordan_Formensystem_English.pdf) | complete |
| *Vorlesungen über Invariantentheorie*, ed. G. Kerschensteiner, vol. I, *Determinanten* (1885) | [German PDF](vorlesungen/pdf/Gordan_Vorlesungen_Band_I_German.pdf) | [pp. 1–28](vorlesungen/pdf/Gordan_Vorlesungen_Band_I_pp001-028_English.pdf) | German: first transcription, complete; English: pages 1–28 |
| *Vorlesungen über Invariantentheorie*, vol. II, *Binäre Formen* (1887) | [German PDF](vorlesungen/pdf/Gordan_Vorlesungen_Band_II_German.pdf) | — | German: complete; collated in part with a second transcription |

The LaTeX sources are in the `tex/` folder of each work.

## Quality and completeness

- ***De linea geodetica* and *Thetafunctionen*.** Complete diplomatic transcriptions with separate English
  translations. Each has an apparatus listing the readings that needed a decision. Both had a final audit against the
  scan in a separate AI session before release; for the *Thetafunctionen* it found and corrected five errors.
- ***Theorie der Abelschen Functionen*.** Complete in German and English. The transcription was checked against the
  scan in installments, and a final pass over the formulas of the last chapter corrected several misread symbol
  families. A spot check of printed pages 128 and 238 on 27 October 2026 found, on page 128, an integral whose
  limits were wrong (0 to ξ instead of ξ to ζ, which reversed the sign of the equation), a misspelling and two
  punctuation marks; these are corrected in both languages. Page 238 agrees with the print, apart from one phrase that
  the print letter-spaces for emphasis. Expect occasional errors of this kind on other pages.
- ***Formensystem*.** Complete in German and English; checked against the scan by AI during production. Not spot
  checked again.
- ***Vorlesungen über Invariantentheorie*.** The German of both volumes is complete.
  - Volume I is a first transcription. It marks 38 places where the scan could not be read with certainty; these are
    unresolved. It has not been collated a second time.
  - Volume II was compared with a second, independent transcription of its pages 1–192 (on pages 26–72 that
    transcription abridges the text and was not used). Every disagreement on pages 1–25 and 73–192 (206) and each of
    the 50 places marked as uncertain throughout the volume was checked against the scan. This corrected 56 places:
    misread symbols, signs, indices and exponents (among them ∇, which had been read as Γ throughout pages 330–336),
    words, and a footnote attached to the wrong place. All 50 uncertain places are resolved. The section sign and
    "mod." now follow the print throughout. Misprints of the print are kept and marked in the LaTeX source. Pages
    26–72 and 193–360 have been read once, apart from the uncertain places. The edition includes the title page,
    preface and table of contents.
  - Four figures or ornaments are replaced by short textual stand-ins. The English covers only pages 1–28 of volume I.
- The readers do not mark the page breaks of the prints; page references in the text refer to the prints.

## How it was made

The complete German transcriptions of both volumes of the *Vorlesungen* were made by Claude (Anthropic) in August
2026: Claude Sonnet 5 agents in Claude Code workflows, one printed page per agent. The second transcription of volume
II, pages 1–192, used for the collation, and the first draft of its front matter were made with OpenAI models in
ChatGPT; the disagreements and the front matter were checked against the scan by Claude Opus 5.5 (Anthropic) agents on
27 October 2026. All other texts, including the German and English of volume I, pages 1–28, were transcribed from
scans, and translated, by AI (OpenAI models in ChatGPT and Codex). The spot check and corrections of 27 October 2026
were made by Claude Opus 5.5 (Anthropic).

## Sources

- *Theorie der Abelschen Functionen*: a Google Books scan.
- *Vorlesungen über Invariantentheorie*: the Göttingen State and University Library scans (GDZ),
  PPN588632619 (vol. I) and PPN588632678 (vol. II).
- *De linea geodetica*, *Thetafunctionen* and *Formensystem*: scans of the prints.

## Building

Run `pdflatex` twice on each source: in the `tex/` folders, and for *De linea geodetica* on `main.tex` in each of
`tex/latin`, `tex/english` and `tex/apparatus`.

## Rights

Gordan's and Clebsch's texts are in the public domain, as is Kerschensteiner's editorial work on the *Vorlesungen*.
The transcriptions, translations and typesetting are dedicated to the public domain under [CC0 1.0](LICENSE).

## Earlier versions

Earlier versions were published on Zenodo, [doi:10.5281/zenodo.20616260](https://doi.org/10.5281/zenodo.20616260).
Zenodo has blocked access to our account, so please use this repository from now on.

---

[Sponsor this work](https://github.com/sponsors/KokunoYumeto)
