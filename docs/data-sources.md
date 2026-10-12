# Data sources

Generated from `data/rules.csv` and `data/lenders.csv` by `scripts/gen_docs.py` - do not hand-edit this file, edit the CSVs and re-run that script instead.

Every row below is one rule collected for one lender: what field, what value, where it came from, when it was read, and how confident the collection is in it.

**Confidence tags used throughout:** `official` (lender's own page, stated as policy), `faq` (lender's own FAQ/help text, not the main eligibility list), `aggregator` (a third-party comparison site, used only when the lender's own page was unreadable), `conflict` (the lender states two different values in two places - the stricter one is kept, flagged), `calculator_inferred` (reverse-engineered from the lender's own live eligibility calculator - see `foir-methodology.md`), `not_published` (checked, no source states this), `assumed` (a last-resort estimate with its basis stated in the note - never silent).

## AXIS — Axis Bank

Sources cited (3):
- https://www.axis.bank.in/retail/loans/personal-loan

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://axisbank.com/retail/loans/personal-loan/personal-loan-for-salaried
- https://bankbazaar.com/cibil/cibil-score-for-personal-loan-in-axis-bank.html

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 21 years | — | official | 2026-10-11 | True |
| max_age_at_apply | <= 58 years | — | official | 2026-10-11 | True |
| max_age_at_maturity | <= 60 years | — | official | 2026-10-11 | True |
| min_current_job_months | >= 12 months | — | official | 2026-10-11 | True |
| min_cibil | >= 700 score | — | faq | 2026-10-11 | False |
| allows_ntc | == False bool | — | official | 2026-10-11 | True |
| foir_cap | <= 0.7 ratio | — | official | 2026-10-11 | True |
| min_income | >= 15000 INR/month | — | official | 2026-10-11 | True |

**Notes:**
- Axis's own text: 'preferred 700+', not stated as a hard cutoff.

## BAJAJ — Bajaj Finance

Sources cited (4):
- https://www.bajajfinserv.in/personal-loan-of-5-lakh-for-3-years

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://www.bajajfinserv.in/grace-period-for-emi-payment
- https://www.bajajfinserv.in/personal-loan
- https://www.bajajfinserv.in/personal-loan-what-is-the-duration-of-personal-loan

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 21 years | — | official | 2026-10-11 | True |
| max_age_at_apply | <= 80 years | — | official | 2026-10-11 | True |
| max_age_at_maturity | <= 80 years | — | official | 2026-10-11 | True |
| min_total_exp_months | >= 24 months | — | official | 2026-10-11 | True |
| min_current_job_months | >= 12 months | — | official | 2026-10-11 | True |
| min_cibil | >= 650 score | — | conflict | 2026-10-11 | True |
| allows_ntc | == False bool | — | official | 2026-10-11 | True |
| foir_cap | <= 0.75 ratio | — | official | 2026-10-11 | True |
| min_income | >= 20000 INR/month | — | official | 2026-10-11 | True |

**Notes:**
- This sheet's confidence text cites 685 as official, but 650 is the value stored - a real conflict, flagging rather than silently picking one.

## BOB — Bank of Baroda

Sources cited (3):
- https://bankofbaroda.bank.in/loans/personal-loan/baroda-personal-loan

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://bankofbaroda.bank.in/loans/personal-loan
- https://www.bankbazaar.com/bank-of-baroda-personal-loan.html

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 21 years | — | official | 2026-10-11 | True |
| max_age_at_apply | <= 58 years | — | official | 2026-10-11 | True |
| max_age_at_maturity | <= 60 years | — | official | 2026-10-11 | True |
| min_total_exp_months | >= 12 months | — | official | 2026-10-11 | True |
| min_current_job_months | >= 12 months | — | official | 2026-10-11 | True |
| min_cibil | >= 726 score | — | official | 2026-10-11 | True |
| allows_ntc | == False bool | — | official | 2026-10-11 | True |
| foir_cap | <= 0.4 ratio | — | official | 2026-10-11 | True |
| min_income | >= 15000 INR/month | — | official | 2026-10-11 | True |

## FEDERAL — Federal Bank

