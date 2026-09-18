"""Offline guards for the one-time final V2 holdout runner."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/evaluation/run_final_holdouts.py"
SPEC = importlib.util.spec_from_file_location("run_final_holdouts", RUNNER)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class FinalHoldoutRunnerTests(unittest.TestCase):
    def test_final_split_guards_preserve_exact_membership(self):
        alice, alice_guard = MODULE.load_split("alice_final_test")
        secret, secret_guard = MODULE.load_split("secret_garden_holdout")
        self.assertEqual(len(alice), 20)
        self.assertEqual(len(secret), 18)
        self.assertEqual([case["case_id"] for case in alice], alice_guard["case_ids"])
        self.assertEqual([case["case_id"] for case in secret], secret_guard["case_ids"])

    def test_completed_artifact_cannot_be_resumed_or_overwritten(self):
        _, guard = MODULE.load_split("alice_final_test")
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.json"
            state = MODULE._new_state("alice_final_test", guard, "doc")
            state["status"] = "complete"
            output.write_text(json.dumps(state), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "final_holdout_already_complete"):
                MODULE._load_or_create_state(
                    output, "alice_final_test", guard, "doc", resume=True
                )

    def test_incomplete_artifact_requires_explicit_resume_and_matching_guard(self):
        _, guard = MODULE.load_split("alice_final_test")
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.json"
            state = MODULE._new_state("alice_final_test", guard, "doc")
            output.write_text(json.dumps(state), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "use_resume"):
                MODULE._load_or_create_state(
                    output, "alice_final_test", guard, "doc", resume=False
                )
            loaded = MODULE._load_or_create_state(
                output, "alice_final_test", guard, "doc", resume=True
            )
            self.assertEqual(loaded["results"], [])

    def test_case_scoring_distinguishes_packing_from_retrieval(self):
        case = {
            "case_id": "case",
            "question": "Question?",
            "category": "test",
            "expected_status": "answered",
            "reference_answer": "Answer.",
            "valid_evidence_locations": [
                {
                    "evidence_id": "E1",
                    "exact_supporting_span": "gold phrase",
                    "source_location": {"page": 7},
                }
            ],
            "required_answer_claims": [
                {"claim_id": "C1", "claim_text": "Claim", "evidence_ids": ["E1"]}
            ],
        }
        response = {
            "status": "answered",
            "answer": "Answer.",
            "clarification": None,
            "reason": None,
            "citations": [{"source_id": "S1", "pages": [7]}],
            "trace_id": "trace",
            "error": None,
        }
        trace = {
            "retrieved_candidates": [{"text": "gold phrase", "pages": [7]}],
            "packed_evidence": [{"text": "other text", "pages": [8]}],
        }
        scored = MODULE.score_case(case, response, trace)
        self.assertTrue(scored["checks"]["dense_full_evidence_coverage"])
        self.assertFalse(scored["checks"]["packed_full_evidence_coverage"])
        self.assertEqual(scored["failure_classification"], "evidence_packing")


if __name__ == "__main__":
    unittest.main()
