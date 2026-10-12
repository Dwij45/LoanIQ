"""
Generates docs/data-sources.md and docs/assumptions-and-estimates.md directly
from data/rules.csv, data/lenders.csv, and data/additional_sources.csv, so the
documentation can never drift out of sync with the actual data - re-run this
any time the data changes instead of hand-editing those two files.

Usage: python scripts/gen_docs.py   (run from the repo root)
"""
import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES = list(csv.DictReader(open(ROOT / "data" / "rules.csv", encoding="utf-8")))
LENDERS = list(csv.DictReader(open(ROOT / "data" / "lenders.csv", encoding="utf-8")))
LENDER_NAME = {r["lender_id"]: r["lender_name"] for r in LENDERS}

# Extra links cited in the original research workbook's source_url/notes
# columns that never got attached to a specific rules.csv row - usually
# background pages, cross-checks against a second aggregator, or a fact
# that ended up on a different page than the one used for the actual rule
# value. Kept in their own file (rather than crammed into rules.csv, which
# is one row per RULE, not per citation) so every link from the original
# dataset still shows up here even when it isn't tied to a specific row.
ADDITIONAL_SOURCES_PATH = ROOT / "data" / "additional_sources.csv"
ADDITIONAL_SOURCES = defaultdict(list)
if ADDITIONAL_SOURCES_PATH.exists():
    for r in csv.DictReader(open(ADDITIONAL_SOURCES_PATH, encoding="utf-8")):
        ADDITIONAL_SOURCES[r["lender_id"]].append(r["url"])


def gen_data_sources():
    by_lender = defaultdict(list)
    for r in RULES:
        by_lender[r["lender_id"]].append(r)

    lines = [
        "# Data sources",
        "",
        "Generated from `data/rules.csv` and `data/lenders.csv` by `scripts/gen_docs.py` "
        "- do not hand-edit this file, edit the CSVs and re-run that script instead.",
        "",
        "Every row below is one rule collected for one lender: what field, what value, "
        "where it came from, when it was read, and how confident the collection is in it.",
        "",
        "**Confidence tags used throughout:** `official` (lender's own page, stated as policy), "
        "`faq` (lender's own FAQ/help text, not the main eligibility list), `aggregator` "
        "(a third-party comparison site, used only when the lender's own page was unreadable), "
        "`conflict` (the lender states two different values in two places - the stricter one is kept, "
        "flagged), `calculator_inferred` (reverse-engineered from the lender's own live eligibility "
        "calculator - see `foir-methodology.md`), `not_published` (checked, no source states this), "
        "`assumed` (a last-resort estimate with its basis stated in the note - never silent).",
        "",
    ]

    for lid in sorted(by_lender):
        name = LENDER_NAME.get(lid, lid)
        rows = by_lender[lid]
        rule_urls = sorted(set(r["source_url"] for r in rows if r["source_url"]))
        extra_urls = sorted(u for u in set(ADDITIONAL_SOURCES.get(lid, [])) if u not in rule_urls)
        lines.append(f"## {lid} — {name}\n")
        lines.append(f"Sources cited ({len(rule_urls) + len(extra_urls)}):")
        for u in rule_urls:
            lines.append(f"- {u}")
        if extra_urls:
            lines.append("")
            lines.append("Also cited in the original research (not tied to one specific rule row above "
                         "- background reading, a cross-check against a second site, or a page the fact "
                         "ended up sourced from elsewhere on):")
            for u in extra_urls:
                lines.append(f"- {u}")
        lines.append("")
        lines.append("| Rule | Value | Condition | Confidence | Date | Hard cutoff |")
        lines.append("|---|---|---|---|---|---|")
        for r in rows:
            cond = r["condition"] or "—"
            lines.append(f"| {r['rule_name']} | {r['operator']} {r['value']} {r['unit']} | {cond} | "
                         f"{r['confidence']} | {r['accessed_date']} | {r['is_hard_cutoff']} |")
        notes = [r["notes"] for r in rows if r["notes"]]
        if notes:
            lines.append("\n**Notes:**")
            for n in notes:
                lines.append(f"- {n}")
        lines.append("")

    (ROOT / "docs" / "data-sources.md").write_text("\n".join(lines))
    print("wrote docs/data-sources.md")


def gen_assumptions():
    lines = [
        "# Assumptions and estimates",
        "",
        "Generated from `data/rules.csv` and `data/lenders.csv` by `scripts/gen_docs.py` "
        "- do not hand-edit this file, edit the CSVs and re-run that script instead.",
        "",
        "Every field below was **not** found in any public, official, or aggregator source "
        "after a real search. Each is filled with an explicit estimate and a stated basis "
        "(confidence=`assumed`), or left blank with a stated reason it couldn't be found "
        "(confidence=`not_published`). Neither case is silent - the basis for every number "
        "below is in its note.",
        "",
        "## Estimated values (confidence = assumed)",
        "",
    ]
    assumed = [r for r in RULES if r["confidence"] == "assumed"]
    if assumed:
        lines.append("| Lender | Field | Value | Basis |")
        lines.append("|---|---|---|---|")
        for r in assumed:
            lines.append(f"| {r['lender_id']} | {r['rule_name']} | {r['value']} {r['unit']} | {r['notes'] or '—'} |")
    else:
        lines.append("_None in rules.csv._")
    lines.append("")

    lines.append("## Genuinely unresearchable fields (left blank, confidence = not_published)")
    lines.append("")
    lines.append("These are documented gaps, not oversights - each was searched and the "
                 "search is recorded, rather than guessing a number with no basis at all.")
    lines.append("")
    not_pub = [r for r in RULES if r["confidence"] == "not_published"]
    if not_pub:
        lines.append("| Lender | Field | Why it's missing |")
        lines.append("|---|---|---|")
        for r in not_pub:
            lines.append(f"| {r['lender_id']} | {r['rule_name']} | {r['notes'] or '—'} |")
    lines.append("")
    lines.append("_Additional per-field `not_published`/N/A notes also live in the `notes` "
                 "column of the main workbook (`personal_loan_rules_20_lenders_v2.xlsx`) for "
                 "fields that are blank in the wide table rather than rows in `rules.csv` - "
                 "e.g. HSBC's missing income floor, Union Bank's missing `min_loan`.")
    lines.append("")

    lines.append("## Calculator-inferred formulas (not published by the lender, reverse-engineered)")
    lines.append("")
    calc = [r for r in RULES if r["confidence"] == "calculator_inferred"]
    if calc:
        lines.append("| Lender | Rule | Value | How it was derived |")
        lines.append("|---|---|---|---|")
        for r in calc:
            lines.append(f"| {r['lender_id']} | {r['rule_name']} | {r['value']} | {r['notes'] or '—'} |")
    lines.append("\nSee `docs/foir-methodology.md` for the full reverse-engineering method.")

    (ROOT / "docs" / "assumptions-and-estimates.md").write_text("\n".join(lines))
    print("wrote docs/assumptions-and-estimates.md")


if __name__ == "__main__":
    gen_data_sources()
    gen_assumptions()
