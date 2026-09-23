"""
Unit test suite for Sylvester's Autonomous Career Agent.
Tests configuration, job scanning, fit scoring, package tailoring, outreach finding, and orchestrator digest generation.
"""

import pytest
from datetime import datetime, timedelta
from career_agent.config import VerifiedCandidateProfile, JobSearchConfig, FORBIDDEN_COPY_TERMS
from career_agent.job_scanner import JobScanner, JobListing
from career_agent.fit_scorer import FitScorer, FitScoreResult
from career_agent.package_tailorer import PackageTailorer, ApplicationPackage
from career_agent.outreach_finder import OutreachFinder, ExecutiveOutreachDraft
from career_agent.executive_digest import ExecutiveDigestBuilder
from career_agent.agent_orchestrator import CareerAgentOrchestrator

@pytest.fixture
def profile():
    return VerifiedCandidateProfile()

@pytest.fixture
def config():
    return JobSearchConfig()

@pytest.fixture
def sample_remote_job():
    return JobListing(
        id="elevenlabs_principal_pm",
        title="Principal AI Product Manager",
        company="ElevenLabs",
        location="Remote - US",
        is_remote=True,
        base_salary_min=240000,
        base_salary_max=290000,
        estimated_tc=360000,
        posting_date=datetime.now() - timedelta(days=3),
        description="Lead AI product strategy, voice orchestration, P&L management, AI prompt architecture, audio licensing, and rights registry.",
        source_url="https://elevenlabs.io/careers/principal-ai-pm"
    )

@pytest.fixture
def sample_onsite_job():
    return JobListing(
        id="local_dev",
        title="Junior Developer",
        company="Local Co",
        location="Atlanta, GA",
        is_remote=False,
        base_salary_min=50000,
        base_salary_max=60000,
        estimated_tc=60000,
        posting_date=datetime.now() - timedelta(days=2),
        description="Entry level junior developer.",
        source_url="https://example.com/job"
    )

# --- CONFIG TESTS ---
def test_config_profile_metrics(profile):
    assert profile.lines_of_code_built == 88000
    assert profile.passing_unit_tests == 455
    assert profile.total_unit_tests == 456
    assert len(profile.patents) >= 3
    assert "Montgomery, TX" in profile.location
    assert "Mary Mary" in profile.executive_experience[2]["highlight"]
    assert "Brij Brands" in profile.executive_experience[3]["company"]
    assert "Park Bom" in profile.executive_experience[3]["highlight"]
    assert "Lisa 'Left Eye' Lopes" in profile.executive_experience[4]["highlight"]

# --- JOB SCANNER TESTS ---
def test_job_scanner_filtering(config, sample_remote_job, sample_onsite_job):
    scanner = JobScanner(config)
    assert scanner.is_valid_candidate_job(sample_remote_job) is True
    # sample_onsite_job is $60k (< $100k min threshold), so it gets filtered out
    assert scanner.is_valid_candidate_job(sample_onsite_job) is False

def test_job_scanner_hybrid_100k_accepted(config):
    scanner = JobScanner(config)
    hybrid_100k_job = JobListing(
        id="hybrid_pm_austin",
        title="Senior AI Product Manager",
        company="Spotify",
        location="Hybrid - Austin, TX",
        is_remote=False,
        base_salary_min=110000,
        base_salary_max=140000,
        estimated_tc=140000,
        posting_date=datetime.now() - timedelta(days=2),
        description="Drive AI recommendations and music audio metadata.",
        source_url="https://example.com/job"
    )
    assert scanner.is_valid_candidate_job(hybrid_100k_job) is True

def test_job_scanner_deduplication(config):
    scanner = JobScanner(config)
    raw_data = [
        {"id": "job1", "title": "Principal AI Product Manager", "company": "Co A", "is_remote": True, "base_salary_max": 200000},
        {"id": "job1", "title": "Principal AI Product Manager", "company": "Co A", "is_remote": True, "base_salary_max": 200000},
    ]
    results = scanner.normalize_and_filter(raw_data)
    assert len(results) == 1

def test_job_scanner_anti_ghost_age(config):
    scanner = JobScanner(config)
    old_job = JobListing(
        id="old_job",
        title="Principal AI Product Manager",
        company="Old Corp",
        location="Remote",
        is_remote=True,
        base_salary_min=200000,
        base_salary_max=250000,
        estimated_tc=250000,
        posting_date=datetime.now() - timedelta(days=50),  # > 45 days old
        description="Old listing",
        source_url="https://example.com"
    )
    assert scanner.is_valid_candidate_job(old_job) is False

