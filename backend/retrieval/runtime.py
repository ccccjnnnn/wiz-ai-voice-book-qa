import time
from collections.abc import Callable

from pydantic import BaseModel, ConfigDict, Field

from ingestion.models import Chunk

from .dense import DenseIndex


class RetrievalRequest(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    document_id: str = Field(min_length=1)
    index_version: str = Field(min_length=1)
    query: str = Field(min_length=1)
    top_k: int = Field(gt=0, le=50)


class RetrievalItem(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    chunk_id: str
    document_id: str
    text: str
    page_start: int
    page_end: int
    pages: list[int]
    rank: int
    score: float
    retrieval_method: str
    index_version: str
    method_metadata: dict = Field(default_factory=dict)


class RetrievalResponse(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    document_id: str
    index_version: str
    query: str
    retrieval_latency_ms: float = Field(ge=0)
    items: list[RetrievalItem]


class DenseRuntimeRetriever:
    """Typed boundary for the frozen exact-cosine winner; no generation concerns."""

    def __init__(
        self,
        document_id: str,
        index_version: str,
        chunks: list[Chunk],
        vectors: list[list[float]],
        embed_query: Callable[[str], list[float]],
    ):
        if any(chunk.document_id != document_id for chunk in chunks):
            raise ValueError("retriever_document_mismatch")
        self.document_id = document_id
        self.index_version = index_version
        self._index = DenseIndex(chunks, vectors)
        self._embed_query = embed_query

    def retrieve(self, request: RetrievalRequest) -> RetrievalResponse:
        if request.document_id != self.document_id:
            raise ValueError("retrieval_document_not_loaded")
        if request.index_version != self.index_version:
            raise ValueError("retrieval_index_version_not_loaded")
        started = time.perf_counter()
        query_vector = self._embed_query(request.query)
        hits = self._index.search(query_vector, request.top_k)
        latency_ms = (time.perf_counter() - started) * 1000
        return RetrievalResponse(
            document_id=request.document_id,
            index_version=request.index_version,
            query=request.query,
            retrieval_latency_ms=latency_ms,
            items=[
                RetrievalItem(
                    chunk_id=hit.chunk.chunk_id,
                    document_id=hit.chunk.document_id,
                    text=hit.chunk.text,
                    page_start=hit.chunk.page_start,
                    page_end=hit.chunk.page_end,
                    pages=hit.chunk.page_numbers,
                    rank=rank,
                    score=hit.score,
                    retrieval_method="dense_exact_cosine",
                    index_version=request.index_version,
                    method_metadata={"embedding_model": "voyage-4"},
                )
                for rank, hit in enumerate(hits, start=1)
            ],
        )
