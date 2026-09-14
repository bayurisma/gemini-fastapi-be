from app.services.cv_matching.schemas import (
    RequirementEvaluation,
)


MATCH_MULTIPLIERS = {
    "full": 1.0,
    "partial": 0.7,
    "weak": 0.3,
    "none": 0.0,
}


def calculate_match_percentage(
    evaluations: list[RequirementEvaluation],
) -> float:
    """
    Calculate the overall match score using
    weighted requirement evaluations.

    Unknown requirements are excluded because
    lack of evidence is different from evidence
    of absence.
    """

    total_weight = 0.0
    earned_weight = 0.0

    for evaluation in evaluations:

        if evaluation.match_level == "unknown":
            continue

        weight = evaluation.weight

        multiplier = MATCH_MULTIPLIERS[
            evaluation.match_level
        ]

        total_weight += weight

        earned_weight += (
            weight * multiplier
        )

    if total_weight == 0:
        return 0.0

    return round(
        (earned_weight / total_weight) * 100,
        2,
    )