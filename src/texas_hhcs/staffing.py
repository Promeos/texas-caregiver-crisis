"""Staffing coverage math and overtime modeling for 24/7 residential care."""

from dataclasses import dataclass

# Constants
HOURS_PER_WEEK = 168  # 24 * 7
STANDARD_WORK_WEEK = 40
DAYS_OFF_PER_YEAR = 78  # weekends (104) adjusted for rotating schedule
PTO_DAYS = 10
TRAINING_DAYS = 5
FICA_RATE = 0.0765  # employer share of FICA


@dataclass
class StaffingModel:
    """Model 24/7 staffing coverage for a residential home."""

    residents: int
    staff_per_shift: int  # minimum staff on duty at any time
    hourly_wage: float
    overtime_multiplier: float = 1.5
    benefits_pct: float = 0.10  # benefits as % of wages (often minimal in this sector)
    workers_comp_pct: float = 0.03

    @property
    def weekly_hours_needed(self) -> float:
        """Total staff-hours needed per week for 24/7 coverage."""
        return HOURS_PER_WEEK * self.staff_per_shift

    @property
    def ftes_needed(self) -> float:
        """FTEs required for coverage (before accounting for absences).

        Rule of thumb: 24/7 coverage of one position requires ~4.2 FTEs
        at 40hr/week. With PTO/training/callouts, closer to 5.0-5.2.
        """
        base = self.weekly_hours_needed / STANDARD_WORK_WEEK
        absence_factor = 1.18  # ~18% absence/coverage buffer
        return base * absence_factor

    @property
    def annual_regular_hours(self) -> float:
        """Total regular (non-OT) hours per year across all staff."""
        return self.ftes_needed * 52 * STANDARD_WORK_WEEK

    def annual_labor_cost(self, overtime_hours_pct: float = 0.10) -> dict:
        """Calculate total annual labor cost.

        Args:
            overtime_hours_pct: Percentage of total hours that end up as OT
                               (industry reality: 10-20% is common)
        """
        total_hours = self.weekly_hours_needed * 52
        regular_hours = total_hours * (1 - overtime_hours_pct)
        ot_hours = total_hours * overtime_hours_pct

        regular_pay = regular_hours * self.hourly_wage
        ot_pay = ot_hours * self.hourly_wage * self.overtime_multiplier
        gross_wages = regular_pay + ot_pay

        fica = gross_wages * FICA_RATE
        benefits = gross_wages * self.benefits_pct
        workers_comp = gross_wages * self.workers_comp_pct

        return {
            "regular_pay": regular_pay,
            "overtime_pay": ot_pay,
            "gross_wages": gross_wages,
            "fica": fica,
            "benefits": benefits,
            "workers_comp": workers_comp,
            "total_labor_cost": gross_wages + fica + benefits + workers_comp,
            "ftes": self.ftes_needed,
            "regular_hours": regular_hours,
            "ot_hours": ot_hours,
        }


def compare_wages(care_wage: float, comparison_wages: dict[str, float]) -> dict:
    """Compare direct care wage to market alternatives.

    Args:
        care_wage: Hourly wage for direct care worker
        comparison_wages: Dict of {employer/role: hourly_wage}
    """
    return {
        name: {
            "wage": wage,
            "difference": wage - care_wage,
            "pct_higher": ((wage - care_wage) / care_wage) * 100 if care_wage > 0 else 0,
        }
        for name, wage in comparison_wages.items()
    }
