#!/usr/bin/env python3
"""Checkpoint C targeted evaluation-data cleanup.

Scope:
- bounded negative-verification metadata
- ambiguity validity/metadata
- category inflation
- evidence epistemic labels for touched cases
- claim-level exact spans for at110
- related-case / shared-event links called out by audit

No provider calls. No retrieval/QA execution. Idempotent field overwrites.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "eval/v2/candidates.json"
AUDIT_LOG = ROOT / "eval/v2/review/AUDIT_REPAIR_LOG.md"


def get_case(by_id: dict[str, dict], cid: str) -> dict:
    if cid not in by_id:
        raise KeyError(f"missing case: {cid}")
    return by_id[cid]


def get_ev(case: dict, eid: str) -> dict:
    for ev in case.get("valid_evidence_locations", []):
        if ev.get("evidence_id") == eid:
            return ev
    raise KeyError(f"{case['case_id']}: missing evidence {eid}")


def sync(case: dict) -> None:
    case["exact_supporting_spans"] = [
        ev["exact_supporting_span"] for ev in case.get("valid_evidence_locations", [])
    ]
    case["local_surrounding_context"] = [
        {
            "evidence_id": ev["evidence_id"],
            "preceding": ev.get("preceding_context", ""),
            "supporting": ev.get("supporting_context", ""),
            "following": ev.get("following_context", ""),
            "context_incomplete": ev.get("context_incomplete", False),
        }
        for ev in case.get("valid_evidence_locations", [])
    ]


def add_related(case: dict, other: str) -> None:
    values = set(case.get("related_case_ids", []))
    values.add(other)
    case["related_case_ids"] = sorted(values)


def append_note(case: dict, note: str) -> None:
    old = (case.get("annotation_notes") or "").strip()
    if note not in old:
        case["annotation_notes"] = (old + (" " if old else "") + note).strip()


def main() -> None:
    payload = json.loads(DATASET.read_text(encoding="utf-8"))
    by_id = {c["case_id"]: c for c in payload["cases"]}

    required = {
        "c001", "c002", "av048", "at075", "sg096", "sg097",
        "av050", "av051", "av052", "av053", "sg098", "sg099",
        "q016", "q024", "q027", "q030", "at106", "at110",
        "av039", "av037", "av057", "q018", "q023", "q028",
    }
    missing = sorted(required - set(by_id))
    if missing:
        raise SystemExit(f"STOP: missing required cases: {missing}")

    # ------------------------------------------------------------------
    # Negative verification: keep bounded conclusions; remove stale
    # generated-PDF excerpts from Secret Garden cases because the canonical
    # Gutenberg text is semantic truth and current PDF coverage is tracked
    # separately in source_consistency_report.json.
    # ------------------------------------------------------------------
    bounded_note = (
        "Negative verification is bounded whole-document review, not mathematical proof of absence; "
        "absolute_absence_claimed remains false."
    )
    for cid in ("c001", "c002", "av048", "at075"):
        c = get_case(by_id, cid)
        append_note(c, bounded_note)
        c["review_tier"] = "DEEP_REVIEW"
        c["requires_owner_attention"] = True

    for cid in ("sg096", "sg097"):
        c = get_case(by_id, cid)
        nv = c["negative_verification"]
        nv["verification_scope"] = (
            "Project Gutenberg eBook #113 canonical body is semantic ground truth; "
            "generated text-layer PDF parser coverage is validated separately by "
            "eval/v2/sources/source_consistency_report.json"
        )
        for search in nv.get("searches", []):
            search["generated_pdf_matches"] = None
        append_note(
            c,
            "Generated-PDF search excerpts are intentionally not embedded in this case because the PDF is "
            "coverage-only and rebuild-specific; current PDF hash/token coverage lives in the source consistency report."
        )
        append_note(c, bounded_note)
        c["review_tier"] = "DEEP_REVIEW"
        c["requires_owner_attention"] = True

    # ------------------------------------------------------------------
    # Ambiguity cases.
    # ------------------------------------------------------------------
    c = get_case(by_id, "av050")
    get_ev(c, "E2")["epistemic_status"] = "narrator_fact"
    append_note(c, "Both candidate interpretations are distinct book events; mushroom-size change is narrator-described.")
    sync(c)

    c = get_case(by_id, "av051")
    for eid in ("A1", "A2"):
        get_ev(c, eid)["epistemic_status"] = "narrator_fact"
    append_note(c, "The anger labels are narrator descriptions attached to two different tea-party moments.")
    sync(c)

    # av052 had duplicate evidence for the same Rabbit departure. Do not preserve
    # artificial ambiguity merely to hit a category quota: convert it into a
    # grounded local-context answered case using the evidence actually packaged.
    c = get_case(by_id, "av052")
    a1 = get_ev(c, "A1")
    original_departure = a1["supporting_context"]
    original_after = a1["following_context"]
    c["question"] = "What did Alice do after the White Rabbit dropped his gloves and fan and ran away?"
    c["expected_status"] = "answered"
    c["reference_answer"] = (
        "She picked up the fan and gloves, kept fanning herself, and began wondering whether she had changed."
    )
    c["required_answer_claims"] = [
        {
            "claim_id": "C1",
            "claim_text": "Alice picked up the fan and gloves.",
            "evidence_ids": ["A1"],
        },
        {
            "claim_id": "C2",
            "claim_text": "She fanned herself and wondered whether she had changed.",
            "evidence_ids": ["A1"],
        },
    ]
    a1["preceding_context"] = original_departure
    a1["supporting_context"] = original_after
    a1["following_context"] = ""
    a1["exact_supporting_span"] = "Alice took up the fan and gloves"
    a1["why_supports"] = (
        "The narrator states what Alice did immediately after the Rabbit fled: she picked up the fan and gloves, "
        "fanned herself, and started questioning whether she had changed."
    )
    a1["epistemic_status"] = "narrator_fact"
    c["valid_evidence_locations"] = [a1]
    c["primary_category"] = "local_context_reasoning"
    c["category"] = "local_context_reasoning"
    c["tags"] = ["sequence_context"]
    c["ambiguity_rationale"] = None
    c["expected_clarification"] = None
    c["ambiguity_type"] = None
    c["plausible_referents"] = []
    c["annotation_notes"] = (
        "Former ambiguity candidate repaired: prior A1/A2 duplicated the same Rabbit departure, so the case is now "
        "an answered local-context sequence rather than artificial ambiguity."
    )
    c["annotation_confidence"] = "medium"
    c["review_tier"] = "DEEP_REVIEW"
    c["requires_owner_attention"] = True
    sync(c)

    c = get_case(by_id, "av053")
    c["plausible_referents"] = [
        "the three card gardeners at the croquet ground",
        "the whole pack of cards at the end of the trial",
    ]
    c["ambiguity_rationale"] = (
        "‘The cards’ can refer to the card gardeners in the croquet-ground scene or the whole pack that later flies at Alice."
    )
    c["expected_clarification"] = (
        "Do you mean the card gardeners at the croquet ground or the whole pack at the end of the trial?"
    )
    append_note(c, "Stale garden-related plausible_referents metadata was replaced with the two card referents actually evidenced.")
    sync(c)

    # sg098: keep the ambiguity category, but repair the question so the two
    # retained passages really are competing interpretations. Drop A1 (generic
    # closed rooms) and use ivy-vs-curtain uncovering events.
    c = get_case(by_id, "sg098")
    a2 = get_ev(c, "A2")
    a3 = get_ev(c, "A3")
    c["question"] = "What did Mary see when a covering moved aside?"
    c["reference_answer"] = (
        "Clarification is required: moving ivy exposed a door knob, while drawing back the silk curtain uncovered a picture of Colin’s mother."
    )
    a2["why_supports"] = "In one scene, moving ivy reveals the knob of a hidden door."
    a3["why_supports"] = "In another scene, drawing back a silk curtain reveals a portrait of Colin’s mother."
    a2["epistemic_status"] = "narrator_fact"
    a3["epistemic_status"] = "narrator_fact"
    c["valid_evidence_locations"] = [a2, a3]
    c["ambiguity_rationale"] = (
        "Two separate scenes involve a covering moving aside: ivy reveals a door knob, while a silk curtain reveals a portrait."
    )
    c["expected_clarification"] = "Do you mean the ivy in the garden or the silk curtain in Colin’s room?"
    c["plausible_referents"] = [
        "ivy moving aside and revealing a door knob",
        "the silk curtain drawing back and revealing Colin’s mother’s portrait",
    ]
    c["annotation_notes"] = (
        "Repaired ambiguity: the former version incorrectly treated a curtain/portrait passage as a door discovery. "
        "The new wording is supported by two genuinely distinct uncovering events."
    )
    c["annotation_confidence"] = "medium"
    c["review_tier"] = "DEEP_REVIEW"
    c["requires_owner_attention"] = True
    sync(c)

    c = get_case(by_id, "sg099")
    get_ev(c, "A1")["epistemic_status"] = "character_statement"
    get_ev(c, "A2")["epistemic_status"] = "narrator_fact"
    get_ev(c, "A3")["epistemic_status"] = "character_statement"
    get_ev(c, "A1")["why_supports"] = "Colin himself expresses distress about his mother’s death and his father’s reaction to him."
    get_ev(c, "A2")["why_supports"] = "Narration and dialogue show a separate angry quarrel between Colin and Mary."
    get_ev(c, "A3")["why_supports"] = "Mary reports Colin’s separate fear that he might develop a lump/hunchback."
    append_note(c, "Speech-vs-narration epistemic labels were separated for the three distinct upset scenes.")
    sync(c)

    # ------------------------------------------------------------------
    # Category inflation / evidence semantics.
    # ------------------------------------------------------------------
    for cid in ("q016", "q027", "at106"):
        c = get_case(by_id, cid)
        c["primary_category"] = "multi_fact_single_context"
        c["category"] = "multi_fact_single_context"
        append_note(c, "Reclassified from multi-source: the answer components belong to one continuous local event/context.")

    c = get_case(by_id, "q024")
    c["primary_category"] = "multi_fact_single_context"
    c["category"] = "multi_fact_single_context"
    for eid in ("E1", "E2", "E3"):
        get_ev(c, eid)["epistemic_status"] = "narrator_fact"
    append_note(c, "All three croquet-equipment facts occur in the same narrator sentence; this is not multi-source evidence.")
    sync(c)

    c = get_case(by_id, "q030")
    c["primary_category"] = "direct_factual_single_source"
    c["category"] = "direct_factual_single_source"
    c["tags"] = sorted(set(c.get("tags", [])) | {"rule_content", "character_statement"})
    get_ev(c, "E1")["epistemic_status"] = "character_statement"
    c["annotation_notes"] = (
        "Direct question about the content of the King’s stated Rule Forty-two. It is not a contrastive item; "
        "the evidence establishes what the King read out, not the legitimacy of the rule."
    )
    c["annotation_confidence"] = "high"
    sync(c)

    # at110 exact spans should contain the competing propositions, not merely
    # speaker labels/fragments. The claims remain about each side's position.
    c = get_case(by_id, "at110")
    e1 = get_ev(c, "E1")
    e2 = get_ev(c, "E2")
    e1["exact_supporting_span"] = "you couldn’t cut oﬀa head unless there was a body to cut it oﬀfrom"
    e2["exact_supporting_span"] = "anything that had a head could be be- headed"
    e1["epistemic_status"] = "narrator_fact"
    e2["epistemic_status"] = "narrator_fact"
    e1["why_supports"] = "The narrator reports the executioner’s position that beheading requires a body."
    e2["why_supports"] = "The narrator reports the King’s opposing position that having a head is sufficient for beheading."
    c["annotation_notes"] = (
        "Competing propositions from two sides remain distinct. Exact spans now contain the propositions themselves; "
        "epistemic status records that narration reports each argument, not that either argument is objectively true."
    )
    sync(c)

    # ------------------------------------------------------------------
    # Related-case / shared-event links. Keep distinct fact-family IDs where
    # the target claim differs, but stop treating same-event cases as unrelated.
    # ------------------------------------------------------------------
    pairs = [
        ("q018", "av039", "event_alice_pigeon_serpent_reasoning"),
        ("q023", "av037", "event_alice_hatter_time_quarrel"),
        ("q028", "av057", "event_alice_tart_trial_opening"),
    ]
    for left, right, event_id in pairs:
        lc = get_case(by_id, left)
        rc = get_case(by_id, right)
        add_related(lc, right)
        add_related(rc, left)
        lc["evidence_event_id"] = event_id
        rc["evidence_event_id"] = event_id
        append_note(lc, f"Linked to {right}: distinct target claim, shared source event; fact-family IDs are not independent-event counts.")
        append_note(rc, f"Linked to {left}: distinct target claim, shared source event; fact-family IDs are not independent-event counts.")

    # av039 E2 is Pigeon dialogue, not narrator-established truth.
    get_ev(get_case(by_id, "av039"), "E2")["epistemic_status"] = "character_statement"
    sync(get_case(by_id, "av039"))

    payload.setdefault("audit_state", {})["checkpoint_c_cleanup"] = {
        "negative_verification_reviewed": ["c001", "c002", "av048", "at075", "sg096", "sg097"],
        "ambiguity_reviewed": ["av050", "av051", "av052", "av053", "sg098", "sg099"],
        "category_cleanup": ["q016", "q024", "q027", "q030", "at106"],
        "exact_span_cleanup": ["at110"],
        "shared_event_links": [
            ["q018", "av039"],
            ["q023", "av037"],
            ["q028", "av057"],
        ],
        "source_policy": (
            "Secret Garden canonical Gutenberg text is semantic ground truth; generated PDF is parser-coverage validation only."
        ),
        "remaining_non_dataset_followups": [
            "q014/q015 family-semantics wording was not included in CHECKPOINT_C_PACK and remains a final delta-review item",
            "historical audit-log person/page wording should be checked in the final small delta pack rather than treated as dataset ground truth",
        ],
    }

    # ---------------------------- targeted assertions ----------------------------
    assert len(payload["cases"]) == 100
    assert get_case(by_id, "av052")["expected_status"] == "answered"
    assert len(get_case(by_id, "av052")["valid_evidence_locations"]) == 1
    assert get_case(by_id, "av053")["plausible_referents"] == [
        "the three card gardeners at the croquet ground",
        "the whole pack of cards at the end of the trial",
    ]
    assert [e["evidence_id"] for e in get_case(by_id, "sg098")["valid_evidence_locations"]] == ["A2", "A3"]
    for cid in ("q016", "q024", "q027", "at106"):
        assert get_case(by_id, cid)["category"] == "multi_fact_single_context"
    assert get_case(by_id, "q030")["category"] == "direct_factual_single_source"
    for cid in ("sg096", "sg097"):
        for search in get_case(by_id, cid)["negative_verification"]["searches"]:
            assert search.get("generated_pdf_matches") is None
    for left, right, event_id in pairs:
        assert right in get_case(by_id, left)["related_case_ids"]
        assert left in get_case(by_id, right)["related_case_ids"]
        assert get_case(by_id, left)["evidence_event_id"] == event_id
        assert get_case(by_id, right)["evidence_event_id"] == event_id

    DATASET.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    section = """\
