# Test results

Generated against 20 lenders, 184 rules.


## P01_high_income_good_cibil
High-income private employee, excellent CIBIL, no existing EMI - should be eligible almost everywhere, good test of ranking.

**Eligible at 17/20 lenders.**

| Rank | Lender | Offered Amt | Rate | Tenure | EMI | Total Cost | Flags |
|---|---|---|---|---|---|---|---|
| 1 | YESBANK | ₹500,000 | 14.91% | 36mo | ₹17,311 | ₹135,683 |  |
| 2 | PNB | ₹1,000,000 | 11.49% | 36mo | ₹32,971 | ₹196,965 |  |
| 3 | ICICI | ₹1,000,000 | 12.49% | 36mo | ₹33,451 | ₹229,227 |  |
| 4 | BOB | ₹1,000,000 | 13.25% | 36mo | ₹33,813 | ₹237,282 |  |
| 5 | AXIS | ₹1,000,000 | 14.39% | 36mo | ₹34,369 | ₹257,295 |  |
| 6 | POONAWALLA | ₹1,000,000 | 14.26% | 36mo | ₹34,305 | ₹274,981 |  |
| 7 | FEDERAL | ₹1,000,000 | 15.19% | 36mo | ₹34,758 | ₹281,304 |  |
| 8 | LTFIN | ₹1,000,000 | 15.90% | 36mo | ₹35,108 | ₹293,877 |  |
| 9 | HDFC | ₹1,000,000 | 16.22% | 36mo | ₹35,264 | ₹309,507 |  |
| 10 | BAJAJ | ₹1,000,000 | 16.56% | 36mo | ₹35,434 | ₹316,929 |  |
| 11 | Fibe | ₹1,000,000 | 18.00% | 36mo | ₹36,152 | ₹321,486 | near-tie with BAJAJ (within 2% cost) - BAJAJ is nbfc, this is fintech; ranking is on cost only, this is a comment, not a bias. |
| 12 | KREDITBEE | ₹1,000,000 | 17.39% | 36mo | ₹35,848 | ₹340,520 |  |
| 13 | INDUSIND | ₹1,000,000 | 19.67% | 36mo | ₹36,996 | ₹351,865 |  |
| 14 | KOTAK | ₹1,000,000 | 18.46% | 36mo | ₹36,385 | ₹359,845 | amount formula is calculator-inferred (reverse-engineered, not published): 20.0x disposable income |
| 15 | IDFC | ₹1,000,000 | 22.36% | 36mo | ₹38,378 | ₹416,619 | amount formula is calculator-inferred (reverse-engineered, not published): 10.0x disposable income |
| 16 | HDBFS | ₹1,000,000 | 23.87% | 36mo | ₹39,163 | ₹459,864 |  |
| 17 | TATACAP | ₹1,000,000 | 26.54% | 36mo | ₹40,577 | ₹510,788 |  |

**Rejected:**

- **SBI**: requires_salary_account failed: applicant's salary account is with no bank, not SBI.
- **HSBC**: requires_salary_account failed: applicant's salary account is with no bank, not HSBC.
- **UNION**: requires_salary_account failed: applicant's salary account is with no bank, not UNION.

## P02_high_existing_emi_rejected_on_foir
Decent income but existing EMI already eats most of it - should be rejected on FOIR at most FOIR-cap lenders.

**Eligible at 2/20 lenders.**

| Rank | Lender | Offered Amt | Rate | Tenure | EMI | Total Cost | Flags |
|---|---|---|---|---|---|---|---|
| 1 | BAJAJ | ₹65,437 | 23.12% | 48mo | ₹2,102 | ₹38,145 |  |
| 2 | IDFC | ₹120,000 | 33.74% | 48mo | ₹4,585 | ₹104,293 | amount formula is calculator-inferred (reverse-engineered, not published): 10.0x disposable income |

**Rejected:**