# --- FIT SCORER TESTS ---
def test_fit_scorer_high_match(profile, config, sample_remote_job):
    scorer = FitScorer(profile, config)
    score_result = scorer.score_job(sample_remote_job)
    
    assert score_result.total_score >= 80
    assert score_result.recommendation == "AUTO_APPLY"
    assert "Executive Strategy" in score_result.pillar_breakdown
    assert "AI Engineering & Code" in score_result.pillar_breakdown
    assert len(score_result.matched_proof_points) > 0

def test_fit_scorer_pillar_breakdown(profile, config, sample_remote_job):
    scorer = FitScorer(profile, config)
    result = scorer.score_job(sample_remote_job)
    
    total_calculated = sum(result.pillar_breakdown.values())
    assert result.total_score == total_calculated

# --- PACKAGE TAILORER TESTS ---
def test_package_tailorer_generation(profile, config, sample_remote_job):
    scorer = FitScorer(profile, config)
    score_result = scorer.score_job(sample_remote_job)
    tailorer = PackageTailorer(profile)
    
    pkg = tailorer.build_tailored_package(sample_remote_job, score_result)
    
    assert pkg.job_id == sample_remote_job.id
    assert pkg.company == "ElevenLabs"
    assert "88,000" in pkg.tailored_resume_markdown
    assert "455" in pkg.tailored_resume_markdown
    assert pkg.verification_status == "VERIFIED_NO_CLICHES"

def test_package_tailorer_cliche_sanitization(profile):
    tailorer = PackageTailorer(profile)
    dirty_text = "I would love to delve into this transformative journey to leverage cutting-edge tech."
    clean_text = tailorer.sanitize_copy(dirty_text)
    
    for term in FORBIDDEN_COPY_TERMS:
        assert term.lower() not in clean_text.lower()

# --- OUTREACH FINDER TESTS ---
def test_outreach_finder_drafting(profile, sample_remote_job):
    finder = OutreachFinder(profile)
    draft = finder.create_outreach_draft(sample_remote_job)
    
    assert draft.job_id == sample_remote_job.id
    assert "VP of Product" in draft.target_title_suggestion
    assert "88,000 LOC" in draft.personalized_message
    assert profile.name in draft.personalized_message

# --- EXECUTIVE DIGEST TESTS ---
def test_executive_digest_builder(profile, config, sample_remote_job):
    scorer = FitScorer(profile, config)
    score_result = scorer.score_job(sample_remote_job)
    tailorer = PackageTailorer(profile)
    pkg = tailorer.build_tailored_package(sample_remote_job, score_result)
    finder = OutreachFinder(profile)
    draft = finder.create_outreach_draft(sample_remote_job)
    
    builder = ExecutiveDigestBuilder()
    digest_md = builder.build_digest_markdown(
        total_scanned=10,
        scored_jobs=[(sample_remote_job, score_result)],
        packages={sample_remote_job.id: pkg},
        outreach_drafts={sample_remote_job.id: draft}
    )
    
    assert "Daily Career Agent Executive Digest" in digest_md
    assert "ElevenLabs" in digest_md
    assert "Fit Score:" in digest_md
    assert "ACTION CHECKLIST" in digest_md

# --- FULL PIPELINE ORCHESTRATOR TEST ---
def test_orchestrator_pipeline_end_to_end():
    orchestrator = CareerAgentOrchestrator()
    sample_data = [
        {
            "id": "anthropic_fd_lead",
            "title": "Forward Deployed AI Solutions Lead",
            "company": "Anthropic",
            "location": "Remote - US",
            "is_remote": True,
            "base_salary_min": 250000,
            "base_salary_max": 320000,
            "estimated_tc": 480000,
            "description": "Forward deployed AI lead working with customers to build AI agents, system architecture, prompt engineering, Python, P&L strategy.",
            "source_url": "https://anthropic.com/careers"
        }
    ]
    
    digest_output = orchestrator.run_daily_pipeline(sample_data)
    assert "Forward Deployed AI Solutions Lead @ Anthropic" in digest_output
    assert "TARGET OPPORTUNITIES" in digest_output

