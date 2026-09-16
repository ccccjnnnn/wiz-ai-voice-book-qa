import math
import re
from collections import Counter
from dataclasses import dataclass

from ingestion.models import Chunk

from .dense import DenseHit, DenseIndex


_TERM = re.compile(r"[\w]+(?:[’'][\w]+)?", re.UNICODE)


def tokenize_lexical(text: str) -> list[str]:
    return [match.group(0).casefold().replace("’", "'") for match in _TERM.finditer(text)]


@dataclass(frozen=True)
class LexicalHit:
    chunk: Chunk
    score: float


class BM25Index:
    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = 0.75):
        if not chunks:
            raise ValueError("BM25 requires chunks")
        self._chunks = chunks
        self._k1 = k1
        self._b = b
        self._frequencies = [Counter(tokenize_lexical(chunk.text)) for chunk in chunks]
        self._lengths = [sum(frequencies.values()) for frequencies in self._frequencies]
        self._average_length = sum(self._lengths) / len(self._lengths)
        document_frequency: Counter[str] = Counter()
        for frequencies in self._frequencies:
            document_frequency.update(frequencies.keys())
        count = len(chunks)
        self._idf = {
            term: math.log(1 + (count - frequency + 0.5) / (frequency + 0.5))
            for term, frequency in document_frequency.items()
        }

    def search(self, query: str, top_k: int) -> list[LexicalHit]:
        if top_k <= 0:
            raise ValueError("top_k must be positive")
        terms = list(dict.fromkeys(tokenize_lexical(query)))
        hits: list[LexicalHit] = []
        for chunk, frequencies, length in zip(
            self._chunks, self._frequencies, self._lengths, strict=True
        ):
            score = 0.0
            for term in terms:
                frequency = frequencies.get(term, 0)
                if not frequency:
                    continue
                denominator = frequency + self._k1 * (
                    1 - self._b + self._b * length / self._average_length
                )
                score += self._idf.get(term, 0.0) * frequency * (self._k1 + 1) / denominator
            if score > 0:
                hits.append(LexicalHit(chunk=chunk, score=score))
        hits.sort(key=lambda hit: (-hit.score, hit.chunk.chunk_index))
        return hits[: min(top_k, len(hits))]


class HybridRRFIndex:
    def __init__(
        self,
        dense: DenseIndex,
        lexical: BM25Index,
        rrf_k: int = 60,
    ):
        if rrf_k <= 0:
            raise ValueError("rrf_k must be positive")
        self._dense = dense
        self._lexical = lexical
        self._rrf_k = rrf_k

    def search(self, query: str, query_vector: list[float], top_k: int) -> list[DenseHit]:
        dense_hits = self._dense.search(query_vector, top_k)
        lexical_hits = self._lexical.search(query, top_k)
        dense_rank = {hit.chunk.chunk_id: rank for rank, hit in enumerate(dense_hits, 1)}
        lexical_rank = {hit.chunk.chunk_id: rank for rank, hit in enumerate(lexical_hits, 1)}
        chunks = {hit.chunk.chunk_id: hit.chunk for hit in dense_hits}
        chunks.update({hit.chunk.chunk_id: hit.chunk for hit in lexical_hits})
        fused = []
        for chunk_id, chunk in chunks.items():
            d_rank = dense_rank.get(chunk_id)
            b_rank = lexical_rank.get(chunk_id)
            score = (1 / (self._rrf_k + d_rank) if d_rank else 0) + (
                1 / (self._rrf_k + b_rank) if b_rank else 0
            )
            fused.append(
                DenseHit(
                    chunk=chunk,
                    score=score,
                    method_metadata={
                        "dense_rank": d_rank,
                        "bm25_rank": b_rank,
                        "fusion": "rrf",
                        "rrf_k": self._rrf_k,
                    },
                )
            )
        fused.sort(key=lambda hit: (-hit.score, hit.chunk.chunk_index))
        return fused[: min(top_k, len(fused))]
