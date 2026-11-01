"""Translate the German parts of Gordan's Vorlesungen into English LaTeX through the Anthropic Message Batches API,
one batch job at a time, keeping the total cost under a limit.

usage:  python api_translate.py [--limit-usd 200] [--only band2_de_001_020.tex,...]
Needs ANTHROPIC_API_KEY in the environment. Run it in an empty working folder: it downloads the German parts and the
reference material from GitHub, writes en/<band>_en_<first>_<last>.tex for every finished part and keeps its state in
PROGRESS.json, so running it again continues where it stopped (an unfinished batch is collected, not sent again).

Cost control: the first batch holds one part, to measure the cost of a part; later batches hold up to four parts.
A batch is sent only when the money spent so far plus 1.5 times the most expensive part so far, times the number of
parts in the batch, stays under the limit. Exit status 0: all parts done. Exit status 3: stopped because the next
batch could take the total over the limit (PROGRESS.json says what is left).
"""
import json
import os
import pathlib
import re
import sys
import time
import urllib.request

RAW = "https://raw.githubusercontent.com/KokunoYumeto/paul-gordan/main/"
API = "https://api.anthropic.com/v1/messages/batches"
MODEL = "claude-opus-5-5"
PRICE_IN, PRICE_OUT = 2.0, 10.0  # USD per million tokens, batch prices of claude-opus-5-5
MAX_TOKENS = 300000
WORST_PART = (40000 * PRICE_IN + MAX_TOKENS * PRICE_OUT) / 1e6  # about 3.08 USD: a part that uses all its output
HEADERS = {"x-api-key": os.environ.get("ANTHROPIC_API_KEY", ""), "anthropic-version": "2023-06-01",
           "content-type": "application/json", "anthropic-beta": "output-300k-2026-03-24"}
PARTS = ["band2_de_%03d_%03d.tex" % (a, a + 19) for a in range(1, 360, 20)] + \
        ["band1_de_029_048.tex", "band1_de_049_068.tex", "band1_de_069_088.tex", "band1_de_089_108.tex",
         "band1_de_109_128.tex", "band1_de_129_148.tex", "band1_de_149_168.tex", "band1_de_169_188.tex",
         "band1_de_189_200.tex"]

RULES = """You translate a 19th-century German mathematics book into English LaTeX for a public-domain edition:
Paul Gordan, Vorlesungen über Invariantentheorie, ed. G. Kerschensteiner, vol. I Determinanten (1885), vol. II Binäre
Formen (1887).
- Translate all German prose into clear, idiomatic English that a mathematician reads easily, faithful to the meaning,
  in the style of the earlier English parts shown below. Do not modernise the mathematics or add explanations.
- Keep every formula, display, \\weq{..}{..} and equation number exactly as in the German (translate only words inside
  \\text{}, \\mbox{}, \\hbox{}). Notation, letters and formula numbers stay as printed.
- Keep every \\weberpage{n} mark and every "% !PRINTED" comment in place. Keep LaTeX comments, translating them where
  they describe the text.
- Section headings stay "§ n." with the title translated; numbered paragraphs keep their numbers; italic paragraph
  titles stay italic. "Theil" is "Part". \\gesperrt{...} (letter-spaced emphasis) becomes \\emph{...}.
- Misprints in formulas stay as printed, with their [sic] comments. For a misprinted word, translate the intended word
  and keep a short comment.
- Vol. II, p. 360: leave out the publisher's advertisements after the text (keep a comment saying they are in the
  German edition).
- Use the glossary's terms consistently.
Output: only the English LaTeX of the part, from its first line to its last, with no text before or after it and no
code fences. End it with a LaTeX comment block that starts with the line "% TRANSLATION NOTES" and lists, one per line,
uncertain readings, terms you chose that are not in the glossary, and places where the German looks mistranscribed."""


def http(url, body=None, headers=None, tries=5):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
                                         headers=headers or {}, method="POST" if body is not None else "GET")
            with urllib.request.urlopen(req, timeout=300) as r:
                return r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")
            if e.code in (429, 500, 502, 503, 529) and k < tries - 1:
                time.sleep(30 * (k + 1))
                continue
            raise SystemExit("HTTP %d from %s: %s" % (e.code, url, msg[:500]))
        except OSError:
            if k < tries - 1:
                time.sleep(30 * (k + 1))
                continue
            raise


def fetch(path, cache):
    # files of the kit itself (de/, GLOSSARY.md) and the reference files shipped in reference/ are used when present
    if path.startswith("vorlesungen/translation/") and pathlib.Path(path[len("vorlesungen/translation/"):]).exists():
        return pathlib.Path(path[len("vorlesungen/translation/"):]).read_text(encoding="utf-8")
    shipped = cache / pathlib.Path(path).name
    if shipped.exists():
        return shipped.read_text(encoding="utf-8")
    p = cache / path.replace("/", "__")
    if not p.exists():
        p.write_text(http(RAW + path), encoding="utf-8")
    return p.read_text(encoding="utf-8")


