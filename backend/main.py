from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.research import router as research_router
from .api.stream import router as stream_router
from .db.database import engine, Base
from .db.models import ResearchSession  # noqa: F401
from .utils.telemetry import TelemetryMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs once on startup before the app accepts requests.
    """
    yield
    await engine.dispose()

app = FastAPI(
    title="Aria API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TelemetryMiddleware)

app.include_router(
    research_router,
)

app.include_router(
    stream_router,
)


@app.get("/health")
async def health():
    return {
        "status": "Ok",
        "service": "aria-api",
    }