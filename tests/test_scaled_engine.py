"""
Unit tests for Scaled 1,000-Enterprise Engine & Independent Adversarial Evaluator.
"""

import pytest
from career_agent.config import VerifiedCandidateProfile
from career_agent.market_scoring_model import MarketScoringModel, MarketStrengthEvaluation
from career_agent.adversarial_evaluator import AdversarialEvaluator
from career_agent.scaled_intelligence_fetcher import ScaledIntelligenceFetcher
from career_agent.agent_orchestrator import CareerAgentOrchestrator

def test_market_scoring_model():
    model = MarketScoringModel()
    brief = """# C-SUITE EXECUTIVE SYSTEM STEERING ALIGNMENT BRIEF FOR ANTHROPIC
Operates as a **Chief Agentic Steering Officer** directing autonomous agentic teams with 10x output velocity and 100% test integrity.
### VERIFIED TELEMETRY
- **88,000+ LOC Polyglot Receipts:** Production microservices across Go, Rust, C++, Python, TS (455/456 unit tests passing).
- **Patent PMG-2025-001:** Autonomous Media Synchronization.
- **Solo Execution Receipt:** These receipts represent modest empirical proof of what I have accomplished solo as a force multiplier.
- **Executive Track Record:** Executive Strategic Advisor @ Brij Brands (Park Bom), Senior Director @ Music World (Destiny's Child/Beyoncé), Founder/CEO @ Yysman Inc.
- **Enterprise Ambition:** Seeking the opportunity to bring Master-Level System Steering to a larger enterprise stage at Anthropic.
"""
    cover = "Dear Dario Amodei, I am seeking the opportunity to bring my system steering capabilities to a larger enterprise stage at Anthropic, with solo receipts of 88,000 LOC."

    eval_res = model.evaluate_brief_strength("Anthropic", "Dario Amodei", brief, cover)
    assert eval_res.total_score >= 95
    assert eval_res.is_certified_95_plus is True

def test_adversarial_evaluator_refinement_loop():
    evaluator = AdversarialEvaluator(target_score_threshold=95)
    weak_brief = "Basic text brief without empirical receipts."
    weak_cover = "Hello"

    refined_brief, refined_cover, eval_res = evaluator.evaluate_and_refine(
        company_name="ElevenLabs",
        exec_name="Mati Staniszewski",
        exec_title="CEO",
        domain="elevenlabs.io",
        brief_markdown=weak_brief,
        cover_letter_markdown=weak_cover,
        max_iterations=3
    )

    assert eval_res.total_score >= 95
    assert eval_res.is_certified_95_plus is True
    assert "88,000" in refined_brief
    assert "PMG-2025-001" in refined_brief

def test_scaled_intelligence_fetcher():
    fetcher = ScaledIntelligenceFetcher()
    targets = fetcher.discover_batch_enterprises(limit=1000)
    assert len(targets) == 1000
    assert targets[0]["company_name"] == "Anthropic"
    assert targets[999]["company_name"] != ""

def test_orchestrator_scaled_1000_batch_run():
    orchestrator = CareerAgentOrchestrator(auto_dispatch=False)
    digest = orchestrator.run_scaled_1000_batch_pipeline(batch_limit=10)
    assert "Scaled 1,000-Enterprise Machine Economy Intelligence Digest" in digest
    assert "Independent Adversarial Evaluator Certification Rate" in digest
