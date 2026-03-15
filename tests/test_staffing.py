"""Tests for the StaffingModel utility."""

from texas_hhcs.staffing import StaffingModel, compare_wages


class TestStaffingModel:
    def test_ftes_for_24_7_single_position(self):
        model = StaffingModel(residents=4, staff_per_shift=1, hourly_wage=10.60)
        # 168 hrs/wk / 40 hrs = 4.2 base, * 1.18 absence factor ≈ 4.96
        assert 4.5 < model.ftes_needed < 6.0

    def test_ftes_scale_with_staff_per_shift(self):
        model_1 = StaffingModel(residents=4, staff_per_shift=1, hourly_wage=10.60)
        model_2 = StaffingModel(residents=4, staff_per_shift=2, hourly_wage=10.60)
        assert model_2.ftes_needed == model_1.ftes_needed * 2

    def test_annual_labor_cost_keys(self):
        model = StaffingModel(residents=4, staff_per_shift=1, hourly_wage=13.00)
        costs = model.annual_labor_cost(overtime_hours_pct=0.15)
        expected_keys = {
            "regular_pay", "overtime_pay", "gross_wages", "fica",
            "benefits", "workers_comp", "total_labor_cost", "ftes",
            "regular_hours", "ot_hours",
        }
        assert set(costs.keys()) == expected_keys

    def test_higher_wage_means_higher_cost(self):
        low = StaffingModel(residents=4, staff_per_shift=1, hourly_wage=10.60)
        high = StaffingModel(residents=4, staff_per_shift=1, hourly_wage=18.00)
        high_cost = high.annual_labor_cost()["total_labor_cost"]
        low_cost = low.annual_labor_cost()["total_labor_cost"]
        assert high_cost > low_cost

    def test_overtime_increases_total_cost(self):
        model = StaffingModel(residents=4, staff_per_shift=1, hourly_wage=13.00)
        no_ot = model.annual_labor_cost(overtime_hours_pct=0.0)
        with_ot = model.annual_labor_cost(overtime_hours_pct=0.20)
        assert with_ot["total_labor_cost"] > no_ot["total_labor_cost"]


class TestCompareWages:
    def test_returns_correct_keys(self):
        result = compare_wages(10.60, {"Buc-ee's": 18.00})
        assert "Buc-ee's" in result
        assert set(result["Buc-ee's"].keys()) == {"wage", "difference", "pct_higher"}

    def test_difference_is_positive_for_higher_wage(self):
        result = compare_wages(10.60, {"Retail": 18.00})
        assert result["Retail"]["difference"] > 0
        assert result["Retail"]["pct_higher"] > 0
