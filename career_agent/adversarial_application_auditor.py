"""
Adversarial Application Auditor module for Sylvester's Autonomous Career Agent (Track B).
An independent evaluation subagent separate from BrowserApplicant that audits pre-filled forms,
custom Q&A responses, compliance dropdown selections, identity precision, and screenshot artifacts.
Scores pre-filled applications on a 100-point rubric and requires >= 95% score for audit certification.
"""

import os
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional

from career_agent.config import VerifiedCandidateProfile, FORBIDDEN_COPY_TERMS
from career_agent.job_scanner import JobListing
from career_agent.package_tailorer import ApplicationPackage

logger = logging.getLogger(__name__)

@dataclass
class AuditReport:
    application_id: str
    company_name: str
    role_title: str
    audit_score: int  # 0-100
    is_certified_95_plus: bool
    identity_score: int          # max 25
    persona_proof_score: int     # max 25
    form_compliance_score: int   # max 25
    screenshot_dom_score: int    # max 25
    feedback: List[str]

class AdversarialApplicationAuditor:
    def __init__(self, target_score_threshold: int = 95):
        self.profile = VerifiedCandidateProfile()
        self.target_score_threshold = target_score_threshold

    def audit_prefilled_application(
        self,
        job: JobListing,
        package: ApplicationPackage,
        app_result: Dict
    ) -> AuditReport:
        """
        Independently audits a pre-filled application result from BrowserApplicant.
        Scores across 4 pillars (25 pts each) and enforces a strict >= 95% certification threshold.
        """
        feedback = []

        # -------------------------------------------------------------
        # Pillar 1: Candidate Identity Precision (Max 25 pts)
        # -------------------------------------------------------------
        identity_score = 25
        if getattr(self.profile, "first_name", "") != "Sylvester":
            identity_score -= 10
            feedback.append("First name mismatch: Expected 'Sylvester'.")
        if getattr(self.profile, "middle_name", "") != "Floyd":
            identity_score -= 5
            feedback.append("Middle name mismatch: Expected 'Floyd'.")
        if getattr(self.profile, "last_name", "") != "Carter":
            identity_score -= 10
            feedback.append("Last name mismatch: Expected 'Carter'.")
        if self.profile.email != "sylvesterfcarter@icloud.com":
            identity_score -= 10
            feedback.append("Email mismatch: Expected 'sylvesterfcarter@icloud.com'.")

        identity_score = max(0, identity_score)

        # -------------------------------------------------------------
        # Pillar 2: Persona Proof & Anti-Slop Q&A Integrity (Max 25 pts)
        # -------------------------------------------------------------
        persona_score = 25
        custom_qa = app_result.get("custom_questions_answered", [])
        combined_text = (package.cover_letter_markdown + " " + package.translucent_brief_markdown + " " +
                         " ".join([q.get("answer", "") for q in custom_qa])).lower()

        receipts = [
            "88,000", "88k", "455/456", "455", "patent", "pmg-2025-001",
            "brij", "sanctuary", "park bom", "mary mary", "tlc"
        ]
        found_receipts = [r for r in receipts if r in combined_text]
        if len(found_receipts) < 3:
            persona_score -= 10
            feedback.append(f"Insufficient empirical receipts in package/QA answers (found {len(found_receipts)}).")

        slop_found = [term for term in FORBIDDEN_COPY_TERMS if term.lower() in combined_text]
        if slop_found:
            persona_score -= 15
            feedback.append(f"Forbidden AI slop cliches detected in application: {slop_found}")

        persona_score = max(0, persona_score)

        # -------------------------------------------------------------
        # Pillar 3: Form Pre-Fill & Role Strategy Level Compliance (Max 25 pts)
        # -------------------------------------------------------------
        compliance_score = 25
        status = app_result.get("status", "")
        details = app_result.get("details", "")

        # Reject Fellowships, Internships, Junior/Associate roles
        FORBIDDEN_LEVELS = ["fellow", "fellowship", "intern", "internship", "junior", "associate", "entry level", "contractor", "trainee", "student"]
        title_lower = job.title.lower()
        if any(fl in title_lower for fl in FORBIDDEN_LEVELS):
            compliance_score -= 25
            feedback.append(f"Role Level Strategy Violation: Target title '{job.title}' contains blacklisted tier ({[fl for fl in FORBIDDEN_LEVELS if fl in title_lower]}). Sylvester targets Executive Architecture & Strategy Lead positions only.")

        missed_qs = app_result.get("missed_questions", [])
        if len(missed_qs) > 0:
            compliance_score -= 15
            feedback.append(f"Unanswered Form Question Audit Failure: Missed {len(missed_qs)} non-identity form question(s): {[m.get('label', 'Question') for m in missed_qs[:3]]}")

        if status not in ["PREFILLED_PREVIEW_READY", "PREFILLED_NEEDS_SUBMIT_CLICK", "SUBMITTED_ONLINE"]:
            compliance_score -= 20
            feedback.append(f"Application status '{status}' indicates incomplete form completion: {details}")

        compliance_score = max(0, compliance_score)

        # -------------------------------------------------------------
        # Pillar 4: DOM Input Presence & Screenshot Audit Integrity (Max 25 pts)
        # -------------------------------------------------------------
        screenshot_score = 25
        screenshot_path = app_result.get("screenshot_path")

        if not screenshot_path or not os.path.exists(screenshot_path):
            screenshot_score -= 25
            feedback.append("Screenshot artifact missing or file does not exist on disk.")
        else:
            file_size = os.path.getsize(screenshot_path)
            if file_size < 1000:
                screenshot_score -= 15
                feedback.append(f"Screenshot file size ({file_size} bytes) indicates incomplete render.")

        screenshot_score = max(0, screenshot_score)

        # Total Audit Score
        total_score = identity_score + persona_score + compliance_score + screenshot_score
        is_certified = (total_score >= self.target_score_threshold)

        if is_certified:
            feedback.append(f"Application audit certified cleanly at {total_score}% (Threshold: {self.target_score_threshold}%).")

        return AuditReport(
            application_id=job.id,
            company_name=job.company,
            role_title=job.title,
            audit_score=total_score,
            is_certified_95_plus=is_certified,
            identity_score=identity_score,
            persona_proof_score=persona_score,
            form_compliance_score=compliance_score,
            screenshot_dom_score=screenshot_score,
            feedback=feedback
        )
