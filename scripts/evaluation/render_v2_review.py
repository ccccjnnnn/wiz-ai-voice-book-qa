"""Render the candidate V2 JSON as a compact, human-reviewable Markdown file."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "eval" / "v2" / "candidates.json"
OUTPUT = ROOT / "eval" / "v2" / "review" / "OWNER_GROUND_TRUTH_REVIEW.md"


def block(text: str | None) -> str:
    return "_Not available._" if text is None else f"```text\n{text.rstrip()}\n```"


def main() -> None:
    payload = json.loads(DATASET.read_text(encoding="utf-8"))
    cases = payload["cases"]
    lines = [
        "# Evaluation V2 — Owner Ground-Truth Review",
        "",
        "> **CANDIDATE ONLY. Codex-generated annotation is not golden ground truth.**",
        "> No case in this file has been run through production retrieval or QA. The dataset becomes",
        "> `owner_reviewed` and later `frozen` only after the project owner checks the original text.",
        "",
        "## Review minimum",
        "",
        "For every case, verify the proposed status and reference answer. For answered cases, check each",
        "claim against its exact span and preceding/following text. For no-answer cases, inspect every",
        "plausible whole-document match. Edit or reject any case whose wording, context, or search coverage",
        "is not defensible. Do not approve a split as a batch based only on counts.",
        "",
        "## Summary",
        "",
        f"- Total candidates: **{len(cases)}**",
        f"- Lifecycle: **{payload['lifecycle_status']}**",
        f"- Human verified: **{str(payload['human_verified']).lower()}**",
        "- Retrieval/QA executed: **no**",
        f"- Fact families: **{len({c['fact_family_id'] for c in cases})}**",
        f"- Replaced TEST cases: **{len(payload['audit_state']['cases_replaced'])}**",
        "",
        "### By proposed split",
        "",
        "| Split | Count |",
        "|---|---:|",
    ]
    for key, value in Counter(c["split_candidate"] for c in cases).items(): lines.append(f"| `{key}` | {value} |")
    lines += ["", "### By category", "", "| Category | Count |", "|---|---:|"]
    for key, value in Counter(c["primary_category"] for c in cases).items(): lines.append(f"| `{key}` | {value} |")
    lines += ["", "### By status / book / difficulty", "", "| Dimension | Value | Count |", "|---|---|---:|"]
    for dimension in ("expected_status", "source_book", "difficulty"):
        for key, value in Counter(c[dimension] for c in cases).items(): lines.append(f"| {dimension} | `{key}` | {value} |")
    for key, value in Counter(c["review_tier"] for c in cases).items(): lines.append(f"| review_tier | `{key}` | {value} |")
    lines += [
        "", "### Repair audit", "",
        "- Removed TEST IDs: " + ", ".join(f"`{x}`" for x in payload["audit_state"]["cases_replaced"]),
        "- Replacement TEST IDs: " + ", ".join(f"`{x}`" for x in payload["audit_state"]["replacement_case_ids"]),
        "- Cases moved between splits: **none**",
        "- Annotation/category/negative/ambiguity repairs: " + ", ".join(
            f"`{x}`" for x in payload["audit_state"]["annotation_repair_case_ids"]
        ),
        "- Evidence context repackaged: **all 100 cases**",
        "- Rejected Astra semantic findings and source reasoning: see `AUDIT_REPAIR_LOG.md`",
        "",
    ]
    attention=[c for c in cases if c["requires_owner_attention"]]
    blocked=[c for c in cases if c['review_tier']=='BLOCKED']
    lines += [
        "", "### Needs owner attention", "",
        "Every case requires an owner decision before freeze. All TEST and holdout cases are explicitly flagged for full review.",
        "",
        f"{len(attention)} cases carry the explicit attention flag: " + ", ".join(f"`{c['case_id']}`" for c in attention),
        "",
        f"Unresolved BLOCKED cases: **{len(blocked)}**" + ((": " + ", ".join(f"`{c['case_id']}`" for c in blocked)) if blocked else "."),
        "",
    ]
    lines += ["## Index by category", ""]
    grouped=defaultdict(list)
    for c in cases: grouped[c['primary_category']].append(c)
    for cat, vals in grouped.items(): lines.append(f"- **{cat}:** " + ", ".join(f"`{c['case_id']}`" for c in vals))
    lines += ["", "## Index by proposed split", ""]
    for split in ("alice_dev_regression", "alice_final_test", "secret_garden_holdout"):
        vals=[c for c in cases if c['split_candidate']==split]
        lines.append(f"- **{split}:** " + ", ".join(f"`{c['case_id']}`" for c in vals))

    for split in ("alice_dev_regression", "alice_final_test", "secret_garden_holdout"):
        lines += ["", f"# {split}", ""]
        for c in [x for x in cases if x['split_candidate']==split]:
            flags=[]
            if c['historical_case']: flags.append('historical')
            if c['requires_owner_attention']: flags.append('needs owner attention')
            label=f" — {', '.join(flags)}" if flags else ''
            lines += [
                f"<details>",
                f"<summary><strong>{c['case_id']}</strong> · {c['primary_category']} · {c['expected_status']} · {c['review_tier']}{label}</summary>",
                "",
                f"**Question:** {c['question']}",
                "",
                f"**Proposed status:** `{c['expected_status']}`",
                "",
                f"**Proposed reference answer:** {c['reference_answer']}",
                "",
                f"**Book / difficulty:** `{c['source_book']}` / `{c['difficulty']}`",
                "",
                f"**Fact family:** `{c['fact_family_id']}`",
                "",
                f"**Evidence event:** `{c['evidence_event_id']}`",
                "",
                f"**Development exposure:** `{c['development_exposure']['status']}`",
                "",
                f"**Exposure review:** {c['development_exposure']['review_method']}",
                "",
                f"**Metamorphic / contrastive group:** `{c['metamorphic_pair_id'] or 'none'}` / `{c['contrastive_pair_id'] or 'none'}`",
                "",
                f"**Related cases:** {', '.join(f'`{item}`' for item in c['related_case_ids']) or '_none_'}",
                "",
                f"**Tags:** {', '.join(f'`{tag}`' for tag in c['tags']) or '_none_'}",
                "",
            ]
            if c['required_answer_claims']:
                by_id={e['evidence_id']:e for e in c['valid_evidence_locations']}
                lines += ["### Required claims and original context", ""]
                for claim in c['required_answer_claims']:
                    lines += [f"#### {claim['claim_id']}: {claim['claim_text']}", ""]
                    for ref in claim['evidence_ids']:
                        e=by_id[ref]
                        lines += [
                            f"**Evidence {ref} location:** `{json.dumps(e['source_location'], ensure_ascii=False)}`",
                            "", "**Exact supporting span:**", "", block(e['exact_supporting_span']), "",
                            "**Preceding context:**", "", block(e['preceding_context']), "",
                            "**Supporting paragraph/context:**", "", block(e['supporting_context']), "",
                            "**Following context:**", "", block(e['following_context']), "",
                            f"**Context incomplete:** `{str(e['context_incomplete']).lower()}`", "",
                            f"**Why it supports this claim:** {e['why_supports']}", "",
                        ]
            if c['negative_verification']:
                n=c['negative_verification']; lines += [
                    "### Whole-document negative verification", "",
                    f"**Scope:** {n['verification_scope']}", "",
                    f"**Entity aliases:** {', '.join(f'`{x}`' for x in n['entity_aliases'])}", "",
                    f"**Negative terms:** {', '.join(f'`{x}`' for x in n['negative_search_terms'])}", "",
                    f"**Relation variants:** {', '.join(f'`{x}`' for x in n['relation_variants'])}", "",
                    f"**Morphological variants:** {', '.join(f'`{x}`' for x in n['morphological_variants'])}", "",
                    f"**Semantic variants:** {', '.join(f'`{x}`' for x in n['semantic_variants'])}", "",
                    f"**Plausible counterexamples:** {', '.join(f'`{x}`' for x in n['plausible_counterexamples']) or '_none_'}", "",
                    f"**Counterexample disposition:** {n['counterexample_disposition']}", "",
                ]
                for item in n['searches']:
                    lines += [f"#### Search: `{item['query']}`", "", f"- Pattern: `{item['pattern']}`", f"- All matches reviewed: `{str(item['all_matches_reviewed']).lower()}`", f"- Assessment: {item['semantic_assessment']}", ""]
                    source=item['canonical_or_parsed_source_matches']; lines.append(f"Source matches ({len(source)}):")
                    lines += [f"- {m['location']}: {m['excerpt']}" for m in source] or ['- none']
                    if item['generated_pdf_matches'] is not None:
                        pdf=item['generated_pdf_matches']; lines.append(f"Generated-PDF matches ({len(pdf)}):"); lines += [f"- {m['location']}: {m['excerpt']}" for m in pdf] or ['- none']
                    lines.append('')
                lines += [f"**Bounded conclusion:** {n['conclusion']}. This is not mathematical proof of absence.", ""]
            if c['ambiguity_rationale']:
                lines += ["### Ambiguity rationale", "", f"**Type:** `{c['ambiguity_type']}`", "", c['ambiguity_rationale'], "", f"**Minimal clarification:** {c['expected_clarification']}", ""]
                for e in c['valid_evidence_locations']:
                    lines += [f"**Plausible referent {e['evidence_id']} — `{json.dumps(e['source_location'], ensure_ascii=False)}`**", "", block(e['supporting_context']), ""]
            lines += [f"**Codex annotation notes:** {c['annotation_notes'] or '_none_'}", "", f"**Annotation confidence / review tier:** `{c['annotation_confidence']}` / `{c['review_tier']}`", "", "Owner ground-truth decision:  ", "[ ] APPROVE  ", "[ ] EDIT  ", "[ ] REJECT  ", "", "Owner note:", "", "</details>", ""]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines).rstrip()+"\n", encoding="utf-8")
    print(f"rendered {len(cases)} cases to {OUTPUT}")


if __name__ == "__main__":
    main()
