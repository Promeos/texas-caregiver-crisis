# The Invisible Pay Cut

**How Texas's $10.60 Wage Assumption Drives a 100,000-Person Waitlist**

Texas sets the pay for Medicaid-funded caregivers using a single number buried in a state spreadsheet: **$10.60 an hour**. That number hasn't changed in over a decade. This investigation follows the money to show what happens next — poverty wages, a workforce exodus to retail, and over 100,000 Texans with disabilities stuck on a waitlist that would take **87 years** to clear.

Every number in this analysis comes from the state's own data. Every calculation has been independently verified.

---

![Texas Direct Care Worker Wages vs. Market Alternatives](reports/wage_comparison_chart.png)

*A Buc-ee's cashier earns $18/hr. An Amazon warehouse worker earns $17.50. The people Texas trusts to care for its most vulnerable residents? $10.60.*

---

![The Invisible Pay Cut — Real Wage Erosion](reports/real_wage_erosion.png)

*Because of inflation, that $10.60 buys what $7.82 bought in 2015. Workers got a 26% pay cut without anyone changing their paycheck — prices just rose around them. To have the same buying power as when the wage was set, it would need to be $14.37 today.*

---

## What We Found

| What | Number | Where it comes from |
|---|---|---|
| State's target wage for caregivers | **$10.60/hr** | HHSC wage calculator, cell B7 (updated 2/7/2025) |
| What $10.60 actually buys today | **$7.82/hr** | Adjusted for inflation (BLS Consumer Price Index, South Region) |
| What $10.60 should be with inflation | **$14.37/hr** | Same inflation data, calculated forward |
| Average pay for TX home health aides | **$12.19/hr** | Bureau of Labor Statistics, May 2024 |
| Number of these workers in Texas | **314,610** | Bureau of Labor Statistics, May 2024 |
| Total wages lost vs. entry-level retail | **~$4.8 billion/yr** | Gap between $10.60 and Buc-ee's $18, across all workers |
| People on the disability services waitlist | **100,000+** | HHSC Interest List data |
| Time to serve everyone at current pace | **87 years** | ~1,500 new slots funded per year |
| Workers who quit each year | **~50%** | National Core Indicators survey, 2023 |
| Lifetime earnings gap vs. Buc-ee's | **$624,424** | 30-year career comparison at 2% annual raises |

## Policy Brief

![Policy Brief](reports/policy_brief.png)

*A one-page summary you can print, email, or hand to a legislator. Also available as a [PDF](reports/policy_brief.pdf).*

## What Needs to Change

The 90th Texas Legislature can fix this by raising the Medicaid caregiver wage floor to **$15/hr** and tying it to inflation so it never falls behind again.

- **$15/hr** restores buying power to roughly 2015 levels and gets close to what providers need to break even (~$15.50/hr)
- **Estimated cost:** ~$4.5 billion per two-year budget cycle (~$1.8 billion from the state, the rest matched by federal funds)
- **For context:** that's *less* than the $4.8 billion care workers already lose every year by accepting below-market pay

The state doesn't need to match Buc-ee's. It needs to stop asking caregivers to finance Medicaid with their poverty.

---

## How This Analysis Works

<details>
<summary><strong>Where the data comes from</strong></summary>

Everything comes from public government sources. No records requests, no proprietary databases, no paywalls.

| Source | What we pulled | Website |
|---|---|---|
| **HHSC** (Texas Health & Human Services) | The $10.60 wage target, by program | pfd.hhs.texas.gov |
| **BLS** (Bureau of Labor Statistics) | How many home health aides work in Texas, and what they earn | bls.gov/oes/ |
| **BLS** Consumer Price Index | Inflation data for the South region | bls.gov/cpi/ |
| **LBB** (Legislative Budget Board) | How many waitlist slots the Legislature funded each session | lbb.texas.gov |
| **NCI** (National Core Indicators) | Caregiver turnover rates nationwide | nationalcoreindicators.org |
| **HHSC** Interest List | Waitlist size over time | hhs.texas.gov |

The full source list with direct links is in [references/sources.yaml](references/sources.yaml).

