"""
Runs every profile in test_profiles.json through the engine and writes a
human-readable results file (test_results.md) - this is the "why this is
best" output the brief asks for, not just a pass/fail.

Usage: python scripts/run_tests.py   (run from the repo root)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from eligibility import ApplicantProfile, load_lenders, load_rules, rank_lenders  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PROFILES_PATH = ROOT / "tests" / "test_profiles.json"
RESULTS_PATH = ROOT / "outputs" / "test_results.md"


def main():
    lenders = load_lenders()
    rules = load_rules()
    profiles = json.loads(PROFILES_PATH.read_text())

    lines = ["# Test results\n", f"Generated against {len(lenders)} lenders, {sum(len(v) for v in rules.values())} rules.\n"]

    for case in profiles:
        p = ApplicantProfile(**case["profile"])
        decisions = rank_lenders(p, lenders, rules)
        eligible = [d for d in decisions if d.eligible]
        ineligible = [d for d in decisions if not d.eligible]

        lines.append(f"\n## {case['id']}\n{case['description']}\n")
        lines.append(f"**Eligible at {len(eligible)}/{len(lenders)} lenders.**\n")

        if eligible:
            lines.append("| Rank | Lender | Offered Amt | Rate | Tenure | EMI | Total Cost | Flags |")
            lines.append("|---|---|---|---|---|---|---|---|")
            for i, d in enumerate(eligible, 1):
                flag_txt = "; ".join(d.flags) if d.flags else ""
                lines.append(
                    f"| {i} | {d.lender_id} | ₹{d.offered_amount:,.0f} | {d.assigned_rate_pct:.2f}% | "
                    f"{d.tenure_months}mo | ₹{d.emi:,.0f} | ₹{d.total_cost:,.0f} | {flag_txt} |"
                )

        if ineligible:
            lines.append("\n**Rejected:**\n")
            for d in ineligible:
                lines.append(f"- **{d.lender_id}**: {d.reason}")

    RESULTS_PATH.write_text("\n".join(lines))
    print(f"wrote {RESULTS_PATH} ({len(profiles)} profiles x {len(lenders)} lenders)")


if __name__ == "__main__":
    main()
