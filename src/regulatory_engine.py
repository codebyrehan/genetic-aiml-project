def regulatory_assessment(genetic_score: float, ecological_score: float, ethical_flags: int) -> dict:
    """Convert model signals into a human-review recommendation, not an approval decision."""
    if not 0 <= genetic_score <= 100 or not 0 <= ecological_score <= 100:
        raise ValueError("Risk scores must be between 0 and 100.")
    if ethical_flags < 0:
        raise ValueError("Ethical flag count cannot be negative.")
    combined = (0.45 * genetic_score) + (0.35 * ecological_score) + (min(ethical_flags, 5) / 5 * 20)
    if combined >= 70:
        recommendation = "Further human review required"
        level = "HIGH"
    elif combined >= 40:
        recommendation = "Additional evidence and expert review recommended"
        level = "MODERATE"
    else:
        recommendation = "Low signal in this educational prototype; expert review still required"
        level = "LOW"
    return {
        "regulatory_signal": round(combined, 1),
        "level": level,
        "recommendation": recommendation,
        "ai_role": "Decision support only; not a regulatory approval or rejection.",
    }
