# Methodology

Audit date: 2026-03-15

This document records only the figures in this repo that are supported by checked-in files or by deterministic calculations with stated inputs. If a claim depends on external reporting, manually entered notebook values, or unsourced scenario assumptions, it is excluded from the audited headline set.

See [VERIFICATION.md](VERIFICATION.md) for the audit log and [results_summary.json](results_summary.json) for the machine-readable headline figures.

---

## Audited Scope

| Figure | Status | Support |
|--------|--------|---------|
| HHSC base target wage = **$10.60/hr** | Verified source observation | Checked-in HHSC workbook, sheet `Fiscal by Program`, cell `B7` |
| BLS Texas SOC 31-1120 hourly mean = **$12.19/hr** | Verified source observation | Checked-in processed OEWS extract |
| BLS Texas SOC 31-1120 employment = **314,610** | Verified source observation | Checked-in processed OEWS extract |
| 2025 CPI-equivalent of `$10.60` = **$14.37/hr** | Derived estimate | Deterministic formula using the repo's explicit 2015 base-year assumption |
| 2025 real purchasing power of `$10.60` = **$7.82/hr** in 2015 dollars | Derived estimate | Same CPI series and same stated assumption |

The last two figures are not direct source observations. They are outputs of a documented calculation that currently treats `$10.60` as a 2015-dollar benchmark.

---

## Data Sources

| Source file | What is used | Notes |
|-------------|--------------|-------|
| `data/raw/rates/ltss-personal-attendant-base-wage-calculator.xlsx` | HHSC target wage | Audited value is sheet `Fiscal by Program`, cell `B7` |
| `data/processed/bls_oews_texas_2024.csv` | Texas OEWS wage and employment values for SOC `31-1120` | Official occupation title is `Home Health and Personal Care Aides` |
| `tests/test_headline_figures.py` | Offline CPI verification inputs | Uses annual CPI values `234.812` for 2015 and `318.451` for 2025 |
| `data/raw/external/lbb-88th-article-ii-rider.txt` | Audit-only disconfirmation file | Used only to show that earlier `3,292` slot claims were misapplied |
| `data/raw/external/nci-state-of-the-workforce-2023.txt` | Audit-only disconfirmation file | Used only to show that earlier turnover claims were misstated or overgeneralized |

The source index with original URLs is maintained in [references/sources.yaml](references/sources.yaml).

---

## Verified Source Observations

### HHSC target wage

The repo verifies the published HHSC base target wage directly from the checked-in workbook:

- File: `data/raw/rates/ltss-personal-attendant-base-wage-calculator.xlsx`
- Sheet: `Fiscal by Program`
- Cell: `B7`
- Verified value: **$10.60/hr**

This is tested in `tests/test_headline_figures.py::TestSourceData::test_hhsc_target_wage_cell_b7_is_10_60`.

### BLS Texas wage and employment context

The repo verifies the following values from `data/processed/bls_oews_texas_2024.csv` for SOC `31-1120`:

- Hourly mean wage: **$12.19/hr**
- Employment: **314,610**
- Occupation title: **Home Health and Personal Care Aides**

This is tested in `tests/test_headline_figures.py::TestSourceData::test_bls_soc_31_1120_matches_processed_extract`.

Important scope note: SOC `31-1120` is broader than Medicaid-funded waiver staff alone. Any statewide scaling based on that occupation should be treated as an upper bound, not a direct count of Medicaid-funded workers.

---

## Derived Estimates

### CPI adjustment to 2025 dollars

The repo currently models the frozen `$10.60` wage as a **2015-dollar benchmark**. That base year is an explicit repo assumption used for the audited inflation calculation. It is **not** a verified claim that HHSC first adopted the figure in exactly 2015.

The offline verification fixture in `tests/test_headline_figures.py` uses:

- `CPI_2015 = 234.812`
- `CPI_2025 = 318.451`

Under that stated assumption:

```text
2025 equivalent = $10.60 * (CPI_2025 / CPI_2015)
                = $10.60 * (318.451 / 234.812)
                = $14.37
```

```text
2025 real value in 2015 dollars = $10.60 * (CPI_2015 / CPI_2025)
                                = $10.60 * (234.812 / 318.451)
                                = $7.82
```

These calculations are verified by:

- `tests/test_headline_figures.py::TestInflationErosion::test_should_be_wage_approximately_14_37`
- `tests/test_headline_figures.py::TestInflationErosion::test_real_purchasing_power_approximately_7_82`

The implementation used by the repo lives in `src/texas_hhcs/cpi.py`, and the machine-readable outputs are written to `results_summary.json`.

---

## Figure Audit

| Figure | Type | Evidence | Verified by |
|--------|------|----------|-------------|
| **$10.60/hr** | Source observation | HHSC workbook cell `B7` | `test_hhsc_target_wage_cell_b7_is_10_60` |
| **$12.19/hr** | Source observation | `data/processed/bls_oews_texas_2024.csv` | `test_bls_soc_31_1120_matches_processed_extract` |
| **314,610** | Source observation | `data/processed/bls_oews_texas_2024.csv` | `test_bls_soc_31_1120_matches_processed_extract` |
| **$14.37/hr** | Derived estimate | CPI formula shown above, using stated 2015 base-year assumption | `test_should_be_wage_approximately_14_37` |
| **$7.82/hr** | Derived estimate | CPI formula shown above, using stated 2015 base-year assumption | `test_real_purchasing_power_approximately_7_82` |

For the current audited headline set, only the figures above should be treated as verified.

---

## Excluded From The Audited Headline Set

The following material exists elsewhere in the repo but is not part of the audited headline set in this document:

- Retail benchmark comparisons such as Buc-ee's, Amazon, H-E-B, Walmart, and any statewide wage-gap figure built from them
- Lifetime earnings comparisons such as the `$624,424` 30-year gap
- Provider breakeven, operating-margin, occupancy, overhead, and overtime scenario models
- Waitlist size, years-to-clear, or slot-funding timeline claims that are based on manually entered notebook values
- Turnover-rate or turnover-cost claims that rely on national context plus local assumptions
- Policy-cost estimates, replacement-wage scenarios, or budget recommendations

Those items may be useful exploratory work, but they are not source-audited headline evidence unless they are backed by checked-in source tables and explicit verification tests.

---

## Limitations

- The BLS wage and employment figures in this repo are for **May 2024**, not a live series.
- The inflation-derived figures depend on the repo's explicit **2015 base-year assumption** for the frozen `$10.60` benchmark.
- SOC `31-1120` covers **Home Health and Personal Care Aides**, which is broader than Medicaid-funded waiver staff alone.
- Older notebooks and report assets may still contain exploratory or stale claims. For audited headline figures, treat `README.md`, `VERIFICATION.md`, `results_summary.json`, and this file as the authoritative set.
