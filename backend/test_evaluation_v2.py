"""Offline guard tests for the unexecuted Evaluation V2 candidate set."""

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class EvaluationV2CandidateTests(unittest.TestCase):
    def test_candidate_validator(self):
        path = ROOT / "scripts/evaluation/validate_v2_candidates.py"
        spec = importlib.util.spec_from_file_location("validate_v2_candidates", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = module.validate()
        self.assertEqual(result["cases"], 98)
        self.assertEqual(result["historical"], 36)
        self.assertEqual(result["test_or_holdout_executed"], 0)

    def test_review_artifact_is_explicitly_candidate_and_has_owner_fields(self):
        review = (ROOT / "eval/v2/review/OWNER_GROUND_TRUTH_REVIEW.md").read_text()
        self.assertIn("CANDIDATE ONLY", review)
        self.assertEqual(review.count("Owner ground-truth decision:"), 98)
        self.assertEqual(review.count("<details>"), 98)
        self.assertNotIn("human-verified", review.casefold())

    def test_holdout_source_is_pinned_but_generated_book_is_not_committed(self):
        source = json.loads((ROOT / "eval/v2/sources/secret_garden.json").read_text())
        self.assertEqual(
            source["canonical_text_sha256"],
            "6b0bb5fbd0c4e873d2d22028da9d753cf3977d5f70ac58221556b28060badbf5",
        )
        self.assertFalse(source["generated_pdf_committed"])
        self.assertEqual(source["latest_local_coverage"]["chapter_count"], 27)
        self.assertEqual(source["latest_local_coverage"]["coverage_status"], "pass")


if __name__ == "__main__":
    unittest.main()
