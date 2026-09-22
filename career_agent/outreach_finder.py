"""
Outreach Finder module for Sylvester's Autonomous Career Agent.
Identifies decision makers and drafts executive direct messages.
"""

from dataclasses import dataclass
from typing import Dict, List
from career_agent.config import VerifiedCandidateProfile
from career_agent.job_scanner import JobListing

@dataclass
class ExecutiveOutreachDraft:
    job_id: str
    company: str
    target_role: str
    target_title_suggestion: str
    personalized_message: str

class OutreachFinder:
    def __init__(self, profile: VerifiedCandidateProfile):
        self.profile = profile

    def create_outreach_draft(self, job: JobListing) -> ExecutiveOutreachDraft:
        target_role_title = self.determine_target_hiring_manager_title(job.title)
        message = self.craft_direct_message(job, target_role_title)

        return ExecutiveOutreachDraft(
            job_id=job.id,
            company=job.company,
            target_role=job.title,
            target_title_suggestion=target_role_title,
            personalized_message=message
        )

    def determine_target_hiring_manager_title(self, job_title: str) -> str:
        title_lower = job_title.lower()
        if "product manager" in title_lower or "pm" in title_lower:
            return "VP of Product / Head of Product"
        elif "forward deployed" in title_lower or "solutions" in title_lower:
            return "Head of Forward Deployed AI / VP of Solutions"
        elif "architect" in title_lower or "prompt" in title_lower or "engineer" in title_lower:
            return "CTO / VP of Engineering"
        elif "director" in title_lower or "vp" in title_lower:
            return "Chief Technology Officer / Chief Product Officer"
        return "Head of AI Talent Acquisition"

    def craft_direct_message(self, job: JobListing, target_title: str) -> str:
        return f"""Hi [Hiring Manager - {target_title}],

I noticed {job.company} is hiring for the {job.title} role.

I bring a unique combination of executive P&L leadership (former Director of Strategy at Music World / Sanctuary Group) and hands-on AI building experience—having recently directed AI agents to build, test, and deploy an 88,000 LOC media and governance platform with 455 passing unit tests and 3 patent applications.

I would love to connect and briefly discuss how my product strategy and AI system orchestration experience can support {job.company}'s current goals.

Best regards,
{self.profile.name}
{self.profile.title}"""
