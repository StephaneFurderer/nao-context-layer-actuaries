"""Run every reference SQL and assert the numbers quoted in the talk. Fails loudly on drift."""
import glob
import sys
from pathlib import Path

import duckdb
import yaml

ROOT = Path(__file__).resolve().parents[1]
con = duckdb.connect(str(ROOT / "warehouse" / "travel.duckdb"), read_only=True)
T = {yaml.safe_load(open(f))["name"]: yaml.safe_load(open(f)) for f in glob.glob(str(ROOT / "context/tests/*.yml"))}


def one(name):
    return con.sql(T[name]["sql"]).fetchall()


def q(path):
    return con.sql((ROOT / path).read_text()).fetchall()


checks = []
def expect(label, got, want, tol=0.0005):
    ok = abs(got - want) <= tol
    checks.append(ok)
    print(f"{'OK ' if ok else 'BAD'}  {label:55s} got {got:,.4f}  quoted {want:,.4f}")


expect("naive AY2025 loss ratio (TP-01: 58.1%)", q("sql/naive_loss_ratio_2025.sql")[0][0], 0.5807)
expect("reference AY2025 loss ratio (TP-01: 49.4%)", one("loss_ratio_ay2025")[0][0], 0.4941)
expect("attritional AY2025, capped (TP-06/08: 38.2%)", one("attritional_loss_ratio_ay2025")[0][0], 0.3822)
expect("attritional AY2025 if large claims DROPPED (TP-06: 32.8%)", q("sql/attritional_dropped_variant_2025.sql")[0][0], 0.3276)
reg = dict(one("loss_ratio_by_region_ay2025"))
expect("Caribbean AY2025 loss ratio (TP-10: ~100%)", reg["Caribbean"], 1.0035)
others = [v for k, v in reg.items() if k != "Caribbean"]
expect("other regions min (TP-10: 23%)", min(others), 0.226, tol=0.005)
expect("other regions max (TP-10: 48%)", max(others), 0.4757, tol=0.005)
expect("large losses AY2025 (count, >= $5k)", one("large_loss_count_ay2025")[0][0], 48)
months = {m.month: n for m, n in one("caribbean_cancellation_claims_by_month_2025")}
expect("Caribbean cancellations: max Jan-Jul 2025 (TP-10: under 20/month)", max(months[i] for i in range(1, 8)), 20)
expect("Caribbean cancellations, Aug 2025 (TP-10: ~100)", months[8], 102)
expect("Caribbean cancellations, Oct 2025 (TP-10: still ~100)", months[10], 94)
expect("policies (60k)", con.sql("select count(*) from mart.policies").fetchone()[0], 60000)
print()
for f in sorted(glob.glob(str(ROOT / "sql" / "*.sql"))):
    print(f"[sql] {Path(f).name}")
    print(con.sql(Path(f).read_text()).df().to_string(index=False), "\n")
if not all(checks):
    sys.exit("Reference numbers drifted from the talk. Update the talk or fix the data.")
print("All quoted numbers reproduce.")
