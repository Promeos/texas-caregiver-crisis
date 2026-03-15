"""Rate parsing and calculation utilities for ICF/IID and HCS reimbursement."""

from dataclasses import dataclass
from enum import Enum


class ProgramType(Enum):
    ICF_IID = "ICF/IID"
    HCS = "HCS"


@dataclass
class ICFRate:
    """ICF/IID per-diem reimbursement rate."""

    level_of_care: str  # e.g., "LOC I", "LOC VIII"
    per_diem: float  # daily rate in dollars
    effective_date: str
    source: str  # citation URL or document reference

    @property
    def monthly_revenue(self) -> float:
        return self.per_diem * 30.44  # average days per month

    @property
    def annual_revenue(self) -> float:
        return self.per_diem * 365


@dataclass
class HCSRate:
    """HCS unit-based fee schedule rate."""

    service_code: str
    service_name: str
    unit_rate: float  # per unit (usually 15-min or hourly)
    unit_type: str  # "15-min", "hourly", "daily", "monthly"
    effective_date: str
    source: str


def calculate_bed_revenue(rate: ICFRate, occupancy_pct: float = 1.0) -> dict:
    """Calculate revenue per bed at given occupancy."""
    return {
        "daily": rate.per_diem * occupancy_pct,
        "monthly": rate.monthly_revenue * occupancy_pct,
        "annual": rate.annual_revenue * occupancy_pct,
    }
