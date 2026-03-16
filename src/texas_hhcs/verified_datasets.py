"""Parsers for audited HHSC waitlist and cost datasets."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import load_workbook


MONTH_MAP = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "march": 3,
    "mar": 3,
    "april": 4,
    "apr": 4,
    "may": 5,
    "june": 6,
    "jun": 6,
    "july": 7,
    "jul": 7,
    "aug": 8,
    "august": 8,
    "sept": 9,
    "sep": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}

PROGRAM_MAP = {
    "CLASS": "CLASS",
    "DBMD": "DBMD",
    "HCS": "HCS",
    "HCS 1": "HCS",
    "MDCP": "MDCP",
    "STAR+": "STAR_PLUS_HCBS",
    "STAR+PLUS": "STAR_PLUS_HCBS",
    "TXHML": "TXHML",
    "TXHML 1": "TXHML",
    "TOTALS": "ALL_PROGRAMS",
}

SETTING_BLOCKS = [
    (
        "State Operated ICF/IID (SSLC)a",
        "STATE_OPERATED_ICF_IID_SSLC",
        [
            "Long-term Care Costs – Average",
            "Administrative/Overhead Costs",
            "Total State Operated ICF/IID Costs",
        ],
        [
            "long_term_care_cost_average",
            "administrative_overhead_costs",
            "total_costs",
        ],
    ),
    (
        "Non-State Operated ICF/IID (Community ICF/IID)",
        "COMMUNITY_ICF_IID",
        [
            "Long-term Care Costs – Average",
            "Acute Care Cost - Average",
            "Total Non-State Operated ICF/IID Costs",
        ],
        [
            "long_term_care_cost_average",
            "acute_care_cost_average",
            "total_costs",
        ],
    ),
    (
        "HCS Waiver: Residential",
        "HCS_RESIDENTIAL",
        [
            "Long-term Care Costs – Average",
            "Acute Care Cost - Average",
            "Total HCS Waiver: Residential Costs",
        ],
        [
            "long_term_care_cost_average",
            "acute_care_cost_average",
            "total_costs",
        ],
    ),
    (
        "HCS Waiver: Non-Residential",
        "HCS_NON_RESIDENTIAL",
        [
            "Long-term Care Costs – Average",
            "Acute Care Cost - Average",
            "Total HCS Waiver: Non-Residential Costs",
        ],
        [
            "long_term_care_cost_average",
            "acute_care_cost_average",
            "total_costs",
        ],
    ),
    (
        "HCS Waiver: All Settings",
        "HCS_ALL_SETTINGS",
        [
            "Long-term Care Costs – Average",
            "Acute Care Cost - Average",
            "Total HCS Waiver: All Settings Costs",
        ],
        [
            "long_term_care_cost_average",
            "acute_care_cost_average",
            "total_costs",
        ],
    ),
    (
        "TxHmL Waiver",
        "TXHML",
        [
            "Long-term Care Costs – Average",
            "Acute Care Cost - Average",
            "Total TxHmL Costs",
        ],
        [
            "long_term_care_cost_average",
            "acute_care_cost_average",
            "total_costs",
        ],
    ),
]

LON_LABELS = {
    "Intermittent (LON 1)": 1,
    "Limited (LON 5)": 5,
    "Extensive (LON 8)": 8,
    "Pervasive (LON 6)": 6,
    "Pervasive Plus (LON 9)": 9,
    "Overall - Total": "ALL",
    "Overall - Average": "ALL",
}

HCS_COST_AREAS = [
    {
        "program": "HCS_TXHML",
        "cost_area": "RESIDENTIAL_SL_RSS",
        "source_file": "2024-hcs-cost-report-instructions.txt",
        "source_line_start": 4071,
        "source_line_end": 4083,
        "description": "Group-home-specific supervised living and residential support costs.",
    },
    {
        "program": "HCS_TXHML",
        "cost_area": "INDIVIDUALIZED_SKILLS_SOCIALIZATION",
        "source_file": "2024-hcs-cost-report-instructions.txt",
        "source_line_start": 4084,
        "source_line_end": 4102,
        "description": "Individualized Skills and Socialization facility and staffing costs.",
    },
    {
        "program": "HCS_TXHML",
        "cost_area": "PROGRAM_ADMINISTRATION_OPERATIONS",
        "source_file": "2024-hcs-cost-report-instructions.txt",
        "source_line_start": 4106,
        "source_line_end": 4112,
        "description": "Direct program-management administrative expenses for the contracted provider.",
    },
    {
        "program": "HCS_TXHML",
        "cost_area": "CENTRAL_OFFICE",
        "source_file": "2024-hcs-cost-report-instructions.txt",
        "source_line_start": 4114,
        "source_line_end": 4136,
        "description": "Allocated shared administrative costs reported at actual cost with no markup.",
    },
]

ICF_COST_AREAS = [
    {
        "program": "ICF_IID",
        "cost_area": "RESIDENTIAL_SMALL_MEDIUM_LARGE",
        "source_file": "2024-icf-cost-report-instructions.txt",
        "source_line_start": 3950,
        "source_line_end": 3961,
        "description": "Residential facility costs reported separately by small, medium, and large homes.",
    },
    {
        "program": "ICF_IID",
        "cost_area": "DAY_HABILITATION",
        "source_file": "2024-icf-cost-report-instructions.txt",
        "source_line_start": 3963,
        "source_line_end": 3979,
        "description": "Day habilitation facility and shared-service costs.",
    },
    {
        "program": "ICF_IID",
        "cost_area": "PROGRAM_ADMINISTRATION_OPERATIONS",
        "source_file": "2024-icf-cost-report-instructions.txt",
        "source_line_start": 3981,
        "source_line_end": 3989,
        "description": "Administrative expenses directly chargeable to the facility itself.",
    },
    {
        "program": "ICF_IID",
        "cost_area": "CENTRAL_OFFICE",
        "source_file": "2024-icf-cost-report-instructions.txt",
        "source_line_start": 3991,
        "source_line_end": 4013,
        "description": "Allocated shared administrative costs reported at actual cost with no markup.",
    },
]


def _normalize_program(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = re.sub(r"[^A-Z+]", "", str(value).strip().upper())
    normalized_map = {
        "CLASS": "CLASS",
        "DBMD": "DBMD",
        "HCS": "HCS",
        "MDCP": "MDCP",
        "STAR+": "STAR_PLUS_HCBS",
        "STARPLUS": "STAR_PLUS_HCBS",
        "STAR+PLUSHCBS": "STAR_PLUS_HCBS",
        "STARPLUSHCBS": "STAR_PLUS_HCBS",
        "TXHML": "TXHML",
        "TOTALS": "ALL_PROGRAMS",
    }
    return normalized_map.get(cleaned)


def _clean_int(value: object) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, str):
        value = value.replace(",", "").strip()
        if value == "":
            return None
    return int(float(value))


def _clean_float(value: object) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def _parse_currency(value: str) -> float:
    return float(value.replace("$", "").replace(",", ""))


def _interest_list_report_month(path: Path) -> str:
    match = re.search(r"interest-list-data-([a-z]+)-(\d{4})\.xlsx$", path.name)
    if not match:
        raise ValueError(f"Could not parse report month from {path.name}")
    month_name, year = match.groups()
    month = MONTH_MAP[month_name.lower()]
    return f"{year}-{month:02d}-01"


def _stripped_lines(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def _find_row(ws, expected: str) -> int:
    for row in range(1, ws.max_row + 1):
        value = ws.cell(row, 1).value
        if value == expected:
            return row
    raise ValueError(f"Row starting with {expected!r} not found in {ws.title}")


def _find_row_prefix(ws, prefix: str) -> int:
    for row in range(1, ws.max_row + 1):
        value = ws.cell(row, 1).value
        if isinstance(value, str) and value.strip().startswith(prefix):
            return row
    raise ValueError(f"Row starting with {prefix!r} not found in {ws.title}")


def _find_row_contains_prefix(ws, prefix: str) -> int:
    for row in range(1, ws.max_row + 1):
        for col in range(1, ws.max_column + 1):
            value = ws.cell(row, col).value
            if isinstance(value, str) and value.strip().startswith(prefix):
                return row
    raise ValueError(f"Row containing {prefix!r} not found in {ws.title}")


def _find_line_prefix(lines: list[str], prefix: str, start: int = 0) -> int:
    for idx in range(start, len(lines)):
        if lines[idx].startswith(prefix):
            return idx
    raise ValueError(f"Line starting with {prefix!r} not found")


def _sheet_by_prefix(workbook, prefix: str):
    for sheet_name in workbook.sheetnames:
        if sheet_name == prefix or sheet_name.startswith(prefix):
            return workbook[sheet_name]
    raise KeyError(f"Worksheet starting with {prefix!r} does not exist")


def _program_columns(ws, program_row: int, value_row: int, expected_metric: str) -> list[tuple[int, str]]:
    columns: list[tuple[int, str]] = []
    for col in range(2, ws.max_column + 1):
        program = _normalize_program(ws.cell(program_row, col).value)
        metric = ws.cell(value_row, col).value
        if not program or not isinstance(metric, str):
            continue
        if metric.replace(" ", "").startswith(expected_metric.replace(" ", "")):
            columns.append((col, program))
    return columns


def _row_texts(ws, row: int) -> list[str]:
    texts: list[str] = []
    for col in range(1, ws.max_column + 1):
        value = ws.cell(row, col).value
        if isinstance(value, str) and value.strip():
            texts.append(" ".join(value.split()))
    return texts


def _row_label_and_reference(ws, row: int, label_prefix: str) -> tuple[str | None, str | None]:
    texts = _row_texts(ws, row)
    label = next((text for text in texts if text.startswith(label_prefix)), None)
    reference = next(
        (
            text
            for text in texts
            if text != label and _normalize_program(text) is None
        ),
        None,
    )
    return label, reference


def build_interest_list_totals(monthly_dir: Path) -> pd.DataFrame:
    rows: list[dict] = []
    for path in sorted(monthly_dir.glob("interest-list-data-*.xlsx")):
        wb = load_workbook(path, data_only=True)
        ws = _sheet_by_prefix(wb, "Time on Interest List")
        header_row = _find_row(ws, "Years on List")
        totals_row = _find_row(ws, "Totals")
        if _normalize_program(ws.cell(header_row, 2).value):
            program_row = header_row
            value_row = header_row + 1
        else:
            program_row = header_row - 1
            value_row = header_row
        report_month = _interest_list_report_month(path)
        for col, program in _program_columns(ws, program_row, value_row, "Individuals"):
            rows.append(
                {
                    "report_month": report_month,
                    "program": program,
                    "individuals": _clean_int(ws.cell(totals_row, col).value),
                    "source_file": path.name,
                }
            )
        wb.close()
    return pd.DataFrame(rows).sort_values(["report_month", "program"]).reset_index(drop=True)


def build_interest_list_years_on_list(monthly_dir: Path) -> pd.DataFrame:
    rows: list[dict] = []
    for path in sorted(monthly_dir.glob("interest-list-data-*.xlsx")):
        wb = load_workbook(path, data_only=True)
        ws = _sheet_by_prefix(wb, "Time on Interest List")
        header_row = _find_row(ws, "Years on List")
        totals_row = _find_row(ws, "Totals")
        if _normalize_program(ws.cell(header_row, 2).value):
            program_row = header_row
            value_row = header_row + 1
            data_start = header_row + 2
        else:
            program_row = header_row - 1
            value_row = header_row
            data_start = header_row + 1
        program_columns = _program_columns(ws, program_row, value_row, "Individuals")
        report_month = _interest_list_report_month(path)
        for row in range(data_start, totals_row):
            bucket = ws.cell(row, 1).value
            if not bucket:
                continue
            for col, program in program_columns:
                individuals = _clean_int(ws.cell(row, col).value)
                percent = _clean_float(ws.cell(row, col + 1).value)
                if individuals is None:
                    continue
                rows.append(
                    {
                        "report_month": report_month,
                        "program": program,
                        "years_on_list_bucket": bucket,
                        "individuals": individuals,
                        "percent_of_program_total": percent,
                        "source_file": path.name,
                    }
                )
        wb.close()
    return pd.DataFrame(rows).sort_values(
        ["report_month", "program", "years_on_list_bucket"]
    ).reset_index(drop=True)


def build_interest_list_closure_summary(monthly_dir: Path) -> pd.DataFrame:
    rows: list[dict] = []
    for path in sorted(monthly_dir.glob("interest-list-data-*.xlsx")):
        wb = load_workbook(path, data_only=True)
        ws = _sheet_by_prefix(wb, "Closure Overview")
        header_row = _find_row(ws, "Categories:")
        totals_row = _find_row(ws, "Totals")
        if _normalize_program(ws.cell(header_row, 2).value):
            program_row = header_row
            value_row = header_row + 1
            data_start = header_row + 2
        else:
            program_row = header_row - 1
            value_row = header_row
            data_start = header_row + 1
        program_columns = _program_columns(ws, program_row, value_row, "Closures")
        report_month = _interest_list_report_month(path)
        for row in range(data_start, totals_row + 1):
            category = ws.cell(row, 1).value
            for col, program in program_columns:
                closures = _clean_int(ws.cell(row, col).value)
                percent = _clean_float(ws.cell(row, col + 1).value)
                if closures is None:
                    continue
                rows.append(
                    {
                        "report_month": report_month,
                        "program": program,
                        "closure_category": category,
                        "closures": closures,
                        "percent_of_program_closures": percent,
                        "source_file": path.name,
                    }
                )
        wb.close()
    return pd.DataFrame(rows).sort_values(
        ["report_month", "program", "closure_category"]
    ).reset_index(drop=True)


def build_interest_list_releases_summary(monthly_dir: Path) -> pd.DataFrame:
    rows: list[dict] = []
    metric_prefixes = [
        ("previous_biennium_counts", "Previous Biennium Counts", False),
        ("enrolled", "Enrolled", False),
        ("denied_declined_withdrawn", "Denied/Declined/Withdrawn", False),
        ("pipeline", "Pipeline", False),
        ("not_categorized", "Not Categorized", True),
        ("total_releases_this_biennium", "Total Releases This Biennium", False),
        ("added_this_biennium", "Added This Biennium", False),
        ("current_interest_list_counts", "Current Interest List Counts", False),
    ]
    for path in sorted(monthly_dir.glob("interest-list-data-*.xlsx")):
        wb = load_workbook(path, data_only=True)
        ws = _sheet_by_prefix(wb, "IL Releases Summary")
        header_row = next(
            row
            for row in range(1, ws.max_row + 1)
            if sum(
                1
                for col in range(1, ws.max_column + 1)
                if _normalize_program(ws.cell(row, col).value)
            )
            >= 4
        )
        program_columns = [
            (col, program)
            for col in range(1, ws.max_column + 1)
            if (program := _normalize_program(ws.cell(header_row, col).value))
        ]
        report_month = _interest_list_report_month(path)
        for metric, prefix, allow_missing in metric_prefixes:
            try:
                row = _find_row_contains_prefix(ws, prefix)
            except ValueError:
                if allow_missing:
                    continue
                raise
            label, reference = _row_label_and_reference(ws, row, prefix)
            for col, program in program_columns:
                value = _clean_int(ws.cell(row, col).value)
                if value is None:
                    continue
                rows.append(
                    {
                        "report_month": report_month,
                        "program": program,
                        "metric": metric,
                        "label": label,
                        "reference_text": reference,
                        "value": value,
                        "source_file": path.name,
                    }
                )
        wb.close()
    return pd.DataFrame(rows).sort_values(
        ["report_month", "program", "metric"]
    ).reset_index(drop=True)


def build_interest_list_legislative_allocations(page_html: Path) -> pd.DataFrame:
    soup = BeautifulSoup(page_html.read_text(), "html.parser")
    table = soup.find("table")
    if table is None:
        raise ValueError("Legislative allocation table not found on interest-list page")
    rows: list[dict] = []
    for tr in table.find_all("tr")[1:]:
        tds = tr.find_all("td")
        if len(tds) != 2:
            continue
        program_text = " ".join(tds[0].get_text(" ", strip=True).split())
        allocation_text = " ".join(tds[1].get_text(" ", strip=True).split())
        rows.append(
            {
                "biennium": "2022-2023",
                "program_label": program_text,
                "program": _normalize_program(program_text.split("(")[-1].rstrip(")")) or (
                    "ALL_PROGRAMS" if "Total of allocations" in program_text else program_text
                ),
                "legislative_allocation": _clean_int(allocation_text.replace(",", "")),
                "source_file": page_html.name,
            }
        )
    return pd.DataFrame(rows)


def build_setting_costs(report_text: Path) -> pd.DataFrame:
    lines = _stripped_lines(report_text)
    rows: list[dict] = []
    block_labels = [label for label, _, _, _ in SETTING_BLOCKS]
    for block_index, (label, setting, metric_labels, metric_names) in enumerate(SETTING_BLOCKS):
        idx = lines.index(label)
        next_idx = (
            lines.index(block_labels[block_index + 1])
            if block_index + 1 < len(block_labels)
            else _find_line_prefix(lines, "Table 2.", idx + 1)
        )
        block_lines = lines[idx + 1 : next_idx]
        for metric_label in metric_labels:
            if metric_label not in block_lines:
                raise ValueError(f"Expected {metric_label!r} after {label!r}")
        currencies = [line for line in block_lines if line.startswith("$")]
        if len(currencies) != len(metric_names):
            raise ValueError(f"Expected {len(metric_names)} currency values for {label!r}")
        for metric_name, value in zip(metric_names, currencies, strict=True):
            rows.append(
                {
                    "fiscal_year": 2023,
                    "setting": setting,
                    "metric": metric_name,
                    "monthly_average_cost": _parse_currency(value),
                    "source_file": report_text.name,
                }
            )
    return pd.DataFrame(rows)


def build_icf_community_costs_by_lon(report_text: Path) -> pd.DataFrame:
    lines = _stripped_lines(report_text)
    table2_headers = ["Small", "Medium", "Large", "Total"]
    table3_headers = ["Small", "Medium", "Large", "Average"]
    counts: list[dict] = []
    costs: list[dict] = []
    table2_start = _find_line_prefix(
        lines, "Table 2. Non-state ICF/IID by Facility Size: Average Number of Individuals Served Per"
    )
    table3_start = _find_line_prefix(
        lines, "Table 3. Non-state ICF/IID by Facility Size: Monthly Average Cost Per Individual"
    )

    for label, lon in LON_LABELS.items():
        if label == "Overall - Average":
            continue
        idx = _find_line_prefix(lines, label, table2_start)
        values = lines[idx - 4 : idx] if label == "Overall - Total" else lines[idx + 1 : idx + 5]
        for offset, facility_size in enumerate(table2_headers, start=1):
            normalized_size = "ALL" if facility_size == "Total" else facility_size.upper()
            counts.append(
                {
                    "level_of_need": lon,
                    "facility_size": normalized_size,
                    "average_individuals_served_per_month": _clean_int(values[offset - 1].replace(",", "")),
                }
            )

    for label, lon in LON_LABELS.items():
        if label == "Overall - Total":
            continue
        idx = _find_line_prefix(lines, label, table3_start)
        for offset, facility_size in enumerate(table3_headers, start=1):
            normalized_size = "ALL" if facility_size == "Average" else facility_size.upper()
            costs.append(
                {
                    "level_of_need": lon,
                    "facility_size": normalized_size,
                    "monthly_average_cost_per_individual": _parse_currency(lines[idx + offset]),
                }
            )

    return pd.merge(pd.DataFrame(counts), pd.DataFrame(costs), on=["level_of_need", "facility_size"])


def build_residential_rate_components(rate_csv: Path) -> pd.DataFrame:
    df = pd.read_csv(rate_csv)

    hcs = df[(df["program"] == "HCS") & (df["service_category"] == "SL/RSS")].copy()
    hcs["program"] = "HCS"
    hcs["setting"] = "SL_RSS"
    hcs["facility_size"] = pd.NA
    hcs["level_of_need"] = hcs["bill_description"].str.extract(r"LON (\d+)").astype(int)

    icf = df[
        (df["program"] == "ICF")
        & (df["bill_description"].str.contains("NON-STATE COMMUNITY RESIDENTIAL", na=False))
    ].copy()
    icf["program"] = "ICF_IID"
    icf["setting"] = "NON_STATE_COMMUNITY_RESIDENTIAL"
    icf["facility_size"] = icf["bill_description"].str.extract(r"- (Small|Medium|Large)$")[0].str.upper()
    icf["level_of_need"] = icf["bill_description"].str.extract(r"LON (\d+)").astype(int)

    combined = pd.concat([hcs, icf], ignore_index=True, sort=False)
    combined["non_attendant_reimbursement_component"] = (
        combined["current_rate"] - combined["attendant_cost"]
    )
    return combined[
        [
            "program",
            "setting",
            "facility_size",
            "level_of_need",
            "bill_description",
            "current_rate",
            "attendant_cost",
            "attendant_cost_pct",
            "non_attendant_reimbursement_component",
            "wage_required",
            "rate_effective_date",
        ]
    ].sort_values(["program", "facility_size", "level_of_need"]).reset_index(drop=True)


def build_cost_report_cost_areas() -> pd.DataFrame:
    return pd.DataFrame(HCS_COST_AREAS + ICF_COST_AREAS)
