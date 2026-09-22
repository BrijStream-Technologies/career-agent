"""
Agent Orchestrator module for Sylvester's Autonomous Career Agent.
Main execution entry point managing the complete 5-phase daily operational pipeline.
"""

import sys
from typing import List, Dict, Optional
from career_agent.config import VerifiedCandidateProfile, JobSearchConfig
from career_agent.job_scanner import JobScanner, JobListing
from career_agent.fit_scorer import FitScorer, FitScoreResult
from career_agent.package_tailorer import PackageTailorer, ApplicationPackage
from career_agent.outreach_finder import OutreachFinder, ExecutiveOutreachDraft
from career_agent.executive_digest import ExecutiveDigestBuilder

class CareerAgentOrchestrator:
    def __init__(self):
        self.profile = VerifiedCandidateProfile()
        self.config = JobSearchConfig()
        self.scanner = JobScanner(self.config)
        self.scorer = FitScorer(self.profile, self.config)
        self.tailorer = PackageTailorer(self.profile)
        self.outreach_finder = OutreachFinder(self.profile)
        self.digest_builder = ExecutiveDigestBuilder()

    def run_daily_pipeline(self, raw_listings: List[Dict]) -> str:
        """
        Executes all 5 operational phases end-to-end.
        """
        # Phase 1: Scan & Filter
        valid_listings = self.scanner.normalize_and_filter(raw_listings)
        
        # Phase 2: Score Jobs
        scored_jobs = []
        for job in valid_listings:
            score = self.scorer.score_job(job)
            scored_jobs.append((job, score))

        # Phase 3 & 4: Tailor Packages & Outreach Drafts for High-Fit Roles
        packages: Dict[str, ApplicationPackage] = {}
        outreach_drafts: Dict[str, ExecutiveOutreachDraft] = {}

        for job, score in scored_jobs:
            if score.recommendation in ["AUTO_APPLY", "REVIEW"]:
                pkg = self.tailorer.build_tailored_package(job, score)
                packages[job.id] = pkg
                
                draft = self.outreach_finder.create_outreach_draft(job)
                outreach_drafts[job.id] = draft

        # Phase 5: Build Executive Digest
        digest_markdown = self.digest_builder.build_digest_markdown(
            total_scanned=len(raw_listings),
            scored_jobs=scored_jobs,
            packages=packages,
            outreach_drafts=outreach_drafts
        )

        return digest_markdown

def main():
    # Sample execution entry point with realistic 2026 remote job opportunities
    sample_listings = [
        {
            "id": "job_001",
            "title": "Principal AI Product Manager",
            "company": "ElevenLabs",
            "location": "Remote - US",
            "is_remote": True,
            "base_salary_min": 240000,
            "base_salary_max": 290000,
            "estimated_tc": 360000,
            "description": "Looking for a Principal AI Product Manager to lead product strategy, AI voice orchestration, and audio licensing partnerships. Must have cross-functional executive leadership, P&L experience, and understanding of AI prompt architecture and royalty models.",
            "source_url": "https://elevenlabs.io/careers/principal-ai-pm"
        },
        {
            "id": "job_002",
            "title": "Forward Deployed AI Solutions Lead",
            "company": "Anthropic",
            "location": "Remote - US / Global",
            "is_remote": True,
            "base_salary_min": 250000,
            "base_salary_max": 320000,
            "estimated_tc": 480000,
            "description": "Forward Deployed AI Lead to work with enterprise customers deploying AI agent architectures. Requires full-stack system architecture, prompt engineering, Python, test-driven development, and customer strategy experience.",
            "source_url": "https://anthropic.com/careers/forward-deployed-lead"
        },
        {
            "id": "job_003",
            "title": "Director of AI Product Strategy",
            "company": "Warner Music Group",
            "location": "Remote - US",
            "is_remote": True,
            "base_salary_min": 260000,
            "base_salary_max": 350000,
            "estimated_tc": 450000,
            "description": "Lead strategic AI music initiatives, rights registry, audio synchronization, and ad-tech monetization. Background in music licensing, P&L management, patents, and AI platform design required.",
            "source_url": "https://wmg.com/careers/director-ai-strategy"
        },
        {
            "id": "job_004",
            "title": "Junior Python Developer (On-site)",
            "company": "Local Agency Inc",
            "location": "Atlanta, GA (On-site)",
            "is_remote": False,
            "base_salary_min": 60000,
            "base_salary_max": 75000,
            "estimated_tc": 75000,
            "description": "Entry level local junior developer position.",
            "source_url": "https://example.com/junior-dev"
        }
    ]

    orchestrator = CareerAgentOrchestrator()
    digest = orchestrator.run_daily_pipeline(sample_listings)
    print(digest)

if __name__ == "__main__":
    main()
