import pytest

from src.ecological_risk import assess_ecological_risk
from src.regulatory_engine import regulatory_assessment
from src.risk_engine import analyze


def test_risk_engine_returns_bounded_score():
    result = analyze({
        "mismatches": 2,
        "pam_correct": True,
        "in_exon": True,
        "conservation_score": 0.72,
        "gc_content": 0.48,
    })
    assert 0 <= result["risk_score"] <= 100
    assert result["model"] == "Random Forest"


def test_ecological_risk_validation():
    with pytest.raises(ValueError):
        assess_ecological_risk(gene_drive=True, off_target_sites=-1, population_impact=0.5, uncertainty=0.2)


def test_regulatory_layer_requires_human_review():
    result = regulatory_assessment(90, 80, 4)
    assert result["level"] == "HIGH"
    assert "human review" in result["recommendation"].lower()
