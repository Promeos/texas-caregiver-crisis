# Methodology

Audit date: 2026-03-16

This document records only the figures and datasets in this repo that are supported by checked-in source files or by deterministic calculations with stated inputs. If a claim depends on external reporting, manually entered notebook values, or unsourced scenario assumptions, it is outside the audited set.

See `VERIFICATION.md` for the audit log and `results_summary.json` for the machine-readable audited figure summary.

## Audited Scope

| Item | Status | Support |
|---|---|---|
| HHSC base target wage = **$10.60/hr** | Verified source observation | Checked-in HHSC workbook, sheet `Fiscal by Program`, cell `B7` |
| BLS Texas SOC 31-1120 hourly mean = **$12.19/hr** | Verified source observation | Checked-in processed OEWS extract |
| BLS Texas SOC 31-1120 employment = **314,610** | Verified source observation | Checked-in processed OEWS extract |
| 2025 CPI-equivalent of `$10.60` = **$14.38/hr** | Verified derived figure | Deterministic formula using the repo's explicit 2015 base-year assumption |
| 2025 real purchasing power of `$10.60` = **$7.82/hr** in 2015 dollars | Verified derived figure | Same CPI series and same stated assumption |
| HHSC monthly interest-list totals, years-on-list buckets, closures, and releases | Verified source-backed datasets | Parsed from checked-in HHSC workbook archive |
| HHSC 2022-23 legislative allocation table | Verified source-backed dataset | Parsed from checked-in HHSC Interest List Reduction page |
| HHSC FY 2023 HCS/ICF/IID setting-level cost tables | Verified source-backed dataset | Parsed from checked-in HHSC cost comparison report |
| HHSC community ICF/IID cost table by LON and facility size | Verified source-backed dataset | Parsed from checked-in HHSC cost comparison report |
| HHSC HCS/ICF cost-report category definitions | Verified source-backed dataset | Extracted from checked-in 2024 HHSC cost-report instructions |
| HHSC HCS `SL/RSS` and community ICF/IID residential reimbursement components | Verified source-backed dataset | Parsed from checked-in processed HHSC rate workbook extract |
| Rider 23 wage increase: $10.60 → **$13.00/hr**, PTB 15%/14% | Verified source observation | `9-1-2025-payment-rate-actions.pdf`, page 3; GAA SB1, 89th Legislature |
| HCS SL/RSS and ICF/IID old-vs-new rate comparison table | Verified source-backed dataset | Parsed from rate actions PDF and existing rate components |
| TX HHA/PCA median wage = **$10.83/hr**, wage gap = **$6.77/hr** (largest nationally) | Verified source observation | ASPE Issue Brief Dec 2024, Table A1 |
| National home care median = **$16.77/hr**, all-DCW median = **$17.36/hr** | Verified source observation | PHI Key Facts 2025 |
| National DCW wage trends (2014-2024) by setting | Verified source-backed dataset | PHI Key Facts 2025 |
| ACRE/DCSE participation rates by program (35%-93%) | Verified source observation | HHSC Rate Enhancement Evaluation Oct 2024, Tables 2-3 |
| ACRE wage differentials by program (1%-16%) | Verified source observation | HHSC Rate Enhancement Evaluation Oct 2024, p.19 |
| ACRE recoupments 2019-20: **$14.9M** total | Verified derived figure | Sum of Table 4 recoupments |
| ACRE program funding trend SFY 2019-2024 | Verified source-backed dataset | HHSC Rate Enhancement Evaluation Oct 2024, Table 1 |
| Attendant base wage history: 5 increases, $5.15 → $10.60 (2000-2023) | Verified source observation | HHSC Rate Enhancement Evaluation Oct 2024, Table 5 |
| TX HHS federal funding: **$27.4B** of **$49.5B** total (55%, adjusted per PDF footnote 2) | Verified source observation | HHSC Annual Federal Funds Report Dec 2024, Figure 1 |
| Medicaid = **$25.5B** = 93% of federal HHS funds | Verified source observation | HHSC Annual Federal Funds Report Dec 2024, p.1 |

## Data Sources

