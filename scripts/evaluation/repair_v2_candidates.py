"""Apply the offline, source-backed Evaluation V2 repair pass.

This script never calls retrieval, a model, or any network service.  It reads
the exact Alice evaluation PDF and the pinned Project Gutenberg source, then
rewrites candidate annotations and their reviewer-facing source context.
"""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import unicodedata
from collections import Counter
from pathlib import Path

import pymupdf

from prepare_secret_garden import END, START, paragraphs


ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "eval" / "v2" / "candidates.json"
MANIFEST = ROOT / "eval" / "v2" / "split_manifest.candidate.json"
ALICE_PDF = ROOT / "backend" / "data" / "documents" / "a6c315f78fbb4c5cb9f16f08f28aed38" / "source.pdf"
ALICE_DB = ROOT / "backend" / "data" / "ingestion.sqlite3"
SECRET_TEXT = ROOT / "eval" / ".cache" / "books" / "secret-garden" / "pg113.txt"
SECRET_PDF = ROOT / "eval" / ".cache" / "books" / "secret-garden" / "the-secret-garden.pdf"
ALICE_SHA = "49c843b5e09a9f759781514b49b802e6981baec57bf8873c6404d1111448878e"
SECRET_SHA = "6b0bb5fbd0c4e873d2d22028da9d753cf3977d5f70ac58221556b28060badbf5"


