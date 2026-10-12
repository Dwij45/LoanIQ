# FOIR methodology

FOIR (Fixed Obligation to Income Ratio) is how most of the 20 lenders in
this dataset size a loan: it caps the *new* EMI at some fraction of the
applicant's income, after accounting for debts they're already paying.
This document covers both ways FOIR-equivalent numbers got into
`data/rules.csv` — the manual ratio method most lenders publish, and the
calculator-reverse-engineering method used for the two lenders (IDFC,
Kotak) whose public calculators turned out to use a different formula
entirely.

## 1. The manual FOIR-ratio method (used by most lenders)

### Definition

```
FOIR = (existing monthly EMI + proposed new monthly EMI) / net monthly income
```

A lender publishes a `foir_cap` (e.g. 0.50, meaning at most 50% of gross
monthly obligations-to-income). Given that cap, income, and existing
EMI, the engine first finds the **maximum new EMI** the applicant can
still take on:

```
max_new_emi = max(foir_cap * net_monthly_income - existing_emi, 0)
```

If `existing_emi` alone already consumes the full FOIR cap, `max_new_emi`
is zero — this is flagged explicitly (`"FOIR exceeded: existing EMI ₹X
already meets/exceeds cap"`), not silently treated as "insufficient data."

### From max EMI to max loan amount: the circular-dependency problem

To turn `max_new_emi` into a loan **amount**, you need an interest rate
(the standard present-value-of-annuity inverse, see below). But the rate
this applicant would actually be charged depends on their CIBIL score and
the lender's own `min_cibil`/`rate_min_pct`/`rate_max_pct` — it does not
depend on the loan amount itself, so there's no true circularity in the
*rate*. There is a **sequencing** issue though: at the amount-sizing step,
nothing downstream (the final rate assignment) has run yet.

**Resolution:** size the loan using the lender's own **band midpoint rate**
— `(rate_min_pct + rate_max_pct) / 2` — as a reasonable first-pass rate,
then assign the applicant's *real* CIBIL-based rate afterward (Stage 3 of
the pipeline, see `system-architecture.md`) and recompute the final EMI
and total cost on the already-fixed principal. This is a transparent,
documented compromise — not a hidden assumption — and it only affects the
sizing step; the rate and EMI the applicant is actually shown are always
the real, CIBIL-specific ones.

### The EMI formula (standard present-value-of-annuity)

```
EMI = P · r · (1+r)^n / ((1+r)^n − 1)
```
where `P` = principal, `r` = monthly interest rate (`annual_rate_pct / 100
/ 12`), `n` = tenure in months.

Sizing the loan requires the **inverse**: given a maximum affordable EMI,
how large a principal does that support?

```
P_max = max_EMI · ((1+r)^n − 1) / (r · (1+r)^n)
```

Both directions are implemented in `src/eligibility.py` (`emi()` and
`max_principal_from_emi()`) and ported line-for-line into the JS engine
embedded in `ui/index.html`. When `r == 0` (not observed in this dataset
but handled defensively), both reduce to simple division:
`EMI = P/n` and `P_max = max_EMI · n`.

## 2. Calculator-inferred formulas (IDFC, Kotak)

Two lenders — **IDFC FIRST Bank** and **Kotak Mahindra Bank** — publish a
live eligibility calculator on their own website, but neither one's
eligibility page states a `foir_cap` number anywhere in text. Rather than
leave these as `not_published` or guess a FOIR cap, their calculators
were tested directly: run the calculator at several different input
combinations, record its outputs, and solve for the simplest formula
that reproduces every output exactly.

### Method

1. Hold net monthly income fixed, vary `existing_emi` across several test
   values (increments of a representative size), and record the
   calculator's reported eligible loan amount at each point.
2. Fit candidate formulas (FOIR-style cap, flat multiplier on income,
   flat multiplier on disposable income) against the recorded outputs.
3. Keep the formula only if it reproduces **every** test point exactly —
   not approximately — within the calculator's own rounding. A formula
   that matches 3 of 4 points is treated as wrong, not "mostly right."
4. Record the exact test points and the matching formula in the `notes`
   column of the corresponding `rules.csv` row, tagged
   `confidence=calculator_inferred` (never `official`, since the lender
   never states this as policy — it was derived by testing their own
   tool against itself).

### Results

| Lender | Formula | Test points | Result |
|---|---|---|---|
| **IDFC FIRST Bank** | `eligible_loan = 10 × (net_monthly_income − existing_emi)`, capped at the product's own `max_loan_inr` (₹15,00,000) | 4 | Exact match at all 4 points |
| **Kotak Mahindra Bank** | `eligible_loan = 20 × (net_monthly_income − existing_emi)` | 3 | Exact match at all 3 points — but the calculator's own *default* tenure (120 months) exceeds this dataset's stored `max_tenure_months=72` for Kotak, which is flagged in the row's `notes` for manual review rather than silently reconciled |

Both are stored in `rules.csv` as `rule_name=salary_multiple_on_disposable_income`,
`operator=*`, with `value` = the multiplier (10 or 20) and `unit=x
(income-obligations)`.

### Why this overrides FOIR for these two lenders

In the amount-computation stage (`compute_amount()`), the engine checks
for a `salary_multiple_on_disposable_income` row **before** falling back
to `foir_cap`:

```python
if mult_rule is not None:
    candidate = multiplier * max(income - existing_emi, 0)
elif foir_rule is not None:
    # the FOIR-cap path described in section 1
    ...
```

This means IDFC and Kotak's loan sizing never touches the FOIR-cap
formula at all — the calculator-derived multiplier formula is a complete
substitute, not an adjustment on top of a FOIR number. Neither lender has
a `foir_cap` row in `rules.csv` for this reason.

## 3. How an estimate, not a calculator result, ends up as `foir_cap`

A separate situation from either of the above: 9 lenders in this dataset
have **no** published `foir_cap` and **no** working public calculator —
their eligibility pages state age/income/CIBIL cutoffs but are silent on
how the loan amount itself is sized. For these, `foir_cap` is filled with
an explicit, flagged estimate (`confidence=assumed`) rather than left
blank, so the engine can still size a loan — but every such row's `notes`
states exactly what the estimate is based on (almost always: the median
`foir_cap` of comparable, *already-verified* lenders of the same
`lender_type` in this same dataset). The full list, with each one's exact
basis, is in `docs/assumptions-and-estimates.md` — this file explains the
*mechanism* those estimates are produced by; that file is the live,
generated record of *which* rows currently carry one.