<!-- CHECKPOINT_C_CLEANUP_START -->
## Checkpoint C — negative / ambiguity / provenance / metadata cleanup

- Bounded negative verification retained for `c001`, `c002`, `av048`, `at075`, `sg096`, `sg097`; absolute absence is not claimed.
- Secret Garden negative cases now rely on canonical Gutenberg text for semantics; rebuild-specific generated-PDF match excerpts are not embedded in case annotations. Current PDF coverage/hash remains in `source_consistency_report.json`.
- `av052` was not a defensible ambiguity case because both evidence entries duplicated the same Rabbit event; it was converted to a grounded answered local-context case.
- `av053` stale garden-related plausible-referent metadata was corrected to the card gardeners vs whole pack.
- `sg098` was repaired so the ambiguity is ivy/door-knob vs silk-curtain/portrait rather than misusing the portrait scene as a door discovery.
- `av050`, `av051`, `sg099` received speech-vs-narration epistemic cleanup.
- `q016`, `q024`, `q027`, `at106` were reclassified as multi-fact single-context; `q030` is direct factual single-source rather than contrastive.
- `at110` exact spans now contain the competing propositions themselves.
- Same-event relationships are explicit for `q018`↔`av039`, `q023`↔`av037`, `q028`↔`av057`; fact-family count must not be described as a count of independent events.

Remaining non-dataset follow-ups for final delta review: `q014/q015` family-semantics wording and historical audit-log person/page wording.
<!-- CHECKPOINT_C_CLEANUP_END -->
"""
    if AUDIT_LOG.exists():
        text = AUDIT_LOG.read_text(encoding="utf-8")
        start = "<!-- CHECKPOINT_C_CLEANUP_START -->"
        end = "<!-- CHECKPOINT_C_CLEANUP_END -->"
        if start in text and end in text:
            before = text.split(start, 1)[0].rstrip()
            after = text.split(end, 1)[1].lstrip()
            new_text = before + "\n\n" + section.strip() + "\n"
            if after:
                new_text += "\n" + after
        else:
            new_text = text.rstrip() + "\n\n" + section
        AUDIT_LOG.write_text(new_text, encoding="utf-8")

    print("Checkpoint C targeted cleanup applied.")
    print("No providers called. No retrieval/QA executed.")
    print("Targeted assertions: PASS")


if __name__ == "__main__":
    main()
