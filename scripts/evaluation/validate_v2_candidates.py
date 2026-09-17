"""Offline structural validation for the unreleased Evaluation V2 candidate."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "eval" / "v2" / "candidates.json"
MANIFEST = ROOT / "eval" / "v2" / "split_manifest.candidate.json"
SOURCE_REPORT = ROOT / "eval" / "v2" / "sources" / "source_consistency_report.json"
SECRET_SOURCE = ROOT / "eval" / ".cache" / "books" / "secret-garden" / "pg113.txt"
EXPECTED_SPLITS = {
    "alice_dev_regression": 60,
    "alice_final_test": 20,
    "secret_garden_holdout": 18,
}
ALLOWED_CATEGORIES = {
    "direct_factual_single_source", "local_context_reasoning",
    "multi_source_multi_fact", "multi_fact_single_context",
    "paraphrase_vocabulary_mismatch", "contrastive_distractor",
    "unanswerable_false_premise", "ambiguous_underspecified",
    "voice_like_noisy_text",
}
NEGATIVE_FIELDS = {
    "entity_aliases", "negative_search_terms", "relation_variants",
    "morphological_variants", "semantic_variants", "plausible_counterexamples",
    "counterexample_disposition", "verification_scope", "source_coverage_status",
    "searches", "all_regex_matches_reviewed",
    "semantic_completeness_not_inferred_from_regex", "conclusion",
    "absolute_absence_claimed",
}
KNOWN_EXPOSED_TEST_IDS = {
    "at101", "at103", "at105", "at107", "at108", "at111", "at116",
}


def normalized_text(value: str) -> str:
    return " ".join(re.findall(
        r"[a-z0-9]+", unicodedata.normalize("NFKD", value).casefold()
    ))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def informational_hash(payload: dict) -> str:
    return hashlib.sha256(
        (json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n").encode()
    ).hexdigest()


def validate() -> dict:
    payload = json.loads(DATASET.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    source_report = json.loads(SOURCE_REPORT.read_text(encoding="utf-8"))
    cases = payload["cases"]
    errors: list[str] = []
    required = {
        "case_id", "lifecycle_status", "split_candidate", "source_book",
        "source_book_sha256", "question", "expected_status", "reference_answer",
        "required_answer_claims", "valid_evidence_locations",
        "exact_supporting_spans", "local_surrounding_context", "primary_category",
        "category", "tags", "difficulty", "annotation_notes",
        "annotation_confidence", "fact_family_id", "metamorphic_pair_id",
        "contrastive_pair_id", "related_case_ids", "review_tier",
        "evaluation_execution", "evidence_event_id", "development_exposure",
    }

    if payload.get("lifecycle_status") != "candidate" or payload.get("human_verified") is not False:
        errors.append("dataset must remain an unverified candidate")
    if payload.get("execution_state") != {
        "retrieval_run": False, "qa_run": False, "metrics_generated": False, "frozen": False
    }:
        errors.append("execution state must remain entirely false")

    ids = [case.get("case_id") for case in cases]
    if len(cases) != 98:
        errors.append(f"expected 98 repaired candidates, found {len(cases)}")
    duplicates = [case_id for case_id, count in Counter(ids).items() if count > 1]
    if duplicates:
        errors.append(f"duplicate case IDs: {duplicates}")
    split_counts = Counter(case.get("split_candidate") for case in cases)
    if split_counts != Counter(EXPECTED_SPLITS):
        errors.append(f"split counts differ: {dict(split_counts)}")

    family_members: dict[str, list[str]] = {}
    for case in cases:
        cid = case.get("case_id", "<missing>")
        missing = required - set(case)
        if missing:
            errors.append(f"{cid}: missing {sorted(missing)}")
            continue
        if case["lifecycle_status"] != "candidate" or case["evaluation_execution"] is not None:
            errors.append(f"{cid}: lifecycle/execution is not candidate-only")
        if case["primary_category"] != case["category"] or case["primary_category"] not in ALLOWED_CATEGORIES:
            errors.append(f"{cid}: invalid or inconsistent category")
        if not case["fact_family_id"]:
            errors.append(f"{cid}: missing fact family")
        else:
            family_members.setdefault(case["fact_family_id"], []).append(cid)
        if case["review_tier"] not in {"FAST_CONFIRM", "DEEP_REVIEW", "BLOCKED"}:
            errors.append(f"{cid}: invalid review tier")
        if not case["evidence_event_id"]:
            errors.append(f"{cid}: missing evidence event ID")
        exposure = case.get("development_exposure") or {}
        if not exposure.get("status") or "sources" not in exposure or not exposure.get("review_method"):
            errors.append(f"{cid}: incomplete development-exposure record")
        if case["source_book_sha256"] != payload["source_books"][case["source_book"]]["sha256"]:
            errors.append(f"{cid}: source hash differs from dataset source record")

        status = case["expected_status"]
        evidence = case["valid_evidence_locations"]
        evidence_ids = {item.get("evidence_id") for item in evidence}
        for item in evidence:
            if item.get("context_incomplete") is not False:
                errors.append(f"{cid}/{item.get('evidence_id')}: context is incomplete")
            if not item.get("supporting_context"):
                errors.append(f"{cid}/{item.get('evidence_id')}: supporting context missing")
            span = item.get("exact_supporting_span")
            if span and span.casefold() not in item.get("supporting_context", "").casefold():
                errors.append(f"{cid}/{item.get('evidence_id')}: exact span absent from context")
            if case["source_book"] == "the_secret_garden":
                location = item.get("source_location", {})
                if not location.get("generated_pdf_pages") or not location.get("canonical_line"):
                    errors.append(f"{cid}/{item.get('evidence_id')}: holdout source mapping missing")

        if status == "answered":
            if not case["required_answer_claims"] or not evidence:
                errors.append(f"{cid}: answered case lacks claims/evidence")
            if not case["exact_supporting_spans"] or not case["local_surrounding_context"]:
                errors.append(f"{cid}: answered case lacks exact/context evidence")
            for claim in case["required_answer_claims"]:
                if not claim.get("claim_text") or not claim.get("evidence_ids"):
                    errors.append(f"{cid}: empty material claim mapping")
                elif not set(claim["evidence_ids"]) <= evidence_ids:
                    errors.append(f"{cid}: claim references unknown evidence")
        elif status == "insufficient_evidence":
            check = case.get("negative_verification") or {}
            missing_negative = NEGATIVE_FIELDS - set(check)
            if missing_negative:
                errors.append(f"{cid}: negative check missing {sorted(missing_negative)}")
            if not all(check.get(field) for field in (
                "entity_aliases", "negative_search_terms", "relation_variants",
                "morphological_variants", "semantic_variants", "searches",
                "verification_scope", "counterexample_disposition",
            )):
                errors.append(f"{cid}: negative verification lacks search breadth")
            if check.get("absolute_absence_claimed") is not False:
                errors.append(f"{cid}: negative check claims absolute absence")
            if check.get("semantic_completeness_not_inferred_from_regex") is not True:
                errors.append(f"{cid}: regex results are treated as semantic proof")
            if "No supporting evidence was found" not in check.get("conclusion", ""):
                errors.append(f"{cid}: bounded negative conclusion missing")
            for search in check.get("searches", []):
                if search.get("all_matches_reviewed") is not True or not search.get("semantic_assessment"):
                    errors.append(f"{cid}: search result lacks semantic review")
                if case["source_book"] == "the_secret_garden" and search.get("generated_pdf_matches") is None:
                    errors.append(f"{cid}: holdout negative lacks generated-PDF cross-check")
        elif status == "ambiguous":
            if not case.get("ambiguity_rationale") or not case.get("expected_clarification"):
                errors.append(f"{cid}: ambiguity rationale/clarification missing")
            if not case.get("ambiguity_type"):
                errors.append(f"{cid}: ambiguity type missing")
            if case.get("ambiguity_type") == "book_dependent_multiple_referents" and len(evidence) < 2:
                errors.append(f"{cid}: book-dependent ambiguity lacks multiple referents")
            if case.get("ambiguity_type", "").startswith("book_dependent") and len(case.get("plausible_referents", [])) < 2:
                errors.append(f"{cid}: plausible book referents/events are not recorded")
        else:
            errors.append(f"{cid}: unknown expected status {status}")

    for field in ("metamorphic_pair_id", "contrastive_pair_id"):
        groups: dict[str, list[dict]] = {}
        for case in cases:
            if case.get(field):
                groups.setdefault(case[field], []).append(case)
        for group, members in groups.items():
            if len(members) < 2:
                errors.append(f"{field} {group}: only one member")
            member_ids = {case["case_id"] for case in members}
            for case in members:
                if not (member_ids - {case["case_id"]}) <= set(case["related_case_ids"]):
                    errors.append(f"{case['case_id']}: incomplete related IDs for {group}")

    dev_families = {
        case["fact_family_id"] for case in cases
        if case["split_candidate"] == "alice_dev_regression"
    }
    test_families = {
        case["fact_family_id"] for case in cases
        if case["split_candidate"] == "alice_final_test"
    }
    if dev_families & test_families:
        errors.append(f"Alice TEST shares DEV fact families: {sorted(dev_families & test_families)}")

    dev_events = {
        case["evidence_event_id"] for case in cases
        if case["split_candidate"] == "alice_dev_regression"
    }
    test_events = {
        case["evidence_event_id"] for case in cases
        if case["split_candidate"] == "alice_final_test"
    }
    if dev_events & test_events:
        errors.append(f"Alice TEST shares DEV evidence events: {sorted(dev_events & test_events)}")

    remaining_known = KNOWN_EXPOSED_TEST_IDS & set(ids)
    if remaining_known:
        errors.append(f"known development-exposed TEST cases remain: {sorted(remaining_known)}")

    dev_exposure_texts: list[str] = []
    for case in cases:
        if case["split_candidate"] != "alice_dev_regression":
            continue
        dev_exposure_texts.extend([case["question"], case["reference_answer"]])
        dev_exposure_texts.extend(claim.get("claim_text", "") for claim in case["required_answer_claims"])
        for item in case["valid_evidence_locations"]:
            dev_exposure_texts.extend(
                item.get(key) or "" for key in (
                    "exact_supporting_span", "preceding_context", "supporting_context", "following_context"
                )
            )
        for search in (case.get("negative_verification") or {}).get("searches", []):
            dev_exposure_texts.extend(
                match.get("excerpt", "")
                for match in search.get("canonical_or_parsed_source_matches", [])
            )
    normalized_dev = [normalized_text(value) for value in dev_exposure_texts if value]
    for case in cases:
        if case["split_candidate"] != "alice_final_test":
            continue
        exposure = case["development_exposure"]
        if exposure["status"] != "no_known_development_exposure" or exposure["sources"]:
            errors.append(f"{case['case_id']}: unresolved development exposure")
        for span in case["exact_supporting_spans"]:
            normalized_span = normalized_text(span)
            if len(normalized_span.split()) >= 4 and any(
                normalized_span in exposed for exposed in normalized_dev
            ):
                errors.append(
                    f"{case['case_id']}: exact answer span appears in development-visible material"
                )
    for case in cases:
        if case["split_candidate"] != "alice_dev_regression" and not case["requires_owner_attention"]:
            errors.append(f"{case['case_id']}: TEST/holdout is not marked for full owner review")

    if manifest.get("lifecycle_status") != "candidate" or manifest.get("evaluated") is not False:
        errors.append("manifest is not candidate-only")
    if manifest.get("owner_reviewed") is not False:
        errors.append("manifest incorrectly claims owner review")
    if manifest.get("dataset_sha256_informational") != informational_hash(payload):
        errors.append("manifest informational dataset hash mismatch")
    manifest_ids = [case_id for values in manifest.get("splits", {}).values() for case_id in values]
    if Counter(manifest_ids) != Counter(ids):
        errors.append("manifest split IDs differ from candidate dataset")
    for split, expected_count in EXPECTED_SPLITS.items():
        if len(manifest.get("splits", {}).get(split, [])) != expected_count:
            errors.append(f"manifest {split} count differs")
    if any(case["evaluation_execution"] is not None for case in cases if case["split_candidate"] != "alice_dev_regression"):
        errors.append("TEST/holdout contains execution data")

    if source_report.get("overall_status") != "pass":
        errors.append("source consistency report failed")
    secret = source_report.get("the_secret_garden", {})
    if secret.get("ordered_token_sequence_equal") is not True or secret.get("content_loss_detected") is not False:
        errors.append("Secret Garden representations are not content-equivalent")
    if secret.get("chapter_boundary_alignment") is not True:
        errors.append("Secret Garden chapter boundary alignment failed")
    if secret.get("canonical_text_sha256") != payload["source_books"]["the_secret_garden"]["sha256"]:
        errors.append("Secret Garden report source hash mismatch")
    if SECRET_SOURCE.exists() and sha256(SECRET_SOURCE) != payload["source_books"]["the_secret_garden"]["sha256"]:
        errors.append("cached Secret Garden canonical source hash mismatch")

    if errors:
        raise SystemExit("\n".join(errors))
    return {
        "cases": len(cases),
        "categories": dict(Counter(case["primary_category"] for case in cases)),
        "splits": dict(split_counts),
        "statuses": dict(Counter(case["expected_status"] for case in cases)),
        "historical": sum(case["historical_case"] for case in cases),
        "fact_families": len(family_members),
        "review_tiers": dict(Counter(case["review_tier"] for case in cases)),
        "blocked": [case["case_id"] for case in cases if case["review_tier"] == "BLOCKED"],
        "known_alice_test_development_exposures": 0,
        "test_or_holdout_executed": 0,
        "source_consistency": source_report["overall_status"],
    }


if __name__ == "__main__":
    print(json.dumps(validate(), indent=2))