- **SBI**: requires_salary_account failed: applicant's salary account is with no bank, not SBI.
- **HDFC**: Eligible amount ₹0 is below this lender's product minimum ₹50,000.
- **ICICI**: Eligible amount ₹0 is below this lender's product minimum ₹50,000.
- **AXIS**: Eligible amount ₹0 is below this lender's product minimum ₹50,000.
- **KOTAK**: min_cibil failed: applicant=740, lender requires >= 750.0
- **INDUSIND**: Eligible amount ₹0 is below this lender's product minimum ₹30,000.
- **HSBC**: requires_salary_account failed: applicant's salary account is with no bank, not HSBC.
- **FEDERAL**: min_cibil failed: applicant=740, lender requires >= 750.0
- **BOB**: Eligible amount ₹0 is below this lender's product minimum ₹50,000.
- **PNB**: Eligible amount ₹0 is below this lender's product minimum ₹25,000.
- **UNION**: requires_salary_account failed: applicant's salary account is with no bank, not UNION.
- **YESBANK**: Eligible amount ₹0 is below this lender's product minimum ₹50,000.
- **TATACAP**: Eligible amount ₹0 is below this lender's product minimum ₹40,000.
- **HDBFS**: min_cibil failed: applicant=740, lender requires >= 750.0
- **POONAWALLA**: Eligible amount ₹0 is below this lender's product minimum ₹100,000.
- **LTFIN**: Eligible amount ₹0 is below this lender's product minimum ₹50,000.
- **Fibe**: Eligible amount ₹0 is below this lender's product minimum ₹30,000.
- **KREDITBEE**: Eligible amount ₹0 is below this lender's product minimum ₹3,000.

## P03_ntc_new_to_credit
New-to-credit (cibil_score=0) applicant - should fail min_cibil gates everywhere that have one, even where allows_ntc isn't explicitly set.

**Eligible at 0/20 lenders.**


**Rejected:**

- **SBI**: min_total_exp_months failed: applicant=10, lender requires >= 12.0
- **HDFC**: min_total_exp_months failed: applicant=10, lender requires >= 24.0
- **ICICI**: min_total_exp_months failed: applicant=10, lender requires >= 24.0
- **AXIS**: min_current_job_months failed: applicant=10, lender requires >= 12.0
- **KOTAK**: min_total_exp_months failed: applicant=10, lender requires >= 12.0
- **IDFC**: min_total_exp_months failed: applicant=10, lender requires >= 12.0
- **INDUSIND**: min_total_exp_months failed: applicant=10, lender requires >= 24.0
- **HSBC**: min_cibil failed: applicant=0, lender requires >= 700.0
- **FEDERAL**: min_total_exp_months failed: applicant=10, lender requires >= 36.0
- **BOB**: min_total_exp_months failed: applicant=10, lender requires >= 12.0
- **PNB**: min_total_exp_months failed: applicant=10, lender requires >= 24.0
- **UNION**: min_total_exp_months failed: applicant=10, lender requires >= 24.0
- **YESBANK**: min_total_exp_months failed: applicant=10, lender requires >= 12.0
- **BAJAJ**: min_total_exp_months failed: applicant=10, lender requires >= 24.0
- **TATACAP**: min_total_exp_months failed: applicant=10, lender requires >= 24.0
- **HDBFS**: min_total_exp_months failed: applicant=10, lender requires >= 12.0
- **POONAWALLA**: min_total_exp_months failed: applicant=10, lender requires >= 12.0
- **LTFIN**: min_total_exp_months failed: applicant=10, lender requires >= 12.0
- **Fibe**: min_total_exp_months failed: applicant=10, lender requires >= 24.0
- **KREDITBEE**: min_total_exp_months failed: applicant=10, lender requires >= 12.0

## P04_govt_employee_sbi
Govt employee - tests the employer_category=='govt' conditional income rule (SBI).

**Eligible at 18/20 lenders.**

