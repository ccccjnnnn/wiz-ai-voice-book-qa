import time

from retrieval.runtime import RetrievalResponse

from .models import EvidencePack, PackedSource


DEFAULT_EVIDENCE_TOKEN_BUDGET = 3_000
DEFAULT_CANDIDATE_DEPTH = 10


def pack_evidence(
    retrieval: RetrievalResponse,
    token_budget: int = DEFAULT_EVIDENCE_TOKEN_BUDGET,
) -> tuple[EvidencePack, float]:
    """Pack whole chunks in retrieval order without model-based rewriting."""
    if token_budget <= 0:
        raise ValueError("invalid_evidence_token_budget")
    started = time.perf_counter()
    selected = []
    used_tokens = 0
    seen_chunk_ids: set[str] = set()
    seen_text: set[str] = set()
    for item in sorted(retrieval.items, key=lambda candidate: candidate.rank):
        if item.chunk_id in seen_chunk_ids or item.text in seen_text:
            continue
        seen_chunk_ids.add(item.chunk_id)
        seen_text.add(item.text)
        if used_tokens + item.estimated_tokens > token_budget:
            continue
        source_id = f"S{len(selected) + 1}"
        selected.append(
            PackedSource(
                source_id=source_id,
                chunk_id=item.chunk_id,
                document_id=item.document_id,
                index_version=item.index_version,
                source_filename=item.source_filename,
                pages=item.pages,
                retrieval_rank=item.rank,
                score=item.score,
                estimated_tokens=item.estimated_tokens,
                text=item.text,
            )
        )
        used_tokens += item.estimated_tokens
    result = EvidencePack(
        document_id=retrieval.document_id,
        index_version=retrieval.index_version,
        candidate_count=len(retrieval.items),
        token_budget=token_budget,
        estimated_tokens=used_tokens,
        sources=selected,
    )
    return result, (time.perf_counter() - started) * 1000
