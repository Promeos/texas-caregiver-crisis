# Data Sources — Raw Files

## rates/

### `2026-2027-ltss-rte-tables.xlsx`
- **Source**: HHSC Provider Finance Department (PFD)
- **URL**: https://pfd.hhs.texas.gov/sites/default/files/documents/long-term-svcs/2026-2027-ltss-rte-tables.xlsx
- **Downloaded**: 2026-03-14
- **Contents**: Official Medicaid reimbursement rate tables for all LTSS programs (ICF/IID, HCS, TxHmL, CLASS, etc.)
- **Format**: Excel, single sheet with 268 rows covering all service types and rate methodologies

### `ltss-personal-attendant-base-wage-calculator.xlsx`
- **Source**: HHSC Provider Finance Department (PFD)
- **URL**: https://pfd.hhs.texas.gov/sites/default/files/documents/rate-tables/ltss-personal-attendant-base-wage-calculator.xlsx
- **Downloaded**: 2026-03-14
- **Last Updated by PFD**: 2/7/2025
- **Contents**: Fiscal impact calculator showing how attendant wage assumptions are baked into every Medicaid service rate
- **Key Data**:
  - Default target wage: $10.60/hr (cell B7 on "Fiscal by Program" sheet)
  - 354 service lines across 18 programs
  - Per-service breakdown: current rate, attendant cost component, attendant cost %, wage required
  - SFY 2026-2027 estimated attendant hours by service
  - FMAP split: ~40.6% state / ~59.4% federal
- **Sheets**: Fiscal by Program, Fiscal Calculation, Rate Table Service Desc XWalk, All Trends, FFS Trends, SP & SK Trends, FMAP as of 4-24

## Processed Files (in `../processed/`)

### `pfd_wage_calculator_all_services.csv`
- 354 service lines extracted from the wage calculator "Fiscal Calculation" sheet
- Columns: bill_code, program, service_category, service_description, current_rate, attendant_cost, attendant_cost_pct, wage_required, etc.

### `pfd_wage_calculator_target_programs.csv`
- 114 service lines filtered to HCS, ICF/IID, TxHmL, CAS, CLASS

### `bls_oews_texas_2024.csv`
- BLS Occupational Employment and Wage Statistics, Texas, May 2024
- SOC codes: 31-1120 (Home Health Aides), 31-1131 (Nursing Assistants), 39-9011 (Childcare Workers)
- Source: BLS Public API v2

### `market_wages.csv`
- Comparison wage dataset: HHSC assumptions, BLS actuals, retail/food service employers
- 13 entries from Buc-ee's ($18) down to minimum wage ($7.25)