# --- WEB SERVER & DASHBOARD TESTS ---
def test_mobile_dashboard_html_exists():
    from pathlib import Path
    html_path = Path(__file__).parent.parent / "career_agent" / "mobile_dashboard.html"
    assert html_path.exists()
    content = html_path.read_text()
    assert "Career Agent Digest" in content
    assert "Sylvester Floyd Carter IV" in content
    assert "Copy InMail" in content

def test_web_server_handler_instantiation():
    from career_agent.web_server import get_local_ip, PORT
    ip = get_local_ip()
    assert isinstance(ip, str)
    assert PORT == 8080

# --- CONTACT DISPATCHER TESTS ---
def test_contact_dispatcher_resolution(profile, sample_remote_job):
    from career_agent.contact_dispatcher import ContactDispatcher
    from career_agent.package_tailorer import ApplicationPackage
    from career_agent.outreach_finder import ExecutiveOutreachDraft

    dispatcher = ContactDispatcher(profile, auto_send=False)
    recipient = dispatcher.resolve_recipient_email(sample_remote_job)
    assert "@" in recipient

    pkg = ApplicationPackage(
        job_id=sample_remote_job.id,
        company=sample_remote_job.company,
        job_title=sample_remote_job.title,
        translucent_brief_markdown="Brief",
        tailored_resume_markdown="Resume",
        cover_letter_markdown="Cover Letter",
        verification_status="VERIFIED_NO_CLICHES"
    )
    draft = ExecutiveOutreachDraft(
        job_id=sample_remote_job.id,
        company=sample_remote_job.company,
        target_role=sample_remote_job.title,
        target_title_suggestion="VP of Product",
        personalized_message="Test Message"
    )
    dispatcher.dispatch_outreach(sample_remote_job, pkg, draft)
    assert dispatcher.is_already_contacted(sample_remote_job.id) is True

def test_contact_verifier_dns_mx_validation():
    from career_agent.contact_verifier import ContactVerifier
    verifier = ContactVerifier()
    contact = verifier.discover_and_verify_executive_contact("ElevenLabs", "Principal AI Product Manager")
    
    assert contact.company == "ElevenLabs"
    assert "Mati Staniszewski" in contact.recipient_name or "Co-Founder" in contact.recipient_title
    assert "elevenlabs.io" in contact.recipient_email
    assert contact.verification_status in ["VERIFIED_EXECUTIVE_DIRECT", "UNVERIFIED_DOMAIN_FAILED"]

    unverified = verifier.discover_and_verify_executive_contact("Unknown AI Corp", "Senior ML Engineer")
    assert verifier.is_officially_verified(unverified) is False
    assert unverified.verification_status in ["UNVERIFIED_EXECUTIVE_HOLD", "UNVERIFIED_DOMAIN_FAILED"]

def test_audit_details_reconciliation_matrix(profile, config, sample_remote_job):
    scorer = FitScorer(profile, config)
    score_result = scorer.score_job(sample_remote_job)
    
    assert "audit_details" in dir(score_result)
    assert len(score_result.audit_details) == 4
    assert "target_requirement" in score_result.audit_details["Executive Strategy"]
    assert "candidate_receipt" in score_result.audit_details["Executive Strategy"]
    assert "deduction_rationale" in score_result.audit_details["Executive Strategy"]

    tailorer = PackageTailorer(profile)
    pkg = tailorer.build_tailored_package(sample_remote_job, score_result)
    
    assert "100-POINT POSITION RECONCILIATION MATRIX (EVIDENCE AUDIT)" in pkg.translucent_brief_markdown
    assert "Job Requirement:" in pkg.translucent_brief_markdown
    assert "Verified Candidate Receipt:" in pkg.translucent_brief_markdown
    assert "Audit & Scoring Rationale:" in pkg.translucent_brief_markdown

def test_browser_applicant_instantiation(profile):
    from career_agent.browser_applicant import BrowserApplicant
    applicant = BrowserApplicant(profile, headless=True)
    assert applicant.profile.name == profile.name
    assert applicant.screenshots_dir.exists()
    assert applicant.default_account_password is not None

def test_browser_applicant_llm_custom_question_answering(profile, sample_remote_job):
    from career_agent.browser_applicant import BrowserApplicant
    applicant = BrowserApplicant(profile, headless=True)
    ans = applicant.generate_authentic_answer("Why do you want to join ElevenLabs?", sample_remote_job)
    assert "ElevenLabs" in ans
    assert "System Steering" in ans or "Brij Brands" in ans or "moat" in ans



