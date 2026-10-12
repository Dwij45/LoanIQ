# Schema reference

This is the single source of truth for every table in `data/`: what each
column means, its type, and how the tables connect. If a column here
disagrees with the CSV, the CSV is right and this file is stale — open
an issue against it rather than trusting it blindly.

## How the tables connect

There are three tables and exactly **one real foreign key** between them:

```
lenders.csv  (1 row per lender, 20 rows)
     │
     │  lender_id  (primary key)
     │
     ▼
rules.csv    (many rows per lender, 184 rows)
     │
     │  lender_id  (foreign key → lenders.lender_id)
     │
     ▼
(joined at query time by src/eligibility.py / the JS port in ui/index.html)

input_variables.csv   — NOT linked to the other two tables.
It is a data dictionary describing the applicant-side fields the engine
reads (ApplicantProfile), documented separately because those fields
never appear as rows — they're the inputs rules.csv rows are tested
against, not data about a lender.
```

`lenders.csv` is **wide**: one row per lender, one column per product
fact (rate range, loan size, tenure, fees). `rules.csv` is **long**: one
row per *rule* per lender, because a lender can have anywhere from a
handful to a dozen eligibility conditions, and forcing those into fixed
columns on the wide table would mean either a column per possible rule
(mostly empty) or silently dropping rules that didn't fit. The `rule_id`
column loosely follows `{LENDER_ID}_R{nn}`, but it is not meant to be
parsed — treat it as an opaque identifier.

A lender with **zero** matching rows in `rules.csv` has no collected
eligibility criteria beyond what's implied by its `lenders.csv` row —
this does not happen in the current dataset (every lender has at least
an age and CIBIL rule) but the engine does not assume it can't.

---

## `lenders.csv`

One row per lender. Primary key: `lender_id`.