| Rank | Lender | Offered Amt | Rate | Tenure | EMI | Total Cost | Flags |
|---|---|---|---|---|---|---|---|
| 1 | Fibe | ₹691,517 | 18.00% | 36mo | ₹25,000 | ₹222,313 |  |
| 2 | YESBANK | ₹500,000 | 16.94% | 60mo | ₹12,410 | ₹257,110 |  |
| 3 | PNB | ₹800,000 | 11.81% | 60mo | ₹17,719 | ₹271,131 |  |
| 4 | SBI | ₹800,000 | 12.61% | 60mo | ₹18,043 | ₹294,557 |  |
| 5 | FEDERAL | ₹800,000 | 16.79% | 48mo | ₹22,997 | ₹327,866 |  |
| 6 | ICICI | ₹800,000 | 13.75% | 60mo | ₹18,509 | ₹330,565 |  |
| 7 | BOB | ₹800,000 | 14.55% | 60mo | ₹18,842 | ₹346,524 |  |
| 8 | AXIS | ₹800,000 | 16.60% | 60mo | ₹19,709 | ₹398,521 |  |
| 9 | POONAWALLA | ₹800,000 | 16.40% | 60mo | ₹19,624 | ₹409,442 |  |
| 10 | LTFIN | ₹800,000 | 18.60% | 60mo | ₹20,577 | ₹458,606 |  |
| 11 | HDFC | ₹800,000 | 19.33% | 60mo | ₹20,898 | ₹485,878 |  |
| 12 | IDFC | ₹550,000 | 28.05% | 60mo | ₹17,141 | ₹497,707 | amount formula is calculator-inferred (reverse-engineered, not published): 10.0x disposable income |
| 13 | BAJAJ | ₹800,000 | 19.84% | 60mo | ₹21,124 | ₹500,477 | near-tie with IDFC (within 2% cost) - IDFC is private_bank, this is nbfc; ranking is on cost only, this is a comment, not a bias. |
| 14 | KREDITBEE | ₹800,000 | 20.09% | 60mo | ₹21,234 | ₹514,030 |  |
| 15 | KOTAK | ₹800,000 | 22.20% | 60mo | ₹22,185 | ₹571,117 | amount formula is calculator-inferred (reverse-engineered, not published): 20.0x disposable income |
| 16 | INDUSIND | ₹800,000 | 24.26% | 60mo | ₹23,136 | ₹604,165 |  |
| 17 | HDBFS | ₹800,000 | 30.80% | 60mo | ₹26,277 | ₹816,632 |  |
| 18 | TATACAP | ₹800,000 | 34.31% | 60mo | ₹28,040 | ₹922,424 |  |

**Rejected:**

- **HSBC**: requires_salary_account failed: applicant's salary account is with SBI, not HSBC.
- **UNION**: requires_salary_account failed: applicant's salary account is with SBI, not UNION.

## P05_self_employed_out_of_scope
Self-employed - should be rejected EVERYWHERE with the explicit scope-limit reason, not silently evaluated against salaried rules.

**Eligible at 0/20 lenders.**


**Rejected:**

- **SBI**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **HDFC**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **ICICI**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **AXIS**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **KOTAK**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **IDFC**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **INDUSIND**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **HSBC**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **FEDERAL**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **BOB**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **PNB**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **UNION**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **YESBANK**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **BAJAJ**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **TATACAP**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **HDBFS**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **POONAWALLA**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **LTFIN**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **Fibe**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).
- **KREDITBEE**: Self-employed/pensioner applicants are out of scope for this model (ITR-based income rules were not collected; see docs/limitations.md).

## P06_near_age_cutoff
Older applicant close to several lenders' max_age_at_maturity - tests the age-at-maturity gate using requested tenure.

**Eligible at 1/20 lenders.**

| Rank | Lender | Offered Amt | Rate | Tenure | EMI | Total Cost | Flags |
|---|---|---|---|---|---|---|---|
| 1 | BAJAJ | ₹400,000 | 19.02% | 60mo | ₹10,381 | ₹239,357 |  |

**Rejected:**

