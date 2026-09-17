"""Apply the final targeted Alice TEST semantic-independence repair.

This script is deliberately narrow: it replaces only the seven Alice TEST
items adjudicated as development-exposed in the second delta audit.  It uses
the local Alice PDF and never calls retrieval, QA, or an external provider.
"""

from __future__ import annotations

import json
from collections import Counter

from repair_v2_candidates import (
    DATASET,
    answered_case,
    claims,
    evidence,
    package_evidence,
    write_manifest,
)


EXPOSED_TEST_IDS = {
    "at101", "at103", "at105", "at107", "at108", "at111", "at116",
}


def replacement_cases() -> list[dict]:
    cases = [
        answered_case(
            "at117",
            "What did Pat claim he was digging for when the White Rabbit called him?",
            "Apples.",
            "direct_factual_single_source",
            "medium",
            [evidence(
                "E1", "alice_in_wonderland", "Digging for apples, yer honour", page=33,
            )],
            claims(("Pat claimed that he was digging for apples.", ["E1"])),
            notes="Replacement TEST fact from a source unit not exposed by DEV evidence or review excerpts.",
        ),
        answered_case(
            "at118",
            "Why did Alice take Bill the Lizard’s pencil, and how did he write afterward?",
            "The pencil squeaked, so Alice took it; Bill then tried to write with one finger, which left no mark.",
            "multi_fact_single_context",
            "hard",
            [evidence(
                "E1", "alice_in_wonderland", "One of the jurors had a pencil that squeaked", page=82,
            )],
            claims(
                ("Alice took the pencil because it squeaked.", ["E1"]),
                ("Bill then wrote with one finger, which left no mark.", ["E1"]),
            ),
            notes="Replacement TEST case with two facts in one continuous, previously unexposed local event.",
        ),
        answered_case(
            "at119",
            "How did the court officers ‘suppress’ a cheering guinea-pig?",
            "They put it head-first into a tied canvas bag and sat on it.",
            "local_context_reasoning",
            "hard",
            [evidence(
                "E1", "alice_in_wonderland", "into this they slipped the guinea-pig, head first, and then sat upon it", page=84,
            )],
            claims(("The officers put the guinea-pig head-first into a tied canvas bag and sat on it.", ["E1"])),
            notes="Replacement TEST meaning-in-context case from a court event not exposed in DEV.",
        ),
        answered_case(
            "at120",
            "What accident did Alice cause when she jumped up after being called as a witness?",
            "She tipped over the jury-box with her skirt and spilled the jurors onto the crowd below.",
            "multi_fact_single_context",
            "medium",
            [evidence(
                "E1", "alice_in_wonderland", "she tipped over the jury-box with the edge of her skirt", page=87,
            )],
            claims(
                ("Alice tipped over the jury-box with her skirt.", ["E1"]),
                ("The jurors fell onto the crowd below.", ["E1"]),
            ),
            notes="Replacement TEST event from a source unit not used by DEV evidence or ambiguity material.",
        ),
        answered_case(
            "at121",
            "What did the Queen throw at the Lizard after denying that she had fits, and how did he use it?",
            "She threw an inkstand; the Lizard used the ink dripping down his face to resume writing.",
            "multi_fact_single_context",
            "hard",
            [evidence(
                "E1", "alice_in_wonderland", "throwing an inkstand at the Lizard", page=90,
            )],
            claims(
                ("The Queen threw an inkstand at the Lizard.", ["E1"]),
                ("The Lizard used the dripping ink to write again.", ["E1"]),
            ),
            notes="Replacement TEST cause-and-use relation from a previously unexposed paragraph.",
        ),
        answered_case(
            "at122",
            "What did the Mock Turtle say he had once been?",
            "A real turtle.",
            "direct_factual_single_source",
            "medium",
            [evidence(
                "E1", "alice_in_wonderland", "I was a real Turtle", page=70,
            )],
            claims(("The Mock Turtle said that he had once been a real turtle.", ["E1"])),
            notes="Replacement TEST speaker-attributed fact from an unexposed paragraph.",
        ),
        answered_case(
            "at123",
            "Why did Alice say there was no use going back to yesterday when telling her adventures?",
            "Because she said she had been a different person yesterday.",
            "local_context_reasoning",
            "medium",
            [evidence(
                "E1", "alice_in_wonderland", "it’s no use going back to yesterday, because I was a different person then", page=76,
            )],
            claims(("Alice said yesterday was not useful because she had been a different person then.", ["E1"])),
            notes="Replacement TEST rationale from an unexposed dialogue unit.",
        ),
    ]
    for case in cases:
        case["fact_family_id"] = f"fact_{case['case_id']}"
        case["evidence_event_id"] = f"event_{case['case_id']}"
        case["development_exposure"] = {
            "status": "no_known_development_exposure",
            "sources": [],
            "review_method": (
                "Compared with DEV answers, preceding/supporting/following context, "
                "negative-search excerpts, ambiguity evidence, and declared variants."
            ),
        }
        case["metamorphic_pair_id"] = None
        case["contrastive_pair_id"] = None
        case["related_case_ids"] = []
        case["requires_owner_attention"] = True
        package_evidence(case)
    return cases