Sources cited (3):
- https://www.federalbank.co.in/fedpremia

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://www.bankbazaar.com/federal-bank-personal-loan-eligibility-calculator.html
- https://www.federalbank.co.in/digital-personal-loans-epifi

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 21 years | — | official | 2026-10-11 | True |
| max_age_at_apply | <= 55 years | — | official | 2026-10-11 | True |
| max_age_at_maturity | <= 60 years | — | official | 2026-10-11 | True |
| min_total_exp_months | >= 36 months | — | official | 2026-10-11 | True |
| min_current_job_months | >= 6 months | — | official | 2026-10-11 | True |
| min_cibil | >= 750 score | — | estimate | 2026-10-11 | True |
| foir_cap | <= 0.5 ratio | — | assumed | 2026-10-11 | True |
| min_income | >= 25000 INR/month | — | official | 2026-10-11 | True |

**Notes:**
- This sheet's own confidence column: estimate, and specific to Federal's digital epiFI product only, not the main product.
- foir_cap=0.50 is an ESTIMATE. Federal Bank publishes no FOIR figure. Assumed = median foir_cap of comparable private_bank lenders (HDFC 0.50, ICICI 0.45, AXIS 0.70 -> median 0.50).

## Fibe — fibe

Sources cited (2):
- https://www.fibe.in/personal-loan/

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://www.airtel.in/finance/personal-loan/fibe-personal-loan

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 19 years | — | official | 2026-10-11 | True |
| max_age_at_apply | <= 55 years | — | official | 2026-10-11 | True |
| max_age_at_maturity | <= 55 years | — | official | 2026-10-11 | True |
| min_total_exp_months | >= 24 months | — | official | 2026-10-11 | True |
| min_current_job_months | >= 12 months | — | estimate | 2026-10-11 | True |
| min_cibil | >= 650 score | — | official | 2026-10-11 | True |
| allows_ntc | == True bool | — | official | 2026-10-11 | True |
| foir_cap | <= 0.5 ratio | — | assumed | 2026-10-11 | True |
| min_income | >= 20000 INR/month | — | official | 2026-10-11 | True |

**Notes:**
- foir_cap=0.50 is an ESTIMATE and is NOT Fibe-specific - no fintech lender in this dataset has a verified foir_cap to take a median from. Basis is Fibe's own blog, which states most Indian lenders cap FOIR between 40% and 55%; 50% (midpoint) used as a sector-generic placeholder.

## HDBFS — HDB Financial Services

Sources cited (3):
- https://paisabazaar.com/hdb/personal-loan

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://www.creditmantri.com/hdb-personal-loan/
- https://www.wishfin.com/hdb-financial-services-personal-loan-689/

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 21 years | — | aggregator | 2026-10-11 | True |
| max_age_at_apply | <= 58 years | — | aggregator | 2026-10-11 | True |
| max_age_at_maturity | <= 60 years | — | aggregator | 2026-10-11 | True |
| min_total_exp_months | >= 12 months | — | aggregator | 2026-10-11 | True |
| min_current_job_months | >= 12 months | — | aggregator | 2026-10-11 | True |
| min_cibil | >= 750 score | — | aggregator | 2026-10-11 | True |
| allows_ntc | == False bool | — | aggregator | 2026-10-11 | True |
| foir_cap | <= 0.65 ratio | — | assumed | 2026-10-11 | True |
| min_income | >= 20000 INR/month | — | aggregator | 2026-10-11 | True |

**Notes:**
- foir_cap=0.65 is an ESTIMATE. HDB Financial Services publishes no FOIR figure. Assumed = median foir_cap of comparable nbfc lenders (BAJAJ 0.75, TATACAP 0.55, POONAWALLA 0.65 -> median 0.65).

## HDFC — HDFC Bank

