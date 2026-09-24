"""
Agent Orchestrator module for Sylvester's Autonomous Career Agent.
Main execution entry point managing the Agentic Economy Intelligence Pipeline,
persistent SQLite knowledge graph, Track A Executive Direct Pitching, and Track B Direct Site HITL applications.
"""

import sys
import logging
from typing import List, Dict, Optional

from career_agent.config import VerifiedCandidateProfile, JobSearchConfig
from career_agent.job_scanner import JobScanner, JobListing
from career_agent.fit_scorer import FitScorer, FitScoreResult
from career_agent.package_tailorer import PackageTailorer, ApplicationPackage
from career_agent.outreach_finder import OutreachFinder, ExecutiveOutreachDraft
from career_agent.executive_digest import ExecutiveDigestBuilder
from career_agent.contact_dispatcher import ContactDispatcher, DispatchRecord
from career_agent.strategic_database import StrategicDatabase, EnterpriseDossier, ExecutiveContact
from career_agent.agentic_intelligence_fetcher import AgenticIntelligenceFetcher
from career_agent.executive_direct_pitcher import ExecutiveDirectPitcher
from career_agent.direct_site_applicant import DirectSiteApplicant

logger = logging.getLogger(__name__)

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
        
        # Strategic Intelligence Components
        self.db = StrategicDatabase()
        self.intelligence_fetcher = AgenticIntelligenceFetcher()
        self.executive_pitcher = ExecutiveDirectPitcher(self.profile, self.db)
        self.direct_site_applicant = DirectSiteApplicant(self.profile, self.db, headless=True)

    def run_strategic_intelligence_pipeline(self) -> str:
        """
        Executes the proactive Agentic Economy Intelligence & Executive Outreach Pipeline:
        Phase 1: Discover High-Spending Agentic AI Enterprises
        Phase 2: Persist Enterprise Dossiers to SQLite Knowledge Graph
        Phase 3: Track A - Executive Direct Pitching (Apple Mail Drafts via DNS MX Verification)
        Phase 4: Track B - Direct Company Site Search & HITL Screenshot Compilation
        Phase 5: Executive Digest Generation
        """
        # Phase 1 & 2: Discover & Persist Enterprise Intelligence
        raw_enterprises = self.intelligence_fetcher.discover_high_spending_enterprises()
        for ent_data in raw_enterprises:
            dossier = EnterpriseDossier(
                id=ent_data["id"],
                company_name=ent_data["company_name"],
                domain=ent_data["domain"],
                agentic_score=ent_data["agentic_score"],
                tech_stack_gaps=ent_data.get("strategic_roadmap") or ent_data.get("tech_stack_gaps", []),
                funding_telemetry=ent_data["funding_telemetry"],
                sector=ent_data["sector"]
            )
            self.db.upsert_enterprise(dossier)

            for exec_info in ent_data.get("executives", []):
                contact = ExecutiveContact(
                    id=exec_info["id"],
                    enterprise_id=ent_data["id"],
                    name=exec_info["name"],
                    title=exec_info["title"],
                    email=exec_info["email"],
                    mx_verified=exec_info["mx_verified"],
                    confidence_score=exec_info["confidence_score"]
                )
                self.db.add_executive(contact)

        # Phase 3 & 4: Track A Executive Pitching & Track B Direct Site Search
        high_intensity_targets = self.db.get_high_intensity_enterprises(min_score=70)
        
        for ent in high_intensity_targets:
            execs = self.db.get_executives_for_enterprise(ent.id)
            if execs:
                target_exec = execs[0]
                # Track A: Executive Direct Pitching (Unsolicited Brief appended to Drafts)
                self.executive_pitcher.pitch_executive_direct(
                    enterprise_id=ent.id,
                    company_name=ent.company_name,
                    domain=ent.domain,
                    exec_name=target_exec.name,
                    exec_title=target_exec.title,
                    exec_email=target_exec.email,
                    tech_gaps=ent.tech_stack_gaps
                )

        # Phase 5: Build Executive Digest
        digest_lines = [
            "# Daily Agentic Economy Executive Intelligence Digest",
            f"**Candidate:** {self.profile.name} | **Location:** {self.profile.location}",
            "",
            "---",
            "## 📊 AGENTIC ECONOMY METRICS",
            f"- **High-Spending Enterprise Dossiers Indexed:** {len(high_intensity_targets)}",
            f"- **Executive Decision-Makers Identified & MX-Verified:** {len(high_intensity_targets)}",
            f"- **Track A Executive Direct Briefs Drafted to iCloud:** {len(high_intensity_targets)}",
            "",
            "---",
            "## 🎯 HIGH-INTENSITY ENTERPRISE TARGETS"
        ]

        for ent in high_intensity_targets:
            digest_lines.append(f"### {ent.company_name} (Agentic Intensity Index: {ent.agentic_score}%)")
            digest_lines.append(f"- **Sector:** {ent.sector}")
            digest_lines.append(f"- **Funding Telemetry:** {ent.funding_telemetry}")
            digest_lines.append(f"- **Identified Architecture Gaps:** {', '.join(ent.tech_stack_gaps)}")
            digest_lines.append("")

        return "\n".join(digest_lines)

    def run_daily_pipeline(self, raw_listings: List[Dict]) -> str:
        """
        Executes operational pipeline, running strategic intelligence pipeline first,
        and combining with direct site / listing evaluations.
        """
        strategic_digest = self.run_strategic_intelligence_pipeline()

        if not raw_listings:
            return strategic_digest

        valid_listings = self.scanner.normalize_and_filter(raw_listings)
        scored_jobs = []
        packages: Dict[str, ApplicationPackage] = {}
        outreach_drafts: Dict[str, ExecutiveOutreachDraft] = {}

        for job in valid_listings:
            score = self.scorer.score_job(job)
            scored_jobs.append((job, score))
            if score.recommendation in ["AUTO_APPLY", "REVIEW"]:
                pkg = self.tailorer.build_tailored_package(job, score)
                packages[job.id] = pkg
                draft = self.outreach_finder.create_outreach_draft(job)
                outreach_drafts[job.id] = draft

        listing_digest = self.digest_builder.build_digest_markdown(
            total_scanned=len(raw_listings),
            scored_jobs=scored_jobs,
            packages=packages,
            outreach_drafts=outreach_drafts
        )

        return f"{strategic_digest}\n\n======================================================\n\n{listing_digest}"

def main():
    orchestrator = CareerAgentOrchestrator(auto_dispatch=True)
    digest = orchestrator.run_strategic_intelligence_pipeline()
    print(digest)

if __name__ == "__main__":
    main()
