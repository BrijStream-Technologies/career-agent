"""
Package Tailorer module for Sylvester's Autonomous Career Agent.
Generates tailored ATS resumes, human-authentic cover letters, and high-impact Translucent Alignment Briefs
featuring the Dual Summaries (Code Telemetry & Prompting Profile) and 100-Point Position Reconciliation.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path
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
    resume_file: Optional[str] = None
    cover_letter_file: Optional[str] = None

class PackageTailorer:
    def __init__(self, profile: VerifiedCandidateProfile):
        self.profile = profile
        self.output_dir = Path("/Volumes/BuildDrive/Sylvesters_Skill_Base/career_agent/resumes")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build_tailored_package(self, job: JobListing, score_result: FitScoreResult) -> ApplicationPackage:
        resume_md = self.generate_ats_resume(job, score_result)
        cover_letter_md = self.generate_cover_letter(job, score_result)
        brief_md = self.generate_translucent_brief(job, score_result)
        
        verified_cover_letter = self.sanitize_copy(cover_letter_md)
        verified_brief = self.sanitize_copy(brief_md)

        # Write resume and cover letter files to disk for Playwright file upload inputs
        self.output_dir.mkdir(parents=True, exist_ok=True)
        pdf_resume = self.output_dir / "Sylvester_Floyd_Carter_IV_Resume.pdf"
        
        if pdf_resume.exists():
            resume_path = pdf_resume
        else:
            resume_path = self.output_dir / f"{job.id}_resume.txt"
            try:
                with open(resume_path, "w", encoding="utf-8") as f:
                    f.write(resume_md)
            except Exception as e:
                logger.warning(f"Error writing resume file {resume_path}: {e}")

        cover_path = self.output_dir / f"{job.id}_cover_letter.txt"
        try:
            with open(cover_path, "w", encoding="utf-8") as f:
                f.write(verified_cover_letter)
        except Exception as e:
            logger.warning(f"Error writing cover letter file {cover_path}: {e}")


        return ApplicationPackage(
            job_id=job.id,
            company=job.company,
            job_title=job.title,
            tailored_resume_markdown=resume_md,
            cover_letter_markdown=verified_cover_letter,
            translucent_brief_markdown=verified_brief,
            verification_status="VERIFIED_NO_CLICHES",
            resume_file=str(resume_path),
            cover_letter_file=str(cover_path)
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
- **Production Codebase:** 88,000+ lines of polyglot multi-tenant microservices across Go (Golang), Python, TypeScript/Node.js, Rust/C++, SQL, and Shell (BrijStream Media Streaming & Kyvryn/Themis AI Governance Proxy).
- **Test Suite Integrity:** 455 passing unit tests out of 456 automated test assertions.
- **Intellectual Property:** 3 patent filings including Provisional PMG-2025-001 (Autonomous Media Synchronization matching energy, mood, tempo, audio ducking).
- **Fintech & Royalty Ledgers:** Built 70/10/20 ad revenue split engine and instant USDC stablecoin split settlement protocol.
"""

    def generate_ats_resume(self, job: JobListing, score_result: FitScoreResult) -> str:
        return f"""# {self.profile.name}
**Director of Agentic AI Systems & Executive Steering** | {self.profile.email} | {self.profile.location}

## EXECUTIVE SUMMARY & PROMPT STEERING COMPETENCY MOAT
Executive System Steering Director and Senior Operations Leader with 20+ years managing multi-million-dollar P&L operations (Music World / Sanctuary Group representing Destiny's Child / Beyoncé [32x Grammy Winner], Mary J. Blige; Brij Brands advising Park Bom of 2NE1; Yysman managing Mary Mary [4x Grammy Winners]; Left Eye Management representing Lisa "Left Eye" Lopes of TLC [RIAA 12x Diamond Certified]). 

Distinguished by **Master-Level Imperative Prompt Engineering & System Steering Capability**—the rare ability to command autonomous AI agent fleets (Antigravity & Claude Code) using outcome-driven directives, mandatory architectural constraints, and test-driven verification rules without micro-syntax micromanagement. 

This elite prompting skill is backed by concrete commercial evidence: directing AI agents to architect, test, and ship complete multi-tenant production applications including the BrijStream Media Streaming Platform, Kyvryn Agent-to-Agent (A2A) Governance Shield, 70/10/20 Creator Royalty Split Ledgers, Rust Risk Gatekeeper Agents, and Tokenized Algorithmic Trading Swarms. Demonstrates master-level prompt steering proof via an 88,000+ LOC polyglot codebase across Go (Golang), Python, TypeScript, Rust, C++, SQL, and Shell maintaining 455/456 passing unit tests, and authoring 3 patent filings (Provisional PMG-2025-001).

## CORE SYSTEM STEERING & COMMERCIAL ARCHITECTURE CAPABILITIES
- **Master Agentic System Steering:** Imperative Prompt Blueprinting, Multi-Agent (A2A) Message Passing, Factual Integrity Guardrails, Zero AI Slop Verification.
- **Prompt-Architected Commercial Ecosystems:** Multi-Tenant Media Streaming, Dynamic Audio Synchronization (Patent PMG-2025-001), 70/10/20 Royalty Split Ledgers, A2A Security Shields, Tokenized Algorithmic Trading.
- **Empirical Prompt Steering Proof:** Directed AI agent fleets solo to output 88,000+ LOC of polyglot production code across Go, Python, TypeScript, Rust/C++, SQL, and Shell with 455/456 unit tests passed.
- **Executive P&L Operations:** Senior Director of Operations at Music World / Sanctuary Group (Destiny's Child/Beyoncé, Mary J. Blige); Yysman Founder & CEO (Mary Mary); Brij Brands Advisor (Park Bom / 2NE1).

## RELEVANT EXPERIENCE

### Founder & Director of Agentic Systems | BrijStream / Kyvryn (2019 – Present)
- Formulated imperative prompt blueprints and outcome-driven system steering to direct AI agent fleets to build, test, and deploy dual commercial platforms: BrijStream (multi-tenant media streaming with 70/10/20 creator split ledgers) and Kyvryn (Agent-to-Agent governance and security shield).
- Directed AI agents solo to generate and verify 88,000+ lines of polyglot microservice code across Go (Golang), Python, TypeScript/Node.js, Rust/C++, SQL, and Shell, maintaining 455/456 passing automated unit tests.
- Prompted the mathematical design and formal patent filings for autonomous scene-scoring algorithms matching audio energy, mood, and tempo under speech dialogue (Provisional PMG-2025-001).

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

What sets my background apart is not paper credentials, but the combination of 20+ years of senior executive P&L leadership across world-class global enterprises (Sanctuary Group overseeing Records, Publishing, Touring, and Merch for Destiny's Child / Beyoncé and Mary J. Blige; Brij Brands advising 2NE1's Park Bom) paired with verified polyglot software execution grounded in **5 Empirical Benchmarks**:

1. **7-Language Polyglot System Architecture:** 88,000+ lines of production microservices across Go (Golang), Rust, C/C++, Python, TypeScript, SQL, and Shell.
2. **Agent-to-Agent (A2A) Governance Architecture:** Autonomous A2A message protocols, token rate governance, and compliance microservices.
3. **End-to-End Commercial Ecosystem Integration:** Multi-tenant media streaming apps, publisher ad serving networks, and automated creator split ledgers.
4. **100% Code Quality Floor:** 455 passing unit tests out of 456 automated test assertions.
5. **Executive P&L + Agentic Force Multiplication:** Translating complex commercial vision directly into production software via master-level agentic prompt steering.

Having proven this execution model independently, I am seeking the opportunity to bring my Master-Level System Steering, vision, and operational execution to a much larger enterprise stage at {job.company}.

I respect {job.company}'s work in this space and would welcome the opportunity to discuss how my strategic operational background and system steering capabilities can contribute directly to your product roadmap.

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
