# Personal loan eligibility - rule-based model

Rule-based (not ML) eligibility engine for personal loans across 20
Indian lenders, built on `data/lenders.csv` + `data/rules.csv`.

LIVE AT : https://dwij45.github.io/LoanIQ/
vdo link https://github.com/user-attachments/assets/f3b68524-b659-4e5f-8d3c-f9e1c966c0f0
## Run it

```
python -m unittest tests.test_model -v        # 20 unit tests
python scripts/run_tests.py                    # 11 sample profiles x 20 lenders -> outputs/test_results.md
python analysis/insights.py                    # ~1,800 synthetic profiles -> outputs/insights.md
python scripts/gen_docs.py                     # regenerates docs/data-sources.md + docs/assumptions-and-estimates.md
open ui/index.html                             # self-contained demo frontend, no backend needed
```

## How it works (4 stages, see `src/eligibility.py`)

1. **GATES** - every hard-cutoff row in `rules.csv` for a lender is
   checked against the applicant; first failure rejects with a plain
   reason. Soft/preferred values are logged, never rejected on.
2. **AMOUNT** - dispatches per lender: either the FOIR-cap formula
   (`max_emi = foir_cap*income - existing_emi`, inverted through the
   standard EMI formula for principal) or, for IDFC/Kotak, the
   calculator-verified `multiplier x disposable_income` formula.
   Clamped to the lender's own `min_loan`/`max_loan`.
3. **PRICE** - CIBIL-based linear interpolation between the lender's
   own `rate_min_pct`/`rate_max_pct` (replaces the dropped
   `rate_bands.csv` with a computed function).
4. **RANK** - sorted by total cost (interest + processing fee) over the
   offered tenure, not advertised rate. Near-ties get a PSU/NBFC
   comment in `flags`, never a silent reorder.

See `docs/system-architecture.md` for the full pipeline walkthrough and
folder layout, `docs/schema-reference.md` for every table/column, and
`docs/foir-methodology.md` for how loan amounts are actually sized.
`docs/limitations.md` covers every modeling decision and why, plus the
full list of fields in the data that are estimates rather than verified
lender policy (the live version of that list is generated at
`docs/assumptions-and-estimates.md`).

## Files

```
data/            lenders.csv, rules.csv, input_variables.csv
src/             eligibility.py (the engine)
tests/           test_model.py (unit tests), test_profiles.json (sample profiles)
scripts/         run_tests.py, gen_docs.py
analysis/        insights.py (synthetic-grid analysis)
outputs/         test_results.md, insights.md (generated)
docs/            schema-reference.md, foir-methodology.md, system-architecture.md,
                 data-sources.md, assumptions-and-estimates.md (generated), limitations.md
ui/              index.html (self-contained demo, JS port of the engine)
```
