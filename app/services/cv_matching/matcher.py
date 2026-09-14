from pathlib import Path

from app.core.config import settings

from app.services import (gemini_service,)
from app.services.cv_matching.prompts import (
    MATCHING_SYSTEM_PROMPT,
    build_matching_prompt,
)
from app.services.cv_matching.schemas import CVMatchAnalysis

class CVMatcher:
    
    def __init__(self) -> None:
        self.gemini = gemini_service.GeminiService()
    
    def analyze(
        self,
        *,
        job_requirement: str,
        cv_path: Path,
        cv_filename: str,
    ) -> CVMatchAnalysis:
        
        prompt = build_matching_prompt(job_requirement)
        
        response = (
            self.gemini.generate_structured(
                prompt=prompt,
                system_instruction=(MATCHING_SYSTEM_PROMPT),
                file_path=cv_path,
                file_mime_type="application/pdf",
                file_display_name=cv_filename,
                response_schema=CVMatchAnalysis,
                model=settings.default_model,   
            )
        )
        
        parsed = getattr(response, "parsed", None)
        
        if isinstance(parsed, CVMatchAnalysis):
            return parsed
        
        return CVMatchAnalysis.model_validate_json(
            response.text
        )
    
    def build_request(
        self,
        job_requirement: str,
        cv_path: Path,
    ) -> dict:
        """
        Build the request payload for the CV matching API.
        """

        return {
            "cv_path": cv_path,
            "system_prompt": MATCHING_SYSTEM_PROMPT,
            "prompt": build_matching_prompt(
                job_requirement
            ),
        }
        
        
cv_matcher = CVMatcher()