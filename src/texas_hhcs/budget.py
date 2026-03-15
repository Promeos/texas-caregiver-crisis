"""LBB/GAA budget trend parsing for HHSC appropriations."""

from dataclasses import dataclass


@dataclass
class BienniumBudget:
    """Texas biennial budget data for HHS-related spending."""

    biennium: str  # e.g., "2024-25", "2022-23"
    legislature: str  # e.g., "88th", "87th"
    total_hhsc_budget: float | None = None
    hcs_strategy_spending: float | None = None
    icf_iid_strategy_spending: float | None = None
    hcs_slots_funded: int | None = None
    hcs_waitlist_size: int | None = None
    attendant_wage_assumption: float | None = None  # $/hr baked into rate
    source: str = ""

    @property
    def cost_per_slot(self) -> float | None:
        if self.hcs_strategy_spending and self.hcs_slots_funded:
            return self.hcs_strategy_spending / self.hcs_slots_funded
        return None


def build_trend_table(budgets: list[BienniumBudget]) -> list[dict]:
    """Convert budget records into a flat table for DataFrame construction."""
    return [
        {
            "biennium": b.biennium,
            "legislature": b.legislature,
            "total_hhsc_budget": b.total_hhsc_budget,
            "hcs_spending": b.hcs_strategy_spending,
            "icf_spending": b.icf_iid_strategy_spending,
            "hcs_slots": b.hcs_slots_funded,
            "waitlist": b.hcs_waitlist_size,
            "wage_assumption": b.attendant_wage_assumption,
            "cost_per_slot": b.cost_per_slot,
            "source": b.source,
        }
        for b in budgets
    ]
