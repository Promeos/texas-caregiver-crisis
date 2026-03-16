"""Generate audited waitlist and HCS/ICF cost datasets from checked-in source files."""

from pathlib import Path

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
RAW = ROOT / "data" / "raw" / "official"
PROCESSED = ROOT / "data" / "processed"


def write_csv(name: str, df) -> None:
    path = PROCESSED / name
    df.to_csv(path, index=False)
    print(f"Wrote {path}")


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)

    monthly_dir = RAW / "interest-list-monthly"
    write_csv(
        "hhsc_interest_list_totals_monthly.csv",
        build_interest_list_totals(monthly_dir),
    )
    write_csv(
        "hhsc_interest_list_years_on_list_monthly.csv",
        build_interest_list_years_on_list(monthly_dir),
    )
    write_csv(
        "hhsc_interest_list_closure_summary_monthly.csv",
        build_interest_list_closure_summary(monthly_dir),
    )
    write_csv(
        "hhsc_interest_list_releases_summary_monthly.csv",
        build_interest_list_releases_summary(monthly_dir),
    )
    write_csv(
        "hhsc_interest_list_legislative_allocations.csv",
        build_interest_list_legislative_allocations(RAW / "interest-list-reduction.html"),
    )
    write_csv(
        "hhsc_setting_costs_fy2023.csv",
        build_setting_costs(RAW / "cost-comparison-report-aug-2024.txt"),
    )
    write_csv(
        "hhsc_community_icf_iid_costs_by_lonsize_fy2023.csv",
        build_icf_community_costs_by_lon(RAW / "cost-comparison-report-aug-2024.txt"),
    )
    write_csv(
        "hhsc_residential_rate_components.csv",
        build_residential_rate_components(PROCESSED / "pfd_wage_calculator_all_services.csv"),
    )
    write_csv(
        "hhsc_cost_report_cost_areas.csv",
        build_cost_report_cost_areas(),
    )


if __name__ == "__main__":
    main()
