from fastapi import FastAPI

from .api.research import router as research_router

app = FastAPI(
    title="Aria API",
    version="1.0.0"
)

app.include_router(
    research_router
)
@app.get("/health")
async def health():
    return {
        "status":"Ok",
        "service":"aria-api"
    }