def main():
    args = sys.argv[1:]
    limit = float(args[args.index("--limit-usd") + 1]) if "--limit-usd" in args else 200.0
    only = args[args.index("--only") + 1].split(",") if "--only" in args else None
    if not HEADERS["x-api-key"]:
        raise SystemExit("ANTHROPIC_API_KEY is not set")
    work = pathlib.Path.cwd()
    (work / "de").mkdir(exist_ok=True)
    (work / "en").mkdir(exist_ok=True)
    cache = work / "reference"
    cache.mkdir(exist_ok=True)
    state_path = work / "PROGRESS.json"
    st = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else \
        {"done": [], "failed": {}, "spent_usd": 0.0, "part_costs": {}, "batches": [], "open_batch": None}

    def save():
        state_path.write_text(json.dumps(st, indent=1), encoding="utf-8")

    glossary = fetch("vorlesungen/translation/GLOSSARY.md", cache)
    style_de = fetch("vorlesungen/tex/Gordan_Vorlesungen_Band_I_pp001-028_German.tex", cache)
    style_en = fetch("vorlesungen/tex/Gordan_Vorlesungen_Band_I_pp001-028_English.tex", cache)
    body_de = style_de[style_de.find("\\begin{document}"):][:30000]
    body_en = style_en[style_en.find("\\begin{document}"):][:30000]
    system = RULES + "\n\nGLOSSARY\n\n" + glossary + \
        "\n\nSTYLE MODEL: the beginning of vol. I in German and in the edition's English\n\nGERMAN\n" + body_de + \
        "\n\nENGLISH\n" + body_en

    def collect(bid, parts):
        t0 = time.time()
        while True:
            b = json.loads(http(API + "/" + bid, headers=HEADERS))
            if b.get("processing_status") == "ended":
                break
            if time.time() - t0 > 36 * 3600:
                raise SystemExit("batch %s still running after 36 h; run this script again later" % bid)
            time.sleep(60)
        cost = 0.0
        for line in http(b["results_url"], headers=HEADERS).splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            part, res = r["custom_id"], r["result"]
            if res["type"] != "succeeded":
                st["failed"][part] = res["type"]
                continue
            m = res["message"]
            u = m.get("usage", {})
            c = ((u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
                  + u.get("cache_read_input_tokens", 0)) * PRICE_IN + u.get("output_tokens", 0) * PRICE_OUT) / 1e6
            cost += c
            st["part_costs"][part] = round(c, 4)
            text = "".join(x.get("text", "") for x in m["content"] if x.get("type") == "text").strip()
            text = re.sub(r"^```[a-zA-Z]*\n|\n```$", "", text)
            if m.get("stop_reason") != "end_turn" or "\\weberpage" not in text:
                st["failed"][part] = "stop_reason %s" % m.get("stop_reason")
                continue
            (work / "en" / part.replace("_de_", "_en_")).write_text(text + "\n", encoding="utf-8")
            st["done"].append(part)
            st["failed"].pop(part, None)
        st["spent_usd"] = round(st["spent_usd"] + cost, 4)
        st["batches"].append({"id": bid, "parts": parts, "cost_usd": round(cost, 4)})
        st["open_batch"] = None
        save()
        print("batch %s: %d parts, %.2f USD; total %.2f USD" % (bid, len(parts), cost, st["spent_usd"]), flush=True)

    if st.get("open_batch"):
        collect(st["open_batch"]["id"], st["open_batch"]["parts"])
    retried = set()
    while True:
        todo = [p for p in (only or PARTS) if p not in st["done"]]
        todo = [p for p in todo if p not in st["failed"] or p not in retried]
        if not todo:
            break
        n = 1 if not st["part_costs"] else min(4, len(todo))
        per_part = 1.5 * max(st["part_costs"].values()) if st["part_costs"] else WORST_PART
        predicted = per_part * n
        if st["spent_usd"] + predicted > limit:
            save()
            print("STOP: %.2f USD spent; the next batch (%d parts, up to %.2f USD) could exceed the limit of %.2f USD."
                  % (st["spent_usd"], n, predicted, limit), flush=True)
            sys.exit(3)
        batch_parts = todo[:n]
        reqs = []
        for part in batch_parts:
            if part in st["failed"]:
                retried.add(part)
            de = fetch("vorlesungen/translation/de/" + part, cache)
            (work / "de" / part).write_text(de, encoding="utf-8")
            reqs.append({"custom_id": part, "params": {
                "model": MODEL, "max_tokens": MAX_TOKENS, "thinking": {"type": "adaptive"},
                "output_config": {"effort": "max"}, "system": system,
                "messages": [{"role": "user", "content": "Translate this German part (%s) into English LaTeX.\n\n%s"
                              % (part, de)}]}})
        b = json.loads(http(API, {"requests": reqs}, headers=HEADERS))
        st["open_batch"] = {"id": b["id"], "parts": batch_parts}
        save()
        print("sent batch %s with %s" % (b["id"], ", ".join(batch_parts)), flush=True)
        collect(b["id"], batch_parts)
    left = [p for p in (only or PARTS) if p not in st["done"]]
    print("finished: %d parts done, %d left %s; %.2f USD spent"
          % (len(st["done"]), len(left), left, st["spent_usd"]), flush=True)
    sys.exit(0 if not left else 4)


if __name__ == "__main__":
    main()
