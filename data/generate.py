"""Generate the synthetic travel-insurance warehouse used in the demo.

Everything here is fictional. Seeded, so the numbers in the talking points are reproducible.

    python data/generate.py            # writes warehouse/travel.duckdb

Codes mimic a legacy policy-admin system: txn_code 10 = payment, 20 = case reserve change,
40 = recovery; policy_status IF / EX / CX with cancel_reason_code FL = free-look.

Deliberate "traps" (things an analyst only knows from institutional knowledge):
  T1  Loss ratio uses EARNED premium (mart.earned_premium_monthly), not written premium.
  T2  Recoveries (airline / subrogation) are stored as POSITIVE amounts and must be subtracted.
  T3  Partner ZZTEST is a QA test partner; its rows are not real business.
  T4  Free-look cancellations are fully refunded: they carry written premium but earn nothing.
  T5  "2025 loss ratio" means ACCIDENT year 2025 (loss_date), not report year or purchase year.
Hidden finding: Caribbean trip-cancellation claims spike in Aug-Oct 2025 (hurricane season).
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

SEED = 20261215  # summit date
VALUATION = date(2026, 9, 30)
START = date(2024, 1, 1)
N_POLICIES = 60_000

REGIONS = {  # weight, base claim prob multiplier, avg trip cost
    "Europe": (0.34, 1.00, 3200),
    "North America": (0.22, 0.85, 1900),
    "Caribbean": (0.14, 1.05, 2600),
    "Asia": (0.13, 1.10, 4100),
    "Latin America": (0.10, 1.15, 2900),
    "Oceania": (0.07, 0.95, 5200),
}
PRODUCTS = {"Basic": (0.45, 0.045), "Plus": (0.38, 0.062), "Premier": (0.17, 0.085)}  # weight, rate on trip cost
AGE_BANDS = {"18-34": (0.27, 0.85), "35-54": (0.36, 0.95), "55-69": (0.27, 1.15), "70+": (0.10, 1.50)}
PARTNERS = [
    ("SKYW", "SkyWay Airlines", "airline"),
    ("ROAM", "RoamBooking.com", "online travel agency"),
    ("CRUZ", "Coral Cruises", "cruise line"),
    ("DIRE", "Direct web", "direct"),
    ("ZZTEST", "ZZ Partner", "internal"),
]
PARTNER_W = [0.33, 0.37, 0.12, 0.17, 0.01]
COVERAGES = {  # share of claims, mean severity, sd(log)
    "trip_cancellation": (0.42, 1700, 0.7),
    "medical": (0.23, 3600, 1.1),
    "baggage": (0.20, 650, 0.6),
    "travel_delay": (0.15, 320, 0.5),
}


def pick(rng, d: dict, n):
    keys = list(d)
    w = np.array([v[0] for v in d.values()])
    return rng.choice(keys, size=n, p=w / w.sum())


def build(rng: np.random.Generator):
    n = N_POLICIES
    span = (VALUATION - START).days
    purchase = pd.Timestamp(START) + pd.to_timedelta(rng.integers(0, span, n), "D")
    lead = rng.gamma(2.0, 22, n).astype(int) + 3
    length = rng.gamma(2.5, 3.2, n).astype(int) + 2
    depart = purchase + pd.to_timedelta(lead, "D")
    ret = depart + pd.to_timedelta(length, "D")

    region = pick(rng, REGIONS, n)
    product = pick(rng, PRODUCTS, n)
    age = pick(rng, AGE_BANDS, n)
    partner = rng.choice([p[0] for p in PARTNERS], size=n, p=PARTNER_W)
    # cruise partner skews Caribbean
    cruise = partner == "CRUZ"
    region[cruise & (rng.random(n) < 0.55)] = "Caribbean"

    trip_cost = np.round(np.array([REGIONS[r][2] for r in region]) * rng.lognormal(0, 0.45, n), 2)
    rate = np.array([PRODUCTS[p][1] for p in product])
    agef = np.array([AGE_BANDS[a][1] for a in age])
    premium = np.round(trip_cost * rate * (0.8 + 0.4 * agef / 1.5), 2)

    free_look = rng.random(n) < 0.035
    cancel_date = purchase + pd.to_timedelta(rng.integers(1, 14, n), "D")
    status = np.where(free_look, "CX", np.where(pd.to_datetime(ret) <= pd.Timestamp(VALUATION), "EX", "IF"))

    pol = pd.DataFrame({
        "policy_id": [f"P{100000 + i}" for i in range(n)],
        "partner_code": partner,
        "product": product,
        "purchase_date": pd.to_datetime(purchase).date,
        "departure_date": pd.to_datetime(depart).date,
        "return_date": pd.to_datetime(ret).date,
        "destination_region": region,
        "traveler_age_band": age,
        "trip_cost_usd": trip_cost,
        "written_premium_usd": premium,
        "policy_status": status,
        "cancel_reason_code": np.where(free_look, "FL", None),
        "cancel_date": pd.to_datetime(cancel_date).date,
    })
    pol.loc[~free_look, "cancel_date"] = None
    return pol


def earned(pol: pd.DataFrame) -> pd.DataFrame:
    """Pro-rata daily earning from purchase_date to return_date, cut at valuation. Free-look earns 0."""
    rows = []
    val = pd.Timestamp(VALUATION)
    live = pol[pol.policy_status != "CX"]
    for r in live.itertuples(index=False):
        s, e = pd.Timestamp(r.purchase_date), pd.Timestamp(r.return_date)
        days = (e - s).days + 1
        daily = r.written_premium_usd / days
        end = min(e, val)
        m = s.to_period("M")
        while m.start_time <= end:
            a, b = max(s, m.start_time), min(end, m.end_time.normalize())
            d = (b - a).days + 1
            if d > 0:
                rows.append((r.policy_id, m.start_time.date(), round(daily * d, 2)))
            m += 1
    return pd.DataFrame(rows, columns=["policy_id", "accounting_month", "earned_premium_usd"])


def claims(rng, pol: pd.DataFrame):
    live = pol[pol.policy_status != "CX"].reset_index(drop=True)
    base = 0.068
    rmult = live.destination_region.map(lambda r: REGIONS[r][1]).to_numpy()
    amult = live.traveler_age_band.map(lambda a: AGE_BANDS[a][1]).to_numpy()
    p = base * rmult * amult
    has = rng.random(len(live)) < p
    c = live[has].copy()

    cov = pick(rng, COVERAGES, len(c))
    # Hurricane season 2025: extra Caribbean trip-cancellation claims for trips departing Aug-Oct 2025
    dep = pd.to_datetime(c.departure_date)
    hurr_pool = live[(live.destination_region == "Caribbean")
                     & (pd.to_datetime(live.departure_date) >= "2025-08-01")
                     & (pd.to_datetime(live.departure_date) <= "2025-10-31")]
    extra = hurr_pool.sample(frac=0.25, random_state=7).copy()
    extra_cov = np.array(["trip_cancellation"] * len(extra))
    is_cat = np.concatenate([np.zeros(len(c), bool), np.ones(len(extra), bool)])
    c = pd.concat([c, extra], ignore_index=True)
    cov = np.concatenate([cov, extra_cov])
    dep = pd.to_datetime(c.departure_date)

    # loss date: cancellation happens before departure; others during the trip
    pur = pd.to_datetime(c.purchase_date)
    ret = pd.to_datetime(c.return_date)
    u = rng.random(len(c))
    tc = (cov == "trip_cancellation")
    loss = pd.DatetimeIndex(np.where(tc, (pur + (dep - pur) * u).to_numpy(), (dep + (ret - dep) * u).to_numpy())).normalize()
    report = loss + pd.to_timedelta(rng.gamma(1.5, 9, len(c)).astype(int), "D")

    sev = np.array([COVERAGES[k][1] * rng.lognormal(-COVERAGES[k][2] ** 2 / 2, COVERAGES[k][2]) for k in cov])
    sev = np.minimum(sev, c.trip_cost_usd.to_numpy() * np.where(cov == "trip_cancellation", 1.0, 3.0))

    keep = np.asarray(report <= pd.Timestamp(VALUATION))
    c, cov, loss, report, sev = c[keep], cov[keep], loss[keep], report[keep], sev[keep]
    is_cat = is_cat[keep]
    n = len(c)
    age_days = (pd.Timestamp(VALUATION) - report).days.to_numpy()
    p_closed = 1 - np.exp(-age_days / 45)
    closed = rng.random(n) < p_closed
    denied = closed & (rng.random(n) < 0.11)
    status = np.where(~closed, "open", np.where(denied, "closed_denied", "closed_paid"))

    cl = pd.DataFrame({
        "claim_id": [f"C{500000 + i}" for i in range(n)],
        "policy_id": c.policy_id.to_numpy(),
        "coverage": cov,
        "loss_date": loss.date,
        "report_date": report.date,
        "claim_status": status,
        # claims team tags claims caused by a declared catastrophe event
        "cat_event_code": np.where(is_cat, "HU25", None),
    })

    tx = []
    tid = 0
    for i, r in enumerate(cl.itertuples(index=False)):
        rep = pd.Timestamp(r.report_date)
        ult = float(sev[i])
        reserve0 = round(ult * rng.uniform(0.8, 1.3), 2)
        tid += 1; tx.append((f"T{tid:07d}", r.claim_id, rep.date(), "20", reserve0))
        if r.claim_status == "open":
            continue
        close = min(rep + pd.Timedelta(days=int(rng.gamma(2, 15)) + 3), pd.Timestamp(VALUATION))
        if r.claim_status == "closed_denied":
            tid += 1; tx.append((f"T{tid:07d}", r.claim_id, close.date(), "20", -reserve0))
            continue
        # one or two payments
        parts = [ult] if rng.random() < 0.6 else [ult * 0.6, ult * 0.4]
        for k, amt in enumerate(parts):
            d = rep + (close - rep) * ((k + 1) / len(parts))
            tid += 1; tx.append((f"T{tid:07d}", r.claim_id, d.date(), "10", round(amt, 2)))
        tid += 1; tx.append((f"T{tid:07d}", r.claim_id, close.date(), "20", -reserve0))
        if r.coverage in ("trip_cancellation", "baggage", "travel_delay") and rng.random() < 0.22:
            rec = round(ult * rng.uniform(0.15, 0.6), 2)
            d = min(close + pd.Timedelta(days=int(rng.integers(10, 90))), pd.Timestamp(VALUATION))
            tid += 1; tx.append((f"T{tid:07d}", r.claim_id, d.date(), "40", rec))
    # QA team's test claims on the ZZTEST partner: round amounts, never real losses (trap T3)
    qa = pol[(pol.partner_code == "ZZTEST") & (pol.policy_status != "CX")
             & (pd.to_datetime(pol.departure_date) < "2026-06-01")].sample(60, random_state=3)
    qa_rows = []
    for j, r in enumerate(qa.itertuples(index=False)):
        cid = f"C{900000 + j}"
        ld = pd.Timestamp(r.departure_date)
        qa_rows.append((cid, r.policy_id, "medical", ld.date(), (ld + pd.Timedelta(days=1)).date(), "closed_paid", None))
        tid += 1; tx.append((f"T{tid:07d}", cid, (ld + pd.Timedelta(days=2)).date(), "10", 9999.99))
    cl = pd.concat([cl, pd.DataFrame(qa_rows, columns=cl.columns)], ignore_index=True)
    txdf = pd.DataFrame(tx, columns=["txn_id", "claim_id", "txn_date", "txn_code", "amount_usd"])
    return cl, txdf


def main(out: Path):
    rng = np.random.default_rng(SEED)
    pol = build(rng)
    ep = earned(pol)
    cl, tx = claims(rng, pol)
    partners = pd.DataFrame(PARTNERS, columns=["partner_code", "partner_name", "channel"])

    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()
    con = duckdb.connect(str(out))
    con.execute("CREATE SCHEMA mart; CREATE SCHEMA staging;")
    for name, df in [("policies", pol), ("earned_premium_monthly", ep), ("claims", cl),
                     ("claim_transactions", tx), ("partners", partners)]:
        con.register("df", df)
        con.execute(f"CREATE TABLE mart.{name} AS SELECT * FROM df")
        con.unregister("df")
    # a raw staging table the agent should never see
    con.execute("""CREATE TABLE staging.raw_policy_feed AS
                   SELECT policy_id, partner_code, written_premium_usd AS prem, purchase_date AS dt,
                          'v1' AS feed_version FROM mart.policies""")
    for t, cnt in con.execute("""SELECT schema_name||'.'||table_name,
            estimated_size FROM duckdb_tables() ORDER BY 1""").fetchall():
        print(f"{t:40s} {cnt:>9,}")
    con.close()


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "warehouse/travel.duckdb"))