- **SBI**: requires_salary_account failed: applicant's salary account is with no bank, not SBI.
- **HDFC**: Age at maturity (61.0) exceeds lender's max_age_at_maturity (60.0).
- **ICICI**: Age at maturity (61.0) exceeds lender's max_age_at_maturity (58.0).
- **AXIS**: Age at maturity (61.0) exceeds lender's max_age_at_maturity (60.0).
- **KOTAK**: Age at maturity (61.0) exceeds lender's max_age_at_maturity (60.0).
- **IDFC**: Age at maturity (61.0) exceeds lender's max_age_at_maturity (60.0).
- **INDUSIND**: Age at maturity (61.0) exceeds lender's max_age_at_maturity (60.0).
- **HSBC**: Age at maturity (61.0) exceeds lender's max_age_at_maturity (60.0).
- **FEDERAL**: max_age_at_apply failed: applicant=56, lender requires <= 55.0
- **BOB**: Age at maturity (61.0) exceeds lender's max_age_at_maturity (60.0).
- **PNB**: Age at maturity (61.0) exceeds lender's max_age_at_maturity (60.0).
- **UNION**: Age at maturity (61.0) exceeds lender's max_age_at_maturity (60.0).
- **YESBANK**: Age at maturity (61.0) exceeds lender's max_age_at_maturity (60.0).
- **TATACAP**: Age at maturity (61.0) exceeds lender's max_age_at_maturity (58.0).
- **HDBFS**: Age at maturity (61.0) exceeds lender's max_age_at_maturity (60.0).
- **POONAWALLA**: Age at maturity (61.0) exceeds lender's max_age_at_maturity (60.0).
- **LTFIN**: Age at maturity (61.0) exceeds lender's max_age_at_maturity (58.0).
- **Fibe**: max_age_at_apply failed: applicant=56, lender requires <= 55.0
- **KREDITBEE**: Age at maturity (61.0) exceeds lender's max_age_at_maturity (60.0).

## P07_idfc_kotak_multiplier_formula
Mid income, moderate existing EMI - exercises the calculator-verified disposable-income-multiple formula lenders (IDFC, Kotak) against FOIR-cap lenders side by side.

**Eligible at 17/20 lenders.**

| Rank | Lender | Offered Amt | Rate | Tenure | EMI | Total Cost | Flags |
|---|---|---|---|---|---|---|---|
| 1 | YESBANK | ₹500,000 | 17.95% | 48mo | ₹14,676 | ₹216,936 |  |
| 2 | Fibe | ₹1,000,000 | 18.00% | 36mo | ₹36,152 | ₹321,486 |  |
| 3 | PNB | ₹1,500,000 | 11.97% | 48mo | ₹39,479 | ₹409,976 |  |
| 4 | BOB | ₹1,293,238 | 15.20% | 48mo | ₹36,120 | ₹466,405 |  |
| 5 | ICICI | ₹1,487,703 | 14.37% | 48mo | ₹40,932 | ₹514,218 |  |
| 6 | KREDITBEE | ₹1,000,000 | 21.43% | 48mo | ₹31,200 | ₹547,601 |  |
| 7 | AXIS | ₹1,500,000 | 17.70% | 48mo | ₹43,825 | ₹633,617 |  |
| 8 | FEDERAL | ₹1,500,000 | 17.59% | 48mo | ₹43,742 | ₹644,606 |  |
| 9 | POONAWALLA | ₹1,500,000 | 17.47% | 48mo | ₹43,645 | ₹654,962 | near-tie with FEDERAL (within 2% cost) - FEDERAL is private_bank, this is nbfc; ranking is on cost only, this is a comment, not a bias. |
| 10 | LTFIN | ₹1,500,000 | 19.95% | 48mo | ₹45,606 | ₹734,068 |  |
| 11 | IDFC | ₹950,000 | 30.89% | 48mo | ₹34,700 | ₹748,868 | amount formula is calculator-inferred (reverse-engineered, not published): 10.0x disposable income |
| 12 | HDFC | ₹1,500,000 | 20.89% | 48mo | ₹46,357 | ₹785,143 |  |
| 13 | BAJAJ | ₹1,500,000 | 21.48% | 48mo | ₹46,837 | ₹810,110 |  |
| 14 | KOTAK | ₹1,500,000 | 24.07% | 48mo | ₹48,958 | ₹924,960 | amount formula is calculator-inferred (reverse-engineered, not published): 20.0x disposable income |
| 15 | INDUSIND | ₹1,472,463 | 26.56% | 48mo | ₹50,110 | ₹962,269 |  |
| 16 | HDBFS | ₹1,500,000 | 34.27% | 48mo | ₹57,794 | ₹1,349,111 |  |
| 17 | TATACAP | ₹1,434,750 | 38.20% | 48mo | ₹58,719 | ₹1,455,485 |  |

