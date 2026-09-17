#!/usr/bin/env python3
"""Idempotently remove low-value V2 holdout negatives.

The frozen candidate set prioritizes defensible ground truth over an
arbitrary round-number benchmark size.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "eval/v2/candidates.json"

REMOVE = {"sg096", "sg097"}

data = json.loads(DATASET.read_text(encoding="utf-8"))

before = len(data["cases"])
data["cases"] = [
    case for case in data["cases"]
    if case["case_id"] not in REMOVE
]
after = len(data["cases"])

data.setdefault("audit_state", {})["checkpoint_c_pruned_cases"] = {
    "removed_case_ids": sorted(REMOVE),
    "reason": (
        "Removed low-value whole-document negative holdout cases whose "
        "verification and maintenance cost exceeded their evaluation value. "
        "Dataset defensibility is prioritized over maintaining an arbitrary "
        "round-number size."
    ),
}

DATASET.write_text(
    json.dumps(data, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)

print(f"Cases before: {before}")
print(f"Cases after: {after}")
print("sg096/sg097 absent:", all(
    c["case_id"] not in REMOVE for c in data["cases"]
))
