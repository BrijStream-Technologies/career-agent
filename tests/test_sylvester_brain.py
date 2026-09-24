"""
Unit tests for SylvesterBrain (Question Intelligence Bank & 95%+ Certification Engine).
"""

import pytest
from career_agent.strategic_database import StrategicDatabase
from career_agent.sylvester_brain import SylvesterBrain

@pytest.fixture
def db(tmp_path):
    db_file = tmp_path / "test_brain_db.db"
    return StrategicDatabase(db_path=db_file)

def test_sylvester_brain_question_classification():
    brain = SylvesterBrain()
    assert brain.classify_question_intent("What is your salary expectation?") == "Compensation & Scope"
    assert brain.classify_question_intent("Why do you want to join Anthropic?") == "Motivation & Strategic Steering Alignment"
    assert brain.classify_question_intent("Describe a complex technical system you built in Rust or Go.") == "Technical Systems Architecture & Microservices"

def test_sylvester_brain_train_and_certify(db):
    brain = SylvesterBrain(db=db)
    bq = brain.train_and_certify_question(
        question="Describe a complex project you built solo.",
        company_name="Anthropic",
        role_title="AI Systems Architect & Executive Strategy Lead",
        ats_platform="Greenhouse"
    )
    assert bq.audit_score >= 95
    assert bq.is_certified is True
    assert "88,000" in bq.canonical_answer or "88k" in bq.canonical_answer
    assert "Patent PMG-2025-001" in bq.canonical_answer

    # Verify persistent storage in SQLite DB
    certified_qs = db.get_certified_brain_questions()
    assert len(certified_qs) >= 1
    assert certified_qs[0].audit_score >= 95

def test_sylvester_brain_100_site_training_benchmark(db):
    brain = SylvesterBrain(db=db)
    mock_enterprises = [
        {"company_name": f"Corp #{i}", "ats_platform": "Greenhouse"} for i in range(5)
    ]
    res = brain.run_100_site_training_benchmark(mock_enterprises)
    assert res["total_sites_processed"] == 5
    assert res["questions_harvested"] == 25
    assert res["certified_95_plus_count"] == 25
    assert "100.0%" in res["certification_rate"]