**Rejected:**

- **SBI**: requires_salary_account failed: applicant's salary account is with no bank, not SBI.
- **HSBC**: requires_salary_account failed: applicant's salary account is with no bank, not HSBC.
- **UNION**: requires_salary_account failed: applicant's salary account is with no bank, not UNION.

## P08_low_income_rejected_everywhere
Below most lenders' minimum income floor - should produce mostly 'min_income failed' rejections.

**Eligible at 1/20 lenders.**

| Rank | Lender | Offered Amt | Rate | Tenure | EMI | Total Cost | Flags |
|---|---|---|---|---|---|---|---|
| 1 | KREDITBEE | ₹100,000 | 25.48% | 24mo | ₹5,361 | ₹33,668 |  |

**Rejected:**

- **SBI**: requires_salary_account failed: applicant's salary account is with no bank, not SBI.
- **HDFC**: min_total_exp_months failed: applicant=12, lender requires >= 24.0
- **ICICI**: min_total_exp_months failed: applicant=12, lender requires >= 24.0
- **AXIS**: min_income failed: applicant=12000, lender requires >= 15000.0
- **KOTAK**: min_cibil failed: applicant=700, lender requires >= 750.0
- **IDFC**: min_cibil failed: applicant=700, lender requires >= 710.0
- **INDUSIND**: min_total_exp_months failed: applicant=12, lender requires >= 24.0
- **HSBC**: requires_salary_account failed: applicant's salary account is with no bank, not HSBC.
- **FEDERAL**: min_total_exp_months failed: applicant=12, lender requires >= 36.0
- **BOB**: min_cibil failed: applicant=700, lender requires >= 726.0
- **PNB**: min_total_exp_months failed: applicant=12, lender requires >= 24.0
- **UNION**: min_total_exp_months failed: applicant=12, lender requires >= 24.0
- **YESBANK**: min_income failed: applicant=12000, lender requires >= 25000.0
- **BAJAJ**: min_total_exp_months failed: applicant=12, lender requires >= 24.0
- **TATACAP**: min_total_exp_months failed: applicant=12, lender requires >= 24.0
- **HDBFS**: min_cibil failed: applicant=700, lender requires >= 750.0
- **POONAWALLA**: min_income failed: applicant=12000, lender requires >= 30000.0
- **LTFIN**: min_income failed: applicant=12000, lender requires >= 25000.0
- **Fibe**: min_total_exp_months failed: applicant=12, lender requires >= 24.0

## P09_rate_vs_fee_tradeoff
Clean profile used specifically to check that ranking is by total_cost, not by advertised rate_min_pct (a lower-rate lender with a high fee should NOT automatically win).

**Eligible at 17/20 lenders.**

