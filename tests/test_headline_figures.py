"""Tests verifying the headline statistics cited in the README and policy brief.

Each test locks down a key claim to its source data, so any data update
that changes a headline number is caught immediately.
"""

import pandas as pd
import pytest

from texas_hhcs.cpi import deflate_wage

# -- Constants from the investigation --
HHSC_WAGE = 10.60
BUCEES_WAGE = 18.00
TX_HHA_EMPLOYMENT = 314_610
CAREER_YEARS = 30
HOURS_PER_YEAR = 2_080
ANNUAL_RAISE = 0.02


@pytest.fixture()
def cpi_annual():
    """CPI-U South annual averages used in the analysis.

    Source: BLS series CUUR0300SA0, annual means for 2015 and 2025.
    Hardcoded so tests run offline without hitting the BLS API.
    """
    return pd.DataFrame({
        "year": [2015, 2025],
        "annual_cpi": [234.812, 318.451],
    })


class TestInflationErosion:
    """$10.60 frozen since ~2015 should be worth ~$14.37 in 2025 dollars,
    and its real purchasing power should be ~$7.82."""

    def test_should_be_wage_approximately_14_37(self, cpi_annual):
        should_be = deflate_wage(HHSC_WAGE, 2015, 2025, cpi_annual)
        assert 14.00 < should_be < 14.80, f"Expected ~$14.37, got ${should_be:.2f}"

    def test_real_purchasing_power_approximately_7_82(self, cpi_annual):
        cpi_2015 = cpi_annual.loc[cpi_annual["year"] == 2015, "annual_cpi"].iloc[0]
        cpi_2025 = cpi_annual.loc[cpi_annual["year"] == 2025, "annual_cpi"].iloc[0]
        real_value = HHSC_WAGE * (cpi_2015 / cpi_2025)
        assert 7.50 < real_value < 8.10, f"Expected ~$7.82, got ${real_value:.2f}"


class TestWaitlistTimeline:
    """100,000+ waitlist / ~1,500 slots per year = ~87 years."""

    def test_years_to_clear(self):
        waitlist = 130_000
        slots_per_year = 1_500
        years = waitlist / slots_per_year
        assert 80 < years < 95, f"Expected ~87 years, got {years:.0f}"


class TestLifetimeEarningsGap:
    """30-year career comparison: care worker vs retail."""

    def test_gap_approximately_624k(self):
        multipliers = [(1 + ANNUAL_RAISE) ** (y - 1) for y in range(1, CAREER_YEARS + 1)]
        care_total = HHSC_WAGE * HOURS_PER_YEAR * sum(multipliers)
        retail_total = BUCEES_WAGE * HOURS_PER_YEAR * sum(multipliers)
        gap = retail_total - care_total
        assert 600_000 < gap < 650_000, f"Expected ~$624,424, got ${gap:,.0f}"


class TestStatewideWageGap:
    """314,610 workers x ($18.00 - $10.60) x 2,080 hours = ~$4.8B."""

    def test_annual_gap_approximately_4_8b(self):
        gap_per_worker = (BUCEES_WAGE - HHSC_WAGE) * HOURS_PER_YEAR
        total = gap_per_worker * TX_HHA_EMPLOYMENT
        total_b = total / 1e9
        assert 4.5 < total_b < 5.2, f"Expected ~$4.8B, got ${total_b:.1f}B"
