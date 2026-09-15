from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class DocumentStatus(str, Enum):
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class Document(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    document_id: str
    source_filename: str
    status: DocumentStatus
    file_size_bytes: int = Field(ge=0)
    page_count: int = Field(default=0, ge=0)
    chunk_count: int = Field(default=0, ge=0)
    error_code: str | None = None
    created_at: datetime
    updated_at: datetime


class Page(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    document_id: str
    page_number: int = Field(ge=1)
    source_filename: str
    text: str
    char_count: int = Field(ge=0)
    has_images: bool = False


class Chunk(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    chunk_id: str
    document_id: str
    chunk_index: int = Field(ge=0)
    text: str = Field(min_length=1)
    page_start: int = Field(ge=1)
    page_end: int = Field(ge=1)
    page_numbers: list[int] = Field(min_length=1)
    source_filename: str

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
        return self
