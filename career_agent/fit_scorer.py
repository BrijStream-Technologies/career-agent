"""
Fit Scorer module for Sylvester's Autonomous Career Agent.
Evaluates Job Listings against Sylvester's verified evidence repository on a 100-point scale.
"""

from dataclasses import dataclass, field
from typing import Dict, List
from career_agent.config import VerifiedCandidateProfile, JobSearchConfig
from career_agent.job_scanner import JobListing

@dataclass
class FitScoreResult:
    job_id: str
    total_score: int
    pillar_breakdown: Dict[str, int]
    matched_proof_points: List[str]
    recommendation: str  # "AUTO_APPLY", "REVIEW", or "REJECT"

class FitScorer:
    def __init__(self, profile: VerifiedCandidateProfile, config: JobSearchConfig):
        self.profile = profile
        self.config = config

    def score_job(self, job: JobListing) -> FitScoreResult:
        desc_lower = job.description.lower()
        title_lower = job.title.lower()
        matched_proofs = []

        # Pillar 1: Executive & Product Strategy (Max 30 pts)
        exec_score = 0
        strategy_keywords = ["strategy", "product management", "roadmap", "p&l", "executive", "vision", "cross-functional", "leader", "go-to-market"]
        exec_matches = [kw for kw in strategy_keywords if kw in desc_lower or kw in title_lower]
        if exec_matches:
            exec_score = min(30, 15 + len(exec_matches) * 3)
            matched_proofs.append(f"Executive Strategy Match: Music World Sanctuary Group P&L Strategy ({len(exec_matches)} keywords)")
        else:
            exec_score = 10

        # Pillar 2: AI Engineering, Prompting & Code Proof (Max 30 pts)
        ai_score = 0
        ai_keywords = ["ai", "prompt", "llm", "orchestration", "agent", "python", "full-stack", "test", "architecture", "microservice"]
        ai_matches = [kw for kw in ai_keywords if kw in desc_lower or kw in title_lower]
        if ai_matches:
            ai_score = min(30, 15 + len(ai_matches) * 3)
            matched_proofs.append(f"AI Code Proof Match: 88,000 LOC & 455/456 unit tests passed in Antigravity/Claude Code")
        else:
            ai_score = 10

        # Pillar 3: Domain Expertise - Music / Fintech / Royalty IP / Governance / Enterprise Solutions (Max 20 pts)
        domain_score = 0
        domain_keywords = [
            "music", "fintech", "royalty", "licensing", "media", "payments", "usdc", 
            "governance", "adtech", "patent", "audio", "saas", "enterprise", "solutions", 
            "deploy", "platform", "customer"
        ]
        domain_matches = [kw for kw in domain_keywords if kw in desc_lower or kw in title_lower]
        if domain_matches:
            domain_score = min(20, 10 + len(domain_matches) * 2.5)
            matched_proofs.append(f"Domain & Platform Fit: Patent PMG-2025-001 & SaaS Architecture ({len(domain_matches)} domain signals)")
        else:
            domain_score = 5

        # Pillar 4: Remote & Compensation Fit (Max 20 pts)
        comp_score = 0
        if job.is_remote:
            comp_score += 10
        if job.estimated_tc >= self.config.min_total_compensation or job.base_salary_max >= self.config.min_base_salary:
            comp_score += 10
        elif job.base_salary_max >= self.config.min_base_salary * 0.8:
            comp_score += 5

        total = int(exec_score + ai_score + domain_score + comp_score)
        total = min(100, max(0, total))

        if total >= self.config.min_fit_score_for_apply:
            recommendation = "AUTO_APPLY"
        elif total >= self.config.min_fit_score_for_review:
            recommendation = "REVIEW"
        else:
            recommendation = "REJECT"

        return FitScoreResult(
            job_id=job.id,
            total_score=total,
            pillar_breakdown={
                "Executive Strategy": int(exec_score),
                "AI Engineering & Code": int(ai_score),
                "Domain & IP Fit": int(domain_score),
                "Remote & Comp": int(comp_score)
            },
            matched_proof_points=matched_proofs,
            recommendation=recommendation
        )