| Rank | Lender | Offered Amt | Rate | Tenure | EMI | Total Cost | Flags |
|---|---|---|---|---|---|---|---|
| 1 | PNB | ₹500,000 | 11.65% | 36mo | ₹16,524 | ₹99,853 |  |
| 2 | ICICI | ₹500,000 | 13.12% | 36mo | ₹16,876 | ₹120,032 |  |
| 3 | BOB | ₹500,000 | 13.90% | 36mo | ₹17,064 | ₹124,298 |  |
| 4 | AXIS | ₹500,000 | 15.50% | 36mo | ₹17,454 | ₹138,348 |  |
| 5 | YESBANK | ₹500,000 | 15.93% | 36mo | ₹17,560 | ₹144,660 |  |
| 6 | POONAWALLA | ₹500,000 | 15.33% | 36mo | ₹17,414 | ₹146,889 | near-tie with YESBANK (within 2% cost) - YESBANK is private_bank, this is nbfc; ranking is on cost only, this is a comment, not a bias. |
| 7 | FEDERAL | ₹500,000 | 15.99% | 36mo | ₹17,576 | ₹147,738 | near-tie with POONAWALLA (within 2% cost) - POONAWALLA is nbfc, this is private_bank; ranking is on cost only, this is a comment, not a bias. |
| 8 | LTFIN | ₹500,000 | 17.25% | 36mo | ₹17,889 | ₹158,991 |  |
| 9 | Fibe | ₹500,000 | 18.00% | 36mo | ₹18,076 | ₹160,743 | near-tie with LTFIN (within 2% cost) - LTFIN is nbfc, this is fintech; ranking is on cost only, this is a comment, not a bias. |
| 10 | HDFC | ₹500,000 | 17.77% | 36mo | ₹18,019 | ₹168,698 |  |
| 11 | BAJAJ | ₹500,000 | 18.20% | 36mo | ₹18,126 | ₹173,200 |  |
| 12 | KREDITBEE | ₹500,000 | 18.74% | 36mo | ₹18,262 | ₹182,437 |  |
| 13 | KOTAK | ₹500,000 | 20.33% | 36mo | ₹18,666 | ₹196,975 | amount formula is calculator-inferred (reverse-engineered, not published): 20.0x disposable income |
| 14 | INDUSIND | ₹500,000 | 21.97% | 36mo | ₹19,087 | ₹197,116 |  |
| 15 | IDFC | ₹500,000 | 25.21% | 36mo | ₹19,934 | ₹235,137 | amount formula is calculator-inferred (reverse-engineered, not published): 10.0x disposable income |
| 16 | HDBFS | ₹500,000 | 27.33% | 36mo | ₹20,502 | ₹263,077 |  |
| 17 | TATACAP | ₹500,000 | 30.42% | 36mo | ₹21,342 | ₹293,317 |  |

**Rejected:**

- **SBI**: requires_salary_account failed: applicant's salary account is with no bank, not SBI.
- **HSBC**: requires_salary_account failed: applicant's salary account is with no bank, not HSBC.
- **UNION**: requires_salary_account failed: applicant's salary account is with no bank, not UNION.

## P10_small_requested_amount_below_min_loan
Requests a very small amount - tests the 'eligible amount below product min_loan' rejection path at the end of Stage 2.

**Eligible at 17/20 lenders.**

| Rank | Lender | Offered Amt | Rate | Tenure | EMI | Total Cost | Flags |
|---|---|---|---|---|---|---|---|
| 1 | PNB | ₹20,000 | 12.05% | 12mo | ₹1,777 | ₹1,529 |  |
| 2 | ICICI | ₹20,000 | 14.69% | 12mo | ₹1,802 | ₹2,126 |  |
| 3 | Fibe | ₹20,000 | 18.00% | 12mo | ₹1,834 | ₹2,403 |  |
| 4 | AXIS | ₹20,000 | 18.25% | 12mo | ₹1,836 | ₹2,431 | near-tie with Fibe (within 2% cost) - Fibe is fintech, this is private_bank; ranking is on cost only, this is a comment, not a bias. |
| 5 | YESBANK | ₹20,000 | 18.46% | 12mo | ₹1,838 | ₹2,556 |  |
| 6 | FEDERAL | ₹20,000 | 17.99% | 12mo | ₹1,834 | ₹2,602 |  |
| 7 | POONAWALLA | ₹20,000 | 18.00% | 12mo | ₹1,834 | ₹2,803 |  |
| 8 | LTFIN | ₹20,000 | 20.62% | 12mo | ₹1,859 | ₹2,904 |  |
| 9 | HDFC | ₹20,000 | 21.66% | 12mo | ₹1,869 | ₹3,224 |  |
| 10 | BAJAJ | ₹20,000 | 22.30% | 12mo | ₹1,875 | ₹3,323 |  |
| 11 | KREDITBEE | ₹20,000 | 22.11% | 12mo | ₹1,873 | ₹3,475 |  |
| 12 | INDUSIND | ₹20,000 | 27.70% | 12mo | ₹1,927 | ₹3,527 | near-tie with KREDITBEE (within 2% cost) - KREDITBEE is fintech, this is private_bank; ranking is on cost only, this is a comment, not a bias. |
| 13 | KOTAK | ₹20,000 | 25.00% | 12mo | ₹1,901 | ₹3,811 | amount formula is calculator-inferred (reverse-engineered, not published): 20.0x disposable income |
| 14 | IDFC | ₹20,000 | 32.31% | 12mo | ₹1,973 | ₹4,371 | amount formula is calculator-inferred (reverse-engineered, not published): 10.0x disposable income |
| 15 | HDBFS | ₹20,000 | 36.00% | 12mo | ₹2,009 | ₹5,111 |  |
| 16 | BOB | ₹20,000 | 15.52% | 36mo | ₹698 | ₹5,543 |  |
| 17 | TATACAP | ₹20,000 | 40.14% | 12mo | ₹2,051 | ₹5,610 | near-tie with BOB (within 2% cost) - BOB is psu_bank, this is nbfc; ranking is on cost only, this is a comment, not a bias. |

