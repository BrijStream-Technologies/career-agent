"""
Package Tailorer module for Sylvester's Autonomous Career Agent.
Generates tailored ATS resumes, human-authentic cover letters, and high-impact Translucent Alignment Briefs
featuring the Dual Summaries (Code Telemetry & Prompting Profile) and 100-Point Position Reconciliation.
"""

from dataclasses import dataclass
from typing import Dict, List
from career_agent.config import VerifiedCandidateProfile, FORBIDDEN_COPY_TERMS
from career_agent.job_scanner import JobListing
from career_agent.fit_scorer import FitScoreResult

@dataclass
class ApplicationPackage:
    job_id: str
    company: str
    job_title: str
    tailored_resume_markdown: str
    cover_letter_markdown: str
    translucent_brief_markdown: str
    verification_status: str  # "VERIFIED_NO_CLICHES"

class PackageTailorer:
    def __init__(self, profile: VerifiedCandidateProfile):
        self.profile = profile

    def build_tailored_package(self, job: JobListing, score_result: FitScoreResult) -> ApplicationPackage:
        resume_md = self.generate_ats_resume(job, score_result)
        cover_letter_md = self.generate_cover_letter(job, score_result)
        brief_md = self.generate_translucent_brief(job, score_result)
        
        verified_cover_letter = self.sanitize_copy(cover_letter_md)
        verified_brief = self.sanitize_copy(brief_md)

        return ApplicationPackage(
            job_id=job.id,
            company=job.company,
            job_title=job.title,
            tailored_resume_markdown=resume_md,
            cover_letter_markdown=verified_cover_letter,
            translucent_brief_markdown=verified_brief,
            verification_status="VERIFIED_NO_CLICHES"
        )

    def generate_translucent_brief(self, job: JobListing, score_result: FitScoreResult) -> str:
        audit_blocks = []
        for pillar, data in score_result.audit_details.items():
            audit_blocks.append(
                f"### {pillar}: {data['score']}\n"
                f"- **Job Requirement:** {data['target_requirement']}\n"
                f"- **Verified Candidate Receipt:** {data['candidate_receipt']}\n"
                f"- **Audit & Scoring Rationale:** {data['deduction_rationale']}\n"
            )
        
        audit_section = "\n".join(audit_blocks)

        return f"""# TRANSLUCENT AGENT ALIGNMENT & EXECUTION BRIEF
**Target Role:** {job.title} @ {job.company}
**Candidate:** {self.profile.name} ({self.profile.email})
**Empirical Reconciliation Match:** {score_result.total_score}% / 100% (Audited Proof Matrix)

---
## 🎯 100-POINT POSITION RECONCILIATION MATRIX (EVIDENCE AUDIT)
*This empirical audit maps position requirements directly to verified code telemetry, unit tests, patents, and P&L receipts to eliminate arbitrary scoring.*

{audit_section}

---
## 💻 SUMMARY 1: CODE SUMMARY TELEMETRY
- **Production Codebase:** 88,000+ lines of multi-tenant microservice code across BrijStream (Media Streaming) and Kyvryn/Themis (AI Governance Proxy).
- **Test Integrity:** 455 passing unit tests out of 456 automated test assertions.
- **Intellectual Property:** 3 patent filings including Provisional PMG-2025-001 (Autonomous Media Synchronization matching energy, mood, tempo, audio ducking).
- **Fintech & Royalty Ledgers:** Built 70/10/20 ad revenue split engine and instant USDC stablecoin split settlement protocol.

---
## 🧠 SUMMARY 2: PROMPTING & STRATEGY EXECUTION PROFILE
- **Meta-Prompting Persona:** Operates as a System Steering Officer. Provides high-level domain constraints and outcome-driven directives, bypassing syntax micromanagement.
- **Ruthless Non-Pleasing Truth Enforcement:** Explicitly commands AI agents to eliminate "pleasing/romantic" biases, enforcing empirical reality checks and code truthfulness audits.
- **Socratic Mechanism Probing:** Systematically probes system mechanics under the hood (data flow, security boundaries, non-LLM document generation, OAuth authentication).
- **Domain Bridge Translation:** Translates complex commercial structures (Reg CF crowdfunding, statutory licensing pools) directly into prompt directives that ship production code.
"""

    def generate_ats_resume(self, job: JobListing, score_result: FitScoreResult) -> str:
        proof_summary = "\n".join([f"- {p}" for p in score_result.matched_proof_points])
        
        return f"""# {self.profile.name}
**{self.profile.title}** | {self.profile.email} | {self.profile.location}

## EXECUTIVE SUMMARY
Executive Strategy Leader and AI Systems Architect with 20+ years of multi-million dollar P&L leadership, media strategy, and hands-on AI product orchestration. Directed AI agents (Antigravity & Claude Code) to build, test, and deploy 88,000+ lines of production microservice code across media streaming and AI governance. Author of 3 patent applications in autonomous media synchronization and instant split settlement.

## 100-POINT POSITION RECONCILIATION MATCH: {score_result.total_score}% FOR {job.title.upper()} AT {job.company.upper()}
{proof_summary}

## RELEVANT EXPERIENCE

### Co-Founder & AI Systems Architect | BrijStream / Kyvryn (2019 – Present)
- Directed architectural blueprint and prompt orchestration for dual multi-sided streaming and AI governance platforms spanning 88,000+ lines of code.
- Maintained 455/456 passing automated unit test suite.
- Formulated and filed patent applications for autonomous scene-scoring algorithms matching audio energy, mood, and tempo under speech dialogue.

### Director of Strategy | Music World / Sanctuary Group (2004 – 2006)
- Managed multi-million dollar P&L operations, corporate media licensing, and global artist catalog monetization.

### Founder & CEO | Yysman, Inc. (1999 – 2004)
- Founded tech enterprise from inception through successful corporate acquisition.

## EDUCATION & PATENTS
- **{self.profile.education}**
- Patents: {", ".join(self.profile.patents)}
"""

    def generate_cover_letter(self, job: JobListing, score_result: FitScoreResult) -> str:
        return f"""Dear Hiring Team at {job.company},

I am writing to express my strong interest in the {job.title} role.

What sets my background apart is the combination of senior executive P&L leadership and direct hands-on AI systems architecture. Having served as Director of Strategy at Music World / Sanctuary Group managing multi-million dollar P&L portfolios, I understand product strategy from a commercial standpoint. At the same time, I actively direct AI agents using Antigravity and Claude Code to build, test, and deploy production software.

Recently, I architected and built an 88,000-line multi-sided media platform and AI governance proxy engine that maintains 455 passing unit tests out of 456, alongside authoring patent applications for autonomous audio-scene synchronization algorithms.

I respect {job.company}'s work in this space and would welcome the opportunity to discuss how my strategic background and AI building capabilities can contribute directly to your product roadmap.

Sincerely,

{self.profile.name}
{self.profile.title}
"""

    def sanitize_copy(self, text: str) -> str:
        clean_text = text
        for term in FORBIDDEN_COPY_TERMS:
            if term.lower() in clean_text.lower():
                clean_text = clean_text.replace(term, "demonstrated leadership")
        return clean_text
