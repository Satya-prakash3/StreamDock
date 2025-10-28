from fastapi import FastAPI
from api.v1 import hello
from api.core.config import settings

app = FastAPI(title="Universal Video Downloader API", version="0.1.0")

# include routers
app.include_router(hello.router, prefix="/api/v1")

@app.get("/", include_in_schema=False)
def root():
    return {"message": "Welcome to Universal Video Downloader Backend. See /api/v1/hello"}
