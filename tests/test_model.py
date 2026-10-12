"""
Unit tests for the eligibility engine. Run: python -m pytest tests/test_model.py -v
(or, with no pytest installed: python tests/test_model.py)
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from eligibility import (  # noqa: E402
    ApplicantProfile, Decision, emi, max_principal_from_emi, assign_rate,
    load_lenders, load_rules, evaluate_lender, rank_lenders,
)

LENDERS = load_lenders()
RULES = load_rules()


def make_profile(**overrides):
    base = dict(
        age=30, employment_type="salaried", employer_category="pvt_ltd",
        net_monthly_income=80000, salary_credit_mode="bank_transfer",
        total_work_exp_months=60, current_job_months=24, city_tier="metro",
        cibil_score=780, existing_emi=0, salary_account_bank=None,
        existing_customer_of=[], requested_amount=500000, requested_tenure_months=36,
    )
    base.update(overrides)
    return ApplicantProfile(**base)


class TestEMIMath(unittest.TestCase):
    def test_emi_known_value(self):
        # P=100000, 12% p.a., 12 months -> standard reducing-balance EMI ~ 8884.88
        self.assertAlmostEqual(emi(100000, 12, 12), 8884.88, delta=1.0)

    def test_emi_zero_rate(self):
        self.assertAlmostEqual(emi(120000, 0, 12), 10000, delta=0.01)

    def test_max_principal_is_inverse_of_emi(self):
        p = 250000
        rate, months = 14.5, 36
        the_emi = emi(p, rate, months)
        back = max_principal_from_emi(the_emi, rate, months)
        self.assertAlmostEqual(p, back, delta=1.0)

    def test_max_principal_zero_emi_is_zero(self):
        self.assertEqual(max_principal_from_emi(0, 12, 36), 0.0)


class TestRateAssignment(unittest.TestCase):
    def test_best_cibil_gets_rate_min(self):
        r = assign_rate(900, 700, rate_min_pct=10, rate_max_pct=20)
        self.assertAlmostEqual(r, 10, delta=0.01)

    def test_cutoff_cibil_gets_rate_max(self):
        r = assign_rate(700, 700, rate_min_pct=10, rate_max_pct=20)
        self.assertAlmostEqual(r, 20, delta=0.01)

    def test_mid_cibil_is_between(self):
        r = assign_rate(800, 700, rate_min_pct=10, rate_max_pct=20)
        self.assertTrue(10 < r < 20)

    def test_below_cutoff_clamped_to_max(self):
        r = assign_rate(650, 700, rate_min_pct=10, rate_max_pct=20)
        self.assertEqual(r, 20)


class TestGatesAndScope(unittest.TestCase):
    def test_self_employed_rejected_everywhere(self):
        p = make_profile(employment_type="self_employed")
        decisions = rank_lenders(p, LENDERS, RULES)
        self.assertTrue(all(not d.eligible for d in decisions))
        self.assertTrue(all("out of scope" in (d.reason or "") for d in decisions))

    def test_ntc_applicant_fails_min_cibil_lenders(self):
        p = make_profile(cibil_score=0, total_work_exp_months=120, current_job_months=60)
        decisions = {d.lender_id: d for d in rank_lenders(p, LENDERS, RULES)}
        # HSBC has a min_cibil=700 hard gate and no allows_ntc override -> must reject
        self.assertFalse(decisions["HSBC"].eligible)

    def test_non_ntc_applicant_not_blocked_by_allows_ntc_rule(self):
        # regression test for the bug where a NON-ntc applicant was
        # incorrectly rejected by lenders whose allows_ntc=False
        p = make_profile(cibil_score=820, total_work_exp_months=120, current_job_months=60)
        decisions = {d.lender_id: d for d in rank_lenders(p, LENDERS, RULES)}
        for lid, d in decisions.items():
            if not d.eligible:
                self.assertNotIn("allows_ntc", d.reason or "")

    def test_salary_account_gate_checks_specific_lender(self):
        # applicant's salary account is with HDFC, not SBI -> SBI (which
        # requires its own salary account) must reject on that basis
        p = make_profile(salary_account_bank="HDFC", total_work_exp_months=120, current_job_months=60)
        d = evaluate_lender(p, "SBI", LENDERS, RULES)
        self.assertFalse(d.eligible)
        self.assertIn("SBI", d.reason)

    def test_salary_account_gate_passes_when_matching(self):
        p = make_profile(salary_account_bank="SBI", total_work_exp_months=120, current_job_months=60,
                          net_monthly_income=60000)
        d = evaluate_lender(p, "SBI", LENDERS, RULES)
        self.assertTrue(d.eligible, d.reason)

    def test_age_at_maturity_uses_requested_tenure(self):
        # 56 + 5 years tenure = 61 at maturity, should breach a 60-year cap
        p = make_profile(age=56, requested_tenure_months=60, total_work_exp_months=200, current_job_months=36)
        d = evaluate_lender(p, "AXIS", LENDERS, RULES)  # AXIS max_age_at_maturity = 60
        self.assertFalse(d.eligible)
        self.assertIn("maturity", d.reason)


class TestAmountCapacity(unittest.TestCase):
    def test_foir_exceeded_gives_zero_capacity(self):
        p = make_profile(net_monthly_income=30000, existing_emi=25000, salary_account_bank=None)
        d = evaluate_lender(p, "HDFC", LENDERS, RULES)  # HDFC foir_cap=0.50 -> max_emi = 15000-25000 < 0
        self.assertFalse(d.eligible)

    def test_multiplier_formula_lenders_use_disposable_income(self):
        p = make_profile(net_monthly_income=100000, existing_emi=10000)
        d = evaluate_lender(p, "IDFC", LENDERS, RULES)
        self.assertTrue(d.eligible)
        self.assertAlmostEqual(d.eligible_amount, min(10 * 90000, LENDERS["IDFC"]["max_loan"]), delta=1)

    def test_offered_amount_never_exceeds_requested(self):
        p = make_profile(net_monthly_income=200000, existing_emi=0, requested_amount=50000)
        d = evaluate_lender(p, "ICICI", LENDERS, RULES)
        self.assertTrue(d.eligible)
        self.assertLessEqual(d.offered_amount, 50000)

    def test_below_min_loan_is_ineligible(self):
        p = make_profile(net_monthly_income=200000, existing_emi=199000)  # tiny disposable income
        d = evaluate_lender(p, "HDFC", LENDERS, RULES)
        self.assertFalse(d.eligible)


class TestRanking(unittest.TestCase):
    def test_ranked_by_total_cost_not_rate(self):
        p = make_profile()
        decisions = rank_lenders(p, LENDERS, RULES)
        eligible = [d for d in decisions if d.eligible]
        self.assertTrue(len(eligible) > 1)
        costs = [d.total_cost for d in eligible]
        self.assertEqual(costs, sorted(costs))

    def test_ineligible_always_sorted_after_eligible(self):
        p = make_profile()
        decisions = rank_lenders(p, LENDERS, RULES)
        seen_ineligible = False
        for d in decisions:
            if not d.eligible:
                seen_ineligible = True
            elif seen_ineligible:
                self.fail("an eligible decision appeared after an ineligible one")


if __name__ == "__main__":
    unittest.main()
