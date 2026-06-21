# NOVA Housing & Remote Work Migration Analysis

**Author:** Emmalynn Verma  
**Tools:** Python (Pandas, Matplotlib) · Tableau Public  
**Data:** Zillow ZHVI · BLS ATUS Telework Data

## Project Goal
Analyze how remote work adoption during COVID-19 (2020–2022) correlated with home value appreciation across four Northern Virginia counties: Fairfax, Loudoun, Prince William, and Arlington.

## Key Findings
| County | Jan 2020 Baseline | Peak (2021–22) | % Rise | Dec 2025 Value |
|---|---|---|---|---|
| Loudoun | $610,503 | $837,887 | **+37.2%** | $926,054 |
| Prince William | $435,101 | $579,947 | **+33.3%** | $634,533 |
| Fairfax | $623,908 | $780,373 | **+25.1%** | $840,602 |
| Arlington | $694,752 | $789,435 | **+13.6%** | $821,673 |

- **Loudoun County** saw the largest surge (+37.2%), coinciding with remote work peaking at 35.4% nationally in Q2 2020. Its outer-ring location, lower baseline price, and more available land made it the top destination for remote-enabled buyers.
- **Arlington** saw the smallest increase (+13.6%) — already dense, expensive, and close to DC, it saw less suburban migration demand.
- **All four counties** remain well above 2020 baselines even after the 2022 rate hike cooldown, suggesting the remote work shift created lasting demand.

## Dashboard
🔗 [View Interactive Tableau Dashboard](YOUR_TABLEAU_LINK_HERE)

## Files
| File | Description |
|---|---|
| `nova_housing_analysis.py` | Full Python analysis script |
| `nova_county_monthly_avg.csv` | County-level monthly averages + index (Tableau input) |
| `nova_zip_home_values.csv` | ZIP-level monthly home values |
| `bls_remote_work_pct.csv` | BLS national remote work % by quarter |
| `nova_county_summary.csv` | Summary stats per county |
| `nova_housing_analysis.png` | Python-generated 3-panel chart |

## Data Sources
- [Zillow Research Data — ZHVI](https://www.zillow.com/research/data/)
- [BLS American Time Use Survey (ATUS)](https://www.bls.gov/tus/)

## How to Run
```bash
pip install pandas matplotlib
python nova_housing_analysis.py
```
Place the Zillow CSV in the same directory before running.
