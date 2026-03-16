"""Generate audited results_summary.json from checked-in data and formulas.

Usage:
    uv run python scripts/generate_results.py
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from texas_hhcs.cpi import build_erosion_table, deflate_wage

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
        },
    }

    OUTPUT.write_text(json.dumps(results, indent=2) + "\n")
    print(f"Wrote {OUTPUT}")
    print(f"  {len(results['figures'])} figures generated")


if __name__ == "__main__":
    main()
