# Methodology

This document describes the data sources, calculations, and assumptions behind every headline figure in this investigation.

---

## Data Sources

| Source | What We Used | Access Method | As Of |
|--------|-------------|---------------|-------|
| HHSC PFD Wage Calculator | $10.60 target wage (cell B7), per-service wage assumptions | Direct download (XLSX) | Feb 7, 2025 |
| HHSC PFD LTSS Rate Tables | Current Medicaid daily/hourly rates by program and LON | Direct download (XLSX) | SFY 2026-27 |
| BLS OEWS (Texas) | Home health aide employment (314,610) and wages ($12.19 mean) | API v2, SOC 31-1120 | May 2024 |
| BLS CPI-U South | Inflation data, series CUUR0300SA0 | API v2 | 2010-2025 |
| LBB Rider Packets | HCS slots funded per biennium, waitlist size | Public PDFs, 83rd-88th Legislatures | 2014-2025 |
| NCI Staff Stability Survey | National DSP turnover rate (43.5%) | Published report | 2023 |
| Market wage data | Buc-ee's ($18), Amazon ($17.50), H-E-B ($15), Walmart ($14) | Public job postings, news reporting | 2024-2025 |

Full source list with direct URLs: [references/sources.yaml](references/sources.yaml)

---

## Calculations

### Inflation Adjustment ($14.37 and $7.82)

**Series:** BLS CPI-U, South Region, All Items (CUUR0300SA0) — not seasonally adjusted.

**Base year:** 2015 (conservative estimate of when HHSC locked $10.60 into rate methodology).

**"What $10.60 should be today":**

```
should_be = $10.60 * (CPI_2025 / CPI_2015)
          = $10.60 * (318.5 / 234.8)
          ≈ $14.37
```

**"What $10.60 actually buys"** (real purchasing power in 2015 dollars):

```
real_value = $10.60 * (CPI_2015 / CPI_2025)
           = $10.60 * (234.8 / 318.5)
           ≈ $7.82
```

This is the same method the federal government uses to adjust Social Security payments.

**Code:** [src/texas_hhcs/cpi.py](src/texas_hhcs/cpi.py) — `deflate_wage()`, `build_erosion_table()`

### Statewide Wage Gap (~$4.8 billion/yr)

```
gap_per_worker = ($18.00 - $10.60) * 2,080 hours/yr = $15,392
statewide      = $15,392 * 314,610 workers = ~$4.84 billion
```

- $18.00 = Buc-ee's entry-level wage (publicly posted)
- $10.60 = HHSC wage assumption (PFD Wage Calculator cell B7)
- 314,610 = BLS OEWS May 2024 Texas employment for SOC 31-1120
- 2,080 = standard full-time hours (40 hrs/wk * 52 wks)

### Waitlist Timeline (87 years)

```
years = ~130,000 people / ~1,500 slots per year ≈ 87
```

- 130,000 = approximate combined IDD waiver interest list (HCS, TxHmL, CLASS, DBMD) as of 88th Legislature, before HHSC list cleanup reduced it to ~100,000
- 1,500 = average slots funded per year across the 83rd-88th Legislatures (total ~13,817 slots / ~10 years)

The README rounds to "87 years" based on the pre-cleanup list. Using the post-cleanup 100,000 figure yields ~67 years.

### Lifetime Earnings Gap ($624,424)

30-year career comparison with 2% annual raises for both paths:

```
cumulative = sum(start_wage * 2,080 * 1.02^(year-1) for year in 1..30)

Care worker:  $10.60 start → $896,739 cumulative
Buc-ee's:     $18.00 start → $1,521,163 cumulative
Gap:          $624,424
```

The gap is not sensitive to the raise rate — at 0% raises it's $462K; at 3% it's $696K.

### Staffing Model (24/7 Coverage)

A single staff position covering 24 hours/day, 7 days/week requires:

```
base FTEs    = 168 hrs/wk / 40 hrs = 4.2
with absence = 4.2 * 1.18 = ~4.96 FTEs
```

The 1.18 absence factor accounts for PTO, sick time, and training days.

