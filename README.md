# The Invisible Pay Cut

**How Texas's $10.60 Wage Assumption Shows Up in Public Rate Data**

Texas publishes a **$10.60 an hour** base target wage in the HHSC Personal Attendant Base Wage Calculator. That figure is directly visible in the raw workbook bundled in this repo, and it anchors the audited claim set below.

This repo was audited on 2026-03-15 to separate checked figures from illustrative or stale claims. This README now shows only figures that are either read directly from checked-in source files or derived deterministically from those files with documented formulas. Older waitlist, turnover, retail-comparison, and policy-brief outputs remain in the repo as exploratory artifacts and are intentionally not embedded here. See [VERIFICATION.md](VERIFICATION.md).

---

![Verified README Summary](reports/readme_verified_summary.png)

*Only audited figures are shown here: the HHSC base wage from the checked-in calculator, the May 2024 Texas BLS mean for SOC 31-1120, and the CPI-derived purchasing-power adjustment documented in this repo.*

---

## What We Found

| What | Number | Type | Where it comes from |
|---|---|---|---|
| HHSC base target wage in calculator | **$10.60/hr** | Source | HHSC wage calculator, cell B7 (updated 2/7/2025) |
| What $10.60 actually buys in 2025 | **$7.82/hr** | Derived | Adjusted to 2015 dollars using BLS CPI-U South |
| What $10.60 should be in 2025 dollars | **$14.37/hr** | Derived | Same CPI data, calculated forward |
| Average pay for TX home health and personal care aides | **$12.19/hr** | Source | Bureau of Labor Statistics, OEWS May 2024, SOC 31-1120 |
| Number of TX home health and personal care aides | **314,610** | Source | Bureau of Labor Statistics, OEWS May 2024, SOC 31-1120 |

*Type key: **Source** = read directly from a checked-in source file. **Derived** = calculated from source data using a documented formula. See [METHODOLOGY.md](METHODOLOGY.md) and [VERIFICATION.md](VERIFICATION.md) for the audit trail.*

The official BLS occupation title for SOC `31-1120` is **Home Health and Personal Care Aides**, which is broader than Medicaid-funded waiver staff alone.

No waitlist, turnover, retail-wage, or policy-cost claim is treated as an audited headline figure in this README.

## What the Audited Evidence Supports

The narrow conclusion that survives the audit is straightforward:

- HHSC's published calculator still starts from **$10.60/hr**
- CPI parity from a 2015 base year is about **$14.37/hr**
- The May 2024 BLS Texas mean for SOC 31-1120 is **$12.19/hr**

The repo does not yet contain a reproducible fiscal model for a specific replacement wage, a source-audited waitlist-clearing timeline, or a Texas-specific turnover estimate. Those claims were removed from the README until the underlying data is checked in and tested.

---

## How This Analysis Works

<details>
<summary><strong>Where the data comes from</strong></summary>

The audited headline set in this README uses only three source families.

| Source | What we pulled | Website |
|---|---|---|
| **HHSC** (Texas Health & Human Services) | The $10.60 wage target and per-service rate inputs | pfd.hhs.texas.gov |
| **BLS** (Bureau of Labor Statistics) | How many home health and personal care aides work in Texas, and what they earn | bls.gov/oes/ |
| **BLS** Consumer Price Index | Inflation data for the South region | bls.gov/cpi/ |

Supplementary audit files from LBB and NCI are kept locally to verify that earlier waitlist and turnover claims were overstated or misapplied. They are documented in [references/sources.yaml](references/sources.yaml) and [VERIFICATION.md](VERIFICATION.md), but they are not used as headline evidence here.

</details>

<details>
<summary><strong>How we did the math</strong></summary>

- **Inflation adjustment:** We used the Consumer Price Index for the South to calculate what $10.60 from ~2015 is worth in 2025 dollars.
- **BLS wage comparison:** We compared the HHSC base wage to the May 2024 Texas OEWS mean for SOC 31-1120 (`$12.19/hr`) and preserved the matching employment count (`314,610`) as context.
- **README visuals:** The embedded chart is regenerated from `results_summary.json`, which is itself built from the checked-in HHSC workbook, the processed BLS extract, and the documented CPI formula.
- **Excluded claims:** Waitlist, turnover, retail-wage, and policy-cost figures are omitted from the README unless they are tied back to checked-in source tables and verification tests.

