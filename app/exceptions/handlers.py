from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.errors import AppError


async def app_error_handler(
    request: Request,
    exc: AppError,
):
    request_id = getattr(
        request.state,
        "request_id",
        "unknown",
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "request_id": request_id,
            }
        },
    )