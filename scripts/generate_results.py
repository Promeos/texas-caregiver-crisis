"""Generate audited results_summary.json from checked-in data and formulas.

Usage:
    uv run python scripts/generate_results.py
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from texas_hhcs.cpi import build_erosion_table, deflate_wage
from texas_hhcs.verified_datasets import (
    RIDER_23_PTB_FACILITY,
    RIDER_23_PTB_NON_FACILITY,
    RIDER_23_WAGE,
)

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "results_summary.json"

# --- Constants ---
HHSC_WAGE = 10.60
SET_YEAR = 2015
CPI_ANNUAL = pd.DataFrame(
    {
        "year": [2015, 2025],
        "annual_cpi": [234.812, 318.451],
    }
)


def main():
    # Load processed BLS data
    df_bls = pd.read_csv(PROCESSED / "bls_oews_texas_2024.csv")
    hha = df_bls[df_bls["soc_code"] == "31-1120"].set_index("measure")["value"]

    # Inflation calculations
    should_be = deflate_wage(HHSC_WAGE, SET_YEAR, 2025, CPI_ANNUAL)
    erosion = build_erosion_table(HHSC_WAGE, SET_YEAR, CPI_ANNUAL)
    latest = erosion.iloc[-1]

    # Verified waitlist and operator-cost datasets
    interest_list_totals = pd.read_csv(PROCESSED / "hhsc_interest_list_totals_monthly.csv")
    latest_report_month = interest_list_totals["report_month"].max()
    latest_totals = (
        interest_list_totals[interest_list_totals["report_month"] == latest_report_month]
        .set_index("program")["individuals"]
    )

    legislative_allocations = pd.read_csv(
        PROCESSED / "hhsc_interest_list_legislative_allocations.csv"
    ).set_index("program")["legislative_allocation"]

    setting_costs = pd.read_csv(PROCESSED / "hhsc_setting_costs_fy2023.csv").set_index(
        ["setting", "metric"]
    )["monthly_average_cost"]
    tx_employment = float(hha["employment"])

    results = {
        "_generated": datetime.now(timezone.utc).isoformat(),
        "_description": "Machine-verifiable summary of audited figures. "
        "Run `uv run python scripts/generate_results.py` to regenerate.",
        "figures": {
            "hhsc_target_wage": {
                "value": HHSC_WAGE,
                "unit": "$/hr",
                "type": "source_observation",
                "source": "HHSC PFD Wage Calculator, cell B7 (updated 2/7/2025)",
            },
            "real_purchasing_power": {
                "value": round(float(latest["real_value"]), 2),
                "unit": "$/hr (2015 dollars)",
                "type": "derived_estimate",
                "formula": f"${HHSC_WAGE} * (CPI_{SET_YEAR} / CPI_2025)",
            },
            "inflation_adjusted_wage": {
                "value": round(float(should_be), 2),
                "unit": "$/hr",
                "type": "derived_estimate",
                "formula": f"${HHSC_WAGE} * (CPI_2025 / CPI_{SET_YEAR})",
            },
            "purchasing_power_lost_pct": {
                "value": round(float(latest["purchasing_power_lost_pct"]), 1),
                "unit": "%",
                "type": "derived_estimate",
            },
            "bls_tx_hha_mean_wage": {
                "value": float(hha["hourly_mean"]),
                "unit": "$/hr",
                "type": "source_observation",
                "source": "BLS OEWS May 2024, SOC 31-1120 (Home Health and Personal Care Aides)",
            },
            "bls_tx_hha_employment": {
                "value": int(tx_employment),
                "unit": "workers",
                "type": "source_observation",
                "source": "BLS OEWS May 2024, SOC 31-1120 (Home Health and Personal Care Aides)",
            },
            "hcs_interest_list_count_latest_report": {
                "value": int(latest_totals["HCS"]),
                "unit": "people",
                "type": "source_observation",
                "source": (
                    "HHSC interest list workbook archive, latest checked-in report month "
                    f"({latest_report_month})"
                ),
            },
            "txhml_interest_list_count_latest_report": {
                "value": int(latest_totals["TXHML"]),
                "unit": "people",
                "type": "source_observation",
                "source": (
                    "HHSC interest list workbook archive, latest checked-in report month "
                    f"({latest_report_month})"
                ),
            },
            "hcs_2022_2023_legislative_allocation": {
                "value": int(legislative_allocations["HCS"]),
                "unit": "slots",
                "type": "source_observation",
                "source": "HHSC Interest List Reduction page, 2022-23 biennium table",
            },
            "community_icf_iid_total_monthly_cost_fy2023": {
                "value": float(setting_costs[("COMMUNITY_ICF_IID", "total_costs")]),
                "unit": "$/person-month",
                "type": "source_observation",
                "source": "HHSC cost comparison report (FY 2023 community ICF/IID total cost)",
            },
            "hcs_residential_total_monthly_cost_fy2023": {
                "value": float(setting_costs[("HCS_RESIDENTIAL", "total_costs")]),
                "unit": "$/person-month",
                "type": "source_observation",
                "source": "HHSC cost comparison report (FY 2023 HCS residential total cost)",
            },
            "new_wage_assumption": {
                "value": RIDER_23_WAGE,
                "unit": "$/hr",
                "type": "source_observation",
                "source": "9-1-2025-payment-rate-actions.pdf, page 3: "
                "GAA SB1, 89th Legislature, Rider 23",
            },
            "new_ptb_facility_pct": {
                "value": RIDER_23_PTB_FACILITY,
                "unit": "fraction",
                "type": "source_observation",
                "source": "9-1-2025-payment-rate-actions.pdf, page 3: "
                "15% PTB for facility-based care",
            },
            "new_ptb_non_facility_pct": {
                "value": RIDER_23_PTB_NON_FACILITY,
                "unit": "fraction",
                "type": "source_observation",
                "source": "9-1-2025-payment-rate-actions.pdf, page 3: "
                "14% PTB for non-facility (community) care",
            },
            "wage_increase_dollar": {
                "value": round(RIDER_23_WAGE - HHSC_WAGE, 2),
                "unit": "$/hr",
                "type": "derived_estimate",
                "formula": f"${RIDER_23_WAGE} - ${HHSC_WAGE}",
            },
            "wage_increase_pct": {
                "value": round(
                    (RIDER_23_WAGE - HHSC_WAGE) / HHSC_WAGE * 100, 1
                ),
                "unit": "%",
                "type": "derived_estimate",
                "formula": f"(${RIDER_23_WAGE} - ${HHSC_WAGE}) / ${HHSC_WAGE}",
            },
            "new_wage_vs_cpi_gap": {
                "value": round(float(should_be) - RIDER_23_WAGE, 2),
                "unit": "$/hr",
                "type": "derived_estimate",
                "formula": (
                    f"CPI-adjusted ${HHSC_WAGE} in 2025 "
                    f"(${round(float(should_be), 2)}) - ${RIDER_23_WAGE}"
                ),
                "note": "Positive value means new wage still below inflation catch-up",
            },
            "tx_hha_pca_median_wage_2023": {
                "value": 10.83,
                "unit": "$/hr",
                "type": "source_observation",
                "source": "ASPE Issue Brief Dec 2024, Table A1 (TX row)",
            },
            "tx_hha_pca_wage_gap_2023": {
                "value": 6.77,
                "unit": "$/hr",
                "type": "source_observation",
                "source": "ASPE Issue Brief Dec 2024, Table A1 "
                "(largest gap nationally)",
            },
            "national_home_care_median_2024": {
                "value": 16.77,
                "unit": "$/hr",
                "type": "source_observation",
                "source": "PHI Key Facts 2025, Executive Summary",
            },
            "national_all_dcw_median_2024": {
                "value": 17.36,
                "unit": "$/hr",
                "type": "source_observation",
                "source": "PHI Key Facts 2025, Executive Summary",
            },
            "acre_hcs_txhml_participation_pct": {
                "value": 0.35,
                "unit": "fraction",
                "type": "source_observation",
                "source": (
                    "HHSC Rate Enhancement Evaluation "
                    "Oct 2024, Table 3"
                ),
            },
            "acre_hcs_txhml_wage_differential_pct": {
                "value": 0.16,
                "unit": "fraction",
                "type": "source_observation",
                "source": (
                    "HHSC Rate Enhancement Evaluation "
                    "Oct 2024, p.19"
                ),
            },
            "acre_nursing_participation_pct": {
                "value": 0.93,
                "unit": "fraction",
                "type": "source_observation",
                "source": (
                    "HHSC Rate Enhancement Evaluation "
                    "Oct 2024, Table 2"
                ),
            },
            "acre_total_recoupments_2019_20": {
                "value": sum(
                    r[4] for r in [
                        (None, None, None, None, 4_050_086),
                        (None, None, None, None, 94_486),
                        (None, None, None, None, 141_113),
                        (None, None, None, None, 1_066_166),
                        (None, None, None, None, 1_219_442),
                        (None, None, None, None, 8_323_355),
                    ]
                ),
                "unit": "$",
                "type": "derived_estimate",
                "formula": "Sum of Table 4 recoupments",
                "source": (
                    "HHSC Rate Enhancement Evaluation "
                    "Oct 2024, Table 4"
                ),
            },
            "medicaid_federal_amount_sfy2024": {
                "value": 25_500_000_000,
                "unit": "$",
                "type": "source_observation",
                "source": (
                    "HHSC Annual Federal Funds Report "
                    "Dec 2024, p.1"
                ),
            },
            "medicaid_pct_of_federal_hhs": {
                "value": 0.93,
                "unit": "fraction",
                "type": "source_observation",
                "source": (
                    "HHSC Annual Federal Funds Report "
                    "Dec 2024, p.1"
                ),
            },
            "hhsc_federal_funds_sfy2024": {
                "value": 26_869_487_588,
                "unit": "$",
                "type": "source_observation",
                "source": (
                    "HHSC Annual Federal Funds Report "
                    "Dec 2024, Figure 1"
                ),
            },
            "hhs_pct_federal_funding": {
                "value": 0.55,
                "unit": "fraction",
                "type": "source_observation",
                "source": (
                    "HHSC Annual Federal Funds Report "
                    "Dec 2024, Figure 1 (adjusted TOTAL per footnote 2)"
                ),
            },
        },
    }

    OUTPUT.write_text(json.dumps(results, indent=2) + "\n")
    print(f"Wrote {OUTPUT}")
    print(f"  {len(results['figures'])} figures generated")


if __name__ == "__main__":
    main()