| Column | Type | What it carries |
|---|---|---|
| `lender_id` | string, short code (e.g. `HDFC`, `LTFIN`) | Primary key. Used as the join key into `rules.csv` and as the dictionary key in both the Python and JS engines (`lenders[lender_id]`). Case matters — the engine does exact-match lookups. |
| `lender_name` | string | Full display name (e.g. "HDFC Bank"). Shown to the end user; never used in any comparison logic. |
| `lender_type` | enum: `psu_bank`, `private_bank`, `nbfc`, `fintech` | Sector classification. Used **only** as a comment on near-ties in the final ranking (see `system-architecture.md`) — it never changes which lender ranks first. |
| `product_variant` | string | Which specific personal-loan product this row describes, when a lender sells more than one (most lenders sell only one relevant product, so this is usually a plain label). |
| `min_loan_inr` | float, INR | Smallest amount the lender will originate. The amount stage rejects an applicant whose computed eligible amount falls below this, even if every other gate passed — a loan too small to be worth originating isn't the same kind of failure as an age or income gate, so it's kept out of `rules.csv` (see "Modeling decisions" in `docs/limitations.md`). |
| `max_loan_inr` | float, INR | Largest amount the lender will originate. The amount stage always caps the computed eligible amount at this ceiling. |
| `min_tenure_months` | float, months | Shortest loan tenure the lender offers. The engine clamps any computed/requested tenure up to at least this. |
| `max_tenure_months` | float, months | Longest loan tenure the lender offers. The engine clamps any computed/requested tenure down to at most this, and it's also the lender's own cap used in `max_age_at_maturity` checks (age at maturity = applicant's age + tenure in years). |
| `rate_min_pct` | float, annual % | Best (lowest) interest rate this lender advertises — paid by an applicant at or above CIBIL 900. One of the two anchors for the CIBIL→rate linear interpolation (see `system-architecture.md`, Stage 3). |
| `rate_max_pct` | float, annual % | Worst (highest) interest rate this lender advertises — paid by an applicant at or below the lender's own `min_cibil` cutoff. The other anchor for the same interpolation. |
| `processing_fee_pct` | float, % of loan amount | One-time fee charged on disbursal. Added straight into `total_cost` for ranking (see Stage 4) — this is exactly why ranking is never done on `rate_min_pct` alone: a lower rate with a high fee can lose to a higher rate with none. |
| `foreclosure_charges_pct` | float, % | Early-repayment penalty, if any. **Collected but not currently used** by the ranking engine — `total_cost` is interest + fee only; foreclosure is ignored unless a future applicant profile explicitly signals prepayment intent (see `docs/limitations.md`). |
| `has_govt_employee_scheme` | bool | Whether this lender runs a separate, usually more favorable, scheme specifically for government employees. Informational; not read by the current engine logic (the actual govt-employee favorable terms, where they exist, are expressed as conditional rows in `rules.csv` via the `condition` column, e.g. `employer_category == 'govt'`). |
| `accessed_date` | date (YYYY-MM-DD) | When this lender's product facts (not its rules — those have their own per-row `accessed_date`) were last read from the source. |
| `main_url` | string, URL | The lender's own personal-loan page this row's product facts were sourced from. |
| `selection_reason` | string | Free-text note on why this lender was included in the 20-lender set (e.g. market share, product category coverage). Documentation only. |

---

## `rules.csv`

One row per rule per lender. No single-column primary key; `rule_id` is
a human-readable label, not a guaranteed-unique database key (treat the
tuple of all columns as the real row identity if you need one).

| Column | Type | What it carries |
|---|---|---|
| `rule_id` | string | Human-readable label, loosely `{LENDER_ID}_R{nn}`. Not parsed by the engine — purely for a human skimming the CSV to find a specific row. |
| `lender_id` | string | **Foreign key → `lenders.lender_id`**. This is the only join between the two tables. |
| `rule_name` | enum, see below | Which eligibility field this row tests. The engine switches behavior per `rule_name` (see `system-architecture.md`). |
| `operator` | enum: `>=`, `<=`, `==`, `*`, `in` | How `value` is compared against the applicant's corresponding field. `*` is special: it doesn't mean "greater than" anything — it marks a **capacity formula** row (`salary_multiple_on_disposable_income`), where `value` is a multiplier, not a threshold. |
| `value` | string (numeric, `True`/`False`, or text depending on `unit`) | The threshold, target, or multiplier. Always stored as plain text in the CSV; the engine parses it per-row based on context (float for `ratio`/`score`/`years`/`months`/`INR/month`, boolean for `bool`, left as a string otherwise). |
| `unit` | enum: `INR/month`, `bool`, `enum`, `months`, `ratio`, `score`, `x (income-obligations)`, `years` | What kind of quantity `value` is. `x (income-obligations)` is unique to the two `salary_multiple_on_disposable_income` rows (IDFC, Kotak) — it means "multiply this many times (income − existing obligations)", not an absolute threshold. |
| `condition` | string, free text or empty | When this row applies. Empty (or the literal word `otherwise`) means "always applies." Non-empty values follow one of a small number of shapes the engine's `_eval_condition()` understands: `field == 'value'`, `field in [a,b]`, `field contains 'value'`. This is how a lender can have two different `min_income` rows (e.g. one for `employer_category == 'govt'`, one for everyone else) without the wide `lenders.csv` needing a column per case. An unrecognized condition shape is treated as **true** (the row is applied) rather than silently skipped — see `system-architecture.md` for why that's the safer default. |
| `source_url` | string, URL | Exactly where this specific rule's value was read. One lender can have several different `source_url` values across its rows if different facts came from different pages (e.g. the lender's own site for most rules, an aggregator for one gap-filled field). |
| `accessed_date` | date (YYYY-MM-DD) | When *this row* was last verified against its source. Independent of `lenders.accessed_date`. |
| `confidence` | enum, see below | How trustworthy this specific value is. This is the column the whole "don't silently estimate" requirement hangs on — see `docs/assumptions-and-estimates.md` for every row not tagged `official`. |
| `is_hard_cutoff` | bool | `True`: failing this rule rejects the applicant outright at this lender. `False`: failing it is recorded as a flag/warning (`Decision.flags`) but does **not** reject — used sparingly, for rules the engine isn't fully confident should be an automatic disqualifier. |
| `notes` | string, free text, often empty | Human-readable justification — required whenever `confidence` is anything other than `official`/`faq` (an assumed value with no note is a bug, not a valid row). For `calculator_inferred` rows, this is where the actual reverse-engineering method and test results live (see `docs/foir-methodology.md`). |

### `rule_name` vocabulary (controlled, 14 values currently used)

