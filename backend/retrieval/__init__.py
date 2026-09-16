"""Measured dense-retrieval baseline for one ingested book."""

from .dense import DenseIndex
from .models import EvaluationDataset, EvaluationReport
from .voyage import VoyageEmbeddingClient

__all__ = ["DenseIndex", "EvaluationDataset", "EvaluationReport", "VoyageEmbeddingClient"]
