import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _csv_env(name: str, default: str) -> set[str]:
    raw = os.getenv(name, default)
    return {
        item.strip()
        for item in raw.split(",")
        if item.strip()
    }


class Settings:
    gemini_api_key: str = os.getenv(
        "GEMINI_API_KEY",
        "",
    )

    default_model: str = os.getenv(
        "DEFAULT_MODEL",
        "gemini-3.7-flash",
    )

    allowed_models: set[str] = _csv_env(
        "ALLOWED_MODELS",
        os.getenv(
            "DEFAULT_MODEL",
            "gemini-3.7-flash",
        ),
    )

    api_auth_enabled: bool = (
        os.getenv(
            "API_AUTH_ENABLED",
            "false",
        ).lower()
        == "true"
    )

    api_key: str = os.getenv(
        "API_KEY",
        "",
    )

    max_files: int = int(
        os.getenv(
            "MAX_FILES",
            "5",
        )
    )

    max_file_size_bytes: int = int(
        os.getenv(
            "MAX_FILE_SIZE_BYTES",
            str(50 * 1024 * 1024),
        )
    )

    max_request_size_bytes: int = int(
        os.getenv(
            "MAX_REQUEST_SIZE_BYTES",
            str(100 * 1024 * 1024),
        )
    )

    allowed_mime_types: set[str] = _csv_env(
    "ALLOWED_MIME_TYPES",
    ",".join(
        [
            # Documents
            "application/pdf",
            "text/plain",
            "text/csv",
            "application/json",
            "text/html",
            "text/markdown",

            # Images
            "image/jpeg",
            "image/png",
            "image/webp",
            "image/bmp",

            # Office
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",

            # Audio
            "audio/mpeg",
            "audio/wav",
            "audio/ogg",

            # Video
            "video/mp4",
            "video/mpeg",
            "video/webm",
        ]
        ),
    )

    default_temperature: float = float(
        os.getenv(
            "DEFAULT_TEMPERATURE",
            "0.2",
        )
    )

    default_max_output_tokens: int = int(
        os.getenv(
            "DEFAULT_MAX_OUTPUT_TOKENS",
            "2048",
        )
    )

    temp_upload_dir: Path = Path(
        os.getenv(
            "TEMP_UPLOAD_DIR",
            "tmp/uploads",
        )
    )


settings = Settings()