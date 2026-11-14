"""Run every reference SQL in context/tests and the evidence queries in sql/. Fails loudly."""
import glob
from pathlib import Path

import duckdb
import yaml

ROOT = Path(__file__).resolve().parents[1]
con = duckdb.connect(str(ROOT / "warehouse" / "travel.duckdb"), read_only=True)
for f in sorted(glob.glob(str(ROOT / "context" / "tests" / "*.yml"))):
    t = yaml.safe_load(open(f))
    if "sql" in t:
        df = con.sql(t["sql"]).df()
        print(f"[test] {t['name']:45s} rows={len(df):3d}  {df.iloc[0].to_dict() if len(df) == 1 else ''}")
for f in sorted(glob.glob(str(ROOT / "sql" / "*.sql"))):
    print(f"\n[sql] {Path(f).name}")
    print(con.sql(Path(f).read_text()).df().to_string(index=False))
