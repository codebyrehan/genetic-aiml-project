def assess_ecological_risk(*, gene_drive: bool, off_target_sites: int, population_impact: float, uncertainty: float) -> dict:
    """Educational ecological-risk proxy; not a real ecological model."""
    if off_target_sites < 0:
        raise ValueError("Off-target sites cannot be negative.")
    for name, value in (("population_impact", population_impact), ("uncertainty", uncertainty)):
        if not 0 <= value <= 1:
            raise ValueError(f"{name} must be between 0 and 1.")
    drive = 1.0 if gene_drive else 0.0
    off_target = min(off_target_sites / 10.0, 1.0)
    score = (0.35 * drive) + (0.30 * off_target) + (0.25 * population_impact) + (0.10 * uncertainty)
    label = "HIGH" if score >= 0.67 else "MODERATE" if score >= 0.34 else "LOW"
    return {
        "score": round(score * 100, 1),
        "label": label,
        "components": {
            "gene_drive": round(drive * 100, 1),
            "off_target_activity": round(off_target * 100, 1),
            "population_impact": round(population_impact * 100, 1),
            "uncertainty": round(uncertainty * 100, 1),
        },
        "disclaimer": "Educational proxy using synthetic inputs; not a real ecological risk prediction.",
    }
