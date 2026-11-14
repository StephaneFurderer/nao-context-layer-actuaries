"""Validate talk/talking-points.md.

Each talking point must:
  - fit in 60 seconds: words in **Say** at WPM words/minute + seconds in **Demo** <= 60
  - state in **Doing** what we are doing, in <= 20 words
  - point to **Proof** paths that exist in this repo
  - cite **Sources** ids that exist in sources/source-bank.md

    python talk/check_talk.py            # exits 1 on any violation
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WPM = 120          # deliberately slow: second-language speaker, prerecorded with on-screen moments
MAX_TOTAL_MIN = 12.0  # the demo segment's budget, excluding interview clips
MAX_SECONDS = 60
TP = re.compile(r"^### (TP-\d+)\s*[—-]\s*(.+)$", re.M)


def spoken_words(text: str) -> int:
    """Count words as they are SAID: '49.4%' is 'forty-nine point four percent' (5), '$5,000' is 'five thousand dollars' (3)."""
    n = 0
    for tok in re.findall(r"[\w'’%.,$-]+", text):
        t = tok.strip(".,")
        if re.search(r"\d", t):
            digits = re.sub(r"[^\d.]", "", t)
            whole, _, frac = digits.partition(".")
            n += max(1, min(len(whole.lstrip("0") or "0"), 3)) + (1 + len(frac) if frac else 0)
            n += ("%" in t) + ("$" in t)
        elif t:
            n += 1
    return n


def field(block: str, name: str) -> str:
    m = re.search(rf"^\*\*{name}:\*\*\s*(.*?)(?=^\*\*\w+:\*\*|\Z)", block, re.M | re.S)
    return m.group(1).strip() if m else ""


def main() -> int:
    text = (ROOT / "talk" / "talking-points.md").read_text()
    bank = (ROOT / "sources" / "source-bank.md").read_text()
    bank_ids = set(re.findall(r"^\| ([A-Z]\d+) \|", bank, re.M))
    heads = list(TP.finditer(text))
    errors, total, rows = [], 0.0, []
    for i, h in enumerate(heads):
        block = text[h.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        tid, title = h.group(1), h.group(2).strip()
        say = re.sub(r"[>*_`]", "", field(block, "Say"))
        words = spoken_words(say)
        demo = field(block, "Demo")
        demo_s = int(re.search(r"(\d+)\s*s", demo).group(1)) if re.search(r"(\d+)\s*s", demo) else 0
        secs = words / WPM * 60 + demo_s
        doing = field(block, "Doing")
        proof = field(block, "Proof")
        srcs = field(block, "Sources")
        if secs > MAX_SECONDS:
            errors.append(f"{tid}: {secs:.0f}s > {MAX_SECONDS}s ({words} words + {demo_s}s demo)")
        if not doing or len(doing.split()) > 20:
            errors.append(f"{tid}: **Doing** missing or > 20 words")
        for p in re.findall(r"`([^`]+)`", proof):
            path = p.split(":")[0].split("#")[0].strip()
            if "/" in path or "." in path:
                if not (ROOT / path).exists():
                    errors.append(f"{tid}: proof path not found: {path}")
        if not re.findall(r"`[^`]+`", proof):
            errors.append(f"{tid}: **Proof** must reference at least one repo file in backticks")
        for s in re.findall(r"\b([A-Z]\d+)\b", srcs):
            if s not in bank_ids:
                errors.append(f"{tid}: source {s} not in source bank")
        total += secs
        rows.append((tid, title, words, demo_s, secs))
    print(f"{'id':6} {'sec':>4} {'words':>5} {'demo':>4}  title")
    for tid, title, w, d, s in rows:
        flag = "  <-- over" if s > MAX_SECONDS else ""
        print(f"{tid:6} {s:4.0f} {w:5d} {d:4d}  {title}{flag}")
    clips = re.findall(r"^> \*\*CLIP (\w+)\*\*.*?(\d+)\s*min", text, re.M)
    clip_min = sum(int(m) for _, m in clips)
    print(f"\n{len(rows)} talking points, {total/60:.1f} min spoken/demo + {clip_min} min interview clips "
          f"= {total/60 + clip_min:.1f} min (at {WPM} wpm)")
    if total / 60 > MAX_TOTAL_MIN:
        errors.append(f"segment total {total/60:.1f} min > budget {MAX_TOTAL_MIN} min")
    if errors:
        print("\nFAILED:\n  " + "\n  ".join(errors))
        return 1
    print("All talking points pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
