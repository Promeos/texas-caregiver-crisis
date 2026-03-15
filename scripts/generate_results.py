"""Generate results_summary.json from source data and calculations.

This script produces a machine-verifiable summary of every headline figure
cited in the README and policy brief. Run it after data collection to
regenerate the results file.

Usage:
    uv run python scripts/generate_results.py
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from texas_hhcs.cpi import annual_cpi, build_erosion_table, deflate_wage, fetch_cpi_series
from texas_hhcs.staffing import StaffingModel

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "results_summary.json"

# --- Constants ---
HHSC_WAGE = 10.60
SET_YEAR = 2015
BUCEES_WAGE = 18.00
HOURS_PER_YEAR = 2_080
CAREER_YEARS = 30
ANNUAL_RAISE = 0.02
WAITLIST_SIZE = 130_000
SLOTS_PER_YEAR = 1_500


def main():
    # Load processed BLS data
    df_bls = pd.read_csv(PROCESSED / "bls_oews_texas_2024.csv")
    hha = df_bls[df_bls["soc_code"] == "31-1120"].set_index("measure")["value"]

    # Fetch CPI data
    cpi_monthly = fetch_cpi_series("CUUR0300SA0", start_year=2010, end_year=2025)
    cpi_yearly = annual_cpi(cpi_monthly)

    # Inflation calculations
    should_be = deflate_wage(HHSC_WAGE, SET_YEAR, 2025, cpi_yearly)
    erosion = build_erosion_table(HHSC_WAGE, SET_YEAR, cpi_yearly)
    latest = erosion.iloc[-1]

    # Career earnings gap
    multipliers = [(1 + ANNUAL_RAISE) ** (y - 1) for y in range(1, CAREER_YEARS + 1)]
    care_total = HHSC_WAGE * HOURS_PER_YEAR * sum(multipliers)
    retail_total = BUCEES_WAGE * HOURS_PER_YEAR * sum(multipliers)

    # Statewide wage gap
    tx_employment = float(hha["employment"])
    gap_per_worker = (BUCEES_WAGE - HHSC_WAGE) * HOURS_PER_YEAR
    statewide_gap = gap_per_worker * tx_employment

    # Waitlist timeline
    years_to_clear = WAITLIST_SIZE / SLOTS_PER_YEAR

    # Staffing model
    model = StaffingModel(residents=4, staff_per_shift=1, hourly_wage=HHSC_WAGE)

    results = {
        "_generated": datetime.now(timezone.utc).isoformat(),
        "_description": "Machine-verifiable summary of headline figures. "
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
                "source": "BLS OEWS May 2024, SOC 31-1120",
            },
            "bls_tx_hha_employment": {
                "value": int(tx_employment),
                "unit": "workers",
                "type": "source_observation",
                "source": "BLS OEWS May 2024, SOC 31-1120",
            },
            "statewide_annual_wage_gap": {
                "value": round(statewide_gap, 0),
                "unit": "$/yr",
                "type": "modeled_comparison",
                "formula": (
                    f"(${BUCEES_WAGE} - ${HHSC_WAGE}) "
                    f"* {HOURS_PER_YEAR} hrs * {int(tx_employment)} workers"
                ),
            },
            "waitlist_size": {
                "value": WAITLIST_SIZE,
                "unit": "people",
                "type": "source_observation",
                "source": "HHSC Interest List, LBB rider packets (pre-cleanup)",
            },
            "years_to_clear_waitlist": {
                "value": round(years_to_clear, 0),
                "unit": "years",
                "type": "derived_estimate",
                "formula": f"{WAITLIST_SIZE} / {SLOTS_PER_YEAR} slots per year",
            },
            "lifetime_earnings_gap": {
                "value": round(retail_total - care_total, 0),
                "unit": "$",
                "type": "modeled_comparison",
                "formula": (
                    f"30-year cumulative at {ANNUAL_RAISE:.0%} raises, "
                    f"${HHSC_WAGE} vs ${BUCEES_WAGE}"
                ),
            },
            "ftes_for_24_7_coverage": {
                "value": round(model.ftes_needed, 2),
                "unit": "FTEs",
                "type": "derived_estimate",
                "formula": "168 hrs/wk / 40 hrs * 1.18 absence factor",
            },
        },
    }

    OUTPUT.write_text(json.dumps(results, indent=2) + "\n")
    print(f"Wrote {OUTPUT}")
    print(f"  {len(results['figures'])} figures generated")


if __name__ == "__main__":
    main()
