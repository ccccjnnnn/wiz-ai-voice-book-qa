import math
from dataclasses import dataclass, field

from ingestion.models import Chunk


@dataclass(frozen=True)
class DenseHit:
    chunk: Chunk
    score: float
    method_metadata: dict = field(default_factory=dict)


class DenseIndex:
    """Small exact-cosine index; adequate and inspectable for a single book."""

    def __init__(self, chunks: list[Chunk], vectors: list[list[float]]):
        if not chunks or len(chunks) != len(vectors):
            raise ValueError("chunks and vectors must be non-empty and aligned")
        dimensions = {len(vector) for vector in vectors}
        if len(dimensions) != 1 or 0 in dimensions:
            raise ValueError("embedding dimensions must be non-empty and consistent")
        if any(not math.isfinite(value) for vector in vectors for value in vector):
            raise ValueError("embeddings must contain finite values")
        norms = [math.sqrt(sum(value * value for value in vector)) for vector in vectors]
        if any(norm == 0 for norm in norms):
            raise ValueError("zero-length embedding is invalid")
        self._chunks = chunks
        self._vectors = vectors
        self._norms = norms
        self.dimensions = dimensions.pop()

    def search(self, query_vector: list[float], top_k: int) -> list[DenseHit]:
        if len(query_vector) != self.dimensions:
            raise ValueError("query embedding dimension mismatch")
        if top_k <= 0:
            raise ValueError("top_k must be positive")
        query_norm = math.sqrt(sum(value * value for value in query_vector))
        if query_norm == 0 or not math.isfinite(query_norm):
            raise ValueError("query embedding is invalid")
        hits = []
        for chunk, vector, vector_norm in zip(
            self._chunks, self._vectors, self._norms, strict=True
        ):
            score = sum(a * b for a, b in zip(query_vector, vector, strict=True))
            score /= query_norm * vector_norm
            hits.append(DenseHit(chunk=chunk, score=score))
        hits.sort(key=lambda hit: (-hit.score, hit.chunk.chunk_index))
        return hits[: min(top_k, len(hits))]
