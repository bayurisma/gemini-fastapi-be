from pathlib import Path

from app.services.processors.base import FileProcessor


class ImageProcessor(FileProcessor):
    
    IMAGE_TYPES = {
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/bmp",
    }
    
    def supports(self, mime_type: str) -> bool:
        return mime_type in self.IMAGE_TYPES

    def process(self, path: Path, filename: str, mime_type: str):
        # Implementation for processing image files
        return {
            "type": "gemini_file",
            "path": path,
            "filename": filename,
            "mime_type": mime_type,
        }