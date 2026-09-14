from app.services.cv_matching.schemas import (
    RequirementEvaluation,
)
from app.services.cv_matching.scoring import (
    calculate_match_percentage,
)


def test_full_match():
    evaluations = [
        RequirementEvaluation(
            category="skill",
            requirement="Python",
            importance="required",
            weight=20,
            match_level="full",
            confidence=0.95,
            evidence=[
                "Python is listed in the CV."
            ],
            assessment="Strong direct match.",
        )
    ]

    assert (
        calculate_match_percentage(evaluations)
        == 100.0
    )


def test_partial_match():
    evaluations = [
        RequirementEvaluation(
            category="skill",
            requirement="Python",
            importance="required",
            weight=20,
            match_level="partial",
            confidence=0.90,
            evidence=[
                "Python appears in project experience."
            ],
            assessment="Relevant but limited evidence.",
        )
    ]

    assert (
        calculate_match_percentage(evaluations)
        == 70.0
    )


def test_unknown_is_excluded():
    evaluations = [
        RequirementEvaluation(
            category="skill",
            requirement="Kubernetes",
            importance="preferred",
            weight=10,
            match_level="unknown",
            confidence=0.80,
            evidence=[],
            assessment="The CV does not provide enough evidence.",
        ),
        RequirementEvaluation(
            category="skill",
            requirement="Python",
            importance="required",
            weight=20,
            match_level="full",
            confidence=0.95,
            evidence=["Python is listed."],
            assessment="Strong match.",
        ),
    ]

    assert (
        calculate_match_percentage(evaluations)
        == 100.0
    )