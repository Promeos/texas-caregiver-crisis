"""Tests for audited HHSC waitlist and HCS/ICF cost datasets."""

from pathlib import Path

import pandas as pd
import pytest

from texas_hhcs.verified_datasets import (
    build_cost_report_cost_areas,
    build_icf_community_costs_by_lon,
    build_interest_list_closure_summary,
    build_interest_list_legislative_allocations,
    build_interest_list_releases_summary,
    build_interest_list_totals,
    build_interest_list_years_on_list,
    build_residential_rate_components,
    build_setting_costs,
)

ROOT = Path(__file__).resolve().parent.parent
RAW_OFFICIAL = ROOT / "data" / "raw" / "official"
MONTHLY_DIR = RAW_OFFICIAL / "interest-list-monthly"
PROCESSED = ROOT / "data" / "processed"


def _normalize_frame(df: pd.DataFrame) -> pd.DataFrame:
    normalized = df.copy()
    for column in normalized.columns:
        if (
            pd.api.types.is_object_dtype(normalized[column])
            or pd.api.types.is_string_dtype(normalized[column])
            or pd.api.types.is_datetime64_any_dtype(normalized[column])
        ):
            normalized[column] = normalized[column].astype("string")
        normalized[column] = normalized[column].where(normalized[column].notna(), pd.NA)
    return normalized.reset_index(drop=True)


def _assert_csv_matches_builder(csv_name: str, expected: pd.DataFrame) -> pd.DataFrame:
    actual = pd.read_csv(PROCESSED / csv_name)
    pd.testing.assert_frame_equal(
        _normalize_frame(actual),
        _normalize_frame(expected),
        check_dtype=False,
        check_exact=False,
        rtol=1e-9,
        atol=1e-9,
    )
    return actual


@pytest.fixture(scope="module")
def interest_list_totals() -> pd.DataFrame:
    return build_interest_list_totals(MONTHLY_DIR)


@pytest.fixture(scope="module")
def interest_list_years_on_list() -> pd.DataFrame:
    return build_interest_list_years_on_list(MONTHLY_DIR)


@pytest.fixture(scope="module")
def interest_list_closure_summary() -> pd.DataFrame:
    return build_interest_list_closure_summary(MONTHLY_DIR)


@pytest.fixture(scope="module")
def interest_list_releases_summary() -> pd.DataFrame:
    return build_interest_list_releases_summary(MONTHLY_DIR)


@pytest.fixture(scope="module")
def legislative_allocations() -> pd.DataFrame:
    return build_interest_list_legislative_allocations(RAW_OFFICIAL / "interest-list-reduction.html")


@pytest.fixture(scope="module")
def setting_costs() -> pd.DataFrame:
    return build_setting_costs(RAW_OFFICIAL / "cost-comparison-report-aug-2024.txt")


@pytest.fixture(scope="module")
def community_icf_costs() -> pd.DataFrame:
    return build_icf_community_costs_by_lon(RAW_OFFICIAL / "cost-comparison-report-aug-2024.txt")


@pytest.fixture(scope="module")
def residential_rate_components() -> pd.DataFrame:
    return build_residential_rate_components(PROCESSED / "pfd_wage_calculator_all_services.csv")


@pytest.fixture(scope="module")
def cost_report_cost_areas() -> pd.DataFrame:
    return build_cost_report_cost_areas()


class TestInterestListDatasets:
    def test_totals_csv_matches_builder_and_jan_2026_values(self, interest_list_totals):
        totals = _assert_csv_matches_builder(
            "hhsc_interest_list_totals_monthly.csv",
            interest_list_totals,
        )
        jan_2026 = totals[totals["report_month"] == "2026-01-01"].set_index("program")["individuals"]
        assert jan_2026["HCS"] == 130_764
        assert jan_2026["TXHML"] == 117_175
        assert jan_2026["STAR_PLUS_HCBS"] == 15_144

    def test_years_on_list_csv_matches_builder_and_hcs_bucket(self, interest_list_years_on_list):
        years = _assert_csv_matches_builder(
            "hhsc_interest_list_years_on_list_monthly.csv",
            interest_list_years_on_list,
        )
        hcs_bucket = years[
            (years["report_month"] == "2026-01-01")
            & (years["program"] == "HCS")
            & (years["years_on_list_bucket"] == "0–1")
        ].iloc[0]
        assert hcs_bucket["individuals"] == 8_304
        assert hcs_bucket["percent_of_program_total"] == pytest.approx(0.0635037)

    def test_closure_summary_csv_matches_builder_and_hcs_enrolled(self, interest_list_closure_summary):
        closures = _assert_csv_matches_builder(
            "hhsc_interest_list_closure_summary_monthly.csv",
            interest_list_closure_summary,
        )
        hcs_enrolled = closures[
            (closures["report_month"] == "2026-01-01")
            & (closures["program"] == "HCS")
            & (closures["closure_category"] == "Enrolled")
        ].iloc[0]
        assert hcs_enrolled["closures"] == 339
        assert hcs_enrolled["percent_of_program_closures"] == pytest.approx(0.5978835978835979)

    def test_releases_summary_csv_matches_builder_and_hcs_release_metrics(
        self, interest_list_releases_summary
    ):
        releases = _assert_csv_matches_builder(
            "hhsc_interest_list_releases_summary_monthly.csv",
            interest_list_releases_summary,
        )
        hcs_metrics = releases[
            (releases["report_month"] == "2026-01-01")
            & (releases["program"] == "HCS")
        ].set_index("metric")["value"]
        assert hcs_metrics["enrolled"] == 339
        assert hcs_metrics["total_releases_this_biennium"] == 284
        assert hcs_metrics["current_interest_list_counts"] == 130_764

    def test_legislative_allocations_csv_matches_builder_and_hcs_slots(self, legislative_allocations):
        allocations = _assert_csv_matches_builder(
            "hhsc_interest_list_legislative_allocations.csv",
            legislative_allocations,
        )
        values = allocations.set_index("program")["legislative_allocation"]
        assert values["HCS"] == 542
        assert values["TXHML"] == 471
        assert values["STAR_PLUS_HCBS"] == 107
        assert values["ALL_PROGRAMS"] == 1_549


