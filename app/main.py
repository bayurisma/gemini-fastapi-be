import logging
import time
import uuid

from fastapi import FastAPI, Request

from app.api.routes import router
from app.api.cv_matching_routes import router as cv_matching_router
from app.exceptions.errors import AppError
from app.exceptions.handlers import app_error_handler

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Gemini AI Backend",
    version="0.1.0",
)

app.include_router(router)
app.include_router(cv_matching_router)
app.add_exception_handler(
    AppError,
    app_error_handler,
)

@app.middleware("http")
async def request_context(
    request: Request,
    call_next,
):

    request_id = request.headers.get(
        "X-Request-ID",
        uuid.uuid4().hex,
    )

    request.state.request_id = request_id

    started = time.perf_counter()

    response = await call_next(request)

    elapsed_ms = (
        time.perf_counter() - started
    ) * 1000

    response.headers["X-Request-ID"] = request_id

    logger.info(
        "%s %s status=%s latency_ms=%.2f",
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )

    return response