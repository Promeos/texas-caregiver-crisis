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


def compare_rate_change(
    old_rate: float,
    new_rate: float,
    occupancy_pct: float = 0.95,
) -> dict:
    """Calculate the revenue impact of a rate change per bed.

    Args:
        old_rate: Old daily per-diem or daily-equivalent rate
        new_rate: New daily per-diem or daily-equivalent rate
        occupancy_pct: Assumed occupancy (default 95%)
    """
    days_per_year = 365
    old_annual = old_rate * days_per_year * occupancy_pct
    new_annual = new_rate * days_per_year * occupancy_pct
    return {
        "old_daily": old_rate,
        "new_daily": new_rate,
        "increase_daily": new_rate - old_rate,
        "increase_pct": (new_rate - old_rate) / old_rate if old_rate > 0 else 0,
        "old_annual_per_bed": round(old_annual, 2),
        "new_annual_per_bed": round(new_annual, 2),
        "annual_increase_per_bed": round(new_annual - old_annual, 2),
    }
