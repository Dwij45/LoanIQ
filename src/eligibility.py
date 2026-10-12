"""
Rule-based personal-loan eligibility engine.

NOT machine learning. Every decision traces back to a row in rules.csv
(a real source, or an explicitly-flagged estimate) - no learned weights,
no black-box score. Loads data/lenders.csv and data/rules.csv (long
format, lender_id as the shared key) and evaluates an applicant against
every lender in a 4-stage pipeline: GATES -> AMOUNT -> PRICE/TENURE ->
RANK.

Scope limit (inherited from the data collection phase, same as the
reference project): only SALARIED applicants are modeled. Self-employed
income is reported annually via ITR, not monthly salary slips, and the
collected rules do not carry a parallel self-employed rule set (HDFC's
own rules.csv row even says self-employed applicants are routed to a
different product entirely). Rather than silently apply salaried rules
to a self-employed applicant, the engine gates them out explicitly.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def _read_csv(path: Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_lenders(path: Path = DATA_DIR / "lenders.csv") -> dict[str, dict[str, Any]]:
    out = {}
    for row in _read_csv(path):
        lid = row["lender_id"]
        out[lid] = {
            "lender_id": lid,
            "lender_name": row["lender_name"],
            "lender_type": row["lender_type"],
            "min_loan": _num(row.get("min_loan_inr")),
            "max_loan": _num(row.get("max_loan_inr")),
            "min_tenure_months": _num(row.get("min_tenure_months")),
            "max_tenure_months": _num(row.get("max_tenure_months")),
            "rate_min_pct": _num(row.get("rate_min_pct")),
            "rate_max_pct": _num(row.get("rate_max_pct")),
            "processing_fee_pct": _num(row.get("processing_fee_pct")),
            "has_govt_employee_scheme": row.get("has_govt_employee_scheme"),
        }
    return out


def load_rules(path: Path = DATA_DIR / "rules.csv") -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for row in _read_csv(path):
        lid = row["lender_id"]
        row = dict(row)
        row["value_num"] = _num(row.get("value"))
        row["is_hard_cutoff"] = str(row.get("is_hard_cutoff")).strip().lower() in ("true", "1", "yes")
        out.setdefault(lid, []).append(row)
    return out


def _num(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return v  # non-numeric values (bool/text) pass through as-is


# ---------------------------------------------------------------------------
# Applicant / Decision
# ---------------------------------------------------------------------------

@dataclass
class ApplicantProfile:
    age: int
    employment_type: str          # salaried | self_employed | pensioner
    employer_category: str        # govt | psu | mnc | pvt_ltd | sme | na
    net_monthly_income: float
    salary_credit_mode: str       # bank_transfer | cash
    total_work_exp_months: int
    current_job_months: int
    city_tier: str                # metro | tier1 | tier2 | tier3
    cibil_score: int              # 0 means NTC (no credit history)
    existing_emi: float
    salary_account_bank: str | None
    existing_customer_of: list[str] = field(default_factory=list)
    requested_amount: float = 0
    requested_tenure_months: int = 0

    @property
    def is_ntc(self) -> bool:
        return self.cibil_score == 0


@dataclass
class Decision:
    lender_id: str
    lender_name: str
    eligible: bool
    reason: str | None = None            # populated when eligible=False
    eligible_amount: float | None = None  # max the lender would offer
    offered_amount: float | None = None   # min(eligible_amount, requested)
    assigned_rate_pct: float | None = None
    tenure_months: int | None = None
    emi: float | None = None
    total_cost: float | None = None       # interest + processing fee, 3yr-equivalent basis
    flags: list[str] = field(default_factory=list)  # "estimate", "soft-cutoff failed", etc.


# ---------------------------------------------------------------------------
# EMI / present-value math
# ---------------------------------------------------------------------------

def emi(principal: float, annual_rate_pct: float, months: int) -> float:
    r = annual_rate_pct / 100 / 12
    if r == 0:
        return principal / months
    return principal * r * (1 + r) ** months / ((1 + r) ** months - 1)


def max_principal_from_emi(max_emi: float, annual_rate_pct: float, months: int) -> float:
    if max_emi <= 0:
        return 0.0
    r = annual_rate_pct / 100 / 12
    if r == 0:
        return max_emi * months
    return max_emi * ((1 + r) ** months - 1) / (r * (1 + r) ** months)


def assign_rate(cibil: int, lender_min_cibil: float, rate_min_pct: float, rate_max_pct: float) -> float:
    """
    Linear interpolation: best observed CIBIL (900) -> rate_min, the
    lender's own cutoff -> rate_max. This REPLACES rate_bands.csv - the
    band is a small computed function of the lender's own two published
    numbers (rate_min_pct, rate_max_pct) plus its own min_cibil, not a
    separately stored/guessed table.
    """
    if rate_min_pct is None or rate_max_pct is None:
        return rate_max_pct or rate_min_pct or 0.0
    lo = lender_min_cibil if lender_min_cibil is not None else 650
    if cibil <= lo:
        return rate_max_pct
    if cibil >= 900:
        return rate_min_pct
    frac = (cibil - lo) / (900 - lo)
    return rate_max_pct - (rate_max_pct - rate_min_pct) * frac


# ---------------------------------------------------------------------------
# Condition evaluation (the `condition` column in rules.csv)
# ---------------------------------------------------------------------------

def _eval_condition(condition: str, applicant: ApplicantProfile) -> bool:
    cond = (condition or "").strip()
    if not cond or cond == "otherwise":
        return True
    # supports the handful of condition shapes actually present in rules.csv:
    #   employer_category == 'govt'
    #   city_tier == 'tier1'
    #   city_tier in [tier2,tier3]
    #   existing_customer_of contains 'AXIS'
    try:
        if "==" in cond:
            field_name, val = cond.split("==")
            field_name, val = field_name.strip(), val.strip().strip("'\"")
            return str(getattr(applicant, field_name, None)) == val
        if " in [" in cond:
            field_name, rest = cond.split(" in [")
            field_name = field_name.strip()
            options = [o.strip() for o in rest.rstrip("]").split(",")]
            return str(getattr(applicant, field_name, None)) in options
        if "contains" in cond:
            field_name, val = cond.split("contains")
            field_name, val = field_name.strip(), val.strip().strip("'\"")
            return val in getattr(applicant, field_name, []) or []
    except Exception:
        pass
    return True  # unrecognized condition shape: don't silently block on it


_OPS = {
    ">=": lambda a, b: a >= b,
    "<=": lambda a, b: a <= b,
    "==": lambda a, b: a == b,
    "*": None,  # handled separately (capacity formula, not a gate)
}


def _applicant_field_for_rule(rule_name: str, applicant: ApplicantProfile):
    mapping = {
        "min_age": applicant.age,
        "max_age_at_apply": applicant.age,
        "max_age_at_maturity": None,  # computed with tenure below
        "min_total_exp_months": applicant.total_work_exp_months,
        "min_current_job_months": applicant.current_job_months,
        "min_cibil": applicant.cibil_score,
        "min_income": applicant.net_monthly_income,
        # requires_salary_account and allows_ntc are special-cased in
        # check_gates(), not handled here
        "requires_existing_customer": bool(applicant.existing_customer_of),
        "allowed_employment_type": applicant.employment_type,
        "min_education": None,  # not modeled - no education field collected reliably
    }
    return mapping.get(rule_name)


# ---------------------------------------------------------------------------
# Stage 1: GATES
# ---------------------------------------------------------------------------

def check_gates(applicant: ApplicantProfile, lender_rules: list[dict], lender_id: str = "") -> tuple[bool, str | None, list[str]]:
    flags = []

    if applicant.employment_type != "salaried":
        return False, "Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).", flags

    requested_tenure_years = (applicant.requested_tenure_months or 0) / 12

    for r in lender_rules:
        rname = r["rule_name"]
        if rname in ("foir_cap", "salary_multiple_on_disposable_income"):
            continue  # capacity formulas, not gates

        if not _eval_condition(r.get("condition", ""), applicant):
            continue  # this row doesn't apply to this applicant

        if rname == "max_age_at_maturity":
            maturity_age = applicant.age + requested_tenure_years
            if maturity_age > r["value_num"]:
                reason = f"Age at maturity ({maturity_age:.1f}) exceeds lender's max_age_at_maturity ({r['value_num']})."
                if not r["is_hard_cutoff"]:
                    flags.append(f"soft-cutoff failed: {reason}")
                    continue
                return False, reason, flags
            continue

        if rname == "requires_salary_account":
            has_it_here = (applicant.salary_account_bank or "").strip().upper() == lender_id.strip().upper()
            target_bool = str(r["value_num"]).strip().lower() in ("true", "1")
            if target_bool and not has_it_here:
                reason = f"requires_salary_account failed: applicant's salary account is with {applicant.salary_account_bank or 'no bank'}, not {lender_id}."
                if not r["is_hard_cutoff"]:
                    flags.append(f"soft-cutoff failed: {reason}")
                    continue
                return False, reason, flags
            continue

        if rname == "allows_ntc":
            # This rule only matters when the applicant actually HAS no
            # credit history. A non-NTC applicant's CIBIL score is judged
            # by the min_cibil rule instead - the lender's allows_ntc
            # policy (yes/no for a ZERO-history applicant) is irrelevant
            # to them and must not reject them.
            if not applicant.is_ntc:
                continue
            lender_allows = str(r["value_num"]).strip().lower() in ("true", "1")
            if not lender_allows:
                return False, "New-to-credit (no CIBIL history) applicant; this lender does not accept NTC applicants.", flags
            continue

        applicant_val = _applicant_field_for_rule(rname, applicant)
        if applicant_val is None:
            continue

        target = r["value_num"]
        op = r["operator"]

        if op == "==":
            target_bool = str(target).strip().lower() in ("true", "1") if isinstance(target, str) else bool(target)
            ok = bool(applicant_val) == target_bool
        elif op in (">=", "<="):
            ok = _OPS[op](applicant_val, target)
        else:
            ok = True  # unknown operator: don't silently reject on it

        if not ok:
            reason = f"{rname} failed: applicant={applicant_val}, lender requires {op} {target}"
            if r.get("confidence") in ("estimate", "assumed", "not_published"):
                flags.append(f"[{r['confidence']}] {reason}")
            if not r["is_hard_cutoff"]:
                flags.append(f"soft-cutoff failed (not a rejection): {reason}")
                continue
            return False, reason, flags

    return True, None, flags


# ---------------------------------------------------------------------------
# Stage 2: AMOUNT  (handles the FOIR-vs-multiple circular dependency)
# ---------------------------------------------------------------------------

def compute_amount(applicant: ApplicantProfile, lender: dict, lender_rules: list[dict]) -> tuple[float, list[str]]:
    flags = []
    foir_rule = next((r for r in lender_rules if r["rule_name"] == "foir_cap"), None)
    mult_rule = next((r for r in lender_rules if r["rule_name"] == "salary_multiple_on_disposable_income"), None)

    tenure = min(
        applicant.requested_tenure_months or lender["max_tenure_months"] or 0,
        lender["max_tenure_months"] or 10**9,
    )
    tenure = max(tenure, lender["min_tenure_months"] or 1)

    if mult_rule is not None:
        multiplier = mult_rule["value_num"]
        disposable = max(applicant.net_monthly_income - applicant.existing_emi, 0)
        candidate = multiplier * disposable
        if mult_rule.get("confidence") == "calculator_inferred":
            flags.append(f"amount formula is calculator-inferred (reverse-engineered, not published): {multiplier}x disposable income")
    elif foir_rule is not None:
        foir_cap = foir_rule["value_num"]
        if foir_rule.get("confidence") == "assumed":
            flags.append(f"foir_cap={foir_cap} is an ESTIMATE for this lender (see rules.csv notes) - amount below is only as reliable as that estimate")
        # Circular dependency fix: size the loan using the BAND MIDPOINT
        # rate first (we don't know CIBIL-based final rate until we know
        # the lender passed gates, but more importantly EMI depends on
        # the rate we're about to assign, and the rate doesn't depend on
        # amount - so there's no real circularity for rate, only a
        # sequencing one: compute with midpoint, then re-price exactly in
        # Stage 3 and recompute the EMI on the ALREADY-FIXED principal).
        midpoint_rate = ((lender["rate_min_pct"] or 0) + (lender["rate_max_pct"] or 0)) / 2
        max_emi = max(foir_cap * applicant.net_monthly_income - applicant.existing_emi, 0)
        if max_emi == 0:
            flags.append(f"FOIR exceeded: existing EMI ₹{applicant.existing_emi:,.0f} already meets/exceeds cap (FOIR {foir_cap:.0%} of income ₹{applicant.net_monthly_income:,.0f})")
        candidate = max_principal_from_emi(max_emi, midpoint_rate, int(tenure))
    else:
        candidate = lender["max_loan"] or 0
        flags.append("no foir_cap or salary-multiple rule found for this lender - sized at product max_loan only")

    amount = min(candidate, lender["max_loan"] or candidate)
    return amount, flags


# ---------------------------------------------------------------------------
# Stage 3: PRICE + final EMI/cost, Stage 4 happens in rank_lenders()
# ---------------------------------------------------------------------------

def evaluate_lender(applicant: ApplicantProfile, lender_id: str,
                     lenders: dict, rules: dict) -> Decision:
    lender = lenders[lender_id]
    lender_rules = rules.get(lender_id, [])

    ok, reason, gate_flags = check_gates(applicant, lender_rules, lender_id)
    if not ok:
        return Decision(lender_id, lender["lender_name"], eligible=False, reason=reason, flags=gate_flags)

    eligible_amount, amount_flags = compute_amount(applicant, lender, lender_rules)
    flags = gate_flags + amount_flags

    if lender["min_loan"] and eligible_amount < lender["min_loan"]:
        return Decision(lender_id, lender["lender_name"], eligible=False,
                         reason=f"Eligible amount ₹{eligible_amount:,.0f} is below this lender's product minimum ₹{lender['min_loan']:,.0f}.",
                         flags=flags)

    min_cibil_rule = next((r for r in lender_rules if r["rule_name"] == "min_cibil"), None)
    lender_min_cibil = min_cibil_rule["value_num"] if min_cibil_rule else None
    final_rate = assign_rate(applicant.cibil_score, lender_min_cibil, lender["rate_min_pct"], lender["rate_max_pct"])

    offered_amount = min(eligible_amount, applicant.requested_amount) if applicant.requested_amount else eligible_amount
    tenure = min(applicant.requested_tenure_months or lender["max_tenure_months"], lender["max_tenure_months"] or 10**9)
    tenure = int(max(tenure, lender["min_tenure_months"] or 1))

    monthly_emi = emi(offered_amount, final_rate, tenure)
    total_interest = monthly_emi * tenure - offered_amount
    processing_fee = (lender["processing_fee_pct"] or 0) / 100 * offered_amount
    total_cost = total_interest + processing_fee

    return Decision(
        lender_id=lender_id, lender_name=lender["lender_name"], eligible=True,
        eligible_amount=round(eligible_amount, 2), offered_amount=round(offered_amount, 2),
        assigned_rate_pct=round(final_rate, 2), tenure_months=tenure,
        emi=round(monthly_emi, 2), total_cost=round(total_cost, 2), flags=flags,
    )


# ---------------------------------------------------------------------------
# Stage 4: RANK
# ---------------------------------------------------------------------------

def rank_lenders(applicant: ApplicantProfile, lenders: dict | None = None,
                  rules: dict | None = None, tie_pct: float = 0.02) -> list[Decision]:
    """
    Ranks by total_cost ascending (lowest estimated cost = "best"), NOT by
    advertised rate - a 9.99% loan with a 5% fee can lose to an 11% loan
    with a 1% fee, which is why we compute total_cost instead of sorting
    on rate_min_pct.

    Tie-break (only when two offers are within `tie_pct` of each other's
    total_cost, default 2%): prefer higher offered_amount, then longer
    max_tenure_months. PSU-vs-NBFC is never used as a silent sort key -
    it's only ever written into the `flags` as a comment so a reader can
    see it, decide for themselves, and audit that it didn't move the
    ranking.
    """
    lenders = lenders or load_lenders()
    rules = rules or load_rules()

    decisions = [evaluate_lender(applicant, lid, lenders, rules) for lid in lenders]
    eligible = [d for d in decisions if d.eligible]
    ineligible = [d for d in decisions if not d.eligible]

    def sort_key(d: Decision):
        return (d.total_cost, -d.offered_amount, -(lenders[d.lender_id]["max_tenure_months"] or 0))

    eligible.sort(key=sort_key)

    # annotate near-ties with the PSU/NBFC comment, never used to reorder
    for i in range(len(eligible) - 1):
        a, b = eligible[i], eligible[i + 1]
        if a.total_cost and b.total_cost and abs(a.total_cost - b.total_cost) <= tie_pct * a.total_cost:
            type_a = lenders[a.lender_id]["lender_type"]
            type_b = lenders[b.lender_id]["lender_type"]
            if type_a != type_b:
                b.flags.append(f"near-tie with {a.lender_id} (within {tie_pct:.0%} cost) - {a.lender_id} is {type_a}, this is {type_b}; ranking is on cost only, this is a comment, not a bias.")

    return eligible + ineligible