Sources cited (5):
- https://www.hdfc.bank.in/personal-loan/eligibility-criteria
- https://www.hdfc.bank.in/personal-loan/loan-for-salaried

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://v.hdfc.bank.in/htdocs/amp/personal-loan/rates_fees.html
- https://v.hdfc.bank.in/htdocs/common/2021/mar/30/pl/index6oct2023.html
- https://www.hdfc.bank.in/personal-loan

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 21 years | — | official | 2026-10-11 | True |
| max_age_at_apply | <= 60 years | — | official | 2026-10-11 | True |
| max_age_at_maturity | <= 60 years | — | assumed | 2026-10-11 | True |
| min_total_exp_months | >= 24 months | — | official | 2026-10-11 | True |
| min_current_job_months | >= 12 months | — | official | 2026-10-11 | True |
| min_cibil | >= 720 score | — | faq | 2026-10-11 | True |
| allows_ntc | == True bool | — | official | 2026-10-11 | True |
| foir_cap | <= 0.5 ratio | — | official | 2026-10-11 | True |
| min_income | >= 25000 INR/month | employer_category == 'govt' | official | 2026-10-11 | True |
| min_income | >= 15000 INR/month | otherwise | aggregator | 2026-10-11 | True |
| allowed_employment_type | in [salaried] enum | — | official | 2026-10-11 | True |

