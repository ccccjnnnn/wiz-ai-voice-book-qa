from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile, status

from .models import Chunk, Document, DocumentStatus, Page
from .service import IngestionService, UploadError


def create_ingestion_router(service: IngestionService) -> APIRouter:
    router = APIRouter(prefix="/api/documents", tags=["documents"])

    def require_document(document_id: str) -> Document:
        document = service.store.get_document(document_id)
        if document is None:
            raise HTTPException(status_code=404, detail={"error": "document_not_found"})
        return document

    @router.post("", response_model=Document, status_code=status.HTTP_202_ACCEPTED)
    async def upload_document(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
    ) -> Document:
        try:
            document = await service.save_upload(file)
        except UploadError as error:
            raise HTTPException(
                status_code=error.status_code, detail={"error": error.code}
            ) from None
        background_tasks.add_task(service.process_document, document.document_id)
        return document

    @router.get("/{document_id}", response_model=Document)
    def get_document(document_id: str) -> Document:
        return require_document(document_id)

    @router.get("/{document_id}/pages", response_model=list[Page])
    def get_pages(document_id: str) -> list[Page]:
        document = require_document(document_id)
        if document.status != DocumentStatus.READY:
            raise HTTPException(status_code=409, detail={"error": "document_not_ready"})
        return service.store.list_pages(document_id)

    @router.get("/{document_id}/chunks", response_model=list[Chunk])
    def get_chunks(document_id: str) -> list[Chunk]:
        document = require_document(document_id)
        if document.status != DocumentStatus.READY:
            raise HTTPException(status_code=409, detail={"error": "document_not_ready"})
        return service.store.list_chunks(document_id)

    return router
