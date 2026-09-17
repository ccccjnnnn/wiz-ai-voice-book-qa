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
    source_filename: str
    estimated_tokens: int = Field(gt=0)


class RetrievalResponse(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    document_id: str
    index_version: str
    query: str
    retrieval_latency_ms: float = Field(ge=0)
    query_embedding_latency_ms: float = Field(ge=0)
    local_retrieval_latency_ms: float = Field(ge=0)
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
        embedding_started = time.perf_counter()
        query_vector = self._embed_query(request.query)
        embedding_latency_ms = (time.perf_counter() - embedding_started) * 1000
        retrieval_started = time.perf_counter()
        hits = self._index.search(query_vector, request.top_k)
        local_latency_ms = (time.perf_counter() - retrieval_started) * 1000
        return RetrievalResponse(
            document_id=request.document_id,
            index_version=request.index_version,
            query=request.query,
            retrieval_latency_ms=embedding_latency_ms + local_latency_ms,
            query_embedding_latency_ms=embedding_latency_ms,
            local_retrieval_latency_ms=local_latency_ms,
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
                    source_filename=hit.chunk.source_filename,
                    estimated_tokens=hit.chunk.token_count,
                )
                for rank, hit in enumerate(hits, start=1)
            ],
        )
