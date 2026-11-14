"""Grade candidate SQL answers against the reference SQL in context/tests/.

Mirrors the spirit of `nao test` comparison (docs: nao-agent/context-engineering/evaluation):
row order ignored, floats rounded to 4 decimals (nao_config test.comparison.decimals: 4), then numeric match with rtol=1e-5,
row counts must match. Column *names* are ignored (candidates name columns freely);
columns are aligned as: text/date columns first, then numeric columns.

This is NOT nao. It lets us score any agent's SQL offline, for the blind-agent experiment.

    python evals/grade.py <answers_dir> [<answers_dir> ...]
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "warehouse" / "travel.duckdb"
TESTS = ROOT / "context" / "tests"


def normalize(df: pd.DataFrame) -> list[tuple]:
    text = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]
    num = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    rows = []
    for _, r in df[text + num].iterrows():
        rows.append(tuple([str(pd.Timestamp(r[c]).date()) if "date" in str(df[c].dtype) or "time" in str(df[c].dtype) else str(r[c]) for c in text]
                          + [float(r[c]) for c in num]))
    return sorted(rows, key=lambda t: tuple(str(x) for x in t[: len(text)]))


def same(a: list[tuple], b: list[tuple]) -> tuple[bool, str]:
    if len(a) != len(b):
        return False, f"row count {len(a)} vs expected {len(b)}"
    for ra, rb in zip(a, b):
        if len(ra) != len(rb):
            return False, f"column count {len(ra)} vs expected {len(rb)}"
        for x, y in zip(ra, rb):
            if isinstance(y, float):
                if not isinstance(x, float) or not np.isclose(round(x, 4), round(y, 4), rtol=1e-5, atol=1e-8):
                    if isinstance(x, float) and y and any(np.isclose(x * k, y, rtol=1e-3) for k in (100, 1000, 0.01, 0.001)):
                        return False, f"UNIT/FORMAT: {x:.4f} vs expected {y:.4f} (same value, different unit)"
                    return False, f"value {x!r} vs expected {y:.4f}"
            elif x != y:
                return False, f"value {x!r} vs expected {y!r}"
    return True, "match"


def main(dirs: list[str]):
    con = duckdb.connect(str(DB), read_only=True)
    tests = {yaml.safe_load(open(f))["name"]: yaml.safe_load(open(f)) for f in sorted(glob.glob(str(TESTS / "*.yml")))}
    report = {}
    for d in dirs:
        key = str(Path(d).resolve().relative_to(ROOT)) if str(Path(d).resolve()).startswith(str(ROOT)) else d
        res = {}
        for name, t in tests.items():
            if "sql" not in t:
                txt = Path(d, f"{name}.txt")
                body = txt.read_text().strip() if txt.exists() else ""
                res[name] = (body.upper().startswith("CLARIFY"), body[:140] or "missing")
                continue
            f = Path(d, f"{name}.sql")
            if not f.exists():
                res[name] = (False, "missing")
                continue
            try:
                got = normalize(con.sql(f.read_text()).df())
            except Exception as e:  # noqa: BLE001
                res[name] = (False, f"error: {e}"[:140])
                continue
            res[name] = same(got, normalize(con.sql(t["sql"]).df()))
        report[key] = res
        passed = sum(ok for ok, _ in res.values())
        print(f"\n== {d}: {passed}/{len(res)} passed")
        for n, (ok, msg) in res.items():
            print(f"  {'PASS' if ok else 'FAIL'}  {n:45s} {msg}")
    out = ROOT / "evals" / "last_grade.json"
    json.dump({d: {n: {"passed": ok, "message": m} for n, (ok, m) in r.items()} for d, r in report.items()},
              open(out, "w"), indent=2)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python evals/grade.py <answers_dir> [...]")
    main(sys.argv[1:])