**Notes:**
- max_age_at_maturity=60 is an ESTIMATE: no HDFC source states a maturity-age distinct from the apply-age cap of 60. Assumed equal to max_age_at_apply by analogy with other lenders in this dataset that publish only one age band (ICICI 58/58, LTFIN 58/58, Fibe 55/55).
- In FAQ text, not the bullet-point eligibility list (per this sheet's own confidence column).
- Condition narrowed to 'govt' only - this lender's raw data distinguishes govt vs private income minimums, not finer employer categories (mnc/psu/sme), even though those exist as possible input_variables values.
- min_income=15000 (non-metro) sourced from BankBazaar's HDFC eligibility page, not HDFC's own site (which is JS-rendered and unreadable by this tool's fetch). BankBazaar also states the requirement rises to Rs 20,000/month in metro cities - not separately modeled here.
- Self-employed routed to a different (business) loan product, not this personal loan.

## HSBC — HSBC India

Sources cited (4):
- https://www.hsbc.co.in/help/faqs/personal-loans/
- https://www.hsbc.co.in/loans/products/personal

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://www.hsbc.bank.in/help/faqs/personal-loans/
- https://www.paisabazaar.com/hsbc-bank/personal-loan/

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 21 years | — | aggregator | 2026-10-11 | True |
| max_age_at_apply | <= 60 years | — | official | 2026-10-11 | True |
| max_age_at_maturity | <= 60 years | — | official | 2026-10-11 | True |
| min_cibil | >= 700 score | — | official | 2026-10-11 | True |
| requires_salary_account | == True bool | — | official | 2026-10-11 | True |
| foir_cap | <= 0.5 ratio | — | assumed | 2026-10-11 | True |
| requires_existing_customer | == True bool | — | official | 2026-10-11 | True |

**Notes:**
- This sheet's own confidence column marks age as aggregator-estimate, not from an HSBC page directly.
- foir_cap=0.50 is an ESTIMATE. HSBC publishes no FOIR figure and has no public eligibility calculator. Assumed = median foir_cap of comparable private_bank lenders (HDFC 0.50, ICICI 0.45, AXIS 0.70 -> median 0.50).
- Eligible applicants hold a liability account, credit card or home loan with HSBC, or work for a select corporate.

## ICICI — ICICI Bank

Sources cited (4):
- https://www.icici.bank.in/personal-banking/loans/personal-loan.html

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://icicibank.com/personal-banking/loans/personal-loan/70000-personal-loan
- https://www.icici.bank.in/personal-banking/loans/personal-loan/eligibility/eligibility-faqs
- https://www.icici.bank.in/personal-banking/loans/personal-loan/personal-loans-faqs

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 20 years | — | official | 2026-10-11 | True |
| max_age_at_apply | <= 58 years | — | official | 2026-10-11 | True |
| max_age_at_maturity | <= 58 years | — | official | 2026-10-11 | True |
| min_total_exp_months | >= 24 months | — | official | 2026-10-11 | True |
| min_cibil | >= 700 score | — | official | 2026-10-11 | True |
| allows_ntc | == False bool | — | official | 2026-10-11 | True |
| foir_cap | <= 0.45 ratio | — | faq | 2026-10-11 | False |
| min_income | >= 20000 INR/month | employer_category == 'govt' | official | 2026-10-11 | True |
| min_income | >= 30000 INR/month | otherwise | official | 2026-10-11 | True |

**Notes:**
- ICICI's FAQ states this as guidance ('prefers 40-45%'), not a hard cutoff.
- Condition narrowed to 'govt' only - this lender's raw data distinguishes govt vs private income minimums, not finer employer categories (mnc/psu/sme), even though those exist as possible input_variables values.

## IDFC — IDFC FIRST Bank

Sources cited (4):
- https://www.idfcfirst.bank.in/personal-banking/loans/personal-loan/personal-loan-eligibility-calculator
- https://www.idfcfirstbank.com/personal-banking/loans/personal-loan/personal-loan-for-salaried

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://www.idfcfirst.bank.in/finfirst-blogs/personal-loan/minimum-salary-required-for-personal-loan
- https://www.idfcfirst.bank.in/finfirst-blogs/personal-loan/personal-loan-eligibility-criteria

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 21 years | — | official | 2026-10-11 | True |
| max_age_at_apply | <= 58 years | — | official | 2026-10-11 | True |
| max_age_at_maturity | <= 60 years | — | official | 2026-10-11 | True |
| min_total_exp_months | >= 12 months | — | official | 2026-10-11 | True |
| min_current_job_months | >= 6 months | — | official | 2026-10-11 | True |
| min_cibil | >= 710 score | — | conflict | 2026-10-11 | True |
| allows_ntc | == False bool | — | official | 2026-10-11 | True |
| min_income | >= 10000 INR/month | — | official | 2026-10-11 | True |
| salary_multiple_on_disposable_income | * 10 x (income-obligations) | — | calculator_inferred | 2026-10-12 | True |

**Notes:**
- Flagged as conflict in this sheet (710 vs 730 seen elsewhere); 710 (from IDFC's own eligibility calculator page) stored.
- Verified formula: eligible_loan = 10 x (net_monthly_income - existing_emi), capped at product max_loan (Rs 15,00,000). 4 test points, exact match.

## INDUSIND — IndusInd Bank

Sources cited (3):
- https://www.indusind.bank.in/in/en/personal/loans/personal-loan/education.html

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://bank.indusind.bank.in/in/en/personal/loans/personal-loan.html
- https://www.paisabazaar.com/indusind-bank/5-lakh-personal-loan-pvamt

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 21 years | — | official | 2026-10-11 | True |
| max_age_at_apply | <= 60 years | — | assumed | 2026-10-11 | True |
| max_age_at_maturity | <= 60 years | — | official | 2026-10-11 | True |
| min_total_exp_months | >= 24 months | — | official | 2026-10-11 | True |
| min_current_job_months | >= 12 months | — | official | 2026-10-11 | True |
| min_cibil | >= 730 score | — | official | 2026-10-11 | True |
| allows_ntc | == False bool | — | official | 2026-10-11 | True |
| foir_cap | <= 0.5 ratio | — | assumed | 2026-10-11 | True |
| min_income | >= 25000 INR/month | — | official | 2026-10-11 | True |

**Notes:**
- max_age_at_apply=60 is an ESTIMATE: IndusInd's own eligibility page was unreadable (JS-rendered) and its blog gives '60' only as a generic industry example, not stated as IndusInd's own cutoff. Assumed equal to this dataset's existing max_age_at_maturity=60 for IndusInd.
- foir_cap=0.50 is an ESTIMATE, not IndusInd's own published or calculator-derived figure. Assumed = median foir_cap of comparable private_bank lenders already verified in this dataset (HDFC 0.50, ICICI 0.45, AXIS 0.70 -> median 0.50).

## KOTAK — Kotak Mahindra Bank

Sources cited (4):
- https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/eligibility.html
- https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/personal-loan-for-15-lakhs.html

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://www.kotak.bank.in/en/personal-banking/loans/personal-loan/small-personal-loan.html
- https://www.paisabazaar.com/kotak-mahindra-bank/30-lakh-personal-loan-pvamt/

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 21 years | — | official | 2026-10-11 | True |
| max_age_at_apply | <= 60 years | — | official | 2026-10-11 | True |
| max_age_at_maturity | <= 60 years | — | official | 2026-10-11 | True |
| min_total_exp_months | >= 12 months | — | official | 2026-10-11 | True |
| min_current_job_months | >= 12 months | — | official | 2026-10-11 | True |
| min_cibil | >= 750 score | — | conflict | 2026-10-11 | True |
| allows_ntc | == False bool | — | official | 2026-10-11 | True |
| min_income | >= 25000 INR/month | — | official | 2026-10-11 | True |
| min_education | >= graduate enum | — | official | 2026-10-11 | True |
| salary_multiple_on_disposable_income | * 20 x (income-obligations) | — | calculator_inferred | 2026-10-12 | True |

**Notes:**
- This sheet's own confidence column flags CIBIL as conflicting across Kotak's own pages (700/730/750); stricter value (750) stored.
- Verified formula: eligible_loan = 20 x (net_monthly_income - existing_emi). 3 test points, exact match. Calculator's own tenure default (120mo) exceeds this sheet's stored max_tenure_months=72 - flag for manual review.

## KREDITBEE — KreditBee

Sources cited (4):
- https://www.paisabazaar.com/personal-loan/kreditbee

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://gocredit.money/lender/kreditbee
- https://www.paisabazaar.com/personal-loan/kreditbee/eligibility
- https://www.tatacapitalmoneyfy.com/content/tata-capital-moneyfy/en/loans/personal-loan/kreditbee.html

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 21 years | — | aggregator | 2026-10-11 | True |
| max_age_at_apply | <= 60 years | — | aggregator | 2026-10-11 | True |
| max_age_at_maturity | <= 60 years | — | aggregator | 2026-10-11 | True |
| min_total_exp_months | >= 12 months | — | aggregator | 2026-10-11 | True |
| min_current_job_months | >= 2 months | — | aggregator | 2026-10-11 | True |
| min_cibil | >= 670 score | — | aggregator | 2026-10-11 | True |
| allows_ntc | == True bool | — | aggregator | 2026-10-11 | True |
| foir_cap | <= 0.5 ratio | — | assumed | 2026-10-11 | True |
| min_income | >= 10000 INR/month | — | aggregator | 2026-10-11 | True |

**Notes:**
- foir_cap=0.50 is an ESTIMATE and is NOT KreditBee-specific - no fintech lender in this dataset has a verified foir_cap to take a median from. Basis is the generic 40-55% industry FOIR-cap range; 50% (midpoint) used as a sector-generic placeholder.

## LTFIN — L&T Finance

Sources cited (4):
- https://www.ltfinance.com/blog/personal-loan/minimum-salary-for-personal-loan
- https://www.ltfinance.com/personal-loan

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://www.ltfinance.com/blog/personal-loan/personal-loan-for-salaried-employees
- https://www.ltfinance.com/personal-loan-eligibility-calculator

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 21 years | — | official | 2026-10-11 | True |
| max_age_at_apply | <= 58 years | — | official | 2026-10-11 | True |
| max_age_at_maturity | <= 58 years | — | official | 2026-10-11 | True |
| min_total_exp_months | >= 12 months | — | estimate | 2026-10-11 | True |
| min_current_job_months | >= 12 months | — | official | 2026-10-11 | True |
| min_cibil | >= 700 score | — | official | 2026-10-11 | True |
| allows_ntc | == False bool | — | official | 2026-10-11 | True |
| foir_cap | <= 0.65 ratio | — | assumed | 2026-10-11 | True |
| min_income | >= 25000 INR/month | — | official | 2026-10-11 | True |
| min_income | >= 25000 INR/month | city_tier == 'tier1' | official | 2026-10-11 | True |
| min_income | >= 15000 INR/month | city_tier in [tier2,tier3] | official | 2026-10-11 | True |

**Notes:**
- foir_cap=0.65 is an ESTIMATE, distinct from the documented attempt to reverse-engineer L&T Finance's own calculator (which produced unreliable/buggy output). Assumed = median foir_cap of comparable nbfc lenders (BAJAJ 0.75, TATACAP 0.55, POONAWALLA 0.65 -> median 0.65).

## PNB — Punjab National Bank

Sources cited (2):
- https://paisabazaar.com/punjab-national-bank/personal-loan

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://pnb.bank.in/Retail-Advances-interst-rate-on-advances-linked-to-mclr.html

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 21 years | — | aggregator | 2026-10-11 | True |
| max_age_at_apply | <= 59 years | — | aggregator | 2026-10-11 | True |
| max_age_at_maturity | <= 60 years | — | aggregator | 2026-10-11 | True |
| min_total_exp_months | >= 24 months | — | aggregator | 2026-10-11 | True |
| min_current_job_months | >= 12 months | — | aggregator | 2026-10-11 | True |
| min_cibil | >= 650 score | — | aggregator | 2026-10-11 | True |
| allows_ntc | == False bool | — | aggregator | 2026-10-11 | True |
| foir_cap | <= 0.6 ratio | — | aggregator | 2026-10-11 | True |
| min_income | >= 25000 INR/month | — | aggregator | 2026-10-11 | True |

## POONAWALLA — Poonawalla Fincorp

Sources cited (4):
- https://poonawallafincorp.com/20-lakh-personal-loan.php

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://poonawallafincorp.com/50-lakh-personal-loan.php
- https://www.mymoneymantra.com/personal-loans/poonawalla-fincorp
- https://www.paisabazaar.com/personal-loan/poonawalla-fincorp/

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 22 years | — | official | 2026-10-11 | True |
| max_age_at_apply | <= 57 years | — | official | 2026-10-11 | True |
| max_age_at_maturity | <= 60 years | — | official | 2026-10-11 | True |
| min_total_exp_months | >= 12 months | — | official | 2026-10-11 | True |
| min_current_job_months | >= 1 months | — | official | 2026-10-11 | True |
| min_cibil | >= 750 score | — | not_published | 2026-10-11 | False |
| allows_ntc | == False bool | — | official | 2026-10-11 | True |
| foir_cap | <= 0.65 ratio | — | official | 2026-10-11 | True |
| min_income | >= 30000 INR/month | — | official | 2026-10-11 | True |

**Notes:**
- This sheet's own notes: 'Min CIBIL not published (needs high bureau score)' - the stored 750 is not a confirmed lender figure.

## SBI — State Bank of India

Sources cited (5):
- https://sbi.bank.in/web/personal-banking/loans/personal-loans/real-time-xpress-credit

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://paisabazaar.com/sbi-bank/personal-loan-interest-rate
- https://sbi.bank.in/web/business/information/interest-rates-perquisite-calculation
- https://sbi.bank.in/web/interest-rates/interest-rates/loan-schemes-interest-rates/personal-loans-schemes
- https://sbi.co.in/portal/web/interest-rates/penal-interest

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 21 years | — | official | 2026-10-11 | True |
| max_age_at_apply | <= 60 years | — | official | 2026-10-11 | True |
| max_age_at_maturity | <= 76 years | — | official | 2026-10-11 | True |
| min_total_exp_months | >= 12 months | — | official | 2026-10-11 | True |
| min_current_job_months | >= 12 months | — | official | 2026-10-11 | True |
| min_cibil | >= 670 score | — | official | 2026-10-11 | True |
| requires_salary_account | == True bool | — | official | 2026-10-11 | True |
| allows_ntc | == True bool | — | official | 2026-10-11 | True |
| foir_cap | <= 0.65 ratio | — | official | 2026-10-11 | True |
| min_income | >= 20000 INR/month | employer_category == 'govt' | official | 2026-10-11 | True |
| min_income | >= 25000 INR/month | otherwise | official | 2026-10-11 | True |

**Notes:**
- Condition narrowed to 'govt' only - this lender's raw data distinguishes govt vs private income minimums, not finer employer categories (mnc/psu/sme), even though those exist as possible input_variables values.

## TATACAP — Tata Capital

Sources cited (4):
- https://www.tatacapital.com/personal-loan/2-lakhs-personal-loan.html

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://tatacapital.com/personal-loan/personal-loan-in-hyderabad.html
- https://www.tatacapital.com/content/tata-capital-web/en/personal-loan/rates-and-charges.html
- https://www.tatacapital.com/personal-loan/3-lakhs-personal-loan.html

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 21 years | — | official | 2026-10-11 | True |
| max_age_at_apply | <= 58 years | — | official | 2026-10-11 | True |
| max_age_at_maturity | <= 58 years | — | official | 2026-10-11 | True |
| min_total_exp_months | >= 24 months | — | official | 2026-10-11 | True |
| min_current_job_months | >= 12 months | — | official | 2026-10-11 | True |
| min_cibil | >= 725 score | — | estimate | 2026-10-11 | False |
| allows_ntc | == False bool | — | official | 2026-10-11 | True |
| foir_cap | <= 0.55 ratio | — | official | 2026-10-11 | True |
| min_income | >= 20000 INR/month | — | official | 2026-10-11 | True |

**Notes:**
- Tata Capital's own text calls this 'preferred', not a stated cutoff.

## UNION — Union Bank of India

Sources cited (4):
- https://unionbankofindia.co.in/english/p-r-personalloan-govtorg.aspx

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://www.paisabazaar.com/union-bank-of-india/personal-loan
- https://www.unionbankofindia.bank.in/pdf/Penal%20Charges_Union%20Bank%20of%20India.pdf
- https://www.wishfin.com/union-bank-of-india-personal-loan-307/

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 18 years | — | official | 2026-10-11 | True |
| max_age_at_apply | <= 59 years | — | official | 2026-10-11 | True |
| max_age_at_maturity | <= 60 years | — | official | 2026-10-11 | True |
| min_total_exp_months | >= 24 months | — | official | 2026-10-11 | True |
| min_current_job_months | >= 6 months | — | aggregator | 2026-10-11 | True |
| min_cibil | >= 700 score | — | official | 2026-10-11 | True |
| requires_salary_account | == True bool | — | official | 2026-10-11 | True |
| allows_ntc | == False bool | — | official | 2026-10-11 | True |
| foir_cap | <= 0.6 ratio | — | assumed | 2026-10-11 | True |
| min_income | >= 15000 INR/month | — | official | 2026-10-11 | True |

**Notes:**
- This sheet's own confidence column marks experience as aggregator-estimate.
- foir_cap=0.60 is an ESTIMATE. Union Bank's own eligibility content was unreachable. Assumed = median foir_cap of comparable psu_bank lenders (SBI 0.65, BOB 0.40, PNB 0.60 -> median 0.60).

## YESBANK — Yes Bank

Sources cited (3):
- https://www.yesbank.in/personal-banking/yes-individual/loans/personal-loan

Also cited in the original research (not tied to one specific rule row above - background reading, a cross-check against a second site, or a page the fact ended up sourced from elsewhere on):
- https://www.creditmantri.com/cibil-score-required-for-yes-bank-personal-loan/
- https://www.yes.bank.in/personal-banking/loans/personal-loan/interest-rates

| Rule | Value | Condition | Confidence | Date | Hard cutoff |
|---|---|---|---|---|---|
| min_age | >= 21 years | — | official | 2026-10-11 | True |
| max_age_at_apply | <= 60 years | — | official | 2026-10-11 | True |
| max_age_at_maturity | <= 60 years | — | official | 2026-10-11 | True |
| min_total_exp_months | >= 12 months | — | official | 2026-10-11 | True |
| min_current_job_months | >= 12 months | — | official | 2026-10-11 | True |
| min_cibil | >= 700 score | — | official | 2026-10-11 | True |
| allows_ntc | == False bool | — | official | 2026-10-11 | True |
| foir_cap | <= 0.5 ratio | — | assumed | 2026-10-11 | True |
| min_income | >= 25000 INR/month | — | official | 2026-10-11 | True |

**Notes:**
- foir_cap=0.50 is an ESTIMATE. No Yes Bank FOIR figure or working calculator was found. Assumed = median foir_cap of comparable private_bank lenders (HDFC 0.50, ICICI 0.45, AXIS 0.70 -> median 0.50).