**Code:** [src/texas_hhcs/staffing.py](src/texas_hhcs/staffing.py) — `StaffingModel`

### Turnover Cost ($2,500 per hire)

Per-hire replacement cost of $2,500 includes recruiting, background checks, onboarding, and training. Source: NCI and PHI national estimates. Full turnover cost per 4-bed house (~$14,250/yr) adds overtime coverage during vacancies and quality/safety incident costs.

---

## Figure Audit

Every headline number traced to its source, formula, generating code, and verification test.

| Figure | Type | Formula / Source | Generated In | Verified By |
|--------|------|-----------------|--------------|-------------|
| **$10.60/hr** | Source observation | HHSC PFD Wage Calculator, cell B7 | `00_data_collection.ipynb` cell 3 | `test_headline_figures.py` |
| **$7.82/hr** | Derived estimate | $10.60 * (CPI_2015 / CPI_2025) | `03_wage_stagnation.ipynb` cell 5 | `TestInflationErosion::test_real_purchasing_power_approximately_7_82` |
| **$14.37/hr** | Derived estimate | $10.60 * (CPI_2025 / CPI_2015) | `03_wage_stagnation.ipynb` cell 7 | `TestInflationErosion::test_should_be_wage_approximately_14_37` |
| **$12.19/hr** | Source observation | BLS OEWS May 2024, SOC 31-1120, hourly mean | `00_data_collection.ipynb` cell 10 | `bls_oews_texas_2024.csv` |
| **314,610 workers** | Source observation | BLS OEWS May 2024, SOC 31-1120, employment | `00_data_collection.ipynb` cell 10 | `bls_oews_texas_2024.csv` |
| **~$4.8B/yr wage gap** | Modeled comparison | ($18.00 - $10.60) * 2,080 hrs * 314,610 | `03_wage_stagnation.ipynb` cell 9 | `TestStatewideWageGap::test_annual_gap_approximately_4_8b` |
| **100,000+ waitlist** | Source observation | HHSC Interest List data, LBB rider packets | `02_waitlist_access.ipynb` cell 3 | LBB 88th Legislature rider packet |
| **87 years** | Derived estimate | ~130,000 / ~1,500 slots per year | `02_waitlist_access.ipynb` cell 4 | `TestWaitlistTimeline::test_years_to_clear` |
| **~50% turnover** | Source observation | NCI Staff Stability Survey 2023 | `02_waitlist_access.ipynb` cell 6 | National Core Indicators report |
| **$624,424 gap** | Modeled comparison | 30-yr cumulative at 2% raises, $10.60 vs $18.00 | `03_wage_stagnation.ipynb` cell 12 | `TestLifetimeEarningsGap::test_gap_approximately_624k` |

**Type key:**
- **Source observation** — read directly from a government dataset or official report
- **Derived estimate** — calculated from source data using a documented formula (e.g., inflation adjustment)
- **Modeled comparison** — scenario built on stated assumptions (e.g., career length, raise rate, employer comparison)

---

## Limitations

- **BLS wage data is May 2024**, not real-time. Wages may have shifted since publication.
- **The $10.60 base year is estimated at ~2015.** The exact year HHSC locked this number into rate methodology is not publicly documented. We use 2015 as a conservative estimate; if the actual year is earlier, the erosion is worse.
- **Turnover cost ($2,500/hire) and rate (~50%) are from national surveys** (NCI 2023, PHI), not Texas-specific data. Texas likely tracks at or above national averages given its below-average wages.
- **Buc-ee's as a comparison is illustrative.** It represents the upper end of entry-level retail. Other retailers pay less ($14-17/hr). The core finding — that Medicaid-funded care work pays less than entry-level retail — holds regardless of which retailer is used.
- **Waitlist slot pace (1,500/yr) is averaged** across the 83rd-88th Legislatures. Individual sessions funded between 1,375 and 3,292 slots.
- **The wage gap calculation assumes all 314,610 home health aides are Medicaid-funded.** In practice, some work in private-pay settings. This makes our $4.8B figure an upper bound.
- **Provider overhead ($45,000/yr for a 4-bed home) is a conservative estimate** based on industry reporting, not audited financial data from specific providers.
