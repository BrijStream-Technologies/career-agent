"""
Unit tests for DualTrackBatchRunner (Track A 700/day Email Outreach & Track B Direct Site Playwright Automation).
"""

import pytest
from career_agent.dual_track_runner import DualTrackBatchRunner

def test_dual_track_runner_instantiation():
    runner = DualTrackBatchRunner(daily_email_limit=700, headless=True)
    assert runner.daily_email_limit == 700
    assert runner.profile.name == "Sylvester Floyd Carter IV"

def test_track_a_batch_dispatch_mock(tmp_path, monkeypatch):
    from career_agent.strategic_database import StrategicDatabase, EnterpriseDossier, ExecutiveContact
    runner = DualTrackBatchRunner(daily_email_limit=700, headless=True)
    temp_db = StrategicDatabase(db_path=tmp_path / "test_dual_track_a.db")
    temp_db.upsert_enterprise(EnterpriseDossier(
        id="ent_mock_a",
        company_name="Mock AI Labs",
        domain="mockailabs.com",
        agentic_score=95,
        tech_stack_gaps=["Agentic Steering"],
        funding_telemetry="$100M Series B",
        sector="Frontier AI"
    ))
    temp_db.add_executive(ExecutiveContact(
        id="exec_mock_a",
        enterprise_id="ent_mock_a",
        name="Jane Doe",
        title="CEO",
        email="jane@mockailabs.com",
        mx_verified=True,
        confidence_score=99
    ))
    runner.db = temp_db
    runner.executive_pitcher.db = temp_db
    monkeypatch.setattr(
        runner.executive_pitcher,
        "pitch_executive_direct",
        lambda **kwargs: {"status": "DRAFTED_TO_ICLOUD", "company_name": kwargs.get("company_name", "")}
    )
    res = runner.execute_track_a_smtp_dispatch(limit=5, live_send=False)
    assert res["track"] == "Track A (C-Suite Email Outreach)"
    assert res["limit"] == 5
    assert "dispatched" in res

def test_track_b_direct_site_mock(tmp_path, monkeypatch):
    from career_agent.strategic_database import StrategicDatabase, EnterpriseDossier
    runner = DualTrackBatchRunner(daily_email_limit=700, headless=True)
    temp_db = StrategicDatabase(db_path=tmp_path / "test_dual_track_b.db")
    temp_db.upsert_enterprise(EnterpriseDossier(
        id="ent_mock_b",
        company_name="Mock AI Labs",
        domain="mockailabs.com",
        agentic_score=95,
        tech_stack_gaps=["Agentic Steering"],
        funding_telemetry="$100M Series B",
        sector="Frontier AI"
    ))
    runner.db = temp_db
    runner.direct_applicant.db = temp_db
    monkeypatch.setattr(
        runner.direct_applicant.browser_applicant,
        "apply_online",
        lambda *args, **kwargs: {
            "status": "PREFILLED_PREVIEW_READY",
            "screenshot_path": "",
            "custom_questions_answered": [],
            "details": "Mocked prefill."
        }
    )
    res = runner.execute_track_b_direct_site_applications(limit=2, submit_live=False)
    assert res["track"] == "Track B (Direct Company Site Applications)"
    assert res["limit"] == 2
    assert "processed" in res