| `rule_name` | Meaning | Compared against |
|---|---|---|
| `min_age` | Minimum applicant age to apply | `applicant.age` |
| `max_age_at_apply` | Maximum applicant age *at the time of applying* | `applicant.age` |
| `max_age_at_maturity` | Maximum applicant age *when the loan would finish repaying* | `applicant.age + requested_tenure_months/12` |
| `min_cibil` | Minimum CIBIL bureau score | `applicant.cibil_score` |
| `allows_ntc` | Whether the lender accepts an applicant with **zero** CIBIL history (`cibil_score == 0`) | only evaluated when `applicant.is_ntc` is true — see `system-architecture.md` for why this row would otherwise wrongly reject ordinary applicants |
| `min_income` | Minimum net monthly income | `applicant.net_monthly_income` |
| `min_total_exp_months` | Minimum total career length | `applicant.total_work_exp_months` |
| `min_current_job_months` | Minimum tenure in the current job | `applicant.current_job_months` |
| `requires_salary_account` | Whether the applicant must hold a salary account **with this specific lender** | `applicant.salary_account_bank` compared to *this row's own* `lender_id`, not just "has a salary account anywhere" |
| `requires_existing_customer` | Whether the applicant must already be a customer of this lender | `bool(applicant.existing_customer_of)` |
| `allowed_employment_type` | Which employment types this lender's rules apply to | `applicant.employment_type` |
| `min_education` | Minimum qualification level | not currently modeled — no education field is collected reliably enough to enforce this, so this `rule_name` is reserved but inert |
| `foir_cap` | Maximum Fixed Obligation to Income Ratio the lender allows | drives the amount stage; see `docs/foir-methodology.md` |
| `salary_multiple_on_disposable_income` | A flat multiplier on disposable income, used **instead of** `foir_cap` wherever the lender's own calculator was reverse-engineered to use this formula | drives the amount stage; currently only IDFC and KOTAK |

### `confidence` vocabulary (controlled, 8 values)

| Value | Meaning |
|---|---|
| `official` | Found on the lender's own page, stated as the lender's own policy. |
| `faq` | Found on the lender's own FAQ/help content, not its main eligibility listing — slightly less authoritative than `official` but still the lender's own words. |
| `aggregator` | Found on a third-party comparison site (e.g. BankBazaar, Paisabazaar), used only when the lender's own page was unreadable (usually JS-rendered). |
| `conflict` | The lender states two different values for the same field in two different places; the stricter value is kept, and the conflict is noted. |
| `calculator_inferred` | Reverse-engineered from the lender's own live eligibility calculator by feeding it test inputs and solving for the formula that reproduces every output exactly — not published as text anywhere. See `docs/foir-methodology.md`. |
| `not_published` | Searched for and genuinely not findable — the gap is recorded, not guessed. |
| `assumed` | A last-resort estimate used only when nothing else was findable, with its basis stated in `notes` (e.g. the median of comparable lenders already verified in this dataset). **Never silent** — the engine surfaces a flag in `Decision.flags` whenever a result depends on an `assumed` value. |
| `estimate` | Used by a small number of rows pre-dating the `assumed` tag; functionally identical to `assumed`. (Both are treated the same by the engine's flag logic; kept distinct in the data only for traceability to when each row was written.) |

---

## `input_variables.csv`

A data dictionary, **not** joined to the other two tables — it documents
the fields `ApplicantProfile` exposes, i.e. the inputs that get tested
against `rules.csv` rows, not facts about a lender.

| Column | What it carries |
|---|---|
| `variable` | The field name, matching `ApplicantProfile`'s attribute name in `src/eligibility.py`. |
| `type` | Python/JS type: `int`, `float`, `bool`, `enum`, `text`, `list`. |
| `unit` | Unit of measurement, or `-` if not applicable. |
| `allowed_values` | Valid range or enum options. |
| `source` | Where this value comes from in a real application: `applicant` (self-declared), `document` (verified from an uploaded document), `bureau` (from the credit bureau report), or `derived` (computed from other fields). |
| `evidence` | The specific document/process that would back this field in a real underwriting flow (e.g. "salary slip / ITR÷12", "CIBIL report"). Documentation only — this demo does not verify any of it. |
| `description` | Plain-English meaning. |

Three rows — `is_ntc`, `age_at_maturity`, `foir` — are marked `derived`:
they are never collected directly from the applicant, they're computed
by the engine from other fields (`is_ntc = cibil_score == 0`,
`age_at_maturity = age + requested_tenure_months/12`, `foir =
(existing_emi + new_emi) / net_monthly_income`). They're listed here
because `rules.csv` conditions and rule logic reference them, even
though no CSV row ever stores them directly.
