from pathlib import Path

from fastapi import FastAPI

from ingestion.api import create_ingestion_router
from ingestion.service import IngestionService


BACKEND_DIR = Path(__file__).resolve().parent


def create_app(data_dir: Path | None = None) -> FastAPI:
    service = IngestionService(data_dir or BACKEND_DIR / "data")
    app = FastAPI(title="WIZ.AI Voice Book QA")
    app.state.ingestion_service = service
    app.include_router(create_ingestion_router(service))
    return app


app = create_app()
