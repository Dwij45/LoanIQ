# Insights

Synthetic grid: 1800 profiles x 20 lenders = 36000 evaluations.


## 1. Hard-gate rejection Pareto

What's actually blocking applicants, ranked by frequency:

| Rejection category | Count | Share |
|---|---|---|
| Credit Score / Bureau Cutoff | 12180 | 46.7% |
| Age Bounds | 6300 | 24.2% |
| Salary Account | 2880 | 11.0% |
| FOIR / Capacity | 2514 | 9.6% |
| Income Floor | 2208 | 8.5% |

## 2. Sector comparison

| Sector | Evaluations | Approval rate | Mean rate | Mean amount | Times best-match |
|---|---|---|---|---|---|
| private_bank | 16200 | 25.5% | 20.05% | ₹389,186 | 264 |
| nbfc | 9000 | 39.9% | 25.03% | ₹399,196 | 450 |
| fintech | 3600 | 32.7% | 19.87% | ₹385,154 | 244 |
| psu_bank | 7200 | 14.2% | 13.03% | ₹407,880 | 418 |

## 3. CIBIL vs assigned-rate spread

| CIBIL | # eligible decisions | Lowest rate | Median rate | Highest rate |
|---|---|---|---|---|
| 650 | 1220 | 12.85% | 21.00% | 45.00% |
| 700 | 1934 | 12.45% | 21.00% | 45.00% |
| 750 | 3382 | 12.05% | 21.66% | 40.14% |
| 820 | 3382 | 11.49% | 16.56% | 26.54% |