| Source file | What is used | Notes |
|---|---|---|
| `data/raw/rates/ltss-personal-attendant-base-wage-calculator.xlsx` | HHSC target wage | Audited value is sheet `Fiscal by Program`, cell `B7` |
| `data/processed/bls_oews_texas_2024.csv` | Texas OEWS wage and employment values for SOC `31-1120` | Official occupation title is `Home Health and Personal Care Aides` |
| `data/raw/official/interest-list-monthly/*.xlsx` | Monthly HHSC interest-list totals, years-on-list buckets, closures, and releases | Archive currently spans September 2023 through January 2026 |
| `data/raw/official/interest-list-reduction.html` | HHSC legislative allocation table and current-page metadata | Includes the 2022-23 allocation table and the link to the latest workbook on the audit date |
| `data/raw/official/cost-comparison-report-aug-2024.txt` | HHSC FY 2023 per-person cost tables for HCS/ICF/IID | Used for setting-level costs and community ICF/IID LON-by-size costs |
| `data/raw/official/2024-hcs-cost-report-instructions.txt` | HHSC HCS cost-report area definitions | Used to verify operator cost-area categories |
| `data/raw/official/2024-icf-cost-report-instructions.txt` | HHSC ICF/IID cost-report area definitions | Used to verify operator cost-area categories |
| `data/processed/pfd_wage_calculator_all_services.csv` | HHSC reimbursement components by service line | Used for HCS `SL/RSS` and non-state community ICF/IID residential rate components |
| `data/raw/rates/9-1-2025-payment-rate-actions.pdf` | Rider 23 rate tables and wage parameters | Tables 1 & 2: proposed HCS SL/RSS and ICF/IID rates effective 9/1/2025 |
| `data/raw/official/rate-enhancement-evaluation-2024.pdf` | ACRE program evaluation | Tables 1-5: participation, funding, recoupments, wage history |
| `data/raw/official/annual-federal-funds-report-2024.pdf` | HHSC federal funding breakdown | Figure 1 and p.1: agency funding, Medicaid share |
| `data/raw/external/aspe-dcw-wages-brief.pdf` | State-by-state HHA/PCA wages | Tables A1/A2: median wages and entry-level gap by state |
| `data/raw/external/phi-dcw-key-facts-2025.pdf` | National DCW wage trends | 2014-2024 median wages by setting |
| `data/raw/external/lbb-88th-article-ii-rider.txt` | Audit-only disconfirmation file | Used to show that earlier `3,292` slot claims were misapplied to HCS |
| `data/raw/external/nci-state-of-the-workforce-2023.txt` | Audit-only disconfirmation file | Used only to show that earlier turnover claims were overstated or overgeneralized |

The source index with original URLs is maintained in `references/sources.yaml`.

## How the Audited Datasets Are Built

### Wage and inflation figures

The wage figures come from a checked-in HHSC workbook and a checked-in BLS OEWS extract. The inflation figures are derived, not observed. The repo currently treats `$10.60` as a 2015-dollar benchmark for the purpose of the audited CPI calculation.

The offline CPI inputs used by the repo are:

- `CPI_2015 = 234.812`
- `CPI_2025 = 318.451`

Under that stated assumption:

```text
2025 equivalent = $10.60 * (318.451 / 234.812) = $14.38
2025 real value in 2015 dollars = $10.60 * (234.812 / 318.451) = $7.82
```

These figures are generated in `scripts/generate_results.py` and validated in `tests/test_headline_figures.py`.

### Waitlist datasets

The repo parses each checked-in HHSC interest-list workbook into four structured tables:

- monthly totals by program
- years-on-list buckets by program
- monthly closure categories by program
- monthly release-summary metrics by program

The parser resolves older and newer workbook variants by sheet-name prefix and detects the actual header layout in each workbook instead of assuming a single tab name or fixed row number.

The legislative allocation table is parsed separately from the checked-in HHSC Interest List Reduction page.

The dataset builder lives in `src/texas_hhcs/verified_datasets.py`, and the checked-in CSVs are generated by `scripts/generate_verified_datasets.py`.

### HCS/ICF operator-cost datasets

The repo builds three kinds of operator-cost evidence from official HHSC files:

1. Setting-level monthly Medicaid cost per individual from the HHSC cost comparison report.
2. Community ICF/IID monthly cost per individual by level of need and facility size from the same report.
3. Cost-report categories and reimbursement components from HHSC cost-report instructions and the HHSC rate workbook extract.

For the cost comparison report, the parser handles the PDF text-extraction quirks explicitly:

- Table 1 is read as setting blocks with currency values mapped in order.
- Table 2 and Table 3 are separated so the LON labels in the counts table are not confused with the same labels in the cost table.

For reimbursement components, the repo uses the processed HHSC rate extract and keeps only:

- HCS `SL/RSS`
- ICF/IID non-state community residential rows

The output preserves:

- current rate
- attendant cost component
- attendant share of the rate
- non-attendant reimbursement component
- wage-required field from the HHSC calculator extract

## Figure and Dataset Audit

