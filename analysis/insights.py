"""
Quantitative insights from running a synthetic grid of applicants through
every lender: which gate rejects the most people, how PSU/private/NBFC/
fintech sectors compare, and how rate spreads with CIBIL. Same idea as
the reference project's analysis/insights.py, rebuilt against our own
engine and data (no data copied from theirs).

Usage: python analysis/insights.py   (run from the repo root)
Writes: outputs/insights.md
"""
import itertools
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from eligibility import ApplicantProfile, load_lenders, load_rules, rank_lenders  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "outputs" / "insights.md"

# Synthetic grid - every combination of these ranges = one applicant.
# Kept to ~750 combinations (not 27,000) since this is one lender-set,
# not a sweep of an entire market; enough to be statistically useful
# without taking minutes to run.
AGES = [24, 32, 45, 58]
INCOMES = [15000, 35000, 60000, 100000, 200000]
CIBILS = [0, 650, 700, 750, 820]
EXISTING_EMI_RATIOS = [0.0, 0.3, 0.6]  # fraction of income already committed
EMPLOYER_CATS = ["govt", "pvt_ltd"]
TENURES = [24, 48, 60]


def build_grid():
    profiles = []
    for age, income, cibil, emi_ratio, emp_cat, tenure in itertools.product(
        AGES, INCOMES, CIBILS, EXISTING_EMI_RATIOS, EMPLOYER_CATS, TENURES
    ):
        profiles.append(ApplicantProfile(
            age=age, employment_type="salaried", employer_category=emp_cat,
            net_monthly_income=income, salary_credit_mode="bank_transfer",
            total_work_exp_months=60, current_job_months=24, city_tier="tier1",
            cibil_score=cibil, existing_emi=round(income * emi_ratio),
            salary_account_bank=None, existing_customer_of=[],
            requested_amount=min(500000, income * 10), requested_tenure_months=tenure,
        ))
    return profiles


REASON_CATEGORIES = [
    ("Credit Score / Bureau Cutoff", ["min_cibil", "new-to-credit", "credit history"]),
    ("FOIR / Capacity", ["FOIR", "below this lender's product minimum"]),
    ("Salary Account", ["salary account"]),
    ("Employment Vintage", ["min_total_exp_months", "min_current_job_months"]),
    ("Age Bounds", ["max_age_at_apply", "maturity"]),
    ("Income Floor", ["min_income"]),
    ("Out of Scope (self-employed)", ["out of scope"]),
]


def categorize(reason: str) -> str:
    for label, keywords in REASON_CATEGORIES:
        if any(k.lower() in reason.lower() for k in keywords):
            return label
    return "Other / Unclassified"


def run_insights():
    lenders = load_lenders()
    rules = load_rules()
    profiles = build_grid()

    rejection_counter = Counter()
    total_evals = 0
    sector_stats = defaultdict(lambda: {"evals": 0, "approvals": 0, "rates": [], "amounts": [], "best_match": 0})
    rate_by_cibil = defaultdict(list)

    for p in profiles:
        decisions = rank_lenders(p, lenders, rules)
        best_id = decisions[0].lender_id if decisions and decisions[0].eligible else None
        for d in decisions:
            total_evals += 1
            sector = lenders[d.lender_id]["lender_type"]
            s = sector_stats[sector]
            s["evals"] += 1
            if d.eligible:
                s["approvals"] += 1
                s["rates"].append(d.assigned_rate_pct)
                s["amounts"].append(d.offered_amount)
                rate_by_cibil[p.cibil_score].append(d.assigned_rate_pct)
                if d.lender_id == best_id:
                    s["best_match"] += 1
            else:
                rejection_counter[categorize(d.reason or "")] += 1

    lines = ["# Insights\n", f"Synthetic grid: {len(profiles)} profiles x {len(lenders)} lenders = {total_evals} evaluations.\n"]

    lines.append("\n## 1. Hard-gate rejection Pareto\n")
    lines.append("What's actually blocking applicants, ranked by frequency:\n")
    total_rejections = sum(rejection_counter.values())
    lines.append("| Rejection category | Count | Share |")
    lines.append("|---|---|---|")
    for label, count in rejection_counter.most_common():
        lines.append(f"| {label} | {count} | {count/total_rejections:.1%} |")

    lines.append("\n## 2. Sector comparison\n")
    lines.append("| Sector | Evaluations | Approval rate | Mean rate | Mean amount | Times best-match |")
    lines.append("|---|---|---|---|---|---|")
    for sector, s in sorted(sector_stats.items(), key=lambda kv: -kv[1]["approvals"]):
        approval_rate = s["approvals"] / s["evals"] if s["evals"] else 0
        mean_rate = mean(s["rates"]) if s["rates"] else float("nan")
        mean_amt = mean(s["amounts"]) if s["amounts"] else float("nan")
        lines.append(f"| {sector} | {s['evals']} | {approval_rate:.1%} | {mean_rate:.2f}% | ₹{mean_amt:,.0f} | {s['best_match']} |")

    lines.append("\n## 3. CIBIL vs assigned-rate spread\n")
    lines.append("| CIBIL | # eligible decisions | Lowest rate | Median rate | Highest rate |")
    lines.append("|---|---|---|---|---|")
    for cibil in sorted(rate_by_cibil):
        rates = rate_by_cibil[cibil]
        lines.append(f"| {cibil} | {len(rates)} | {min(rates):.2f}% | {median(rates):.2f}% | {max(rates):.2f}% |")

    OUT_PATH.write_text("\n".join(lines))
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    run_insights()
