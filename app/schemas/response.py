from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    summary: str = Field(
        description="A concise summary."
    )

    findings: list[str] = Field(
        default_factory=list,
        description="Important findings."
    )

    risks: list[str] = Field(
        default_factory=list,
        description="Potential risks."
    )

    references: list[str] = Field(
        default_factory=list,
        description="Relevant uploaded filenames."
    )