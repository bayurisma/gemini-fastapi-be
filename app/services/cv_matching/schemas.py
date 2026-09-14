from typing import Literal

from pydantic import BaseModel, Field


MatchLevel = Literal[
    "full",
    "partial",
    "weak",
    "none",
    "unknown",
]


class RequirementEvaluation(BaseModel):
    category: str 
    requirement: str 

    importance: Literal[
        "required",
        "preferred",
    ]

    weight: float = Field(
        ge=0,
        le=100,
    )

    match_level: MatchLevel

    confidence: float = Field(
        ge=0,
        le=1,
    )

    evidence: list[str] = Field(
        default_factory=list,
        description=(
            "Concrete evidence from the CV."
        ),
    )

    assessment: str 
    

class CVMatchAnalysis(BaseModel):
    summary: str

    evaluations: list[
        RequirementEvaluation
    ]

    strengths: list[str] 

    gaps: list[str] 

    recommendation: str


class CVMatchResponse(BaseModel):
    request_id: str
    status: str
    match_percentage: float
    summary: str
    factors: list[RequirementEvaluation]
    strengths: list[str]
    gaps: list[str]
    recommendation: str