# Verification Notes

Audit date: 2026-03-16

This note records which figures and datasets in the repo are directly supported by checked-in source files, which claims remain excluded from the audited set, and where earlier waitlist/operator-cost assertions were corrected.

## Verified from local source files

| Figure or dataset | Status | Evidence |
|---|---|---|
| HHSC base target wage = **$10.60/hr** | Verified | `data/raw/rates/ltss-personal-attendant-base-wage-calculator.xlsx`, sheet `Fiscal by Program`, cell `B7` |
| CPI-adjusted value of $10.60 in 2025 = **$14.38/hr** | Verified derived figure | Deterministic formula using checked-in CPI annual values documented in `tests/test_headline_figures.py` |
| Real purchasing power of $10.60 in 2025 = **$7.82/hr** in 2015 dollars | Verified derived figure | Same CPI series and formula as above |
| BLS SOC 31-1120 hourly mean = **$12.19/hr** | Verified | `data/processed/bls_oews_texas_2024.csv` |
| BLS SOC 31-1120 employment = **314,610** | Verified | `data/processed/bls_oews_texas_2024.csv` |
| Monthly HHSC interest-list totals by program | Verified dataset | `data/processed/hhsc_interest_list_totals_monthly.csv`, generated from the checked-in HHSC workbook archive |
| Monthly HHSC interest-list years-on-list buckets | Verified dataset | `data/processed/hhsc_interest_list_years_on_list_monthly.csv`, generated from the checked-in HHSC workbook archive |
| Monthly HHSC interest-list closures and release summaries | Verified dataset | `data/processed/hhsc_interest_list_closure_summary_monthly.csv` and `data/processed/hhsc_interest_list_releases_summary_monthly.csv` |
| HHSC 2022-23 legislative allocation table | Verified dataset | `data/processed/hhsc_interest_list_legislative_allocations.csv`, parsed from the checked-in HHSC Interest List Reduction page |
| HHSC FY 2023 setting-level monthly cost tables for HCS/ICF/IID | Verified dataset | `data/processed/hhsc_setting_costs_fy2023.csv` |
| HHSC community ICF/IID cost table by LON and facility size | Verified dataset | `data/processed/hhsc_community_icf_iid_costs_by_lonsize_fy2023.csv` |
| HHSC HCS/ICF cost-report categories and residential reimbursement components | Verified dataset | `data/processed/hhsc_cost_report_cost_areas.csv` and `data/processed/hhsc_residential_rate_components.csv` |

Important scope note: the official BLS occupation title for SOC `31-1120` is **Home Health and Personal Care Aides**. That is broader than Medicaid-funded waiver staff alone.

## Verified values now checked in