class TestOperatorCostDatasets:
    def test_setting_costs_csv_matches_builder_and_key_totals(self, setting_costs):
        costs = _assert_csv_matches_builder("hhsc_setting_costs_fy2023.csv", setting_costs)
        values = costs.set_index(["setting", "metric"])["monthly_average_cost"]
        assert values[("COMMUNITY_ICF_IID", "total_costs")] == pytest.approx(5247.52)
        assert values[("HCS_RESIDENTIAL", "total_costs")] == pytest.approx(6563.91)
        assert values[("HCS_ALL_SETTINGS", "total_costs")] == pytest.approx(4559.15)

    def test_community_icf_costs_csv_matches_builder_and_small_lon1(self, community_icf_costs):
        costs = _assert_csv_matches_builder(
            "hhsc_community_icf_iid_costs_by_lonsize_fy2023.csv",
            community_icf_costs,
        )
        lon1_small = costs[
            (costs["level_of_need"] == "1") | (costs["level_of_need"] == 1)
        ]
        lon1_small = lon1_small[lon1_small["facility_size"] == "SMALL"].iloc[0]
        assert lon1_small["average_individuals_served_per_month"] == 999
        assert lon1_small["monthly_average_cost_per_individual"] == pytest.approx(4232.10)

        overall = costs[
            (costs["level_of_need"] == "ALL") & (costs["facility_size"] == "ALL")
        ].iloc[0]
        assert overall["average_individuals_served_per_month"] == 4264
        assert overall["monthly_average_cost_per_individual"] == pytest.approx(4779.48)

    def test_residential_rate_components_csv_matches_builder_and_key_rows(
        self, residential_rate_components
    ):
        rates = _assert_csv_matches_builder(
            "hhsc_residential_rate_components.csv",
            residential_rate_components,
        )
        icf_small_lon1 = rates[
            (rates["program"] == "ICF_IID")
            & (rates["facility_size"] == "SMALL")
            & (rates["level_of_need"] == 1)
        ].iloc[0]
        assert icf_small_lon1["current_rate"] == pytest.approx(155.04)
        assert icf_small_lon1["attendant_cost"] == pytest.approx(60.3944)
        assert icf_small_lon1["non_attendant_reimbursement_component"] == pytest.approx(94.6456)

        hcs_lon5 = rates[
            (rates["program"] == "HCS")
            & (rates["bill_description"] == "SUPERVISED LIVING LON 5")
        ].iloc[0]
        assert hcs_lon5["current_rate"] == pytest.approx(158.00)
        assert hcs_lon5["attendant_cost"] == pytest.approx(85.74)
        assert hcs_lon5["non_attendant_reimbursement_component"] == pytest.approx(72.26)

    def test_cost_report_cost_areas_csv_matches_builder(self, cost_report_cost_areas):
        areas = _assert_csv_matches_builder(
            "hhsc_cost_report_cost_areas.csv",
            cost_report_cost_areas,
        )
        expected_pairs = {
            ("HCS_TXHML", "RESIDENTIAL_SL_RSS"),
            ("HCS_TXHML", "CENTRAL_OFFICE"),
            ("ICF_IID", "RESIDENTIAL_SMALL_MEDIUM_LARGE"),
            ("ICF_IID", "DAY_HABILITATION"),
        }
        assert expected_pairs.issubset(set(zip(areas["program"], areas["cost_area"])))