**Rejected:**

- **SBI**: requires_salary_account failed: applicant's salary account is with no bank, not SBI.
- **HSBC**: requires_salary_account failed: applicant's salary account is with no bank, not HSBC.
- **UNION**: requires_salary_account failed: applicant's salary account is with no bank, not UNION.

## P11_fintech_quick_small_loan
Profile shaped for fintech/NBFC digital lenders (Fibe, KreditBee) - modest income, short tenure request.

**Eligible at 2/20 lenders.**

| Rank | Lender | Offered Amt | Rate | Tenure | EMI | Total Cost | Flags |
|---|---|---|---|---|---|---|---|
| 1 | KREDITBEE | ₹80,000 | 24.80% | 12mo | ₹7,596 | ₹15,151 |  |
| 2 | IDFC | ₹80,000 | 38.00% | 12mo | ₹8,117 | ₹20,206 | amount formula is calculator-inferred (reverse-engineered, not published): 10.0x disposable income |

**Rejected:**

- **SBI**: min_current_job_months failed: applicant=8, lender requires >= 12.0
- **HDFC**: min_total_exp_months failed: applicant=14, lender requires >= 24.0
- **ICICI**: min_total_exp_months failed: applicant=14, lender requires >= 24.0
- **AXIS**: min_current_job_months failed: applicant=8, lender requires >= 12.0
- **KOTAK**: min_current_job_months failed: applicant=8, lender requires >= 12.0
- **INDUSIND**: min_total_exp_months failed: applicant=14, lender requires >= 24.0
- **HSBC**: requires_salary_account failed: applicant's salary account is with no bank, not HSBC.
- **FEDERAL**: min_total_exp_months failed: applicant=14, lender requires >= 36.0
- **BOB**: min_current_job_months failed: applicant=8, lender requires >= 12.0
- **PNB**: min_total_exp_months failed: applicant=14, lender requires >= 24.0
- **UNION**: min_total_exp_months failed: applicant=14, lender requires >= 24.0
- **YESBANK**: min_current_job_months failed: applicant=8, lender requires >= 12.0
- **BAJAJ**: min_total_exp_months failed: applicant=14, lender requires >= 24.0
- **TATACAP**: min_total_exp_months failed: applicant=14, lender requires >= 24.0
- **HDBFS**: min_current_job_months failed: applicant=8, lender requires >= 12.0
- **POONAWALLA**: min_income failed: applicant=28000, lender requires >= 30000.0
- **LTFIN**: min_current_job_months failed: applicant=8, lender requires >= 12.0
- **Fibe**: min_total_exp_months failed: applicant=14, lender requires >= 24.0