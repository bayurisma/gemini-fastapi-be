from pathlib import Path
from typing import Any

from google import genai
from google.genai import types

from app.core.config import settings
from app.exceptions.errors import AppError
from app.schemas.response import AnalysisResult
from app.services.prompt_service import (
    SYSTEM_INSTRUCTION,
    build_prompt,
)

class GeminiService:
    

    def __init__(self) -> None:
        self._client: genai.Client | None = None

    @property
    def client(self) -> genai.Client:
        if self._client is None:
            if not settings.gemini_api_key:
                raise RuntimeError(
                    "GEMINI_API_KEY is not configured"
                )

            self._client = genai.Client(
                api_key=settings.gemini_api_key
            )

        return self._client

    def upload_file(
        self,
        path: Path,
        mime_type: str,
        display_name: str,
    ):
        return self.client.files.upload(
            file=path,
            config=types.UploadFileConfig(
                mime_type=mime_type,
                display_name=display_name[:512],
            ),
        )

    def delete_file(
        self,
        file_name: str,
    ) -> None:
        try:
            self.client.files.delete(
                name=file_name
            )
        except Exception:
            # Cleanup should not mask the original failure.
            pass
    
    def generate_structured(
        self,
        *,
        prompt: str,
        system_instruction: str,
        file_path: Path,
        file_mime_type: str,
        file_display_name: str,
        response_schema: Any,
        model: str,
    ):
        uploaded_file = None

        try:
            # 1. Upload CV to Gemini.
            uploaded_file = self.upload_file(
                path=file_path,
                mime_type=file_mime_type,
                display_name=file_display_name,
            )

            # 2. Configure structured output.
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=response_schema,
                temperature=0.1,
                max_output_tokens=4096,
            )

            # 3. Ask Gemini to evaluate the CV.
            response = self.client.models.generate_content(
                model=model,
                contents=[
                    prompt,
                    uploaded_file,
                ],
                config=config,
            )

            if not response.text:
                raise AppError(
                    "EMPTY_AI_RESPONSE",
                    "Gemini returned an empty response.",
                    502,
                )

            return response

        except AppError:
            raise

        except Exception as exc:
            raise AppError(
                "GEMINI_MATCHING_ERROR",
                f"Gemini CV matching request failed: {exc}",
                502,
            ) from exc

        finally:
            if uploaded_file is not None:
                file_name = getattr(
                    uploaded_file,
                    "name",
                    None,
                )

                if file_name:
                    self.delete_file(
                        file_name
                    )


# class GeminiService:
#     def __init__(self) -> None:
#         if not settings.GEMINI_API_KEY:
#             raise RuntimeError("GEMINI_API_KEY is not configured")

#         self.client = genai.Client(
#             api_key=settings.GEMINI_API_KEY
#         )

#     def generate_text(
#         self,
#         prompt: str,
#         model: str | None = None,
#     ) -> str:
#         response = self.client.models.generate_content(
#             model=model or settings.DEFAULT_MODEL,
#             contents=prompt,
#         )

#         return response.text


gemini_service = GeminiService()