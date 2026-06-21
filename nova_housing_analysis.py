"""
NOVA Housing & Remote Work Migration Analysis
=============================================
Author: Emmalynn Verma
Tools: Python (Pandas, Matplotlib, Seaborn), Zillow ZHVI Data, BLS Telework Data

Project Goal:
    Analyze how remote work adoption during and after COVID-19 (2020–2022)
    correlated with home value appreciation across four Northern Virginia counties:
    Fairfax, Loudoun, Prince William, and Arlington.

Data Sources:
    - Zillow Home Value Index (ZHVI): ZIP-level, mid-tier SFR/Condo
      https://www.zillow.com/research/data/
    - BLS American Time Use Survey (ATUS) — telework rates, national
      https://www.bls.gov/tus/
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── CONFIGURATION ────────────────────────────────────────────────────────────

ZHVI_PATH = "Zip_zhvi_uc_sfrcondo_tier_0_33_0_67_sm_sa_month.csv"

NOVA_COUNTIES = [
    'Fairfax County',
    'Loudoun County',
    'Prince William County',
    'Arlington County'
]

COLORS = {
    'Fairfax County':       '#d63384',
    'Loudoun County':       '#9b59b6',
    'Prince William County':'#3498db',
    'Arlington County':     '#e67e22'
}

BG         = '#fafaf8'
GRID_COLOR = '#e2e0e8'

# ── STEP 1: LOAD & FILTER TO NOVA ────────────────────────────────────────────

print("Loading Zillow ZHVI data...")
zhvi = pd.read_csv(ZHVI_PATH)

nova = zhvi[zhvi['CountyName'].isin(NOVA_COUNTIES)].copy()
print(f"  → {len(nova)} ZIP codes found across NOVA counties")

# ── STEP 2: RESHAPE FROM WIDE TO LONG FORMAT ─────────────────────────────────

id_cols   = ['RegionName', 'CountyName', 'City']
date_cols = [c for c in nova.columns if c.startswith('20')]

nova_long = nova[id_cols + date_cols].melt(
    id_vars=id_cols, var_name='date', value_name='home_value'
)
nova_long['date'] = pd.to_datetime(nova_long['date'])
nova_long = nova_long.dropna(subset=['home_value'])

# Filter to 2019–2025 for analysis window
nova_long = nova_long[
    (nova_long['date'] >= '2019-01-01') &
    (nova_long['date'] <= '2025-12-31')
]

print(f"  → {len(nova_long):,} data points after reshape and filter")

# ── STEP 3: COUNTY-LEVEL MONTHLY AVERAGES ────────────────────────────────────

county_monthly = (
    nova_long
    .groupby(['CountyName', 'date'])['home_value']
    .mean()
    .reset_index()
)

# ── STEP 4: INDEX TO JAN 2020 BASELINE (100) ─────────────────────────────────

baseline = (
    county_monthly[county_monthly['date'] == '2020-01-31']
    .set_index('CountyName')['home_value']
)

county_monthly['indexed'] = county_monthly.apply(
    lambda r: r['home_value'] / baseline.get(r['CountyName'], np.nan) * 100,
    axis=1
)

# ── STEP 5: KEY FINDINGS ─────────────────────────────────────────────────────

print("\n" + "="*60)
print("KEY FINDINGS — NOVA Home Value Analysis (2020–2025)")
print("="*60)

findings = {}
for county in NOVA_COUNTIES:
    sub = (
        county_monthly[county_monthly['CountyName'] == county]
        .set_index('date')['home_value']
        .sort_index()
    )
    jan2020   = sub.loc['2020-01-31']
    peak_val  = sub['2021':'2022'].max()
    peak_date = sub['2021':'2022'].idxmax().strftime('%b %Y')
    latest    = sub.iloc[-1]
    pct_rise  = (peak_val  - jan2020) / jan2020 * 100
    pct_now   = (latest    - jan2020) / jan2020 * 100

    findings[county] = {
        'Jan 2020 Baseline': jan2020,
        'Peak Value':        peak_val,
        'Peak Date':         peak_date,
        '% Rise to Peak':    pct_rise,
        'Dec 2025 Value':    latest,
        '% Change vs 2020':  pct_now,
    }

    name = county.replace(' County', '')
    print(f"\n{name}")
    print(f"  Baseline (Jan 2020):  ${jan2020:>10,.0f}")
    print(f"  Peak ({peak_date}):    ${peak_val:>10,.0f}  (+{pct_rise:.1f}%)")
    print(f"  Dec 2025:             ${latest:>10,.0f}  (+{pct_now:.1f}% vs 2020)")

# ── STEP 6: BLS REMOTE WORK DATA (NATIONAL) ──────────────────────────────────
# Source: BLS ATUS Supplement — % workers who worked from home on days worked
# Key note: NOVA remote work likely higher than national avg (fed/contractor heavy)

remote_df = pd.DataFrame({
    'date': pd.to_datetime([
        '2019-01-01','2019-07-01',
        '2020-01-01','2020-04-01','2020-07-01',
        '2021-01-01','2021-07-01',
        '2022-01-01','2022-07-01',
        '2023-01-01','2023-07-01',
        '2024-01-01','2024-07-01',
        '2025-01-01'
    ]),
    'remote_pct': [
        5.7,  5.9,
        8.2,  35.4, 28.1,
        26.1, 22.3,
        17.9, 15.2,
        12.7, 11.9,
        11.1, 10.8,
        11.3
    ]
})

# ── STEP 7: BUILD 3-PANEL VISUALIZATION ──────────────────────────────────────

fig = plt.figure(figsize=(16, 13), facecolor=BG)
fig.suptitle(
    'NOVA Housing & Remote Work Migration Analysis  |  2019–2025',
    fontsize=15, fontweight='bold', color='#0f0e11', y=0.98
)

gs  = fig.add_gridspec(2, 2, hspace=0.42, wspace=0.32,
                        left=0.07, right=0.97, top=0.93, bottom=0.07)
ax1 = fig.add_subplot(gs[0, :])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[1, 1])


def style_ax(ax):
    ax.set_facecolor(BG)
    ax.spines[['top','right']].set_visible(False)
    ax.spines[['left','bottom']].set_color(GRID_COLOR)
    ax.tick_params(colors='#5a5566', labelsize=9)
    ax.yaxis.label.set_color('#5a5566')
    ax.xaxis.label.set_color('#5a5566')
    ax.grid(axis='y', color=GRID_COLOR, linewidth=0.8, zorder=0)


# Panel 1: Indexed home values + remote work overlay
style_ax(ax1)
ax1_r = ax1.twinx()
ax1_r.set_facecolor(BG)

for county in NOVA_COUNTIES:
    sub = county_monthly[county_monthly['CountyName'] == county]
    ax1.plot(sub['date'], sub['indexed'],
             color=COLORS[county], linewidth=2.2,
             label=county.replace(' County', ''), zorder=3)

ax1_r.plot(remote_df['date'], remote_df['remote_pct'],
           color='#888', linewidth=1.5, linestyle='--',
           label='US Remote Work %', zorder=2)
ax1_r.fill_between(remote_df['date'], remote_df['remote_pct'],
                   alpha=0.08, color='#888')
ax1_r.set_ylabel('Remote Work % (US)', color='#888', fontsize=9)
ax1_r.tick_params(colors='#888', labelsize=8)
ax1_r.spines[['top','left']].set_visible(False)
ax1_r.spines[['right','bottom']].set_color(GRID_COLOR)

ax1.axvline(pd.Timestamp('2020-03-01'), color='#d63384', linewidth=1,
            linestyle=':', alpha=0.6)
ax1.text(pd.Timestamp('2020-03-15'), 98, 'COVID-19\nLockdowns',
         fontsize=7.5, color='#d63384', alpha=0.85)
ax1.axvline(pd.Timestamp('2022-03-01'), color='#3498db', linewidth=1,
            linestyle=':', alpha=0.5)
ax1.text(pd.Timestamp('2022-04-01'), 98, 'Fed Rate\nHikes Begin',
         fontsize=7.5, color='#3498db', alpha=0.85)

ax1.set_title('Home Value Index by County  (Jan 2020 = 100)  vs. US Remote Work Rate',
              fontsize=11, color='#0f0e11', pad=8)
ax1.set_ylabel('Home Value Index (Jan 2020 = 100)', fontsize=9)
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f'))

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_r.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=8.5,
           loc='upper left', framealpha=0.85, edgecolor=GRID_COLOR)

# Panel 2: % Rise to peak
style_ax(ax2)
ordered = ['Loudoun County', 'Prince William County', 'Fairfax County', 'Arlington County']
rises   = [findings[c]['% Rise to Peak'] for c in ordered]
labels  = [c.replace(' County', '') for c in ordered]
clrs    = [COLORS[c] for c in ordered]

bars2 = ax2.barh(labels[::-1], rises[::-1], color=clrs[::-1],
                 edgecolor='none', height=0.55, zorder=3)
for bar, val in zip(bars2, rises[::-1]):
    ax2.text(val + 0.4, bar.get_y() + bar.get_height()/2,
             f'+{val:.1f}%', va='center', fontsize=9,
             color='#0f0e11', fontweight='bold')
ax2.set_title('Peak Home Value Increase\n(Jan 2020 → Peak 2021–22)',
              fontsize=10, color='#0f0e11')
ax2.set_xlabel('% Increase', fontsize=9)
ax2.set_xlim(0, 45)

# Panel 3: Dec 2025 absolute values
style_ax(ax3)
dec25 = {c: findings[c]['Dec 2025 Value'] for c in NOVA_COUNTIES}
sorted_counties = sorted(dec25, key=dec25.get, reverse=True)
vals   = [dec25[c] for c in sorted_counties]
clrs3  = [COLORS[c] for c in sorted_counties]
labels3 = [c.replace(' County', '') for c in sorted_counties]

bars3 = ax3.bar(labels3, vals, color=clrs3, edgecolor='none',
                width=0.55, zorder=3)
for bar, val in zip(bars3, vals):
    ax3.text(bar.get_x() + bar.get_width()/2, val + 8000,
             f'${val/1e3:.0f}K', ha='center', fontsize=8.5,
             color='#0f0e11', fontweight='bold')
ax3.set_title('Median Home Value by County\n(Dec 2025)',
              fontsize=10, color='#0f0e11')
ax3.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f'${x/1e3:.0f}K')
)
ax3.set_ylim(0, 1050000)
ax3.tick_params(axis='x', labelsize=8.5)

fig.text(
    0.5, 0.01,
    'Data: Zillow ZHVI (ZIP-level, mid-tier SFR/condo) filtered to NOVA counties · '
    'BLS ATUS remote work data (national) · Analysis by Emmalynn Verma',
    ha='center', fontsize=7, color='#999'
)

output_path = 'nova_housing_analysis.png'
plt.savefig(output_path, dpi=180, bbox_inches='tight', facecolor=BG)
print(f"\nChart saved → {output_path}")
print("\nAnalysis complete.")
