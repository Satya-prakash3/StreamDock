from fastapi import FastAPI
from api.core.logging import logger
from api.core.config import settings

app = FastAPI(title=settings.app_name, version="0.1.0")


@app.get("/", include_in_schema=False)
def root():
    return {"message": "Welcome to Universal Video Downloader Backend. See /api/v1/hello"}


@app.get("/health", tags=["Health"])
async def health_check():
    logger.info("Health check requested")
    return {"status": "ok", "env": settings.app_env}
