"""
Unit tests for Agentic Economy Intelligence & Executive Strategic Outreach Engine.
Tests database persistence, intelligence fetching, Track A executive pitching, and Track B direct site applicants.
"""

import pytest
import os
from pathlib import Path
from career_agent.config import VerifiedCandidateProfile
from career_agent.strategic_database import StrategicDatabase, EnterpriseDossier, ExecutiveContact, StrategicOpportunity
from career_agent.agentic_intelligence_fetcher import AgenticIntelligenceFetcher
from career_agent.executive_direct_pitcher import ExecutiveDirectPitcher
from career_agent.direct_site_applicant import DirectSiteApplicant
from career_agent.agent_orchestrator import CareerAgentOrchestrator

@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_agentic_intelligence.db"
    return StrategicDatabase(db_path=db_file)

@pytest.fixture
def profile():
    return VerifiedCandidateProfile()

def test_strategic_database_crud(temp_db):
    dossier = EnterpriseDossier(
        id="ent_test",
        company_name="Test AI Corp",
        domain="testai.com",
        agentic_score=95,
        tech_stack_gaps=["Proxy Metering", "Audio Sync"],
        funding_telemetry="$50M Series A",
        sector="Enterprise AI Infrastructure"
    )
    temp_db.upsert_enterprise(dossier)
    
    high_scoring = temp_db.get_high_intensity_enterprises(min_score=90)
    assert len(high_scoring) == 1
    assert high_scoring[0].company_name == "Test AI Corp"
    assert high_scoring[0].agentic_score == 95

    exec_contact = ExecutiveContact(
        id="exec_test",
        enterprise_id="ent_test",
        name="Test Executive",
        title="CEO",
        email="exec@testai.com",
        mx_verified=True,
        confidence_score=98
    )
    temp_db.add_executive(exec_contact)

    retrieved_execs = temp_db.get_executives_for_enterprise("ent_test")
    assert len(retrieved_execs) == 1
    assert retrieved_execs[0].name == "Test Executive"

def test_agentic_intelligence_fetcher():
    fetcher = AgenticIntelligenceFetcher()
    enterprises = fetcher.discover_high_spending_enterprises()
    assert len(enterprises) >= 8
    assert any(e["company_name"] == "ElevenLabs" for e in enterprises)
    assert any(e["company_name"] == "Anthropic" for e in enterprises)

def test_executive_direct_pitcher(profile, temp_db):
    pitcher = ExecutiveDirectPitcher(profile, temp_db)
    res = pitcher.pitch_executive_direct(
        enterprise_id="ent_elevenlabs",
        company_name="ElevenLabs",
        domain="elevenlabs.io",
        exec_name="Mati Staniszewski",
        exec_title="Co-Founder & CEO",
        exec_email="mati@elevenlabs.io",
        tech_gaps=["Multi-LLM Voice Proxy Metering", "Real-Time Audio Scene Ducking"]
    )
    assert res["company_name"] == "ElevenLabs"
    assert res["status"] in ["DRAFTED_TO_ICLOUD", "SIMULATED_DISPATCH", "HOLD_UNVERIFIED"]

def test_orchestrator_strategic_pipeline():
    orchestrator = CareerAgentOrchestrator(auto_dispatch=False)
    digest = orchestrator.run_strategic_intelligence_pipeline()
    assert "Daily Agentic Economy Executive Intelligence Digest" in digest
    assert "ElevenLabs" in digest
    assert "Anthropic" in digest
