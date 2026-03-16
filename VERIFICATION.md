# Verification Notes

Audit date: 2026-03-15

This note records which figures in the repo are directly supported by checked-in source files, which are illustrative scenarios, and which claims should not currently be treated as verified.

## Verified from local source files

| Figure | Status | Evidence |
|---|---|---|
| HHSC base target wage = **$10.60/hr** | Verified | [`data/raw/rates/ltss-personal-attendant-base-wage-calculator.xlsx`](data/raw/rates/ltss-personal-attendant-base-wage-calculator.xlsx), sheet `Fiscal by Program`, cell `B7` |
| CPI-adjusted value of $10.60 in 2025 = **$14.37/hr** | Verified | Deterministic calculation from BLS CPI-U South annual averages used in [`tests/test_headline_figures.py`](tests/test_headline_figures.py) |
| Real purchasing power of $10.60 in 2025 = **$7.82/hr** in 2015 dollars | Verified | Same CPI series and formula as above |
| BLS SOC 31-1120 hourly mean = **$12.19/hr** | Verified | [`data/processed/bls_oews_texas_2024.csv`](data/processed/bls_oews_texas_2024.csv) |
| BLS SOC 31-1120 employment = **314,610** | Verified | [`data/processed/bls_oews_texas_2024.csv`](data/processed/bls_oews_texas_2024.csv) |

Important scope note: the official BLS occupation title for SOC `31-1120` is **Home Health and Personal Care Aides**. That is broader than Medicaid-funded waiver staff alone.

## Kept as illustrative scenarios

| Figure | Why it is not a source observation |
|---|---|
| **~$4.8B/yr** statewide wage gap vs. `$18/hr` retail | Assumes every worker counted by BLS SOC `31-1120` is full-time, affected by the HHSC base wage, and directly comparable to the retail benchmark |
| **$624,424** 30-year earnings gap | Assumes a 30-year career, 2% annual raises, and a fixed retail comparison wage |

These are useful scenario calculations, but they should not be described as measured statewide losses.

## Not currently verified in-repo

| Claim | Audit finding |
|---|---|
| `100,000+` waitlist / `87 years` to clear | The notebook uses manually entered biennium values and mixes a `100,000+` headline with a separate `130,000 / 1,500 = 87 years` scenario. The repo does not include a checked-in waitlist dataset that reproduces those figures. |
| `3,292` slots used as the pace for HCS access | The downloaded LBB rider packet shows `3,292` under **Strategy A.3.4, Texas Home Living**, as an **end-of-year waiver slots** count. It is not a checked local source for HCS new annual slots. |
| `~50%` turnover and related per-house turnover costs | The downloaded NCI 2023 workforce report says the **weighted average turnover ratio was 39.7%**. The report is national, Texas is not a participating state in that edition, and the repo adds extra house-level cost assumptions on top of it. |
| "Everything comes from public government sources" | Not accurate. Market wage and turnover context rely on nongovernment sources. |

## Current repo caveat

Several files under `reports/` and the policy brief were generated before this audit. They still contain waitlist and turnover claims that are no longer part of the verified headline set.

## Downloaded external evidence

- [`data/raw/external/lbb-88th-article-ii-rider.txt`](data/raw/external/lbb-88th-article-ii-rider.txt) confirms the `3,292` figure is tied to Texas Home Living, not HCS.
- [`data/raw/external/nci-state-of-the-workforce-2023.txt`](data/raw/external/nci-state-of-the-workforce-2023.txt) confirms the 2023 weighted-average turnover ratio is `39.7%`.
