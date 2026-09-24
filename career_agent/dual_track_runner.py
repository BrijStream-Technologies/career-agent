"""
Dual-Track Automated Execution Engine for Sylvester's Autonomous Career Agent.
Track A: Dispatches up to 700 direct C-suite executive email packages per day via Apple Mail SMTP (smtp.mail.me.com:587).
Track B: Navigates target enterprise career sites & ATS portals via Playwright Chrome, auto-filling applications, answering custom AI questions, handling IMAP OTP verification, and saving HITL audit screenshots.
"""

import os
import sys
import time
import logging
from datetime import datetime
from typing import Dict, List

from career_agent.config import VerifiedCandidateProfile
from career_agent.strategic_database import StrategicDatabase, StrategicOpportunity
from career_agent.scaled_intelligence_fetcher import ScaledIntelligenceFetcher
from career_agent.adversarial_evaluator import AdversarialEvaluator
from career_agent.executive_direct_pitcher import ExecutiveDirectPitcher
from career_agent.direct_site_applicant import DirectSiteApplicant
from career_agent.package_tailorer import PackageTailorer
from career_agent.job_scanner import JobListing

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class DualTrackBatchRunner:
    def __init__(self, daily_email_limit: int = 700, headless: bool = True):
        # Configure iCloud SMTP credentials for live sending
        if "ICLOUD_APP_PASSWORD" not in os.environ:
            os.environ["ICLOUD_APP_PASSWORD"] = "oqpx-ebgr-cioh-ajtg"
        
        self.profile = VerifiedCandidateProfile()
        self.db = StrategicDatabase()
        self.daily_email_limit = daily_email_limit
        self.scaled_fetcher = ScaledIntelligenceFetcher()
        self.evaluator = AdversarialEvaluator(target_score_threshold=95)
        self.tailorer = PackageTailorer(self.profile)
        self.executive_pitcher = ExecutiveDirectPitcher(self.profile, self.db)
        self.direct_applicant = DirectSiteApplicant(self.profile, self.db, headless=headless)

    def execute_track_a_smtp_dispatch(self, limit: int = 700, live_send: bool = True) -> Dict:
        """
        Track A: Dispatches up to 700 C-suite direct email packages per day.
        If live_send is True, sends via Apple Mail SMTP (smtp.mail.me.com:587).
        """
        if live_send:
            os.environ["SAVE_AS_DRAFT"] = "false"
        else:
            os.environ["SAVE_AS_DRAFT"] = "true"

        # Fetch candidate target enterprises from SQLite DB
        raw_enterprises = self.db.get_high_intensity_enterprises(min_score=50)
        enterprises = [e for e in raw_enterprises if not ('scale' in e.domain and any(c.isdigit() for c in e.domain))]
        dispatched_count = 0
        failed_count = 0
        hold_count = 0

        logger.info(f"Starting Track A Email Outreach Batch (Limit: {limit}, Live Send: {live_send})...")

        for ent in enterprises:
            if dispatched_count >= limit:
                logger.info(f"Daily email limit ({limit}) reached for Track A.")
                break

            execs = self.db.get_executives_for_enterprise(ent.id)
            if not execs:
                continue

            target_exec = execs[0]
            if not target_exec.mx_verified:
                hold_count += 1
                continue

            pitch_res = self.executive_pitcher.pitch_executive_direct(
                enterprise_id=ent.id,
                company_name=ent.company_name,
                domain=ent.domain,
                exec_name=target_exec.name,
                exec_title=target_exec.title,
                exec_email=target_exec.email,
                tech_gaps=ent.tech_stack_gaps
            )

            status = pitch_res.get("status", "")
            if status in ["DISPATCHED", "DRAFTED_TO_ICLOUD"]:
                dispatched_count += 1
                logger.info(f"[{dispatched_count}/{limit}] Sent executive package to {target_exec.name} ({target_exec.email}) @ {ent.company_name}")
                # Modest pacing delay between SMTP transmissions
                if live_send:
                    time.sleep(1.5)
            elif "HOLD" in status:
                hold_count += 1
            else:
                failed_count += 1

        return {
            "track": "Track A (C-Suite Email Outreach)",
            "limit": limit,
            "dispatched": dispatched_count,
            "held_unverified": hold_count,
            "failed": failed_count,
            "live_send": live_send
        }

    def execute_track_b_direct_site_applications(self, limit: int = 10, submit_live: bool = False) -> Dict:
        """
        Track B: Searches target company career portals, pre-fills online forms using Playwright Chrome,
        answers custom AI questions, handles account creation / OTP codes, and saves full-page screenshots.
        """
        raw_enterprises = self.db.get_high_intensity_enterprises(min_score=70)
        enterprises = [e for e in raw_enterprises if not ('scale' in e.domain and any(c.isdigit() for c in e.domain))]
        processed_count = 0
        prefilled_count = 0
        screenshots = []

        logger.info(f"Starting Track B Direct Site Application Batch (Limit: {limit}, Submit Live: {submit_live})...")

        for ent in enterprises:
            if processed_count >= limit:
                break

            careers_url = f"https://{ent.domain}/careers"
            job = JobListing(
                id=f"direct_{ent.id}",
                title="Chief Agentic Steering Officer / Executive AI Systems Architect",
                company=ent.company_name,
                location="Remote / Hybrid",
                is_remote=True,
                base_salary_min=250000,
                base_salary_max=400000,
                estimated_tc=550000,
                posting_date=datetime.now(),
                description=f"Executive strategic steering and AI systems architecture for {ent.company_name}.",
                source_url=careers_url
            )

            # Build tailored application package
            from career_agent.fit_scorer import FitScorer, FitScoreResult
            from career_agent.config import JobSearchConfig
            scorer = FitScorer(self.profile, JobSearchConfig())
            score_res = scorer.score_job(job)
            pkg = self.tailorer.build_tailored_package(job, score_res)

            app_res = self.direct_applicant.browser_applicant.apply_online(job, pkg, submit_live=submit_live)
            processed_count += 1

            # Independent Adversarial Audit Cycle (Requires >= 95% score)
            from career_agent.adversarial_application_auditor import AdversarialApplicationAuditor
            auditor = AdversarialApplicationAuditor(target_score_threshold=95)
            audit_report = auditor.audit_prefilled_application(job, pkg, app_res)

            if audit_report.is_certified_95_plus and app_res.get("screenshot_path"):
                prefilled_count += 1
                screenshots.append(app_res["screenshot_path"])
                logger.info(f"[{processed_count}/{limit}] CERTIFIED (Audit Score {audit_report.audit_score}% >= 95%) pre-filled application for {ent.company_name}. Screenshot: {app_res['screenshot_path']}")
                
                # Record in database
                opp = StrategicOpportunity(
                    id=job.id,
                    enterprise_id=ent.id,
                    company_name=ent.company_name,
                    role_title=job.title,
                    source_type="DIRECT_SITE",
                    url=careers_url,
                    status="AUDIT_CERTIFIED_PREVIEW_READY",
                    screenshot_path=app_res["screenshot_path"]
                )
                self.db.upsert_opportunity(opp)
            else:
                logger.warning(f"[{processed_count}/{limit}] REJECTED by Adversarial Auditor for {ent.company_name} (Score: {audit_report.audit_score}% < 95%): {audit_report.feedback}")

        return {
            "track": "Track B (Direct Company Site Applications)",
            "limit": limit,
            "processed": processed_count,
            "prefilled_with_screenshots": prefilled_count,
            "screenshots": screenshots,
            "submit_live": submit_live
        }

    def run_daily_dual_track_execution(
        self,
        email_limit: int = 700,
        direct_site_limit: int = 10,
        live_send_emails: bool = True,
        submit_live_forms: bool = False
    ) -> str:
        """
        Executes both Track A and Track B, returning a high-level executive report.
        """
        start_time = datetime.now()
        track_a_res = self.execute_track_a_smtp_dispatch(limit=email_limit, live_send=live_send_emails)
        track_b_res = self.execute_track_b_direct_site_applications(limit=direct_site_limit, submit_live=submit_live_forms)
        duration = (datetime.now() - start_time).total_seconds()

        report_lines = [
            "# DUAL-TRACK AUTOMATED AGENT EXECUTION REPORT",
            f"**Candidate:** {self.profile.name} | **Execution Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Total Execution Duration:** {duration:.1f} seconds",
            "",
            "---",
            "## 📧 TRACK A: C-SUITE DIRECT EMAIL OUTREACH (700/DAY RATE LIMIT)",
            f"- **Target Daily Email Limit:** {track_a_res['limit']} emails",
            f"- **Emails Dispatched via SMTP (Apple Mail):** {track_a_res['dispatched']}",
            f"- **Hold (Unverified MX Records):** {track_a_res['held_unverified']}",
            f"- **Dispatch Status:** {'LIVE SMTP DISPATCH' if live_send_emails else 'DRAFTED TO ICLOUD'}",
            "",
            "---",
            "## 🌐 TRACK B: DIRECT COMPANY SITE APPLICATIONS (PLAYWRIGHT CHROME)",
            f"- **Company Portals Processed:** {track_b_res['processed']}",
            f"- **Forms Pre-filled & Audited:** {track_b_res['prefilled_with_screenshots']}",
            f"- **Screenshots Saved for HITL Review:** {len(track_b_res['screenshots'])}",
            f"- **Submission Mode:** {'LIVE SUBMIT' if submit_live_forms else 'PRE-FILLED PREVIEW (HITL AUDIT)'}",
            "",
            "---",
            "## 📸 CAPTURED APPLICATION SCREENSHOTS (HITL AUDIT TRAIL)"
        ]

        for path in track_b_res.get("screenshots", []):
            report_lines.append(f"- `file://{path}`")

        report_md = "\n".join(report_lines)
        return report_md

def main():
    runner = DualTrackBatchRunner(daily_email_limit=700, headless=True)
    # Run active dual-track execution
    report = runner.run_daily_dual_track_execution(
        email_limit=700,
        direct_site_limit=5,
        live_send_emails=True,
        submit_live_forms=False
    )
    print(report)

if __name__ == "__main__":
    main()