For the full methodology, assumptions, and limitations, see [METHODOLOGY.md](METHODOLOGY.md).

</details>

<details>
<summary><strong>How to reproduce everything yourself</strong></summary>

### What you need

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Internet access (to pull data from BLS and HHSC — no accounts or API keys needed)

### Setup

```bash
git clone https://github.com/Promeos/texas-caregiver-crisis.git
cd texas-caregiver-crisis

# Option A: uv (recommended)
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# Option B: pip
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### Quick start (with [just](https://github.com/casey/just))

```bash
just setup    # install deps + editable package
just check    # lint + run tests
just results  # regenerate results_summary.json + audited README chart
just build    # rebuild audited notebooks + results summary
```

### Run the notebooks interactively

```bash
jupyter lab
```

**Audited notebooks** (included in `just build`):

| Notebook | What it does | Pulls data from | Creates |
|---|---|---|---|
| `00_data_collection` | Downloads wage and rate data | HHSC, BLS | CSV files in `data/processed/` |
| `01_wage_policy_analysis` | Core wage analysis | Processed CSVs | 6 charts |
| `03_wage_stagnation` | Inflation erosion and lost wages | BLS inflation API | 4 charts |

**Exploratory notebooks** (in `notebooks/exploratory/`, not in build pipeline):

| Notebook | What it does | Status |
|---|---|---|
| `02_waitlist_access` | Waitlist and turnover analysis | Uses manually entered data, not source-audited |
| `04_policy_brief` | One-page brief generator | Mixes audited and unaudited figures |

### Regenerate audited outputs

```bash
just build   # runs only audited notebooks + results generation
```

All outputs go to `reports/`. Only `reports/readme_verified_summary.png` and `results_summary.json` are produced from checked-in source data.

</details>

<details>
<summary><strong>Project file structure</strong></summary>

```
texas-caregiver-crisis/
├── notebooks/
│   ├── 00_data_collection.ipynb        — Downloads and cleans the data
│   ├── 01_wage_policy_analysis.ipynb    — Wage analysis (6 charts)
│   ├── 03_wage_stagnation.ipynb        — Inflation erosion + lost wages (4 charts)
│   └── exploratory/                    — Draft notebooks (not in build pipeline)
│       ├── 02_waitlist_access.ipynb    — Waitlist + turnover (unaudited)
│       └── 04_policy_brief.ipynb       — Old one-page brief (unaudited)
├── src/texas_hhcs/
│   ├── cpi.py       — Pulls inflation data from BLS
│   ├── rates.py     — HHSC Medicaid rate structures
│   ├── budget.py    — Legislative budget data by session
│   ├── staffing.py  — 24/7 staffing coverage calculator
│   └── scraper.py   — Downloads HHSC rate spreadsheets
├── scripts/
│   ├── generate_results.py — Produces results_summary.json
│   └── generate_verified_readme_visuals.py — Produces the audited README chart
├── tests/           — Headline figure verification (pytest)
├── data/
│   ├── raw/         — Original downloaded files (HHSC rate spreadsheets)
│   └── processed/   — Cleaned, analysis-ready CSVs
├── reports/         — All charts (README uses only audited visuals)
├── results_summary.json — Machine-verifiable headline figures
├── METHODOLOGY.md   — Full methodology, figure audit, limitations
└── references/
    └── sources.yaml — Every source with URLs
```

</details>

## Future Work

Provider classification (linking HHSC/TMHP/PPP records to identify provider types) and per-house profit-and-loss modeling are planned extensions.

## License

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — free to share and adapt, but **you must give credit**.

> Ortiz, C. (2026). "The Invisible Pay Cut: How Texas's $10.60 Wage Assumption Shows Up in Public Rate Data." Data science investigation. https://github.com/Promeos/texas-caregiver-crisis

---

*Analysis by Christopher Ortiz — March 2026*
