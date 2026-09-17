from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    PARSING = "parsing"
    READY = "ready"
    FAILED = "failed"


class IndexStatus(str, Enum):
    MISSING = "missing"
    INDEXING = "indexing"
    READY = "ready"
    PAUSED = "paused"
    STALE = "stale"
    FAILED = "failed"


class Document(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    document_id: str = Field(min_length=1)
    source_filename: str = Field(min_length=1)
    status: DocumentStatus
    file_size_bytes: int = Field(ge=0)
    page_count: int = Field(default=0, ge=0)
    chunk_count: int = Field(default=0, ge=0)
    error_code: str | None = None
    index_status: IndexStatus = IndexStatus.MISSING
    index_version: str | None = None
    index_error_code: str | None = None
    total_chunks: int = Field(default=0, ge=0)
    indexed_chunks: int = Field(default=0, ge=0)
    progress_percent: float = Field(default=0.0, ge=0.0, le=100.0)
    ready_for_qa: bool = False
    stage: str = "uploaded"
    asr_keyterms: list[str] = Field(default_factory=list, max_length=50)
    created_at: datetime
    updated_at: datetime


class Page(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    document_id: str = Field(min_length=1)
    page_number: int = Field(ge=1)
    source_filename: str = Field(min_length=1)
    text: str
    char_count: int = Field(ge=0)
    has_images: bool = False
    normalization_issues: list[str] = Field(default_factory=list)


class Chunk(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    chunk_id: str = Field(min_length=1)
    document_id: str = Field(min_length=1)
    chunk_index: int = Field(ge=0)
    text: str = Field(min_length=1)
    page_start: int = Field(ge=1)
    page_end: int = Field(ge=1)
    page_numbers: list[int] = Field(min_length=1)
    source_filename: str = Field(min_length=1)
    char_count: int = Field(gt=0)
    token_count: int = Field(gt=0)
    quality_issues: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_page_provenance(self):
        ordered_unique = sorted(set(self.page_numbers))
        if (
            self.page_end < self.page_start
            or self.page_numbers != ordered_unique
            or self.page_numbers[0] != self.page_start
            or self.page_numbers[-1] != self.page_end
        ):
            raise ValueError("invalid chunk page provenance")
        if self.char_count != len(self.text):
            raise ValueError("chunk char_count does not match text")
        return self
