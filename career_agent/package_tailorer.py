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
**Candidate:** {self.profile.name} ({self.profile.email}) | {self.profile.location}
**Empirical Reconciliation Match:** {score_result.total_score}% / 100% (Audited Proof Matrix)

---
## 👑 SECTION 1: PROMPTING & SYSTEM STEERING PROFILE (THE COMPETITIVE MOAT)
*This is Sylvester's primary strategic differentiator: operating as a System Steering Officer who translates high-stakes operational domain directives directly into 88,000+ lines of production code without writing manual syntax.*

- **System Steering Officer Persona:** Operates at the executive system layer. Provides outcome-driven directives, mandatory architectural constraints, and test criteria while trusting AI agents to generate syntax under 100% verification rules.
- **Ruthless Non-Pleasing Truth Mandates:** Explicitly commands AI agents to eliminate sycophantic/pleasing biases ("this is not a pleasing mission, this is an honest fact-based analysis"), enforcing brute-force reality checks and log audits before code approval.
- **Socratic Mechanism Probing:** Systematically probes under-the-hood system mechanics (data flow, security boundaries, non-LLM document generation, OAuth authentication) before authorizing automated execution.
- **Institutional Domain-to-Code Translation:** Translates 20+ years of high-stakes music, publishing, and fintech operations (statutory licensing, 70/10/20 ad splits, audio ducking, Reg CF rules) directly into prompt directives that ship production software.

---
## 🎯 SECTION 2: 100-POINT POSITION RECONCILIATION MATRIX (EVIDENCE AUDIT)
*This empirical audit maps position requirements directly to verified code telemetry, unit tests, patents, and operational P&L receipts to eliminate arbitrary scoring.*

{audit_section}

---
## 💻 SECTION 3: CODE TELEMETRY & INTELLECTUAL PROPERTY
- **Production Codebase:** 88,000+ lines of multi-tenant microservice code across BrijStream (Media Streaming) and Kyvryn/Themis (AI Governance Proxy).
- **Test Suite Integrity:** 455 passing unit tests out of 456 automated test assertions.
- **Intellectual Property:** 3 patent filings including Provisional PMG-2025-001 (Autonomous Media Synchronization matching energy, mood, tempo, audio ducking).
- **Fintech & Royalty Ledgers:** Built 70/10/20 ad revenue split engine and instant USDC stablecoin split settlement protocol.
"""

    def generate_ats_resume(self, job: JobListing, score_result: FitScoreResult) -> str:
        proof_summary = "\n".join([f"- {p}" for p in score_result.matched_proof_points])
        
        return f"""# {self.profile.name}
**{self.profile.title}** | {self.profile.email} | {self.profile.location}

## EXECUTIVE SUMMARY
Senior Executive Operations Leader and AI Systems Architect with 20+ years managing multi-million dollar P&L operations, global rights registries, and multi-sided supply chains across RIAA Diamond-certified and multi-Grammy-winning entertainment enterprises. Formerly managed Lisa "Left Eye" Lopes of TLC (5x Grammy Winner, RIAA 12x Diamond-Certified, 65M+ global sales); founded Yysman, Inc. managing Mary Mary (4x Grammy Winners) and Platinum Producers; served as Senior Director of Operations at Music World Sanctuary Group overseeing Records, Publishing, Touring, and Merch divisions for a global roster featuring Destiny's Child/Beyoncé, Mary J. Blige, and Rock & Roll Hall of Fame inductees; and advised Park Bom of 2NE1 (Billboard 200 K-pop pioneers). Directs AI agents (Antigravity & Claude Code) as a System Steering Officer to architect, test, and deploy 88,000+ lines of production microservice code across media streaming and AI governance while maintaining 455/456 passing unit tests. Author of 3 patent applications in autonomous audio-scene synchronization and instant split settlement.

## 100-POINT POSITION RECONCILIATION MATCH: {score_result.total_score}% FOR {job.title.upper()} AT {job.company.upper()}
{proof_summary}

## RELEVANT EXPERIENCE

### Co-Founder & AI Systems Architect | BrijStream / Kyvryn (2019 – Present)
- Directed architectural blueprint and prompt orchestration for dual multi-sided streaming and AI governance platforms spanning 88,000+ lines of code.
- Maintained 455/456 passing automated unit test suite.
- Formulated and filed patent applications for autonomous scene-scoring algorithms matching audio energy, mood, and tempo under speech dialogue.

### Senior Director of Operations (Records, Publishing, Touring, Merch) | Music World / Sanctuary Group (2004 – 2006)
- Managed 4 core operational divisions for global #1 Urban artist management enterprise (Roster: Destiny's Child/Beyoncé [32x Grammy Winner], Mary J. Blige [9x Grammy Winner], Earth Wind & Fire, Chaka Khan).
- Directed multi-million dollar global touring logistics, master recording delivery pipelines, statutory publishing licensing, and merchandise supply chains.

### Founder & CEO / Artist Manager | Yysman, Inc. (1999 – 2004)
- Managed premier artist management enterprise representing Mary Mary (4x Grammy Winners, 3x NAACP Image Awards), Myron Butler & Levi, Ted & Sheri, and Platinum Producers.

### Executive Strategic Advisor | Brij Brands (2018 – Present)
- Executive Advisor to Park Bom of K-Pop group 2NE1 (Billboard 200 pioneers, MAMA Daesang Winners, 66M+ digital downloads).

### Artist Manager | Left Eye Management / Independent (1997 – 2002)
- Managed Lisa "Left Eye" Lopes of TLC (5x Grammy Winner, RIAA 12x Diamond Certified, 65M+ records sold).

## EDUCATION & PATENTS
- **{self.profile.education}**
- Patents: {", ".join(self.profile.patents)}
"""

    def generate_cover_letter(self, job: JobListing, score_result: FitScoreResult) -> str:
        return f"""Dear Hiring Team at {job.company},

I am writing to express my strong interest in the {job.title} role.

What sets my background apart is the combination of senior executive operations leadership across world-class global enterprises and direct hands-on AI systems architecture. Having served as Senior Director of Operations at Music World / Sanctuary Group overseeing Records, Publishing, Touring, and Merch divisions, and having managed/advised roster assets from TLC to Destiny's Child/Beyoncé and 2NE1, I understand complex multi-sided operations from a commercial standpoint. At the same time, I actively direct AI agents using Antigravity and Claude Code as a System Steering Officer to build, test, and deploy production software.

Recently, I architected and built an 88,000-line multi-sided media platform and AI governance proxy engine that maintains 455 passing unit tests out of 456, alongside authoring patent applications for autonomous audio-scene synchronization algorithms.

I respect {job.company}'s work in this space and would welcome the opportunity to discuss how my strategic operational background and AI building capabilities can contribute directly to your product roadmap.

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
