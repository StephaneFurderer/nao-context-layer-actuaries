"""Render the deck's charts from the warehouse, so slides never drift from the data.

    python slides/charts.py   # writes slides/public/*.svg
Palette: dataviz reference palette (light). One series per chart -> one hue; emphasis = blue vs muted gray.
"""
from pathlib import Path

import duckdb
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "slides" / "public"
OUT.mkdir(parents=True, exist_ok=True)
con = duckdb.connect(str(ROOT / "warehouse" / "travel.duckdb"), read_only=True)

BLUE, MUTED, INK, INK2, GRID, SURF = "#2a78d6", "#c9c8c2", "#0b0b0b", "#52514e", "#e7e6e1", "#fcfcfb"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 15, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": SURF, "axes.facecolor": SURF, "svg.fonttype": "none",
})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, format="svg", transparent=True)
    plt.close(fig)


# 1. Waterfall naive -> reference (one ratio per step; bars, final one emphasised)
w = con.sql((ROOT / "sql" / "waterfall_2025.sql").read_text()).df()
labels = ["Naive\n(written prem.,\nall txns, all partners)", "+ earned\npremium", "+ subtract\nrecoveries", "+ drop test\npartner\n= reference"]
fig, ax = plt.subplots(figsize=(10, 4.6))
cols = [MUTED, MUTED, MUTED, BLUE]
bars = ax.bar(labels, w.loss_ratio * 100, color=cols, width=0.55, edgecolor=SURF, linewidth=2)
for b, v in zip(bars, w.loss_ratio * 100):
    ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.1f}%", ha="center", va="bottom", color=INK, fontsize=17, fontweight="bold")
ax.set_ylim(0, 72); ax.set_ylabel("AY 2025 loss ratio (%)"); ax.yaxis.grid(True, color=GRID); ax.set_axisbelow(True)
save(fig, "waterfall.svg")

# 2. Loss ratio by region AY2025 (reference test SQL)
import yaml  # noqa: E402
t = yaml.safe_load(open(ROOT / "context" / "tests" / "loss_ratio_by_region_ay2025.yml"))
r = con.sql(t["sql"]).df().sort_values("loss_ratio")
fig, ax = plt.subplots(figsize=(10, 4.4))
cols = [BLUE if x == "Caribbean" else MUTED for x in r.destination_region]
ax.barh(r.destination_region, r.loss_ratio * 100, color=cols, height=0.6, edgecolor=SURF, linewidth=2)
for y, v in enumerate(r.loss_ratio * 100):
    ax.text(v + 1, y, f"{v:.1f}%", va="center", color=INK, fontsize=15)
ax.set_xlim(0, 110); ax.set_xlabel("AY 2025 loss ratio (%), net incurred / earned, excl. IBNR")
ax.xaxis.grid(True, color=GRID); ax.set_axisbelow(True)
save(fig, "region.svg")

# 3. Caribbean trip-cancellation claims by loss month, 2024-2025
m = con.sql("""
  SELECT DATE_TRUNC('month', c.loss_date) AS m, COUNT(*) AS n
  FROM mart.claims c JOIN mart.policies p USING (policy_id)
  WHERE p.destination_region = 'Caribbean' AND c.coverage = 'trip_cancellation'
    AND p.partner_code <> 'ZZTEST' AND c.loss_date < DATE '2026-01-01'
  GROUP BY 1 ORDER BY 1""").df()
fig, ax = plt.subplots(figsize=(10, 4.2))
hl = m.m.dt.year.eq(2025) & m.m.dt.month.between(8, 10)
ax.bar(m.m, m.n, width=24, color=[BLUE if h else MUTED for h in hl], edgecolor=SURF, linewidth=2)
peak = m.loc[m.n.idxmax()]
ax.annotate(f"Aug 2025: {int(peak.n)} claims\n(tagged HU25)", (peak.m, peak.n), xytext=(-170, -10),
            textcoords="offset points", color=INK, fontsize=14, arrowprops=dict(arrowstyle="-", color=INK2))
ax.set_ylabel("claims per loss month"); ax.yaxis.grid(True, color=GRID); ax.set_axisbelow(True)
save(fig, "caribbean_monthly.svg")
print("wrote", sorted(p.name for p in OUT.glob("*.svg")))