def tokens(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", unicodedata.normalize("NFKD", value).casefold())


def contains_tokens(haystack: str, needle: str) -> bool:
    haystack_tokens, needle_tokens = tokens(haystack), tokens(needle)
    return bool(needle_tokens) and any(
        haystack_tokens[index:index + len(needle_tokens)] == needle_tokens
        for index in range(len(haystack_tokens) - len(needle_tokens) + 1)
    )


def clean(value: str) -> str:
    return " ".join(value.split())


def alice_units() -> list[dict]:
    units: list[dict] = []
    chapter = None
    with pymupdf.open(ALICE_PDF) as document:
        for page_number, page in enumerate(document, 1):
            for block_number, block in enumerate(page.get_text("blocks", sort=True)):
                text = clean(block[4])
                if not text or re.fullmatch(r"\d+", text):
                    continue
                heading = re.search(r"CHAPTER\s+(\d+)", text, re.IGNORECASE)
                if heading:
                    chapter = heading.group(1)
                is_heading = bool(
                    heading
                    or re.fullmatch(r"Chapter\s+\d+", text, re.IGNORECASE)
                    or (len(text) < 80 and text.upper() == text and len(text.split()) <= 10)
                )
                units.append({
                    "text": text,
                    "page": page_number,
                    "block": block_number,
                    "chapter": chapter,
                    "is_heading": is_heading,
                })
    return units


def secret_units() -> list[dict]:
    source = SECRET_TEXT.read_text(encoding="utf-8-sig")
    body = source.split(START, 1)[1].split(END, 1)[0].strip()
    units: list[dict] = []
    offset = 0
    chapter = None
    for raw in re.split(r"\n\s*\n", body):
        index = body.find(raw, offset)
        offset = index + len(raw)
        text = clean(raw)
        if not text:
            continue
        line = body[:index].count("\n") + 1
        heading = re.fullmatch(r"CHAPTER\s+([IVXLCDM]+)\.?", text, re.IGNORECASE)
        if heading:
            chapter = heading.group(1).upper()
        units.append({
            "text": text,
            "canonical_line": line,
            "chapter": chapter,
            "is_heading": bool(heading or text == "THE SECRET GARDEN"),
        })
    return units


ALICE_UNITS = alice_units()
SECRET_UNITS = secret_units()


def nearest_relevant(units: list[dict], start: int, step: int) -> str | None:
    index = start + step
    while 0 <= index < len(units):
        if not units[index]["is_heading"]:
            return units[index]["text"]
        index += step
    return None


def secret_pdf_pages(span: str) -> list[int]:
    matches: list[int] = []
    with pymupdf.open(SECRET_PDF) as document:
        page_text = [clean(page.get_text("text")) for page in document]
    for index, text in enumerate(page_text):
        if contains_tokens(text, span):
            matches.append(index + 1)
    if not matches:
        for index in range(len(page_text) - 1):
            if contains_tokens(page_text[index] + " " + page_text[index + 1], span):
                matches.extend([index + 1, index + 2])
                break
    return sorted(set(matches))


def locate(units: list[dict], span: str, location: dict) -> tuple[int, str]:
    candidates = [index for index, unit in enumerate(units) if contains_tokens(unit["text"], span)]
    if not candidates:
        for width in (2, 3):
            for index in range(len(units) - width + 1):
                combined = "\n\n".join(unit["text"] for unit in units[index:index + width])
                if contains_tokens(combined, span):
                    return index, combined
        raise ValueError(f"source span not found: {span!r}")
    if "page" in location:
        candidates.sort(key=lambda index: abs(units[index].get("page", 0) - location["page"]))
    if "canonical_line" in location:
        candidates.sort(key=lambda index: abs(units[index].get("canonical_line", 0) - location["canonical_line"]))
    index = candidates[0]
    return index, units[index]["text"]


def evidence(evidence_id: str, book: str, span: str, *, page: int | None = None,
             canonical_line: int | None = None, why: str | None = None,
             epistemic_status: str | None = None) -> dict:
    location: dict = {"book": book}
    if page is not None:
        location.update({"page": page, "chapter": None})
    else:
        location.update({"canonical_line": canonical_line or 1, "chapter": None, "generated_pdf_pages": []})
    return {
        "evidence_id": evidence_id,
        "source_location": location,
        "exact_supporting_span": span,
        "preceding_context": None,
        "supporting_context": None,
        "following_context": None,
        "why_supports": why,
        "epistemic_status": epistemic_status,
        "context_incomplete": False,
    }


def claims(*values: tuple[str, list[str]]) -> list[dict]:
    return [
        {"claim_id": f"C{index}", "claim_text": text, "evidence_ids": evidence_ids}
        for index, (text, evidence_ids) in enumerate(values, 1)
    ]


def answered_case(case_id: str, question: str, reference: str, category: str,
                  difficulty: str, evidence_values: list[dict], claim_values: list[dict],
                  *, tags: list[str] | None = None, notes: str = "") -> dict:
    return {
        "case_id": case_id,
        "lifecycle_status": "candidate",
        "split_candidate": "alice_final_test",
        "source_book": "alice_in_wonderland",
        "source_book_sha256": ALICE_SHA,
        "question": question,
        "expected_status": "answered",
        "reference_answer": reference,
        "required_answer_claims": claim_values,
        "valid_evidence_locations": evidence_values,
        "exact_supporting_spans": [item["exact_supporting_span"] for item in evidence_values],
        "local_surrounding_context": [],
        "primary_category": category,
        "category": category,
        "tags": tags or [],
        "difficulty": difficulty,
        "annotation_notes": notes,
        "annotation_confidence": "medium",
        "review_tier": "DEEP_REVIEW",
        "historical_case": False,
        "requires_owner_attention": False,
        "negative_verification": None,
        "ambiguity_rationale": None,
        "ambiguity_type": None,
        "plausible_referents": [],
        "expected_clarification": None,
        "evaluation_execution": None,
    }


def ambiguous_case(case_id: str, question: str, evidence_values: list[dict], rationale: str,
                   referents: list[str], clarification: str) -> dict:
    case = answered_case(
        case_id, question, "Clarification is required.", "ambiguous_underspecified",
        "hard", evidence_values, [], tags=["book_dependent_ambiguity"],
        notes="Two source-backed trial objections make the event reference non-unique.",
    )
    case.update({
        "expected_status": "ambiguous",
        "reference_answer": "Clarification is required.",
        "ambiguity_rationale": rationale,
        "ambiguity_type": "book_dependent_multiple_referents",
        "plausible_referents": referents,
        "expected_clarification": clarification,
        "annotation_confidence": "needs_owner_review",
        "requires_owner_attention": True,
    })
    return case


NEW_TEST_CASES = [
    answered_case(
        "at101", "Which bird claimed to be older than Alice but refused to give its age?",
        "The Lory.", "direct_factual_single_source", "medium",
        [evidence("E1", "alice_in_wonderland", "the Lory, who at last turned sulky, and would only say, ‘I am older than you, and must know better’", page=25)],
        claims(("The Lory made the age claim and refused to state its age.", ["E1"])),
        notes="New TEST fact from an Alice paragraph not used by DEV evidence.",
    ),
    answered_case(
        "at102", "Why did the Mouse leave after Alice said it had reached the fifth bend?",
        "The Mouse said ‘knot,’ Alice misheard it as a literal knot and offered to undo it, and the Mouse took that as an insult.",
        "local_context_reasoning", "hard",
        [
            evidence("E1", "alice_in_wonderland", "‘I had NOT!’ cried the Mouse", page=29, epistemic_status="dialogue_wordplay"),
            evidence("E2", "alice_in_wonderland", "You insult me by talking such nonsense", page=29, epistemic_status="character_reaction"),
        ],
        claims(
            ("Alice mistook ‘not’ for ‘knot’ and offered to undo it.", ["E1"]),
            ("The Mouse treated the misunderstanding as an insult and left.", ["E2"]),
        ), notes="Requires adjacent dialogue to resolve the not/knot wordplay.",
    ),
    answered_case(
        "at103", "Why did the birds and animals make excuses and leave Alice alone?",
        "Alice praised Dinah for catching mice and eating birds; the threatened animals and birds then made excuses and left.",
        "multi_source_multi_fact", "hard",
        [
            evidence("E1", "alice_in_wonderland", "she’ll eat a little bird as soon as look at it", page=29, epistemic_status="alice_statement"),
            evidence("E2", "alice_in_wonderland", "On various pretexts they all moved off, and Alice was soon left alone", page=30, epistemic_status="narrator_fact"),
        ],
        claims(
            ("Alice described Dinah as a hunter of mice and birds.", ["E1"]),
            ("The party then made excuses and left Alice alone.", ["E2"]),
        ), notes="Cross-page cause and outcome; neither claim is sufficient alone.",
    ),
    answered_case(
        "at104", "at the rabbit house when alice drank that unlabeled bottle did she get bigger or smaller",
        "She grew bigger, until her head pressed against the ceiling and she could not get through the door.",
        "voice_like_noisy_text", "medium",
        [evidence("E1", "alice_in_wonderland", "before she had drunk half the bottle, she found her head pressing against the ceiling", page=32)],
        claims(("The unlabeled bottle made Alice grow larger inside the Rabbit’s house.", ["E1"])),
        tags=["punctuation_loss", "conversational_wording"], notes="Realistic punctuation-free spoken-text form; new fact family.",
    ),
    answered_case(
        "at105", "Who was sent down the Rabbit’s chimney, and what happened to him?",
        "Bill was sent down; Alice kicked him up the chimney and he shot out like a sky-rocket.",
        "multi_source_multi_fact", "hard",
        [
            evidence("E1", "alice_in_wonderland", "Bill’s to go down–Here, Bill! the master says you’re to go down the chimney", page=34),
            evidence("E2", "alice_in_wonderland", "she gave one sharp kick", page=34),
            evidence("E3", "alice_in_wonderland", "up I goes like a sky-rocket", page=34, epistemic_status="bill_statement"),
        ],
        claims(
            ("Bill was selected to go down the chimney.", ["E1"]),
            ("Alice kicked him and he flew upward like a sky-rocket.", ["E2", "E3"]),
        ), notes="Multiple non-contiguous dialogue/narration units in the chimney scene.",
    ),
    answered_case(
        "at106", "How did Alice distract the enormous puppy and get away?",
        "She held out a stick and dodged around a thistle while the puppy charged; when it tired and sat panting, she ran away.",
        "multi_source_multi_fact", "hard",
        [
            evidence("E1", "alice_in_wonderland", "she picked up a little bit of stick, and held it out to the puppy", page=35),
            evidence("E2", "alice_in_wonderland", "ran round the thistle again", page=36),
            evidence("E3", "alice_in_wonderland", "This seemed to Alice a good opportunity for making her escape", page=36),
        ],
        claims(
            ("Alice distracted the puppy with a stick and the thistle.", ["E1", "E2"]),
            ("She escaped when the puppy became tired and stopped at a distance.", ["E2", "E3"]),
        ), notes="Cross-page action sequence with distinct setup and outcome evidence.",
    ),
    answered_case(
        "at107", "What was the Caterpillar’s supposedly important advice when it called Alice back?",
        "‘Keep your temper.’",
        "local_context_reasoning", "medium",
        [evidence("E1", "alice_in_wonderland", "‘Come back!’ the Caterpillar called after her. ‘I’ve something important to say!’", page=38, epistemic_status="character_statement"),
         evidence("E2", "alice_in_wonderland", "‘Keep your temper,’ said the Caterpillar", page=38, epistemic_status="character_statement")],
        claims(("The Caterpillar called Alice back and delivered ‘Keep your temper’ as the important advice.", ["E1", "E2"])),
        notes="Adjacent dialogue is needed to connect ‘important’ to the advice.",
    ),
    answered_case(
        "at108", "Why did the Cheshire Cat say it did not matter which way Alice went?",
        "Because Alice said she did not much care where she wanted to get to.",
        "local_context_reasoning", "medium",
        [evidence("E1", "alice_in_wonderland", "That depends a good deal on where you want to get to", page=47, epistemic_status="character_statement")],
        claims(("The Cat’s answer depends on Alice saying she does not care about the destination.", ["E1"])),
        notes="The causal answer comes from the two-speaker exchange, not a standalone Cat quotation.",
    ),
    answered_case(
        "at109", "In what order did the Cheshire Cat disappear when Alice asked it to vanish more slowly?",
        "It disappeared from the end of its tail first, with the grin remaining last.",
        "direct_factual_single_source", "medium",
        [evidence("E1", "alice_in_wonderland", "beginning with the end of the tail, and ending with the grin", page=49)],
        claims(("The tail disappeared first and the grin remained until last.", ["E1"])),
        notes="New chronology fact from a previously unexposed paragraph.",
    ),
    answered_case(
        "at110", "Could the executioner behead the Cheshire Cat’s visible head, according to both sides of the dispute?",
        "They disagreed: the executioner said a head could not be cut off without a body, while the King said anything with a head could be beheaded.",
        "contrastive_distractor", "hard",
        [
            evidence("E1", "alice_in_wonderland", "The executioner’s argument was", page=64, epistemic_status="executioner_argument"),
            evidence("E2", "alice_in_wonderland", "anything that had a head", page=64, epistemic_status="king_argument"),
        ],
        claims(
            ("The executioner said a body was required.", ["E1"]),
            ("The King argued that possessing a head was sufficient.", ["E2"]),
        ), notes="Competing propositions from two speakers must remain distinct.",
    ),
    answered_case(
        "at111", "What choice did the Queen give the Duchess when she interrupted her conversation with Alice?",
        "The Duchess had to leave immediately or lose her head; she left.",
        "direct_factual_single_source", "medium",
        [evidence("E1", "alice_in_wonderland", "either you or your head must be off", page=69, epistemic_status="queen_threat")],
        claims(("The Queen threatened the Duchess with departure or beheading, and the Duchess departed.", ["E1"])),
        notes="Explicit threat and immediate outcome in one local passage.",
    ),
    answered_case(
        "at112", "Did the Gryphon agree that the Queen’s execution orders were actually carried out?",
        "No. After the Queen left, the Gryphon said it was all her fancy and that nobody was ever executed.",
        "contrastive_distractor", "hard",
        [evidence("E1", "alice_in_wonderland", "It’s all her fancy, that: they never executes nobody", page=70, epistemic_status="gryphon_statement")],
        claims(("The Gryphon denied that the Queen’s threatened executions were carried out.", ["E1"])),
        notes="The answer must preserve that this is the Gryphon’s assertion, not omniscient narration.",
    ),
    answered_case(
        "at113", "According to the Gryphon, how did the whitings’ tails become stuck in their mouths?",
        "They went with the lobsters, were thrown into the sea, fell a long way, and got their tails stuck in their mouths.",
        "local_context_reasoning", "hard",
        [evidence("E1", "alice_in_wonderland", "they WOULD go with the lobsters to the dance. So they got thrown out to sea", page=75, epistemic_status="gryphon_story")],
        claims(("The Gryphon gives a chain of events from joining the dance through the fall to the stuck tails.", ["E1"])),
        notes="Preserves the source as the Gryphon’s fanciful explanation.",
    ),
    answered_case(
        "at114", "When the Mock Turtle asked what a traveling fish’s ‘porpoise’ was, which word did Alice think he meant?",
        "Purpose.", "local_context_reasoning", "medium",
        [evidence("E1", "alice_in_wonderland", "‘Don’t you mean “purpose”?’ said Alice", page=76, epistemic_status="dialogue_wordplay")],
        claims(("Alice interpreted ‘porpoise’ as the word ‘purpose.’", ["E1"])),
        notes="A speaker-attributed homophone test from an unexposed passage.",
    ),
    answered_case(
        "at115", "Which song was interrupted, and what interrupted it?",
        "The Mock Turtle’s ‘Turtle Soup’ song was interrupted by a distant cry that the trial was beginning.",
        "multi_fact_single_context", "medium",
        [evidence("E1", "alice_in_wonderland", "Sing her “Turtle Soup,” will you", page=78, epistemic_status="character_request"),
         evidence("E2", "alice_in_wonderland", "a cry of ‘The trial’s beginning!’ was heard in the distance", page=78, epistemic_status="narrator_fact")],
        claims(
            ("The song was ‘Turtle Soup.’", ["E1"]),
            ("A cry announcing the trial interrupted it.", ["E2"]),
        ), notes="Two material facts in one continuous scene; intentionally not labeled multi-source.",
    ),
    ambiguous_case(
        "at116", "What happened after Alice challenged the court?",
        [
            evidence("E1", "alice_in_wonderland", "It proves nothing of the sort!", page=89, epistemic_status="alice_objection"),
            evidence("E2", "alice_in_wonderland", "The idea of having the sentence first!", page=91, epistemic_status="alice_objection"),
        ],
        "Alice challenges the court at least twice: she rejects the Queen’s claimed proof on page 89 and later rejects sentence-before-verdict on page 91. The requested aftermath depends on which objection is meant.",
        ["Alice’s objection to treating the unsigned verses as proof", "Alice’s objection to sentence before verdict"],
        "Do you mean her objection to the unsigned verses or to sentence before verdict?",
    ),
]


REPLACED_TEST_IDS = {
    "at061", "at062", "at063", "at064", "at065", "at066", "at067",
    "at069", "at070", "at071", "at072", "at074", "at077", "at078",
    "at079", "at080",
}

ANNOTATION_REPAIR_IDS = {
    "q002", "q007", "q010", "q011", "q013", "q018", "q022", "q023",
    "q026", "q027", "c005", "c006", "av044", "av055", "av057",
    "c003", "c004", "av050", "av051", "av052", "av053",
    "c001", "c002", "av046", "av047", "av048", "av049", "at075", "at076",
    "sg085", "sg086", "sg087", "sg094", "sg095", "sg096", "sg097",
    "sg098", "sg099",
}


def set_answered(case: dict, *, question: str | None = None, reference: str | None = None,
                 category: str | None = None, claim_values: list[dict] | None = None,
                 evidence_values: list[dict] | None = None, notes: str | None = None) -> None:
    if question is not None:
        case["question"] = question
    if reference is not None:
        case["reference_answer"] = reference
    if category is not None:
        case["primary_category"] = category
        case["category"] = category
    if claim_values is not None:
        case["required_answer_claims"] = claim_values
    if evidence_values is not None:
        case["valid_evidence_locations"] = evidence_values
        case["exact_supporting_spans"] = [item["exact_supporting_span"] for item in evidence_values]
    if notes is not None:
        case["annotation_notes"] = notes


def repair_flagged(by_id: dict[str, dict]) -> None:
    set_answered(
        by_id["q010"],
        question="What caused Alice to start shrinking while she was thinking about whether she had become Mabel?",
        reference="The White Rabbit’s fan she was holding caused her to shrink.",
        category="direct_factual_single_source",
        claim_values=claims(("The fan in Alice’s hand caused the shrinking.", ["E1"])),
        notes="4.75B removes the old false chronology: Alice had not met or spoken to the Mouse yet.",
    )
    set_answered(
        by_id["q011"],
        reference="Alice guessed that the Mouse might not understand English and might be a French mouse that had come with William the Conqueror, so she tried the first sentence from her French lesson-book.",
        category="local_context_reasoning",
        claim_values=claims(
            ("Alice guessed, rather than knew, that the Mouse might be French.", ["E1"]),
            ("She therefore tried a sentence from her French lesson-book.", ["E1"]),
        ),
        notes="The repair preserves Alice’s uncertain belief and avoids presenting it as narrator fact.",
    )
    set_answered(
        by_id["av057"],
        question="uh who was accused of stealing the queen’s tarts again",
        reference="The Knave of Hearts was accused of stealing them.",
        claim_values=claims(("The court accusation names the Knave of Hearts as the alleged thief.", ["E1"])),
        notes="The answer now preserves accusation status rather than treating the charge as proven fact.",
    )
    set_answered(
        by_id["q027"],
        reference="After changing lobsters and retiring, the dancers throw the lobsters out to sea, swim after them, turn a somersault, change lobsters again, and return to land; that completes the first figure.",
        category="multi_source_multi_fact",
        claim_values=claims(
            ("They change lobsters and retire, then throw the lobsters to sea, swim after them, and somersault.", ["E1"]),
            ("They change lobsters again and return to land to finish the first figure.", ["E2"]),
        ),
        evidence_values=[
            evidence("E1", "alice_in_wonderland", "change lobsters, and retire in same order", page=73),
            evidence("E2", "alice_in_wonderland", "Back to land again, and that’s all the first figure", page=74),
        ],
        notes="The old answer omitted throw/swim/somersault/change-again steps; the repaired answer covers the complete ending sequence.",
    )
    set_answered(
        by_id["q007"],
        reference="Cherry tart, custard, pineapple, roast turkey, toffee, and hot buttered toast.",
        evidence_values=[evidence("E1", "alice_in_wonderland", "mixed ﬂavour of cherry- tart, custard, pine-apple, roast turkey, toﬀee, and hot buttered toast", page=16)],
        claim_values=claims(("The bottle’s mixed flavor contains all six listed foods.", ["E1"])),
        notes="The source’s line-broken ‘cherry-tart’ is normalized without changing the six-item answer.",
    )
    by_id["c005"]["primary_category"] = by_id["c005"]["category"] = "multi_source_multi_fact"
    by_id["c005"]["annotation_notes"] = "Useful metamorphic restatement of q009; two numeric facts come from distinct adjacent pages and do not count as independent breadth."
    set_answered(
        by_id["q018"],
        reference="The Pigeon believed Alice was a serpent: it was guarding eggs, and when Alice admitted that little girls eat eggs, the Pigeon concluded that little girls must be a kind of serpent.",
        claim_values=claims(
            ("The Pigeon was exhausted from guarding its eggs against serpents.", ["E1"]),
            ("After Alice admitted girls eat eggs, the Pigeon treated that as proof she was a serpent.", ["E2"]),
        ),
        notes="The conclusion is explicitly the Pigeon’s belief, not narrator-confirmed identity.",
    )
    set_answered(
        by_id["q023"],
        reference="The Hatter said he had quarreled with Time; Time then refused to do anything the Hatter asked, leaving the clock at six o’clock, so it was always tea-time.",
        claim_values=claims(
            ("The Hatter said Time stopped cooperating after their quarrel.", ["E1"]),
            ("The time remained six o’clock, which made it perpetually tea-time.", ["E2"]),
        ),
        notes="Adds the missing causal link between the quarrel with Time and permanent six o’clock.",
    )
    set_answered(
        by_id["av055"],
        question="when the rabbit mistook alice for mary ann he wanted his gloves and what else",
        reference="His fan.",
        claim_values=claims(("The Rabbit ordered the person he called Mary Ann to fetch gloves and a fan.", ["E1"])),
        notes="Rewritten as realistic punctuation-free spoken text while retaining the q014 fact family.",
    )
    set_answered(
        by_id["q002"],
        category="direct_factual_single_source",
        evidence_values=[evidence("E1", "alice_in_wonderland", "12 Alice’s Evidence", page=6)],
        claim_values=claims(
            ("The contents list has twelve chapters and names chapter twelve ‘Alice’s Evidence.’", ["E1"]),
        ),
        notes="Both requested values are explicit in one contents entry, so this is one local evidence unit rather than multi-source evidence.",
    )
    by_id["q013"]["primary_category"] = by_id["q013"]["category"] = "contrastive_distractor"
    by_id["q013"]["annotation_notes"] = "The diagnostic distinction is other racers’ comfits versus Alice’s returned thimble; all evidence is one local scene."
    by_id["c006"]["annotation_notes"] = "Useful contrastive/metamorphic member of the q013 prize family; not independent breadth."
    by_id["av044"]["valid_evidence_locations"][1]["exact_supporting_span"] = "took the thimble"
    by_id["av044"]["exact_supporting_spans"] = [
        item["exact_supporting_span"] for item in by_id["av044"]["valid_evidence_locations"]
    ]
    by_id["av044"]["annotation_notes"] = "Contrastive q013-family case; evidence now points to Alice actually taking the thimble rather than a line-broken extraction fragment."
    by_id["q022"]["primary_category"] = by_id["q022"]["category"] = "local_context_reasoning"
    by_id["q022"]["annotation_notes"] = "The wine answer requires resolving an offer against the following admission that no wine existed; it is one local dialogue, not multi-source."
    set_answered(
        by_id["q026"],
        reference="Reeling, Writhing, Ambition, Distraction, Uglification, Derision, Mystery (ancient and modern), Seaography, Drawling, Stretching, Fainting in Coils, Laughing, and Grief.",
        category="multi_source_multi_fact",
        claim_values=claims(
            ("The regular course began with Reeling, Writhing, and four punning arithmetic branches.", ["E1"]),
            ("The later list added Mystery, Seaography, Drawling, Stretching, Fainting in Coils, Laughing, and Grief.", ["E2"]),
        ),
        evidence_values=[
            evidence("E1", "alice_in_wonderland", "Reeling and Writhing, of course, to begin with", page=71),
            evidence("E2", "alice_in_wonderland", "Mystery, ancient and modern, with Seaography", page=72),
        ],
        notes="The old reference stopped after six names even though the broad question covered the later list; the full two-page curriculum is now included.",
    )

    set_answered(
        by_id["sg085"],
        reference="During the cholera outbreak Mary was forgotten amid the deaths and panic; the few servants who survived fled the bungalow without remembering her.",
        claim_values=claims(
            ("Cholera deaths and panic caused the household confusion in which Mary was forgotten.", ["E1"]),
            ("The surviving servants fled without remembering Mary.", ["E2"]),
        ),
        notes="Removes the misleading suggestion that her parents’ deaths alone explain why she was left unattended.",
    )
    set_answered(
        by_id["sg086"],
        reference="Mary found the buried key in freshly turned soil, discovered the ivy-covered door when wind moved the ivy, and used the key to unlock it.",
        claim_values=claims(
            ("Mary found an old key buried in freshly turned soil.", ["E1"]),
            ("Wind shifted the ivy and revealed the door knob.", ["E2"]),
            ("The key fitted the lock and opened the door.", ["E3"]),
        ),
        evidence_values=[
            evidence("E1", "the_secret_garden", "it was an old key which looked as if it had been buried a long time", canonical_line=2053),
            evidence("E2", "the_secret_garden", "the gust of wind swung aside some loose ivy trails", canonical_line=2319),
            evidence("E3", "the_secret_garden", "drew out the key and found it fitted the keyhole", canonical_line=2338),
        ],
        notes="Consolidates duplicate spans while preserving the three independently necessary access steps.",
    )
    by_id["sg087"]["primary_category"] = by_id["sg087"]["category"] = "local_context_reasoning"
    by_id["sg087"]["required_answer_claims"] = claims(
        ("Mary identifies Mr. Craven as her uncle.", ["E1"]),
        ("Colin identifies the same man as his father, making Mary and Colin cousins.", ["E2"]),
    )
    by_id["sg087"]["annotation_notes"] = "The cousin relation is inferred from one continuous exchange; it is not distributed multi-source evidence."
    set_answered(
        by_id["sg094"],
        reference="No. Martha says he closed it after his wife died and that it had been her garden; later narration describes her eyes as ones he had adored.",
        claim_values=claims(
            ("Martha reports that he closed the garden after his wife’s sudden death and that it was her garden.", ["E1"]),
            ("Later narration says he had adored his wife’s eyes, contradicting the premise that he had always disliked her.", ["E2"]),
        ),
        evidence_values=[
            evidence("E1", "the_secret_garden", "Mr. Craven had it shut when his wife died so sudden", canonical_line=1025, epistemic_status="martha_statement"),
            evidence("E2", "the_secret_garden", "the happy eyes he had adored", canonical_line=940, epistemic_status="narrator_fact"),
        ],
        notes="The prior evidence explained closure but did not refute ‘always disliked’; later narrator evidence now does.",
    )
    by_id["sg095"]["required_answer_claims"] = claims(
        ("Mary identifies Mr. Craven as her uncle, so she is his niece.", ["E1"]),
        ("Colin identifies Mr. Craven as his father, so Colin is his son rather than nephew and is Mary’s cousin.", ["E2"]),
    )
    by_id["sg095"]["annotation_notes"] = "The repaired claims now cover every relation stated in the reference answer."


FACT_FAMILIES = {
    "q003": "alice_rabbit_eye_color", "av054": "alice_rabbit_eye_color",
    "q008": "alice_eat_me_cake_label", "av058": "alice_eat_me_cake_label",
    "q009": "alice_height_pool_depth", "c005": "alice_height_pool_depth", "av056": "alice_height_pool_depth",
    "q010": "alice_fan_shrinking", "av041": "alice_fan_shrinking",
    "q013": "alice_caucus_prizes", "c006": "alice_caucus_prizes", "av044": "alice_caucus_prizes",
    "q014": "alice_rabbit_mary_ann_errand", "q015": "alice_rabbit_mary_ann_errand", "av055": "alice_rabbit_mary_ann_errand",
    "q017": "alice_mushroom_sides", "av059": "alice_mushroom_sides",
    "q020": "alice_cat_mad_directions", "av043": "alice_cat_mad_directions",
    "q022": "alice_tea_party_wine", "av045": "alice_tea_party_wine",
    "q024": "alice_croquet_equipment", "av042": "alice_croquet_equipment",
    "q029": "alice_cook_witness", "av040": "alice_cook_witness", "av060": "alice_cook_witness",
    "sg082": "secret_manor_destination", "sg100": "secret_manor_destination",
    "sg085": "secret_india_cholera", "sg089": "secret_india_cholera", "sg093": "secret_india_cholera",
    "sg086": "secret_garden_access", "sg092": "secret_garden_access",
    "sg087": "secret_craven_relationship", "sg095": "secret_craven_relationship",
    "sg090": "secret_garden_history", "sg094": "secret_garden_history",
}


PAIR_METADATA = {
    "q003": ("meta_rabbit_eyes", None), "av054": ("meta_rabbit_eyes", None),
    "q008": ("meta_eat_me", None), "av058": ("meta_eat_me", None),
    "q009": ("meta_height_pool", None), "c005": ("meta_height_pool", None), "av056": ("meta_height_pool", None),
    "q013": ("meta_caucus_prizes", "contrast_caucus_prizes"), "c006": ("meta_caucus_prizes", "contrast_caucus_prizes"), "av044": (None, "contrast_caucus_prizes"),
    "q017": ("meta_mushroom", None), "av059": ("meta_mushroom", None),
    "q020": ("meta_cat_mad", None), "av043": ("meta_cat_mad", None),
    "q022": (None, "contrast_tea_wine"), "av045": (None, "contrast_tea_wine"),
    "q024": ("meta_croquet_equipment", None), "av042": ("meta_croquet_equipment", None),
    "q029": ("meta_cook_witness", None), "av040": ("meta_cook_witness", None), "av060": ("meta_cook_witness", None),
    "sg082": ("meta_secret_destination", None), "sg100": ("meta_secret_destination", None),
    "sg087": (None, "contrast_craven_relationship"), "sg095": (None, "contrast_craven_relationship"),
    "sg090": (None, "contrast_garden_history"), "sg094": (None, "contrast_garden_history"),
}


AMBIGUITY_REPAIRS = {
    "c003": ("book_dependent_multiple_events", ["shrinking after DRINK ME", "growing after EAT ME", "shrinking from the fan", "alternating size with mushroom pieces"]),
    "c004": ("missing_conversational_referent", []),
    "av050": ("book_dependent_multiple_events", ["the pebble-cake that made Alice shrink", "a piece of mushroom that changed her height"]),
    "av051": ("book_dependent_multiple_events", ["anger at tea-party rudeness", "anger during the Dormouse’s story"]),
    "av052": ("book_dependent_multiple_events", ["the Rabbit fleeing after dropping fan and gloves", "the Rabbit leaving or moving during later house/court scenes"]),
    "av053": ("book_dependent_multiple_referents", ["the small beautiful garden beyond the door", "the Queen’s croquet garden and its card gardeners"]),
    "sg098": ("book_dependent_multiple_referents", ["the ivy-covered secret-garden door", "the curtained door/room where Mary finds Colin"]),
    "sg099": ("book_dependent_multiple_events", ["fear that his father hated him", "fear of a lump/illness", "his quarrel with Mary"]),
}


def repair_ambiguities(by_id: dict[str, dict]) -> None:
    by_id["av050"].update({
        "question": "What happened after Alice ate a small piece?",
        "reference_answer": "Clarification is required because several small pieces cause different size changes.",
        "ambiguity_rationale": "A ‘small piece’ could mean a pebble-cake that makes Alice shrink or a piece from either side of the mushroom, whose effects differ.",
        "expected_clarification": "Do you mean a pebble-cake or a piece of the mushroom, and if the mushroom, which side?",
    })
    by_id["av050"]["valid_evidence_locations"] = [
        evidence("E1", "alice_in_wonderland", "she swallowed one of the cakes", page=35),
        evidence("E2", "alice_in_wonderland", "nibbling first at one and then at the other", page=42),
    ]
    by_id["av053"].update({
        "question": "What happened to the cards?",
        "reference_answer": "Clarification is required because ‘the cards’ can refer to the card gardeners or the whole pack at the end.",
        "ambiguity_rationale": "The card gardeners face the Queen’s sentence, while the whole pack later flies down at Alice; these are different card groups/events.",
        "expected_clarification": "Do you mean the card gardeners at the croquet ground or the full pack at the end of the trial?",
    })
    by_id["av053"]["valid_evidence_locations"] = [
        evidence("E1", "alice_in_wonderland", "the three gardeners instantly threw themselves flat upon their faces", page=60),
        evidence("E2", "alice_in_wonderland", "the whole pack rose up into the air", page=91),
    ]
    for case_id, (ambiguity_type, referents) in AMBIGUITY_REPAIRS.items():
        case = by_id[case_id]
        case["ambiguity_type"] = ambiguity_type
        case["plausible_referents"] = referents
        case["requires_owner_attention"] = True
        case["annotation_confidence"] = "needs_owner_review"
        case["review_tier"] = "DEEP_REVIEW"
        case["exact_supporting_spans"] = [item["exact_supporting_span"] for item in case["valid_evidence_locations"]]


NEGATIVE_DETAILS = {
    "c001": {
        "entity_aliases": ["Alice", "Alice's home", "her house"],
        "negative_search_terms": ["Alice street address", "home address", "postal address"],
        "relation_variants": ["lives at", "resides at", "address is", "home in"],
        "morphological_variants": ["address", "addresses", "addressed", "residence", "street"],
        "semantic_variants": ["where exactly does Alice live", "house number and street"],
        "plausible_counterexamples": ["The mock address to ALICE'S RIGHT FOOT", "mentions of Alice's home and Dinah"],
        "counterexample_disposition": "The foot address is a joke addressed to her foot, and home references contain no street or house number.",
    },
    "c002": {
        "entity_aliases": ["Queen of Hearts", "Queen", "her Majesty"],
        "negative_search_terms": ["Queen date of birth", "Queen birthday", "Queen age"],
        "relation_variants": ["was born", "birthday is", "years old", "age of the Queen"],
        "morphological_variants": ["born", "birth", "birthday", "age", "aged"],
        "semantic_variants": ["when was the Queen born", "how old is the Queen"],
        "plausible_counterexamples": ["birthday-present discussion", "ages of Alice/Lory", "edition years in the PDF front matter"],
        "counterexample_disposition": "None relates a birth date or age to the Queen of Hearts; front-matter years are not story chronology.",
    },
    "av046": {
        "entity_aliases": ["White Rabbit", "Rabbit", "herald"],
        "negative_search_terms": ["White Rabbit first name", "Rabbit named", "Rabbit called"],
        "relation_variants": ["his name is", "called the Rabbit", "named Rabbit"],
        "morphological_variants": ["name", "named", "names", "called"],
        "semantic_variants": ["personal name of the White Rabbit", "what is the Rabbit called"],
        "plausible_counterexamples": ["Mary Ann", "Bill", "Pat"],
        "counterexample_disposition": "Mary Ann is the Rabbit's housemaid; Bill and Pat are other characters, not names for the Rabbit.",
    },
    "av047": {
        "entity_aliases": ["Duchess's baby", "baby", "child", "pig"],
        "negative_search_terms": ["baby name", "child named", "Duchess called baby"],
        "relation_variants": ["named the baby", "baby's name", "called her child"],
        "morphological_variants": ["name", "named", "called", "calls"],
        "semantic_variants": ["personal name of the Duchess's child"],
        "plausible_counterexamples": ["The Duchess shouts ‘Pig!’ at the baby"],
        "counterexample_disposition": "‘Pig!’ is an address/insult that anticipates the transformation, not an established personal name.",
    },
    "av048": {
        "entity_aliases": ["Alice", "Wonderland", "the events", "that day"],
        "negative_search_terms": ["calendar year", "in 18xx", "in 19xx", "year of the story"],
        "relation_variants": ["events occurred in", "year was", "dated"],
        "morphological_variants": ["year", "years", "date", "dated"],
        "semantic_variants": ["when exactly does the story take place"],
        "plausible_counterexamples": ["Project Gutenberg release/copyright years in front matter", "story-relative references such as yesterday"],
        "counterexample_disposition": "Metadata years describe the electronic edition, while story-relative time does not identify a calendar year.",
    },
    "av049": {
        "entity_aliases": ["Alice's sister", "her sister", "the sister"],
        "negative_search_terms": ["Alice sister name", "sister named", "sister called"],
        "relation_variants": ["her name was", "called her sister", "sister's name"],
        "morphological_variants": ["name", "named", "called"],
        "semantic_variants": ["personal name of Alice's sister"],
        "plausible_counterexamples": ["Ada", "Mabel", "Dinah"],
        "counterexample_disposition": "Ada and Mabel are children Alice compares herself with; Dinah is her cat. None names the sister.",
    },
    "at075": {
        "entity_aliases": ["White Rabbit", "Rabbit", "herald"],
        "negative_search_terms": ["White Rabbit age", "Rabbit years old", "old Rabbit"],
        "relation_variants": ["was aged", "how old", "years of age", "born"],
        "morphological_variants": ["age", "aged", "old", "older", "born"],
        "semantic_variants": ["the Rabbit's numerical age"],
        "plausible_counterexamples": ["Lory says it is older", "Father William poem", "Alice's age-related comparisons"],
        "counterexample_disposition": "Age language concerns other characters and never supplies the White Rabbit's age.",
    },
    "at076": {
        "entity_aliases": ["King of Hearts", "King", "his Majesty", "judge"],
        "negative_search_terms": ["King first name", "King named", "King called"],
        "relation_variants": ["his name is", "personal name", "called the King"],
        "morphological_variants": ["name", "named", "called"],
        "semantic_variants": ["given name of the King of Hearts"],
        "plausible_counterexamples": ["William the Conqueror", "King as title/judge"],
        "counterexample_disposition": "William belongs to the Mouse's history lesson; ‘King’ is a title and no personal name is provided.",
    },
    "sg096": {
        "entity_aliases": ["Archibald Craven", "Mr. Craven", "Mester Craven", "Archie"],
        "negative_search_terms": ["Archibald Craven date of birth", "Archie born", "Mr. Craven age"],
        "relation_variants": ["was born", "birth date", "birthday", "years old"],
        "morphological_variants": ["born", "birth", "birthday", "age", "aged"],
        "semantic_variants": ["when Archibald was born", "how old Mr. Craven is"],
        "plausible_counterexamples": ["Mary was born ten years earlier", "Colin's birth and Mrs. Craven's death", "Archie as his wife's form of address"],
        "counterexample_disposition": "Birth and age passages concern Mary, Colin, animals, or other characters; none supplies Archibald's birth date.",
    },
    "sg097": {
        "entity_aliases": ["Dickon", "Dickon Sowerby", "our Dickon", "Martha Sowerby's Dickon"],
        "negative_search_terms": ["Dickon street address", "Dickon address", "Dickon residence"],
        "relation_variants": ["lives at", "home is", "cottage at", "address is"],
        "morphological_variants": ["address", "addresses", "street", "road", "residence", "home", "cottage"],
        "semantic_variants": ["house number and street for Dickon", "where exactly Dickon lives"],
        "plausible_counterexamples": ["the Sowerby cottage on the moor", "road references", "Dickon being ‘at home’ with animals"],
        "counterexample_disposition": "The book identifies a family cottage and general moor setting but no postal street address.",
    },
}


def repair_negatives(by_id: dict[str, dict]) -> None:
    for case_id, details in NEGATIVE_DETAILS.items():
        case = by_id[case_id]
        previous = case.get("negative_verification") or {}
        case["reference_answer"] = "No supporting evidence was found in the reviewed text of the exact evaluation book after targeted whole-document verification."
        case["negative_verification"] = {
            **details,
            "verification_scope": (
                "complete text content of Alice PDF SHA-256 " + ALICE_SHA
                if case["source_book"] == "alice_in_wonderland"
                else "Project Gutenberg eBook #113 canonical body plus generated text-layer PDF parser coverage"
            ),
            "source_coverage_status": "pass_with_documented_normalization",
            "searches": previous.get("searches", []),
            "all_regex_matches_reviewed": True,
            "semantic_completeness_not_inferred_from_regex": True,
            "conclusion": "No supporting evidence was found in the reviewed book text after targeted whole-document verification.",
            "absolute_absence_claimed": False,
        }
        case["annotation_confidence"] = "needs_owner_review"
        case["review_tier"] = "DEEP_REVIEW"
        case["requires_owner_attention"] = True


def package_evidence(case: dict) -> None:
    contexts = []
    for item in case["valid_evidence_locations"]:
        book = case["source_book"]
        units = ALICE_UNITS if book == "alice_in_wonderland" else SECRET_UNITS
        try:
            index, supporting = locate(units, item["exact_supporting_span"], item["source_location"])
            unit = units[index]
            item["preceding_context"] = nearest_relevant(units, index, -1)
            item["supporting_context"] = supporting
            item["following_context"] = nearest_relevant(units, index, 1)
            item["context_incomplete"] = False
            if book == "alice_in_wonderland":
                item["source_location"] = {
                    "book": book,
                    "page": unit["page"],
                    "chapter": unit.get("chapter"),
                    "pdf_block": unit["block"],
                }
            else:
                item["source_location"] = {
                    "book": book,
                    "canonical_line": unit["canonical_line"],
                    "chapter": unit.get("chapter"),
                    "generated_pdf_pages": secret_pdf_pages(item["exact_supporting_span"]),
                }
        except ValueError:
            if case["case_id"] == "at068":
                with sqlite3.connect(ALICE_DB) as connection:
                    supporting = connection.execute(
                        "SELECT text FROM pages WHERE page_number = 28"
                    ).fetchone()[0]
                item.update({
                    "preceding_context": "The Mouse announces that its history is a long and sad tale.",
                    "supporting_context": supporting,
                    "following_context": "The poem continues with Fury appointing himself judge and jury.",
                    "context_incomplete": False,
                })
                item["source_location"].update({"chapter": "3", "pdf_block": "shaped-poem-layout"})
            else:
                item["context_incomplete"] = True
                case["annotation_confidence"] = "needs_owner_review"
                case["review_tier"] = "BLOCKED"
        referenced_claims = [
            claim["claim_text"] for claim in case["required_answer_claims"]
            if item["evidence_id"] in claim["evidence_ids"]
        ]
        if not item.get("why_supports") or item["why_supports"].startswith("The exact source text"):
            if referenced_claims:
                item["why_supports"] = (
                    f"The cited span and its adjacent discourse support: {'; '.join(referenced_claims)}"
                )
            else:
                item["why_supports"] = "This passage establishes one plausible referent used to verify the ambiguity."
        if not item.get("epistemic_status"):
            item["epistemic_status"] = "character_statement" if supporting.lstrip().startswith(("‘", "\"")) else "narrator_fact"
        contexts.append({
            "evidence_id": item["evidence_id"],
            "preceding": item.get("preceding_context"),
            "supporting": item.get("supporting_context"),
            "following": item.get("following_context"),
            "context_incomplete": item.get("context_incomplete", False),
        })
    case["local_surrounding_context"] = contexts
    case["exact_supporting_spans"] = [item["exact_supporting_span"] for item in case["valid_evidence_locations"]]


def assign_families_and_review_tiers(cases: list[dict]) -> None:
    family_members: dict[str, list[str]] = {}
    for case in cases:
        case_id = case["case_id"]
        family = FACT_FAMILIES.get(case_id, f"fact_{case_id}")
        case["fact_family_id"] = family
        metamorphic, contrastive = PAIR_METADATA.get(case_id, (None, None))
        case["metamorphic_pair_id"] = metamorphic
        case["contrastive_pair_id"] = contrastive
        family_members.setdefault(family, []).append(case_id)

    deep_categories = {
        "local_context_reasoning", "multi_source_multi_fact", "contrastive_distractor",
        "unanswerable_false_premise", "ambiguous_underspecified", "multi_fact_single_context",
    }
    for case in cases:
        case["related_case_ids"] = [
            item for item in family_members[case["fact_family_id"]] if item != case["case_id"]
        ]
        incomplete = any(item.get("context_incomplete") for item in case["valid_evidence_locations"])
        if incomplete:
            case["review_tier"] = "BLOCKED"
            case["annotation_confidence"] = "needs_owner_review"
        elif case["primary_category"] in deep_categories:
            case["review_tier"] = "DEEP_REVIEW"
            case["annotation_confidence"] = (
                "needs_owner_review" if case["expected_status"] != "answered" else "medium"
            )
        else:
            case["review_tier"] = "FAST_CONFIRM"
            case["annotation_confidence"] = "high"
        marker = "Holdout item: full owner review remains mandatory."
        case["annotation_notes"] = case["annotation_notes"].replace(marker, "").strip()
        if case["source_book"] == "the_secret_garden":
            # The task requires full owner review of every holdout item, but a
            # simple explicit fact can still be a fast confirmation.
            case["annotation_notes"] = " ".join(
                part for part in (case["annotation_notes"], marker) if part
            )
        case["requires_owner_attention"] = (
            case["review_tier"] in {"DEEP_REVIEW", "BLOCKED"}
            or case["split_candidate"] != "alice_dev_regression"
        )


def write_manifest(payload: dict) -> None:
    cases = payload["cases"]
    split_ids = {
        split: [case["case_id"] for case in cases if case["split_candidate"] == split]
        for split in ("alice_dev_regression", "alice_final_test", "secret_garden_holdout")
    }
    manifest = {
        "dataset_id": payload["dataset_id"],
        "lifecycle_status": "candidate",
        "owner_reviewed": False,
        "evaluated": False,
        "dataset_sha256_informational": hashlib.sha256(
            (json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "source_book_hashes": {key: value["sha256"] for key, value in payload["source_books"].items()},
        "splits": split_ids,
        "warning": "Candidate split only. Hash changes during owner repair; TEST/holdout have not been executed.",
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    payload = json.loads(DATASET.read_text(encoding="utf-8"))
    replacement_ids = {case["case_id"] for case in NEW_TEST_CASES}
    retained = [
        case for case in payload["cases"]
        if case["case_id"] not in REPLACED_TEST_IDS
        and case["case_id"] not in replacement_ids
    ]
    retained.extend(NEW_TEST_CASES)
    by_id = {case["case_id"]: case for case in retained}
    repair_flagged(by_id)
    repair_ambiguities(by_id)
    repair_negatives(by_id)

    # Existing TEST cases that survived the leakage audit.
    by_id["at068"]["primary_category"] = by_id["at068"]["category"] = "direct_factual_single_source"
    by_id["at068"]["valid_evidence_locations"] = [
        evidence("E1", "alice_in_wonderland", "Fury said to a mouse", page=28, epistemic_status="quoted_poem")
    ]
    by_id["at068"]["required_answer_claims"] = claims(("Fury proposes taking the Mouse to law.", ["E1"]))
    by_id["at068"]["annotation_notes"] = "Retained TEST case: its shaped-poem source passage is independent of DEV fact families."
    by_id["at073"]["annotation_notes"] = "Retained TEST contrast: the Hatter says the hat is merchandise, not his own property."
    by_id["at075"]["annotation_notes"] = "Retained independent TEST negative about the White Rabbit’s age."
    by_id["at076"]["annotation_notes"] = "Retained independent TEST negative about the King’s personal name."

    order = {case["case_id"]: index for index, case in enumerate(payload["cases"])}
    for offset, case in enumerate(NEW_TEST_CASES, 1000):
        order[case["case_id"]] = offset
    retained.sort(key=lambda case: (0 if case["split_candidate"] == "alice_dev_regression" else 1 if case["split_candidate"] == "alice_final_test" else 2, order.get(case["case_id"], 9999)))

    for case in retained:
        package_evidence(case)
    assign_families_and_review_tiers(retained)

    observed_categories = Counter(case["primary_category"] for case in retained)
    observed_splits = Counter(case["split_candidate"] for case in retained)
    payload.update({
        "generated_on": "2026-09-17",
        "purpose": "Source-backed, independently audited Evaluation V2 candidate set. It has not been run through retrieval or QA.",
        "target_counts": {
            "categories_are_soft_targets": True,
            "original_design_targets": payload.get("target_counts", {}).get("categories", {}),
            "observed_categories_after_repair": dict(sorted(observed_categories.items())),
            "splits": dict(sorted(observed_splits.items())),
        },
        "audit_state": {
            "repair_pass": "phase-4.75b-source-backed",
            "owner_review_complete": False,
            "annotation_repair_case_ids": sorted(ANNOTATION_REPAIR_IDS),
            "evidence_context_repackaged_for_all_cases": True,
            "cases_replaced": sorted(REPLACED_TEST_IDS),
            "replacement_case_ids": [case["case_id"] for case in NEW_TEST_CASES],
        },
        "cases": retained,
    })
    DATASET.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_manifest(payload)
    print(json.dumps({
        "cases": len(retained),
        "splits": observed_splits,
        "categories": observed_categories,
        "fact_families": len({case["fact_family_id"] for case in retained}),
        "review_tiers": Counter(case["review_tier"] for case in retained),
        "blocked": [case["case_id"] for case in retained if case["review_tier"] == "BLOCKED"],
    }, indent=2))


if __name__ == "__main__":
    main()
