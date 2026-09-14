from pathlib import Path

from app.services.processors.base import FileProcessor


class PDFProcessor(FileProcessor):
    
    def supports(
        self,
        mime_type: str,
    ) -> bool:
        return mime_type == "application/pdf"

    def process(
        self,
        path: Path,
        filename: str,
        mime_type: str,
    ):
        # Keep PDF intact.
        # Gemini can process PDF text and visual information.
        return {
            "type": "gemini_file",
            "path": path,
            "filename": filename,
            "mime_type": mime_type,
        }