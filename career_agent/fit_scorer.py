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
    audit_details: Dict[str, Dict[str, str]] = field(default_factory=dict)

class FitScorer:
    def __init__(self, profile: VerifiedCandidateProfile, config: JobSearchConfig):
        self.profile = profile
        self.config = config

    def score_job(self, job: JobListing) -> FitScoreResult:
        desc_lower = job.description.lower()
        title_lower = job.title.lower()
        matched_proofs = []
        audit_details = {}

        # Pillar 1: Executive & Product Strategy (Max 30 pts)
        exec_score = 0
        strategy_keywords = ["strategy", "product management", "roadmap", "p&l", "executive", "vision", "cross-functional", "leader", "go-to-market"]
        exec_matches = [kw for kw in strategy_keywords if kw in desc_lower or kw in title_lower]
        if exec_matches:
            exec_score = min(30, 15 + len(exec_matches) * 3)
            matched_proofs.append(f"Executive Strategy Match: Music World Sanctuary Group P&L Strategy ({len(exec_matches)} keywords)")
            audit_details["Executive Strategy"] = {
                "score": f"{int(exec_score)}/30 pts",
                "target_requirement": f"Requires executive leadership, product strategy, and P&L oversight ({', '.join(exec_matches[:3])}).",
                "candidate_receipt": "Senior Director of Operations @ Music World Sanctuary Group (Records, Publishing, Touring, Merch); Founder @ Yysman, Inc. (Mary Mary [4x Grammy]); Manager for Lisa 'Left Eye' Lopes (TLC [12x Diamond]); Advisor to Park Bom (2NE1 [Billboard 200]).",
                "deduction_rationale": "Full 30 pts awarded based on 20+ yrs managing operations across RIAA Diamond-certified and multi-Grammy-winning global assets." if exec_score == 30 else f"Awarded {int(exec_score)}/30 pts based on executive strategy alignment."
            }
        else:
            exec_score = 10
            audit_details["Executive Strategy"] = {
                "score": "10/30 pts",
                "target_requirement": "General leadership & strategy execution.",
                "candidate_receipt": "Sanctuary Group Director of Strategy & Yysman CEO experience.",
                "deduction_rationale": "Base 10 pts. Position description has low explicit executive strategy requirements."
            }

        # Pillar 2: AI Engineering, Polyglot Code Proof & System Architecture (Max 30 pts)
        ai_score = 0
        ai_keywords = ["ai", "prompt", "llm", "orchestration", "agent", "go", "golang", "rust", "c++", "cpp", "python", "typescript", "javascript", "node", "sql", "full-stack", "test", "architecture", "microservice"]
        ai_matches = [kw for kw in ai_keywords if kw in desc_lower or kw in title_lower]
        if ai_matches:
            ai_score = min(30, 15 + len(ai_matches) * 3)
            matched_proofs.append(f"AI Polyglot Code Match: 88,000 LOC (Go, Python, TypeScript, Rust/C++, SQL) & 455/456 unit tests passed")
            deduct_reason = "Full 30 pts awarded: 88,000+ LOC polyglot microservices, 455/456 passing tests, and system steering prompt profile." if ai_score == 30 else f"Awarded {int(ai_score)}/30 pts. 88k LOC + 455 unit tests verified."
            audit_details["AI Engineering & Code"] = {
                "score": f"{int(ai_score)}/30 pts",
                "target_requirement": f"Hands-on AI systems architecture, agentic orchestration, polyglot software engineering ({', '.join(ai_matches[:3])}).",
                "candidate_receipt": "88,000+ lines of polyglot production code (Go/Golang, Python, TypeScript/Node.js, Rust/C++, SQL, Shell) across BrijStream & Kyvryn; 455 passing unit tests out of 456; author of System Steering prompt architecture.",
                "deduction_rationale": deduct_reason
            }
        else:
            ai_score = 10
            audit_details["AI Engineering & Code"] = {
                "score": "10/30 pts",
                "target_requirement": "Technical oversight.",
                "candidate_receipt": "88,000 LOC multi-tenant code + 455 passing unit tests.",
                "deduction_rationale": "Base 10 pts. Position is non-technical or lacks explicit AI engineering requirements."
            }

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
            audit_details["Domain & IP Fit"] = {
                "score": f"{int(domain_score)}/20 pts",
                "target_requirement": f"Domain alignment in {', '.join(domain_matches[:3])}.",
                "candidate_receipt": "Author of Provisional Patent PMG-2025-001 (Autonomous Audio Sync), 70/10/20 royalty split engine, Kyvryn AI Governance Proxy.",
                "deduction_rationale": "Full 20 pts awarded: Direct domain fit with media/IP/SaaS patents." if domain_score == 20 else f"Awarded {int(domain_score)}/20 pts. Strong overlap with candidate's IP patent and platform architecture."
            }
        else:
            domain_score = 5
            audit_details["Domain & IP Fit"] = {
                "score": "5/20 pts",
                "target_requirement": "Industry domain expertise.",
                "candidate_receipt": "Provisional Patent PMG-2025-001 & 70/10/20 split engine.",
                "deduction_rationale": "Base 5 pts. Role domain differs from candidate's specialized media/fintech/governance IP."
            }

        # Pillar 4: Location, Arrangement & Compensation Fit (Max 20 pts)
        comp_score = 10  # Base points awarded for accepted arrangement (Remote, Hybrid, or In-Office)
        if job.estimated_tc >= self.config.min_total_compensation or job.base_salary_max >= self.config.min_base_salary:
            comp_score += 10
        elif job.base_salary_max >= self.config.min_base_salary * 0.8:
            comp_score += 5

        arr_type = "Remote" if job.is_remote else ("Hybrid" if "hybrid" in desc_lower or "hybrid" in job.location.lower() else "In-Office / Hybrid")
        comp_deduct = f"Full 20 pts awarded: {arr_type} arrangement + Total Comp (${job.estimated_tc:,}) meets/exceeds $100k threshold." if comp_score == 20 else f"Partial points awarded for arrangement and compensation."
        
        audit_details["Location & Comp"] = {
            "score": f"{int(comp_score)}/20 pts",
            "target_requirement": f"Accepts Remote, Hybrid, or In-Office (Domestic/Global), Target TC >= ${self.config.min_total_compensation:,}.",
            "candidate_receipt": f"Location: {job.location} ({arr_type}) | Comp: ${job.estimated_tc:,} Total Comp.",
            "deduction_rationale": comp_deduct
        }

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
            recommendation=recommendation,
            audit_details=audit_details
        )
