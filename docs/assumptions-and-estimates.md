# Assumptions and estimates

Generated from `data/rules.csv` and `data/lenders.csv` by `scripts/gen_docs.py` - do not hand-edit this file, edit the CSVs and re-run that script instead.

Every field below was **not** found in any public, official, or aggregator source after a real search. Each is filled with an explicit estimate and a stated basis (confidence=`assumed`), or left blank with a stated reason it couldn't be found (confidence=`not_published`). Neither case is silent - the basis for every number below is in its note.

## Estimated values (confidence = assumed)

| Lender | Field | Value | Basis |
|---|---|---|---|
| HDFC | max_age_at_maturity | 60 years | max_age_at_maturity=60 is an ESTIMATE: no HDFC source states a maturity-age distinct from the apply-age cap of 60. Assumed equal to max_age_at_apply by analogy with other lenders in this dataset that publish only one age band (ICICI 58/58, LTFIN 58/58, Fibe 55/55). |
| INDUSIND | max_age_at_apply | 60 years | max_age_at_apply=60 is an ESTIMATE: IndusInd's own eligibility page was unreadable (JS-rendered) and its blog gives '60' only as a generic industry example, not stated as IndusInd's own cutoff. Assumed equal to this dataset's existing max_age_at_maturity=60 for IndusInd. |
| INDUSIND | foir_cap | 0.5 ratio | foir_cap=0.50 is an ESTIMATE, not IndusInd's own published or calculator-derived figure. Assumed = median foir_cap of comparable private_bank lenders already verified in this dataset (HDFC 0.50, ICICI 0.45, AXIS 0.70 -> median 0.50). |
| HSBC | foir_cap | 0.5 ratio | foir_cap=0.50 is an ESTIMATE. HSBC publishes no FOIR figure and has no public eligibility calculator. Assumed = median foir_cap of comparable private_bank lenders (HDFC 0.50, ICICI 0.45, AXIS 0.70 -> median 0.50). |
| FEDERAL | foir_cap | 0.5 ratio | foir_cap=0.50 is an ESTIMATE. Federal Bank publishes no FOIR figure. Assumed = median foir_cap of comparable private_bank lenders (HDFC 0.50, ICICI 0.45, AXIS 0.70 -> median 0.50). |
| UNION | foir_cap | 0.6 ratio | foir_cap=0.60 is an ESTIMATE. Union Bank's own eligibility content was unreachable. Assumed = median foir_cap of comparable psu_bank lenders (SBI 0.65, BOB 0.40, PNB 0.60 -> median 0.60). |
| YESBANK | foir_cap | 0.5 ratio | foir_cap=0.50 is an ESTIMATE. No Yes Bank FOIR figure or working calculator was found. Assumed = median foir_cap of comparable private_bank lenders (HDFC 0.50, ICICI 0.45, AXIS 0.70 -> median 0.50). |
| HDBFS | foir_cap | 0.65 ratio | foir_cap=0.65 is an ESTIMATE. HDB Financial Services publishes no FOIR figure. Assumed = median foir_cap of comparable nbfc lenders (BAJAJ 0.75, TATACAP 0.55, POONAWALLA 0.65 -> median 0.65). |
| LTFIN | foir_cap | 0.65 ratio | foir_cap=0.65 is an ESTIMATE, distinct from the documented attempt to reverse-engineer L&T Finance's own calculator (which produced unreliable/buggy output). Assumed = median foir_cap of comparable nbfc lenders (BAJAJ 0.75, TATACAP 0.55, POONAWALLA 0.65 -> median 0.65). |
| Fibe | foir_cap | 0.5 ratio | foir_cap=0.50 is an ESTIMATE and is NOT Fibe-specific - no fintech lender in this dataset has a verified foir_cap to take a median from. Basis is Fibe's own blog, which states most Indian lenders cap FOIR between 40% and 55%; 50% (midpoint) used as a sector-generic placeholder. |
| KREDITBEE | foir_cap | 0.5 ratio | foir_cap=0.50 is an ESTIMATE and is NOT KreditBee-specific - no fintech lender in this dataset has a verified foir_cap to take a median from. Basis is the generic 40-55% industry FOIR-cap range; 50% (midpoint) used as a sector-generic placeholder. |

## Genuinely unresearchable fields (left blank, confidence = not_published)

These are documented gaps, not oversights - each was searched and the search is recorded, rather than guessing a number with no basis at all.

| Lender | Field | Why it's missing |
|---|---|---|
| POONAWALLA | min_cibil | This sheet's own notes: 'Min CIBIL not published (needs high bureau score)' - the stored 750 is not a confirmed lender figure. |

_Additional per-field `not_published`/N/A notes also live in the `notes` column of the main workbook (`personal_loan_rules_20_lenders_v2.xlsx`) for fields that are blank in the wide table rather than rows in `rules.csv` - e.g. HSBC's missing income floor, Union Bank's missing `min_loan`.

## Calculator-inferred formulas (not published by the lender, reverse-engineered)

| Lender | Rule | Value | How it was derived |
|---|---|---|---|
| IDFC | salary_multiple_on_disposable_income | 10 | Verified formula: eligible_loan = 10 x (net_monthly_income - existing_emi), capped at product max_loan (Rs 15,00,000). 4 test points, exact match. |
| KOTAK | salary_multiple_on_disposable_income | 20 | Verified formula: eligible_loan = 20 x (net_monthly_income - existing_emi). 3 test points, exact match. Calculator's own tenure default (120mo) exceeds this sheet's stored max_tenure_months=72 - flag for manual review. |

See `docs/foir-methodology.md` for the full reverse-engineering method.