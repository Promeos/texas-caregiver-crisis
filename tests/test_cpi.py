"""Tests for CPI utility functions (offline, no BLS API calls)."""

import pandas as pd
import pytest

from texas_hhcs.cpi import annual_cpi, build_erosion_table, deflate_wage


def _make_monthly_cpi():
    """Synthetic CPI data for testing."""
    rows = []
    for year in range(2015, 2026):
        for month in range(1, 13):
            rows.append({"year": year, "month": month, "cpi": 230.0 + (year - 2015) * 8.0})
    return pd.DataFrame(rows)


def test_annual_cpi_returns_one_row_per_year():
    df = annual_cpi(_make_monthly_cpi())
    assert len(df) == 11
    assert list(df.columns) == ["year", "annual_cpi"]


def test_annual_cpi_values_are_means():
    monthly = _make_monthly_cpi()
    result = annual_cpi(monthly)
    # All months in a given year have the same CPI in our synthetic data
    for _, row in result.iterrows():
        expected = 230.0 + (row["year"] - 2015) * 8.0
        assert row["annual_cpi"] == pytest.approx(expected)


def test_deflate_wage_identity():
    """Deflating a wage to its own year should return the same wage."""
    cpi_df = pd.DataFrame({"year": [2020], "annual_cpi": [300.0]})
    assert deflate_wage(15.00, 2020, 2020, cpi_df) == pytest.approx(15.00)


def test_deflate_wage_increases_with_inflation():
    """A wage from an earlier year should be worth more in a later year."""
    cpi_df = pd.DataFrame({"year": [2015, 2025], "annual_cpi": [230.0, 300.0]})
    result = deflate_wage(10.00, 2015, 2025, cpi_df)
    assert result > 10.00


def test_build_erosion_table_shape():
    cpi_ann = annual_cpi(_make_monthly_cpi())
    table = build_erosion_table(10.60, 2015, cpi_ann)
    assert "real_value" in table.columns
    assert "purchasing_power_lost_pct" in table.columns
    assert len(table) == 11  # 2015 through 2025


def test_build_erosion_table_base_year_no_erosion():
    """In the base year, real_value should equal nominal and erosion should be 0."""
    cpi_ann = annual_cpi(_make_monthly_cpi())
    table = build_erosion_table(10.60, 2015, cpi_ann)
    base_row = table[table["year"] == 2015].iloc[0]
    assert base_row["real_value"] == pytest.approx(10.60)
    assert base_row["purchasing_power_lost_pct"] == pytest.approx(0.0)
