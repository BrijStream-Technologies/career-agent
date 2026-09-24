"""
Unit tests for AdversarialApplicationAuditor (Track B pre-fill evaluation engine).
"""

import pytest
from datetime import datetime
from career_agent.config import VerifiedCandidateProfile, JobSearchConfig
from career_agent.job_scanner import JobListing
from career_agent.package_tailorer import PackageTailorer
from career_agent.fit_scorer import FitScorer
from career_agent.adversarial_application_auditor import AdversarialApplicationAuditor, AuditReport

@pytest.fixture
def profile():
    return VerifiedCandidateProfile()

@pytest.fixture
def job():
    return JobListing(
        id="anthropic_auditor_test",
        title="AI Systems Architect",
        company="Anthropic",
        location="Remote - US",
        is_remote=True,
        base_salary_min=250000,
        base_salary_max=350000,
        estimated_tc=450000,
        posting_date=datetime.now(),
        description="Lead AI system architecture, polyglot microservices, and multi-LLM proxy steering.",
        source_url="https://job-boards.greenhouse.io/anthropic/jobs/5183044008"
    )

def test_profile_explicit_name_attributes(profile):
    assert profile.first_name == "Sylvester"
    assert profile.middle_name == "Floyd"
    assert profile.last_name == "Carter"
    assert profile.suffix == "IV"

def test_adversarial_application_auditor_certification(profile, job, tmp_path):
    tailorer = PackageTailorer(profile)
    scorer = FitScorer(profile, JobSearchConfig())
    score_res = scorer.score_job(job)
    pkg = tailorer.build_tailored_package(job, score_res)

    # Create dummy valid screenshot file
    screenshot_file = tmp_path / "test_screenshot.png"
    screenshot_file.write_bytes(b"PNG_FAKE_IMAGE_DATA_" * 100)

    mock_app_res = {
        "job_id": job.id,
        "company": job.company,
        "url": job.source_url,
        "status": "PREFILLED_PREVIEW_READY",
        "screenshot_path": str(screenshot_file),
        "custom_questions_answered": [
            {
                "question": "Why Anthropic?",
                "answer": "My approach is outcome-driven System Steering. I direct AI agent pipelines to convert requirements into production software—evidenced by 88,000 LOC across Go, Rust, C++, Python, TS, 455/456 unit tests, and Patent PMG-2025-001. Leading operations at Brij Brands and Sanctuary Group..."
            }
        ],
        "details": "Form pre-filled cleanly with 8 visible candidate inputs."
    }

    auditor = AdversarialApplicationAuditor(target_score_threshold=95)
    report = auditor.audit_prefilled_application(job, pkg, mock_app_res)

    assert isinstance(report, AuditReport)
    assert report.identity_score == 25
    assert report.persona_proof_score == 25
    assert report.form_compliance_score == 25
    assert report.screenshot_dom_score == 25
    assert report.audit_score == 100
    assert report.is_certified_95_plus is True
