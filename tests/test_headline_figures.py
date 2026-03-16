"""Tests verifying the headline statistics cited in the README and policy brief.

Each test locks down a key claim to its source data, so any data update
that changes a headline number is caught immediately.
"""

from pathlib import Path

import pandas as pd
import pytest
from openpyxl import load_workbook

from texas_hhcs.cpi import deflate_wage

# -- Constants from the investigation --
ROOT = Path(__file__).resolve().parent.parent
RAW_WAGE_CALCULATOR = (
    ROOT / "data" / "raw" / "rates" / "ltss-personal-attendant-base-wage-calculator.xlsx"
)
PROCESSED_BLS = ROOT / "data" / "processed" / "bls_oews_texas_2024.csv"
LBB_RIDER_TEXT = ROOT / "data" / "raw" / "external" / "lbb-88th-article-ii-rider.txt"
NCI_WORKFORCE_TEXT = ROOT / "data" / "raw" / "external" / "nci-state-of-the-workforce-2023.txt"
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


class TestSourceData:
    """Source-backed figures should come from checked-in data files."""

    def test_hhsc_target_wage_cell_b7_is_10_60(self):
        wb = load_workbook(RAW_WAGE_CALCULATOR, data_only=True, read_only=True)
        ws = wb["Fiscal by Program"]
        assert ws["B7"].value == pytest.approx(HHSC_WAGE)

    def test_bls_soc_31_1120_matches_processed_extract(self):
        df_bls = pd.read_csv(PROCESSED_BLS)
        soc_311120 = df_bls[df_bls["soc_code"] == "31-1120"]
        assert set(soc_311120["occupation"].unique()) == {"Home Health and Personal Care Aides"}

        measures = soc_311120.set_index("measure")["value"]
        assert measures["hourly_mean"] == pytest.approx(12.19)
        assert int(measures["employment"]) == TX_HHA_EMPLOYMENT

    def test_lbb_3292_figure_is_for_txhml_not_hcs(self):
        lbb_text = LBB_RIDER_TEXT.read_text()
        assert "Strategy A.3.4, Texas Home Living" in lbb_text
        assert "fiscal year 2025 for 3,292 end-of-year waiver slots." in lbb_text

    def test_nci_weighted_average_turnover_ratio_is_39_7(self):
        nci_text = NCI_WORKFORCE_TEXT.read_text()
        assert "weighted average turnover ratio was 39.7%." in nci_text


class TestLifetimeEarningsGap:
    """Illustrative 30-year career comparison: care worker vs retail."""

    def test_gap_approximately_624k(self):
        multipliers = [(1 + ANNUAL_RAISE) ** (y - 1) for y in range(1, CAREER_YEARS + 1)]
        care_total = HHSC_WAGE * HOURS_PER_YEAR * sum(multipliers)
        retail_total = BUCEES_WAGE * HOURS_PER_YEAR * sum(multipliers)
        gap = retail_total - care_total
        assert 600_000 < gap < 650_000, f"Expected ~$624,424, got ${gap:,.0f}"


class TestStatewideWageGap:
    """Upper-bound scenario using all BLS SOC 31-1120 workers."""

    def test_annual_gap_approximately_4_8b(self):
        gap_per_worker = (BUCEES_WAGE - HHSC_WAGE) * HOURS_PER_YEAR
        total = gap_per_worker * TX_HHA_EMPLOYMENT
        total_b = total / 1e9
        assert 4.5 < total_b < 5.2, f"Expected ~$4.8B, got ${total_b:.1f}B"
