import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

from app.config import settings
from app.routers import transcribe, query, chat, consultations, health, audio

app = FastAPI(
    title="DrDejaVu API",
    description="Voice-First Longitudinal Health Memory — powered by Eigen AI",
    version="1.0.0",
)

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# In development, also allow Codespaces / Gitpod forwarded URLs
if settings.app_env == "development":
    allowed_origins.append("https://*.app.github.dev")
    allowed_origins.append("https://*.github.dev")
    allowed_origins.append("https://*.gitpod.io")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.app_env == "development" else allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(">> %s %s (origin=%s)", request.method, request.url.path, request.headers.get("origin", "none"))
        response = await call_next(request)
        logger.info("<< %s %s -> %s", request.method, request.url.path, response.status_code)
        return response


app.add_middleware(RequestLogMiddleware)

app.include_router(health.router, tags=["Health"])
app.include_router(audio.router, prefix="/api", tags=["Audio"])
app.include_router(transcribe.router, prefix="/api", tags=["Transcription"])
app.include_router(query.router, prefix="/api", tags=["Query"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(consultations.router, prefix="/api", tags=["Consultations"])
