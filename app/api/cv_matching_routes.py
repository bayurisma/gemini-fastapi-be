import uuid
from pathlib import Path
from typing import Annotated

from fastapi import (
    APIRouter,
    File, 
    Form,
    UploadFile,
)

from app.exceptions.errors import AppError
from app.services.cv_matching.schemas import CVMatchResponse
from app.services.cv_matching.scoring import calculate_match_percentage
from app.services.file_service import TemporaryFileService
from app.services.cv_matching.matcher import (
    cv_matcher,
)

router = APIRouter(
    prefix="/v1",
    tags=["CV Matching"],
)

file_service = TemporaryFileService()

@router.post("/match-cv", response_model=CVMatchResponse)
async def match_cv(
    job_requirement: Annotated[
        str,
        Form(
            min_length=20,
            max_length=20_000,
        ),
    ],
    cv: Annotated[
        UploadFile,
        File()
    ]
):
    
    # -------------------------------------------------
    # 1. Validate file type
    # -------------------------------------------------
    
    if cv.content_type != "application/pdf":
        raise AppError(
            "INVALID_CV_FORMAT",
            "CV must be a PDF file.",
            400,
        )
    
    request_id = uuid.uuid4().hex
    
    request_dir = (
        file_service.create_request_dir(request_id)
    )
    
    try:
        
        # ---------------------------------------------
        # 2. Store temporary PDF
        # ---------------------------------------------
        
        path, size = (
            await file_service.save_upload(
                cv,
                request_dir,
            )
        )
        
        # ---------------------------------------------
        # 3. Ask Gemini to evaluate
        # ---------------------------------------------
        
        analysis = cv_matcher.analyze(
            job_requirement=job_requirement,
            cv_path=path,
            cv_filename=cv.filename,
        )
        
        # ---------------------------------------------
        # 4. Calculate percentage locally
        # ---------------------------------------------
        
        percentage = (
            calculate_match_percentage(analysis.evaluations)
        )
        
        # ---------------------------------------------
        # 5. Return normalized API response
        # ---------------------------------------------
        
        return CVMatchResponse(
            request_id=request_id,
            status="success",
            match_percentage=percentage,
            summary=analysis.summary,
            factors=analysis.evaluations,
            strengths=analysis.strengths,
            gaps=analysis.gaps,
            recommendation=analysis.recommendation,
        )
    finally:
        file_service.cleanup_request_dir(request_dir)