| Claim | Verified value | Source file |
|---|---|---|
| HCS interest-list total as of **January 31, 2026** | **130,764** | `hhsc_interest_list_totals_monthly.csv` |
| TxHmL interest-list total as of **January 31, 2026** | **117,175** | `hhsc_interest_list_totals_monthly.csv` |
| HCS enrolled from interest-list releases in the January 2026 workbook | **339** | `hhsc_interest_list_releases_summary_monthly.csv` |
| HCS total releases this biennium in the January 2026 workbook | **284** | `hhsc_interest_list_releases_summary_monthly.csv` |
| HCS legislative allocation for the 2022-23 biennium | **542 slots** | `hhsc_interest_list_legislative_allocations.csv` |
| TxHmL legislative allocation for the 2022-23 biennium | **471 slots** | `hhsc_interest_list_legislative_allocations.csv` |
| Community ICF/IID monthly average Medicaid cost per individual, FY 2023 | **$5,247.52** | `hhsc_setting_costs_fy2023.csv` |
| HCS residential monthly average Medicaid cost per individual, FY 2023 | **$6,563.91** | `hhsc_setting_costs_fy2023.csv` |
| Community ICF/IID small-home LON 1 average monthly cost per individual | **$4,232.10** | `hhsc_community_icf_iid_costs_by_lonsize_fy2023.csv` |
| Community ICF/IID small-home LON 1 average individuals served per month | **999** | `hhsc_community_icf_iid_costs_by_lonsize_fy2023.csv` |
| ICF/IID non-state community residential LON 1 small-home attendant component | **$60.3944** | `hhsc_residential_rate_components.csv` |
| HCS supervised living LON 5 attendant component | **$85.74** | `hhsc_residential_rate_components.csv` |
| Rider 23 new wage assumption | **$13.00/hr** | `verified_datasets.RIDER_23_WAGE` (from `9-1-2025-payment-rate-actions.pdf`) |
| Rider 23 PTB facility | **15%** | `verified_datasets.RIDER_23_PTB_FACILITY` |
| Rider 23 PTB non-facility | **14%** | `verified_datasets.RIDER_23_PTB_NON_FACILITY` |
| HCS SL LON 1 proposed rate | **$163.66/day** | `hhsc_rate_comparison_old_vs_new.csv` |
| ICF/IID small LON 1 proposed rate | **$173.61/day** | `hhsc_rate_comparison_old_vs_new.csv` |
| Wage increase ($10.60 → $13.00) | **$2.40/hr (+22.6%)** | Derived from audited constants |
| New wage vs CPI parity gap | **-$1.38/hr** | $14.38 − $13.00 |
| TX HHA/PCA median wage (BLS OEWS May 2023) | **$10.83/hr** | `aspe_state_dcw_wages.csv` |
| TX HHA/PCA wage gap vs entry-level — **largest nationally** | **$6.77/hr** | `aspe_state_dcw_wages.csv` |
| National home care median wage (2024) | **$16.77/hr** | `phi_national_dcw_wage_trends.csv` |
| National all-DCW median wage (2024) | **$17.36/hr** | `phi_national_dcw_wage_trends.csv` |
| DCSE nursing facility participation rate | **93%** | `hhsc_acre_participation.csv` |
| ACRE HCS/TxHmL participation rate | **35%** (lowest) | `hhsc_acre_participation.csv` |
| ACRE HCS/TxHmL wage differential | **16%** | HHSC Rate Enhancement Evaluation p.19 |
| ICF/IID ACRE participation rate | **70%** | `hhsc_acre_participation.csv` |
| Total ACRE recoupments (2019-20) | **$14,894,648** | `hhsc_acre_recoupments.csv` |
| Attendant base wage: latest entry (2023-09-01) | **$10.60** | `hhsc_acre_wage_history.csv` |
| Medicaid federal funds SFY 2024 | **$25.5B** (93% of federal HHS) | `hhsc_federal_funds_summary.csv` |
| HHSC federal funds SFY 2024 | **$26,869,487,588** | `hhsc_federal_funds_summary.csv` |
| TX HHS system: 55% federally funded (adjusted TOTAL per PDF footnote 2) | **$27.4B of $49.5B** | `hhsc_federal_funds_summary.csv` |

## Not currently verified in-repo

| Claim | Audit finding |
|---|---|
| `87 years` to clear the HCS waitlist or any similar clearing timeline | The repo now contains verified monthly counts and release tables, but it still does not contain a reproducible, source-audited model that converts those counts into a defensible years-to-clear estimate. |
| `3,292` slots used as the pace for HCS access | The checked-in LBB rider packet shows `3,292` under **Strategy A.3.4, Texas Home Living**, as an end-of-year TxHmL waiver-slot count. It is not an HCS annual-enrollment figure. |
| `~50%` turnover and related per-house turnover costs | The checked-in NCI 2023 workforce report says the weighted average turnover ratio was **39.7%** across participating states. It is not a Texas-specific rate, and the repo’s older house-level turnover costs add extra assumptions on top of it. |
| Retail-wage gap headlines such as `~$4.8B/yr` or `$624,424` | These are scenario calculations, not source observations. They were removed from the audited outputs. |
| Provider margin or profit claims inferred from these cost tables alone | The HHSC cost comparison report gives Medicaid cost per individual and the rate workbook gives reimbursement components. Neither file, by itself, is an audited provider profit-and-loss statement. |

## Current repo caveat

The repo now has audited waitlist and operator-cost CSVs, but some exploratory notebooks and older report assets still contain stale scenarios or pre-audit framing. Treat `README.md`, `METHODOLOGY.md`, `results_summary.json`, and the `data/processed/hhsc_*.csv` files as the authoritative audited set.

## Checked external evidence used for corrections

- `data/raw/external/lbb-88th-article-ii-rider.txt` confirms the `3,292` figure is tied to Texas Home Living, not HCS.
- `data/raw/external/nci-state-of-the-workforce-2023.txt` confirms the 2023 weighted-average turnover ratio is `39.7%`.
- `data/raw/official/interest-list-reduction.html` contains the official HHSC legislative-allocation table and the direct link to the January 2026 interest-list workbook.
- `data/raw/official/cost-comparison-report-aug-2024.txt` contains the official FY 2023 HCS/ICF/IID cost tables used in the new operator-cost datasets.
