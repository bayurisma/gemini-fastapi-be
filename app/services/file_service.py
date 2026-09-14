import re
import uuid
import shutil
from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings
from app.exceptions.errors import AppError


_FILENAME_RE = re.compile(r"[^A-Za-z0-9._-]+")


class TemporaryFileService:
    def __init__(self) -> None:
        settings.temp_upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def create_request_dir(self, request_id: str) -> Path:
        directory = settings.temp_upload_dir / request_id
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )
        return directory

    async def save_upload(
        self,
        upload: UploadFile,
        request_dir: Path,
    ) -> tuple[Path, int]:

        if not upload.filename:
            raise AppError(
                "INVALID_FILENAME",
                "Uploaded file has no filename.",
                400,
            )

        if upload.content_type not in settings.allowed_mime_types:
            raise AppError(
                "INVALID_FILE_TYPE",
                f"Unsupported MIME type: "
                f"{upload.content_type or 'unknown'}",
                400,
            )

        safe_name = _FILENAME_RE.sub(
            "_",
            Path(upload.filename).name,
        ).strip("._")

        if not safe_name:
            safe_name = f"upload-{uuid.uuid4().hex}"

        destination = (
            request_dir
            / f"{uuid.uuid4().hex}-{safe_name}"
        )

        total_size = 0

        try:
            await upload.seek(0)

            with destination.open("wb") as output:
                while True:
                    chunk = await upload.read(
                        1024 * 1024
                    )

                    if not chunk:
                        break

                    total_size += len(chunk)

                    if (
                        total_size
                        > settings.max_file_size_bytes
                    ):
                        raise AppError(
                            "FILE_TOO_LARGE",
                            f"{upload.filename} exceeds "
                            "the configured file size limit.",
                            413,
                        )

                    output.write(chunk)

        finally:
            await upload.close()

        return destination, total_size  
    
    def cleanup_request_dir(self, request_dir: Path) -> None:
        if request_dir.exists():
            shutil.rmtree(request_dir, ignore_errors=True)