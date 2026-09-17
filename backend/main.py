from pathlib import Path

from fastapi import FastAPI

from feedback.api import create_feedback_router
from ingestion.api import create_ingestion_router
from ingestion.service import IngestionService
from qa.api import create_qa_router
from qa.service import build_default_qa_service
from voice_smoke import VoiceError, get_ingestion_store, router as voice_router, voice_error


BACKEND_DIR = Path(__file__).resolve().parent


def create_app(
    data_dir: Path | None = None, qa_service_builder=None, index_client_factory=None
) -> FastAPI:
    resolved_data_dir = data_dir or BACKEND_DIR / "data"
    service = IngestionService(resolved_data_dir, index_client_factory=index_client_factory)
    app = FastAPI(title="WIZ.AI Voice Book QA")
    app.state.ingestion_service = service
    app.include_router(create_ingestion_router(service))
    # Voice providers stay backend-only, but share the product's one FastAPI process.
    app.include_router(voice_router)
    app.dependency_overrides[get_ingestion_store] = lambda: service.store
    app.add_exception_handler(VoiceError, voice_error)
    app.include_router(create_feedback_router(resolved_data_dir, service.store))
    app.include_router(
        create_qa_router(
            resolved_data_dir,
            service.store,
            qa_service_builder or build_default_qa_service,
        )
    )
    return app


app = create_app()
