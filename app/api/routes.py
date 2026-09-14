import uuid
from typing import Annotated

from fastapi import APIRouter, File, Form, Path, UploadFile

from app.core.config import settings
from app.exceptions.errors import AppError
from app.services.file_service import (
    TemporaryFileService,
)
from app.services.gemini_service import (
    gemini_service,
)

router = APIRouter()

file_service = TemporaryFileService()

@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/v1/generate")
async def generate(
    prompt: Annotated[str, Form(min_length=1, max_length=20_000)],
    files: Annotated[list[UploadFile] | None, File(),] = None,
    ):
    
    selected_files = files or []
    
    if len(selected_files) > settings.max_files:
        raise AppError(
            "TOO_MANY_FILES",
            f"Number of files exceeds the limit of {settings.max_files}.",
            400,
        )
        
    request_id = uuid.uuid4().hex
    
    request_dir = (
        file_service.create_request_dir(request_id)
    )
    
    local_files: list[tuple[Path, str, str]] = []
    
    try:
        for upload in selected_files:
            path, size = await file_service.save_upload(
                upload,
                request_dir,
            )
            local_files.append(
                (
                    path,
                    upload.content_type or "application/octet-stream",
                    upload.filename or path.name,
                )
            )
        
        result = gemini_service.generate(
            prompt=prompt,
            files=local_files,
            model=settings.default_model,
        )
        
        return {
            "request_id": request_id,
            "status": "success",
            "result": result,
        }
    
    finally:
        file_service.cleanup_request_dir(request_dir)