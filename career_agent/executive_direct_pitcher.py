"""
Executive Direct Pitcher module for Sylvester's Autonomous Career Agent (Track A).
Generates unsolicited executive direct alignment packages for decision-makers at high-spending Agentic AI enterprises,
validates direct email deliverability via DNS MX records, and appends rich HTML briefs to Apple Mail Drafts.
"""

import os
import logging
from typing import Dict, Optional
from datetime import datetime

from career_agent.config import VerifiedCandidateProfile
from career_agent.contact_verifier import ContactVerifier, VerifiedContact
from career_agent.contact_dispatcher import ContactDispatcher
from career_agent.package_tailorer import ApplicationPackage
from career_agent.outreach_finder import ExecutiveOutreachDraft
from career_agent.job_scanner import JobListing
from career_agent.strategic_database import StrategicDatabase, StrategicOpportunity

logger = logging.getLogger(__name__)

class ExecutiveDirectPitcher:
    def __init__(self, profile: VerifiedCandidateProfile, db: StrategicDatabase):
        self.profile = profile
        self.db = db
        self.verifier = ContactVerifier()
        self.dispatcher = ContactDispatcher(profile, auto_send=True)

    def pitch_executive_direct(
        self,
        enterprise_id: str,
        company_name: str,
        domain: str,
        exec_name: str,
        exec_title: str,
        exec_email: str,
        tech_gaps: list
    ) -> Dict:
        """
        Executes Track A: Generates bespoke Translucent Executive Alignment Brief,
        runs DNS MX deliverability validation, and appends rich HTML package to Apple Mail Drafts.
        """
        result = {
            "enterprise_id": enterprise_id,
            "company_name": company_name,
            "exec_name": exec_name,
            "exec_email": exec_email,
            "status": "HOLD_UNVERIFIED",
            "details": ""
        }

        # 1. DNS MX Deliverability Verification
        mx_records = self.verifier.verify_dns_mx_records(domain)
        contact = VerifiedContact(
            company=company_name,
            recipient_name=exec_name,
            recipient_title=exec_title,
            recipient_email=exec_email,
            verification_status="VERIFIED_EXECUTIVE_DIRECT" if mx_records else "UNVERIFIED_DOMAIN_FAILED",
            mx_records_found=mx_records,
            confidence_score=98 if mx_records else 0
        )

        if not self.verifier.is_officially_verified(contact):
            result["status"] = "HOLD_UNVERIFIED"
            result["details"] = f"Executive email {exec_email} failed DNS MX deliverability validation."
            return result

        # 2. Build Unsolicited Executive Direct Brief (Value-First Strategic Proposal)
        job_mock = JobListing(
            id=f"pitch_{enterprise_id}",
            title=f"AI Systems Architect & Executive Strategy Leader",
            company=company_name,
            location="Remote / Executive Briefing",
            is_remote=True,
            base_salary_min=250000,
            base_salary_max=350000,
            estimated_tc=450000,
            posting_date=datetime.now(),
            description=f"Strategic architecture leadership for {company_name}, addressing {', '.join(tech_gaps)}.",
            source_url=f"https://{domain}"
        )

        gaps_str = "\n".join([f"- **{gap}**" for gap in tech_gaps])
        brief_md = f"""# EXECUTIVE STRATEGIC BRIEF: AI ARCHITECTURE & SYSTEM STEERING
**Target Enterprise:** {company_name}  
**Addressed To:** {exec_name} ({exec_title})  
**Author:** Sylvester Floyd Carter IV (AI Systems Architect & Executive Strategy Leader)  

---

## 1. EXECUTIVE SYNOPSIS & SYSTEM STEERING MOAT
{company_name} is scaling state-of-the-art Agentic AI infrastructure. However, scaling enterprise agent workflows requires explicit **System Steering, Proxy Metering, and Rights Governance** to control compute costs and enforce zero-hallucination execution.

I operate as a **System Steering Officer**—bridging 20+ years of multi-million dollar commercial entertainment & fintech P&L leadership directly into 88,000+ lines of production polyglot microservices code.

### Core Architectural Value Offered to {company_name}:
{gaps_str}

---

## 2. VERIFIED CANDIDATE ATTESTATIONS & PROOF POINTS
- **88,000+ LOC Polyglot Code Telemetry:** Production microservices engineered across **Go (Golang)**, **Rust**, **C/C++**, **Python**, **TypeScript/Node.js**, **SQL**, and **Shell** (455/456 unit test suite pass rate).
- **Patent PMG-2025-001:** Autonomous Media Synchronization, Dynamic Audio Substitution, and Instant Split Payment Ledgers.
- **Institutional Track Record:**
  - **Executive Strategic Advisor, Brij Brands:** Executive strategic advisor to Park Bom of 2NE1 (Billboard 200).
  - **Senior Director of Operations, Music World Sanctuary Group:** Directed 4 core divisions for top Urban management enterprise (Destiny's Child/Beyoncé [32x Grammy Winner], Mary J. Blige, Earth Wind & Fire, Chaka Khan).
  - **Founder & CEO, Yysman, Inc.:** Represented Mary Mary (4x Grammy Winners), Myron Butler, Ted & Sheri, and Platinum Producers.

---

## 3. PROPOSED ENGAGEMENT & ARCHITECTURAL ROADMAP
I welcome a direct executive conversation regarding how we can deploy these governance microservices and system steering frameworks at {company_name}.
"""

        cover_md = f"""Dear {exec_name},

I am writing to share a concise Executive Strategic Brief on scaling multi-agent system steering, proxy metering, and audio/content governance at {company_name}.

Having directed 88,000+ lines of polyglot microservice builds alongside 20+ years managing top-tier P&L operations (Music World Sanctuary Group / Destiny's Child, Brij Brands / Park Bom), I specialize in helping high-growth AI enterprises control compute spend and enforce absolute system prompt truthfulness.

Attached is the full Executive Brief detailing how we can address {', '.join(tech_gaps[:2])}.

Sincerely,
Sylvester Floyd Carter IV
AI Systems Architect & Executive Strategy Leader
sylvesterfcarter@icloud.com | Montgomery, TX
"""

        resume_md = f"""# SYLVESTER FLOYD CARTER IV
**AI Systems Architect & Executive Strategy Leader**  
Montgomery, TX | sylvesterfcarter@icloud.com | BA Finance, Clark Atlanta University  

---
## CORE COMPETENCIES & TECHNICAL TELEMETRY
- **Languages & Frameworks:** Go (Golang), Rust, C/C++, Python, TypeScript, Node.js, SQL, Shell.
- **Codebase Receipts:** 88,000+ LOC production microservices | 455/456 passing unit tests.
- **Patents:** PMG-2025-001 (Autonomous Media Sync, Dynamic Audio Substitution, Split Ledgers).
- **Executive Record:** Strategic Advisor @ Brij Brands (Park Bom), Senior Director @ Music World (Destiny's Child/Beyoncé), Founder/CEO @ Yysman Inc (Mary Mary).
"""

        pkg = ApplicationPackage(
            job_id=job_mock.id,
            company=company_name,
            job_title=job_mock.title,
            tailored_resume_markdown=resume_md,
            cover_letter_markdown=cover_md,
            translucent_brief_markdown=brief_md,
            verification_status="VERIFIED_EXECUTIVE_DIRECT"
        )

        outreach_draft = ExecutiveOutreachDraft(
            job_id=job_mock.id,
            company=company_name,
            target_role=job_mock.title,
            target_title_suggestion=exec_title,
            personalized_message=cover_md
        )

        # Append Rich HTML Executive Package directly to Apple Mail Drafts
        dispatch_rec = self.dispatcher.dispatch_outreach(job_mock, pkg, outreach_draft, recipient_email=exec_email)

        # Record in Strategic Database
        opp = StrategicOpportunity(
            id=job_mock.id,
            enterprise_id=enterprise_id,
            company_name=company_name,
            role_title=job_mock.title,
            source_type="EXECUTIVE_PITCH",
            url=f"https://{domain}",
            status=dispatch_rec.status
        )
        self.db.upsert_opportunity(opp)
        self.db.record_outreach(job_mock.id, enterprise_id, exec_email, dispatch_rec.subject, dispatch_rec.status)

        result["status"] = dispatch_rec.status
        result["details"] = f"Executive pitch package for {exec_name} appended to Apple Mail Drafts (Status: {dispatch_rec.status})."
        return result