| Output | Type | Built from | Verified by |
|---|---|---|---|
| `results_summary.json` wage figures | Source observations and deterministic derived figures | HHSC workbook, BLS OEWS extract, offline CPI inputs | `tests/test_headline_figures.py` |
| `hhsc_interest_list_totals_monthly.csv` | Source-backed dataset | HHSC monthly workbook archive | `tests/test_verified_datasets.py` |
| `hhsc_interest_list_years_on_list_monthly.csv` | Source-backed dataset | HHSC monthly workbook archive | `tests/test_verified_datasets.py` |
| `hhsc_interest_list_closure_summary_monthly.csv` | Source-backed dataset | HHSC monthly workbook archive | `tests/test_verified_datasets.py` |
| `hhsc_interest_list_releases_summary_monthly.csv` | Source-backed dataset | HHSC monthly workbook archive | `tests/test_verified_datasets.py` |
| `hhsc_interest_list_legislative_allocations.csv` | Source-backed dataset | HHSC Interest List Reduction page | `tests/test_verified_datasets.py` |
| `hhsc_setting_costs_fy2023.csv` | Source-backed dataset | HHSC cost comparison report | `tests/test_verified_datasets.py` |
| `hhsc_community_icf_iid_costs_by_lonsize_fy2023.csv` | Source-backed dataset | HHSC cost comparison report | `tests/test_verified_datasets.py` |
| `hhsc_residential_rate_components.csv` | Source-backed dataset | Processed HHSC rate extract | `tests/test_verified_datasets.py` |
| `hhsc_cost_report_cost_areas.csv` | Source-backed dataset | HHSC cost-report instructions | `tests/test_verified_datasets.py` |
| `hhsc_rate_comparison_old_vs_new.csv` | Source-backed dataset | Rate actions PDF + existing rate components | `tests/test_headline_figures.py` (TestRider23RateChange) |
| `aspe_state_dcw_wages.csv` | Source-backed dataset | ASPE Issue Brief Dec 2024, Tables A1/A2 | `tests/test_headline_figures.py` (TestNationalWageComparison) |
| `phi_national_dcw_wage_trends.csv` | Source-backed dataset | PHI Key Facts 2025 | `tests/test_headline_figures.py` (TestNationalWageComparison) |
| `hhsc_acre_participation.csv` | Source-backed dataset | HHSC Rate Enhancement Evaluation Oct 2024 | `tests/test_headline_figures.py` (TestRateEnhancementEvaluation) |
| `hhsc_acre_program_funding.csv` | Source-backed dataset | HHSC Rate Enhancement Evaluation Oct 2024 | `tests/test_headline_figures.py` (TestRateEnhancementEvaluation) |
| `hhsc_acre_recoupments.csv` | Source-backed dataset | HHSC Rate Enhancement Evaluation Oct 2024 | `tests/test_headline_figures.py` (TestRateEnhancementEvaluation) |
| `hhsc_acre_wage_history.csv` | Source-backed dataset | HHSC Rate Enhancement Evaluation Oct 2024 | `tests/test_headline_figures.py` (TestRateEnhancementEvaluation) |
| `hhsc_federal_funds_summary.csv` | Source-backed dataset | HHSC Annual Federal Funds Report Dec 2024 | `tests/test_headline_figures.py` (TestFederalFundingContext) |
| `results_summary.json` Rider 23, ASPE, PHI, ACRE, federal funding figures | Source observations and derived figures | Multiple HHSC/federal sources | `tests/test_headline_figures.py` |

## Excluded From the Audited Set

The following material exists elsewhere in the repo but is not part of the audited set in this document:

- Retail benchmark comparisons such as Buc-ee's, Amazon, H-E-B, Walmart, and any statewide wage-gap figure built from them
- Lifetime earnings comparisons such as the `$624,424` 30-year gap
- Waitlist-clearing timelines such as `87 years to clear`
- Turnover-rate or turnover-cost claims that rely on national context plus local assumptions
- Provider breakeven, occupancy, overhead, and overtime scenario models
- Provider margin or profit claims inferred from these cost tables without provider-level cost reports
- Policy-cost estimates, replacement-wage scenarios, or budget recommendations

Those items may be useful exploratory work, but they are not audited evidence unless they are backed by checked-in source tables and explicit verification tests.

## Limitations

- The BLS wage and employment figures in this repo are for **May 2024**, not a live series.
- The inflation-derived figures depend on the repo's explicit **2015 base-year assumption** for the frozen `$10.60` benchmark.
- SOC `31-1120` covers **Home Health and Personal Care Aides**, which is broader than Medicaid-funded waiver staff alone.
- The HHSC interest-list archive in the repo currently runs through **January 2026**, which was the latest checked-in workbook on the audit date.
- The HHSC cost comparison report provides Medicaid cost per individual by setting. It does not, by itself, prove provider profit margins or cash flow.
- The reimbursement-component dataset describes HHSC payment structure, not audited provider books.
- Older notebooks and report assets may still contain exploratory or stale claims. For audited material, treat `README.md`, `VERIFICATION.md`, `results_summary.json`, and the `data/processed/hhsc_*.csv` outputs as authoritative.
