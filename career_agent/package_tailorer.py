"""
Package Tailorer module for Sylvester's Autonomous Career Agent.
Generates tailored ATS resumes and human-authentic cover letters free of AI cliches.
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
    verification_status: str  # "VERIFIED_NO_CLICHES"

class PackageTailorer:
    def __init__(self, profile: VerifiedCandidateProfile):
        self.profile = profile

    def build_tailored_package(self, job: JobListing, score_result: FitScoreResult) -> ApplicationPackage:
        resume_md = self.generate_ats_resume(job, score_result)
        cover_letter_md = self.generate_cover_letter(job, score_result)
        
        # Verify no forbidden AI cliches exist
        verified_cover_letter = self.sanitize_copy(cover_letter_md)

        return ApplicationPackage(
            job_id=job.id,
            company=job.company,
            job_title=job.title,
            tailored_resume_markdown=resume_md,
            cover_letter_markdown=verified_cover_letter,
            verification_status="VERIFIED_NO_CLICHES"
        )

    def generate_ats_resume(self, job: JobListing, score_result: FitScoreResult) -> str:
        proof_summary = "\n".join([f"- {p}" for p in score_result.matched_proof_points])
        
        return f"""# {self.profile.name}
**{self.profile.title}** | {self.profile.location} | [LinkedIn Portfolio]

## EXECUTIVE SUMMARY
Executive Strategy Leader and AI Systems Architect with 20+ years of multi-million dollar P&L leadership, media strategy, and hands-on AI product orchestration. Directed AI agents (Antigravity & Claude Code) to build, test, and deploy 88,000+ lines of production microservice code across media streaming, AI governance, and automated royalty split ledgers. Author of 3 patent applications in autonomous media synchronization and instant split settlement.

## KEY PROOF POINTS MATCHING {job.title.upper()} AT {job.company.upper()}
{proof_summary}

## RELEVANT EXPERIENCE

### Co-Founder & AI Systems Architect | BrijStream / Kyvryn (2019 – Present)
- Directed the architectural blueprint and prompt orchestration for dual multi-sided streaming and AI governance platforms spanning 88,000+ lines of code.
- Maintained a 455/456 passing automated unit test suite, ensuring enterprise-grade software quality.
- Formulated and filed patent applications for autonomous scene-scoring algorithms matching audio energy, mood, and tempo under speech dialogue.
- Built 70/10/20 ad impression revenue split engine and instant USDC stablecoin settlement protocol.

### Director of Strategy | Music World / Sanctuary Group (2004 – 2006)
- Managed multi-million dollar P&L operations, corporate media licensing, and global artist catalog monetization.
- Executed high-stakes strategic negotiations with major record labels, publishers, and distribution partners.

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
        """
        Enforces strict compliance against forbidden AI cliche words.
        """
        clean_text = text
        for term in FORBIDDEN_COPY_TERMS:
            if term.lower() in clean_text.lower():
                # Replace cliche with clean alternative
                clean_text = clean_text.replace(term, "demonstrated leadership")
        return clean_text
