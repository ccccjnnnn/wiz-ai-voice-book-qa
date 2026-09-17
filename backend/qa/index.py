from pathlib import Path

from ingestion.models import DocumentStatus
from ingestion.store import IngestionStore
from retrieval.evaluate import _cache_path, _load_vector_cache
from retrieval.runtime import DenseRuntimeRetriever
from retrieval.voyage import VoyageEmbeddingClient


FROZEN_INDEX_VERSION = "fixed-window-dense-v1"
EMBEDDING_MODEL = "voyage-4"


def load_frozen_retriever(
    store: IngestionStore,
    data_dir: Path,
    document_id: str,
    index_version: str,
    voyage: VoyageEmbeddingClient,
) -> DenseRuntimeRetriever:
    if index_version != FROZEN_INDEX_VERSION:
        raise ValueError("index_version_unavailable")
    document = store.get_document(document_id)
    if document is None:
        raise ValueError("document_not_found")
    if document.status != DocumentStatus.READY or not document.ready_for_qa:
        raise ValueError("document_not_ready")
    chunks = store.list_chunks(document_id)
    cache = _load_vector_cache(
        _cache_path(data_dir, document_id, EMBEDDING_MODEL),
        document_id,
        EMBEDDING_MODEL,
        chunks,
    )
    if cache is None or not cache.get("complete"):
        raise ValueError("index_unavailable")

    def embed_query(query: str) -> list[float]:
        response = voyage.embed([query], "query")
        if response.model != EMBEDDING_MODEL:
            raise ValueError("query_embedding_model_mismatch")
        return response.vectors[0]

    return DenseRuntimeRetriever(
        document_id=document_id,
        index_version=index_version,
        chunks=chunks,
        vectors=cache["vectors"],
        embed_query=embed_query,
    )