def add_exposure_metadata(case: dict) -> None:
    if case.get("evidence_event_id") is None:
        case["evidence_event_id"] = f"event_{case['fact_family_id']}"
    if case["split_candidate"] == "alice_dev_regression":
        case["development_exposure"] = {
            "status": "development_material",
            "sources": [case["case_id"]],
            "review_method": "This case and its reviewer-facing context are development-visible.",
        }
    elif case["split_candidate"] == "alice_final_test":
        case["development_exposure"] = {
            "status": "no_known_development_exposure",
            "sources": [],
            "review_method": (
                "Compared with DEV answers, preceding/supporting/following context, "
                "negative-search excerpts, ambiguity evidence, and declared variants."
            ),
        }
    else:
        case["development_exposure"] = {
            "status": "not_applicable_different_book",
            "sources": [],
            "review_method": "Secret Garden is a separate-book holdout.",
        }


def main() -> None:
    payload = json.loads(DATASET.read_text(encoding="utf-8"))
    replacements = replacement_cases()
    replacement_ids = {case["case_id"] for case in replacements}
    ids_to_replace = EXPOSED_TEST_IDS | replacement_ids
    retained = [
        case for case in payload["cases"]
        if case["case_id"] not in ids_to_replace
    ]
    retained.extend(replacements)

    for case in retained:
        add_exposure_metadata(case)

    retained.sort(key=lambda case: (
        0 if case["split_candidate"] == "alice_dev_regression" else
        1 if case["split_candidate"] == "alice_final_test" else 2,
        case["case_id"],
    ))

    categories = Counter(case["primary_category"] for case in retained)
    splits = Counter(case["split_candidate"] for case in retained)
    payload["cases"] = retained
    payload["target_counts"]["observed_categories_after_repair"] = dict(sorted(categories.items()))
    payload["target_counts"]["splits"] = dict(sorted(splits.items()))
    payload["audit_state"]["final_targeted_test_repair"] = {
        "adjudication": "confirmed_development_exposure",
        "removed_test_case_ids": sorted(EXPOSED_TEST_IDS),
        "replacement_test_case_ids": [case["case_id"] for case in replacements],
        "remaining_known_development_exposures": 0,
        "method": (
            "Manual event/relation review plus deterministic exact-span checks across DEV answer evidence, "
            "local context, negative-search excerpts, ambiguity evidence, and declared variants."
        ),
    }
    payload["audit_state"]["cases_replaced"] = sorted(
        set(payload["audit_state"].get("cases_replaced", [])) | EXPOSED_TEST_IDS
    )
    payload["audit_state"]["replacement_case_ids"] = [
        case["case_id"] for case in retained
        if case["split_candidate"] == "alice_final_test"
        and case["case_id"].startswith("at")
        and int(case["case_id"][2:]) >= 101
    ]

    DATASET.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_manifest(payload)
    print(json.dumps({
        "removed": sorted(EXPOSED_TEST_IDS),
        "added": [case["case_id"] for case in replacements],
        "cases": len(retained),
        "splits": dict(splits),
        "categories": dict(categories),
    }, indent=2))


if __name__ == "__main__":
    main()
