from pathlib import Path
from typing import Literal

from .evaluate import sha256_file
from .models import EvaluationDataset, FrozenEvaluationSplit


def load_frozen_split(path: Path) -> FrozenEvaluationSplit:
    try:
        return FrozenEvaluationSplit.model_validate_json(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise ValueError(f"invalid frozen split: {path}") from error


def validate_frozen_split(
    split: FrozenEvaluationSplit,
    dataset: EvaluationDataset,
    dataset_path: Path,
) -> None:
    if split.dataset_id != dataset.dataset_id:
        raise ValueError("split_dataset_id_mismatch")
    if split.dataset_sha256_at_freeze != sha256_file(dataset_path):
        raise ValueError("dataset_changed_after_split_freeze")
    expected_ids = {question.id for question in dataset.questions}
    split_ids = set(split.dev_question_ids).union(split.test_question_ids)
    if split_ids != expected_ids:
        raise ValueError("split_does_not_partition_dataset")


def select_dataset_subset(
    dataset: EvaluationDataset,
    split: FrozenEvaluationSplit,
    subset: Literal["dev", "test"],
) -> EvaluationDataset:
    selected_ids = set(
        split.dev_question_ids if subset == "dev" else split.test_question_ids
    )
    return dataset.model_copy(
        update={
            "dataset_id": f"{dataset.dataset_id}:{subset}",
            "questions": [
                question for question in dataset.questions if question.id in selected_ids
            ],
        }
    )
