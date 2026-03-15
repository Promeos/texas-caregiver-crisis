"""BLS CPI data retrieval and wage deflation utilities."""

import requests
import pandas as pd


def fetch_cpi_series(
    series_id: str = "CUUR0300SA0",  # South Urban CPI-U
    start_year: int = 2010,
    end_year: int = 2025,
) -> pd.DataFrame:
    """Fetch CPI data from BLS API v2.

    Default series: CUUR0300SA0 (CPI-U, South Urban, All Items)
    BLS API v2 allows 20-year spans without a key.
    """
    # BLS API v2 without registration key limits to 10 years per request
    all_rows = []
    for chunk_start in range(start_year, end_year + 1, 10):
        chunk_end = min(chunk_start + 9, end_year)
        resp = requests.post(
            "https://api.bls.gov/publicAPI/v2/timeseries/data/",
            json={
                "seriesid": [series_id],
                "startyear": str(chunk_start),
                "endyear": str(chunk_end),
            },
            timeout=30,
        )
        data = resp.json()
        for series in data["Results"]["series"]:
            for rec in series["data"]:
                if rec["period"].startswith("M") and rec["value"] not in ("-", ""):
                    try:
                        cpi_val = float(rec["value"])
                    except (ValueError, TypeError):
                        continue
                    all_rows.append({
                        "year": int(rec["year"]),
                        "month": int(rec["period"][1:]),
                        "cpi": cpi_val,
                    })

    df = pd.DataFrame(all_rows).sort_values(["year", "month"]).reset_index(drop=True)
    # Compute annual averages
    return df


def annual_cpi(cpi_monthly: pd.DataFrame) -> pd.DataFrame:
    """Compute annual average CPI from monthly data."""
    return (
        cpi_monthly.groupby("year")["cpi"]
        .mean()
        .reset_index()
        .rename(columns={"cpi": "annual_cpi"})
    )


def deflate_wage(
    nominal_wage: float,
    wage_year: int,
    target_year: int,
    cpi_annual: pd.DataFrame,
) -> float:
    """Convert a nominal wage to real dollars in target_year.

    If wage_year=2015 and target_year=2024, this answers:
    'What is $10.60 in 2015 worth in 2024 dollars?'
    """
    base_cpi = cpi_annual.loc[cpi_annual["year"] == wage_year, "annual_cpi"].iloc[0]
    target_cpi = cpi_annual.loc[cpi_annual["year"] == target_year, "annual_cpi"].iloc[0]
    return nominal_wage * (target_cpi / base_cpi)


def build_erosion_table(
    nominal_wage: float,
    set_year: int,
    cpi_annual: pd.DataFrame,
) -> pd.DataFrame:
    """Build a year-by-year table showing real value erosion of a frozen wage.

    Returns DataFrame with columns: year, nominal, real_value, purchasing_power_lost_pct
    """
    base_cpi = cpi_annual.loc[cpi_annual["year"] == set_year, "annual_cpi"].iloc[0]
    years = cpi_annual[cpi_annual["year"] >= set_year].copy()

    years["nominal"] = nominal_wage
    years["real_value"] = nominal_wage * (base_cpi / years["annual_cpi"])
    years["purchasing_power_lost_pct"] = (
        (years["nominal"] - years["real_value"]) / years["nominal"] * 100
    )

    return years[["year", "nominal", "real_value", "purchasing_power_lost_pct"]].reset_index(
        drop=True
    )