</details>

<details>
<summary><strong>How we did the math</strong></summary>

- **Inflation adjustment:** We used the Consumer Price Index for the South (where these workers live) to calculate what $10.60 from ~2015 is worth today. Same method the government uses to adjust Social Security payments.
- **"Lost wages" estimate:** We took the gap between $10.60 and Buc-ee's entry wage ($18/hr), multiplied by a full-time year (2,080 hours), and scaled it across all 314,610 Texas home health aides. This is conservative — many retail jobs pay even more.
- **Waitlist timeline:** We divided the 100,000-person waitlist by the average number of new slots the Legislature funds each year (~1,500). At that rate: 87 years.
- **Turnover costs:** Replacing one worker costs about $2,500 in recruiting and training alone. Add overtime to cover empty shifts and quality problems from constant new staff, and a single four-bed home loses ~$14,250/yr to turnover. A $1/hr raise for the whole house costs $10,400 — and would save $3,850.
- **Career earnings gap:** We compared 30-year earnings at $10.60/hr vs. $18/hr, both with 2% annual raises. The gap ($624,424) isn't sensitive to the raise rate — it persists no matter what you assume.

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
just build    # regenerate all charts from scratch
```

### Run the notebooks interactively

```bash
jupyter lab
```

| Notebook | What it does | Pulls data from | Creates |
|---|---|---|---|
| `00_data_collection` | Downloads wage and rate data | HHSC, BLS | CSV files in `data/processed/` |
| `03_wage_policy_analysis` | Core wage analysis | — | 6 charts |
| `04_waitlist_access` | Waitlist and turnover crisis | — | 3 charts |
| `05_wage_stagnation` | Inflation erosion and lost wages | BLS inflation API | 4 charts |
| `06_policy_brief` | Generates the one-page brief | — | PNG + PDF |

### Regenerate all charts from scratch

```bash
jupyter nbconvert --to notebook --execute notebooks/00_data_collection.ipynb
jupyter nbconvert --to notebook --execute notebooks/03_wage_policy_analysis.ipynb
jupyter nbconvert --to notebook --execute notebooks/04_waitlist_access.ipynb
jupyter nbconvert --to notebook --execute notebooks/05_wage_stagnation.ipynb
jupyter nbconvert --to notebook --execute notebooks/06_policy_brief.ipynb
```

All outputs go to `reports/`.

</details>

<details>
<summary><strong>Project file structure</strong></summary>

```
texas-caregiver-crisis/
├── notebooks/
│   ├── 00_data_collection.ipynb        — Downloads and cleans the data
│   ├── 03_wage_policy_analysis.ipynb    — Wage analysis (6 charts)
│   ├── 04_waitlist_access.ipynb        — Waitlist + turnover (3 charts)
│   ├── 05_wage_stagnation.ipynb        — Inflation erosion + lost wages (4 charts)
│   └── 06_policy_brief.ipynb           — One-page brief generator
├── src/texas_hhcs/
│   ├── cpi.py       — Pulls inflation data from BLS
│   ├── rates.py     — HHSC Medicaid rate structures
│   ├── budget.py    — Legislative budget data by session
│   ├── staffing.py  — 24/7 staffing coverage calculator
│   └── scraper.py   — Downloads HHSC rate spreadsheets
├── tests/           — Headline figure verification (pytest)
├── data/
│   ├── raw/         — Original downloaded files (HHSC rate spreadsheets)
│   └── processed/   — Cleaned, analysis-ready CSVs
├── reports/         — All charts + policy brief
└── references/
    └── sources.yaml — Every source with URLs
```

</details>

## Future Work

Provider classification (linking HHSC/TMHP/PPP records to identify provider types) and per-house profit-and-loss modeling are planned extensions.

## License

This work is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — free to share and adapt, but **you must give credit**.

> Ortiz, C. (2026). "The Invisible Pay Cut: How Texas's $10.60 Wage Assumption Drives a 100,000-Person Waitlist." Data science investigation. https://github.com/Promeos/texas-caregiver-crisis

---

*Analysis by Christopher Ortiz — March 2026*
