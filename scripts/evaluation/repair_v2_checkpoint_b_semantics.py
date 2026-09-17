#!/usr/bin/env python3
"""Checkpoint B semantic/evidence repair.

Edits only:
q007, c005, q018, q023, q026, at068, at102, sg085, sg088, sg092

No provider calls. No retrieval/QA execution. Idempotent field overwrites.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "eval/v2/candidates.json"

TARGET_IDS = {
    "q007", "c005", "q018", "q023", "q026",
    "at068", "at102", "sg085", "sg088", "sg092",
}


def evidence(case: dict, eid: str) -> dict:
    for item in case.get("valid_evidence_locations", []):
        if item.get("evidence_id") == eid:
            return item
    raise KeyError(f"{case['case_id']}: missing evidence {eid}")


def sync(case: dict) -> None:
    case["exact_supporting_spans"] = [
        e["exact_supporting_span"] for e in case["valid_evidence_locations"]
    ]
    case["local_surrounding_context"] = [
        {
            "evidence_id": e["evidence_id"],
            "preceding": e.get("preceding_context", ""),
            "supporting": e.get("supporting_context", ""),
            "following": e.get("following_context", ""),
            "context_incomplete": e.get("context_incomplete", False),
        }
        for e in case["valid_evidence_locations"]
    ]


def main() -> None:
    payload = json.loads(DATASET.read_text(encoding="utf-8"))
    by_id = {c["case_id"]: c for c in payload["cases"]}

    missing = sorted(TARGET_IDS - set(by_id))
    if missing:
        raise SystemExit(f"STOP: missing target cases: {missing}")

    # q007
    c = by_id["q007"]
    c["question"] = "Which foods did the DRINK ME bottle taste like?"
    c["annotation_notes"] = (
        "The six-food flavour list is narrator description, not dialogue by Alice. "
        "The normalized answer preserves all six foods."
    )
    c["annotation_confidence"] = "high"
    c["requires_owner_attention"] = False
    c["review_tier"] = "FAST_CONFIRM"
    evidence(c, "E1")["epistemic_status"] = "narrator_fact"
    sync(c)

    # c005
    c = by_id["c005"]
    c["question"] = (
        "How tall did Alice become before the pool formed, and how deep was the pool?"
    )
    c["reference_answer"] = (
        "Alice became more than nine feet tall, and the pool was about four inches deep."
    )
    c["primary_category"] = "multi_fact_single_context"
    c["category"] = "multi_fact_single_context"
    c["annotation_notes"] = (
        "Metamorphic restatement of q009. Both numeric facts belong to one continuous "
        "growth-and-tears sequence; the four-inch depth is narrator description."
    )
    c["annotation_confidence"] = "medium"
    c["requires_owner_attention"] = True
    c["review_tier"] = "DEEP_REVIEW"
    e = evidence(c, "E2")
    e["epistemic_status"] = "narrator_fact"
    e["why_supports"] = (
        "The narrator states that the pool around Alice was about four inches deep."
    )
    sync(c)

    # q018
    c = by_id["q018"]
    c["reference_answer"] = (
        "The Pigeon was guarding its eggs against serpents and, seeing Alice’s unusually "
        "long neck, insisted she was a serpent. When Alice said little girls eat eggs too, "
        "the Pigeon replied conditionally that if that were true, little girls were a kind "
        "of serpent."
    )
    c["required_answer_claims"] = [
        {
            "claim_id": "C1",
            "claim_text": (
                "The Pigeon was watching its eggs for serpents and treated Alice’s unusually "
                "long neck as a reason to call her a serpent."
            ),
            "evidence_ids": ["E1", "E2"],
        },
        {
            "claim_id": "C2",
            "claim_text": (
                "After Alice said little girls eat eggs, the Pigeon said conditionally that "
                "if girls do eat eggs, they are a kind of serpent."
            ),
            "evidence_ids": ["E2"],
        },
    ]
    e = evidence(c, "E2")
    old = " ".join([
        e.get("preceding_context", ""),
        e.get("supporting_context", ""),
        e.get("following_context", ""),
    ]).strip()
    e["preceding_context"] = (
        "The Pigeon challenges Alice’s claim that she is a little girl and focuses on "
        "her altered appearance."
    )
    e["supporting_context"] = old
    e["following_context"] = (
        "The exchange continues with the Pigeon accusing Alice of looking for eggs."
    )
    e["exact_supporting_span"] = (
        "No, no! You’re a serpent; and there’s no use denying it."
    )
    e["why_supports"] = (
        "The continuous dialogue shows the Pigeon’s long-neck accusation and later "
        "conditional egg-based reasoning; both are character beliefs, not narrator facts."
    )
    e["epistemic_status"] = "character_statement"
    c["annotation_notes"] = (
        "Preserves chronology and epistemic status: long-neck suspicion first, then "
        "conditional reasoning about girls eating eggs."
    )
    c["annotation_confidence"] = "medium"
    c["requires_owner_attention"] = True
    c["review_tier"] = "DEEP_REVIEW"
    sync(c)

    # q023
    c = by_id["q023"]
    c["reference_answer"] = (
        "The Hatter said he and Time had quarreled. After the concert incident, Time "
        "would no longer do anything the Hatter asked, so it stayed six o’clock and "
        "therefore was always tea-time."
    )
    c["required_answer_claims"] = [
        {
            "claim_id": "C1",
            "claim_text": (
                "The Hatter said he had quarreled with Time and that afterward Time "
                "would no longer do what he asked."
            ),
            "evidence_ids": ["E1"],
        },
        {
            "claim_id": "C2",
            "claim_text": (
                "The Hatter said it stayed six o’clock and confirmed that this was why "
                "it was always tea-time."
            ),
            "evidence_ids": ["E1", "E2"],
        },
    ]
    e = evidence(c, "E1")
    e["preceding_context"] = (
        "The Hatter personifies Time and says that if one stays on good terms with him, "
        "Time can move or hold the clock as requested. When Alice asks whether that is how "
        "the Hatter manages, he says no and explains that they quarrelled last March."
    )
    e["supporting_context"] = (
        "The Hatter says that at the concert the Queen cried, ‘He’s murdering the time! "
        "Off with his head!’ He continues that ever since then, Time ‘won’t do a thing I "
        "ask! It’s always six o’clock now.’"
    )
    e["exact_supporting_span"] = "It’s always six o’clock now"
    e["why_supports"] = (
        "The expanded context resolves ‘he’ as Time and supplies the quarrel to "
        "non-cooperation to six-o’clock causal chain."
    )
    c["annotation_notes"] = (
        "Evidence now includes the Time antecedent and causal chain through permanent "
        "six o’clock and tea-time."
    )
    c["annotation_confidence"] = "medium"
    c["requires_owner_attention"] = True
    c["review_tier"] = "DEEP_REVIEW"
    sync(c)

    # q026
    c = by_id["q026"]
    c["question"] = (
        "Which oddly named subjects did the Mock Turtle list in the regular course "
        "and in the Drawling-master’s lessons?"
    )
    c["reference_answer"] = (
        "Reeling, Writhing, Ambition, Distraction, Uglification, Derision, Mystery "
        "(ancient and modern), Seaography, Drawling, Stretching, and Fainting in Coils."
    )
    c["required_answer_claims"] = [
        {
            "claim_id": "C1",
            "claim_text": (
                "The regular course began with Reeling, Writhing, Ambition, Distraction, "
                "Uglification, and Derision."
            ),
            "evidence_ids": ["E1"],
        },
        {
            "claim_id": "C2",
            "claim_text": (
                "The packaged later passage lists Mystery, Seaography, Drawling, Stretching, "
                "and Fainting in Coils."
            ),
            "evidence_ids": ["E2"],
        },
    ]
    e = evidence(c, "E2")
    e["why_supports"] = (
        "The cited passage explicitly lists Mystery, Seaography, Drawling, Stretching, "
        "and Fainting in Coils."
    )
    c["annotation_notes"] = (
        "Question/reference narrowed to what packaged E1/E2 explicitly support; no "
        "unsupported Laughing/Grief claim is made."
    )
    c["annotation_confidence"] = "high"
    c["requires_owner_attention"] = True
    c["review_tier"] = "DEEP_REVIEW"
    sync(c)

    # at068
    c = by_id["at068"]
    e = evidence(c, "E1")
    e["supporting_context"] = (
        "‘Fury said to a mouse, That he met in the house, “Let us both go to law: "
        "I will prosecute you. Come, I’ll take no denial; We must have a trial: "
        "For really this morning I’ve nothing to do.” Said the mouse to the cur, "
        "“Such a trial, dear sir, With no jury or judge, would be wasting our breath.” "
        "“I’ll be judge, I’ll be jury,” Said cunning old Fury: “I’ll try the whole cause, "
        "and condemn you to death.”’"
    )
    e["following_context"] = "The Mouse then rebukes Alice for not attending to the tale."
    e["exact_supporting_span"] = "Let us both go to law: I will prosecute you"
    e["why_supports"] = (
        "The restored poem text explicitly has Fury propose going to law and prosecuting the Mouse."
    )
    e["context_incomplete"] = False
    c["annotation_notes"] = (
        "Retained TEST case. Evidence restored far enough to contain the proposition being scored."
    )
    c["annotation_confidence"] = "medium"
    c["requires_owner_attention"] = True
    c["review_tier"] = "DEEP_REVIEW"
    sync(c)

    # at102
    c = by_id["at102"]
    c["reference_answer"] = (
        "The Mouse cried ‘I had NOT!’; Alice interpreted the sound as ‘A knot!’, offered "
        "to undo it, and the Mouse called her talk nonsense and insulting before walking away."
    )
    c["required_answer_claims"] = [
        {
            "claim_id": "C1",
            "claim_text": (
                "The Mouse said ‘I had NOT!’ and Alice interpreted it as ‘A knot!’, "
                "offering to undo it."
            ),
            "evidence_ids": ["E1"],
        },
        {
            "claim_id": "C2",
            "claim_text": (
                "The Mouse called Alice’s talk nonsense and insulting and walked away."
            ),
            "evidence_ids": ["E2"],
        },
    ]
    c["annotation_notes"] = (
        "Speaker attribution fixed: the Mouse says ‘NOT’; Alice supplies ‘A knot!’."
    )
    c["annotation_confidence"] = "high"
    c["requires_owner_attention"] = True
    c["review_tier"] = "DEEP_REVIEW"
    sync(c)

    # sg085
    c = by_id["sg085"]
    c["reference_answer"] = (
        "Mary’s parents had died, and the few servants who survived left the bungalow "
        "without remembering her, leaving her alone."
    )
    c["required_answer_claims"] = [
        {
            "claim_id": "C1",
            "claim_text": "Mary’s father and mother had died and been carried away.",
            "evidence_ids": ["E1"],
        },
        {
            "claim_id": "C2",
            "claim_text": (
                "The few servants who had not died left the house without remembering Mary."
            ),
            "evidence_ids": ["E1"],
        },
    ]
    e = evidence(c, "E1")
    e["exact_supporting_span"] = (
        "the few native servants who had not died also had left the house as quickly as "
        "they could get out of it, none of them even remembering that there was a Missie Sahib"
    )
    e["why_supports"] = (
        "This narrator passage states that Mary’s parents were gone and that surviving "
        "servants left without remembering her."
    )
    c["valid_evidence_locations"] = [e]
    c["primary_category"] = "multi_fact_single_context"
    c["category"] = "multi_fact_single_context"
    c["annotation_notes"] = (
        "Unsupported cholera/panic causality removed from this package; duplicate copies "
        "of the same paragraph are not counted as multi-source evidence."
    )
    c["annotation_confidence"] = "high"
    c["requires_owner_attention"] = True
    c["review_tier"] = "DEEP_REVIEW"
    sync(c)

    # sg088
    c = by_id["sg088"]
    e1 = evidence(c, "E1")
    e2 = evidence(c, "E2")
    bridge = (
        "Mrs. Medlock is describing Misselthwaite Manor and explicitly names Mr. Craven. "
        "The conversation continues with Mary reacting to what she hears; no competing male "
        "referent is introduced before Mrs. Medlock says, ‘He’s not going to trouble himself "
        "about you.’"
    )
    e1["following_context"] = bridge
    e2["preceding_context"] = bridge
    e1["epistemic_status"] = "character_statement"
    e2["epistemic_status"] = "character_statement"
    e1["why_supports"] = "Mrs. Medlock explicitly names Mr. Craven in the continuing discourse."
    e2["why_supports"] = (
        "No competing male referent intervenes between Mr. Craven and Mrs. Medlock’s ‘He’."
    )
    c["annotation_notes"] = (
        "Answer remains Mr. Archibald Craven; reviewer-visible coreference bridge and "
        "speech-type metadata repaired."
    )
    c["annotation_confidence"] = "medium"
    c["requires_owner_attention"] = True
    c["review_tier"] = "DEEP_REVIEW"
    sync(c)

    # sg092
    c = by_id["sg092"]
    destination = (
        "Mary pulls the ivy aside, finds the door’s lock, uses the buried key, turns it, "
        "pushes the door open, slips through, closes it behind her, and is then standing "
        "inside the secret garden."
    )
    for eid in ("E1", "E2"):
        e = evidence(c, eid)
        e["following_context"] = destination
    evidence(c, "E2")["why_supports"] = (
        "The extended continuous scene connects the ivy-covered door directly to Mary "
        "entering and standing inside the secret garden."
    )
    c["annotation_notes"] = (
        "Answer preserved; evidence package extended through Mary’s arrival inside the secret garden."
    )
    c["annotation_confidence"] = "medium"
    c["requires_owner_attention"] = True
    c["review_tier"] = "DEEP_REVIEW"
    sync(c)

    payload.setdefault("audit_state", {})["checkpoint_b_semantic_repair"] = {
        "scope": sorted(TARGET_IDS),
        "remaining_blocked_in_scope": [],
        "note": (
            "Semantic/evidence repair only. Source-version/provenance reconciliation "
            "remains for the next checkpoint."
        ),
    }

    DATASET.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("Checkpoint B semantic repair applied.")
    print("Edited:", ", ".join(sorted(TARGET_IDS)))
    print("No providers called. No retrieval/QA executed.")


if __name__ == "__main__":
    main()
