"""
Agent Orchestrator module for Sylvester's Autonomous Career Agent.
Main execution entry point managing the complete 5-phase daily operational pipeline including automated contact dispatch.
"""

import sys
from typing import List, Dict, Optional
from career_agent.config import VerifiedCandidateProfile, JobSearchConfig
from career_agent.job_scanner import JobScanner, JobListing
from career_agent.fit_scorer import FitScorer, FitScoreResult
from career_agent.package_tailorer import PackageTailorer, ApplicationPackage
from career_agent.outreach_finder import OutreachFinder, ExecutiveOutreachDraft
from career_agent.executive_digest import ExecutiveDigestBuilder
from career_agent.contact_dispatcher import ContactDispatcher, DispatchRecord

class CareerAgentOrchestrator:
    def __init__(self, auto_dispatch: bool = True):
        self.profile = VerifiedCandidateProfile()
        self.config = JobSearchConfig()
        self.scanner = JobScanner(self.config)
        self.scorer = FitScorer(self.profile, self.config)
        self.tailorer = PackageTailorer(self.profile)
        self.outreach_finder = OutreachFinder(self.profile)
        self.digest_builder = ExecutiveDigestBuilder()
        self.dispatcher = ContactDispatcher(self.profile, auto_send=auto_dispatch)

    def run_daily_pipeline(self, raw_listings: List[Dict]) -> str:
        """
        Executes all 5 operational phases end-to-end:
        Phase 1: Scan & Filter
        Phase 2: Score Jobs (100-pt proof matrix)
        Phase 3: Tailor Packages (ATS Resume & Cover Letter)
        Phase 4: Direct Executive Contact Identification & Automated Dispatch
        Phase 5: Executive Digest Generation
        """
        # Phase 1: Scan & Filter
        valid_listings = self.scanner.normalize_and_filter(raw_listings)
        
        # Phase 2: Score Jobs
        scored_jobs = []
        for job in valid_listings:
            score = self.scorer.score_job(job)
            scored_jobs.append((job, score))

        # Phase 3 & 4: Tailor Packages, Outreach Drafts & Auto-Dispatch
        packages: Dict[str, ApplicationPackage] = {}
        outreach_drafts: Dict[str, ExecutiveOutreachDraft] = {}
        dispatches: Dict[str, DispatchRecord] = {}

        for job, score in scored_jobs:
            if score.recommendation in ["AUTO_APPLY", "REVIEW"]:
                pkg = self.tailorer.build_tailored_package(job, score)
                packages[job.id] = pkg
                
                draft = self.outreach_finder.create_outreach_draft(job)
                outreach_drafts[job.id] = draft

                # Automated Identification & Contact Dispatch for High & Medium Fit Roles
                if score.recommendation in ["AUTO_APPLY", "REVIEW"]:
                    dispatch_rec = self.dispatcher.dispatch_outreach(job, pkg, draft)
                    dispatches[job.id] = dispatch_rec

        # Phase 5: Build Executive Digest
        digest_markdown = self.digest_builder.build_digest_markdown(
            total_scanned=len(raw_listings),
            scored_jobs=scored_jobs,
            packages=packages,
            outreach_drafts=outreach_drafts
        )

        return digest_markdown

def main():
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
            "description": "Lead AI voice orchestration, P&L management, AI prompt architecture, audio licensing, and rights registry.",
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
            "description": "Forward deployed AI lead working with customers to build AI agents, system architecture, prompt engineering, Python, P&L strategy.",
            "source_url": "https://anthropic.com/careers/forward-deployed-lead"
        }
    ]

    orchestrator = CareerAgentOrchestrator(auto_dispatch=True)
    digest = orchestrator.run_daily_pipeline(sample_listings)
    print(digest)

if __name__ == "__main__":
    main()
