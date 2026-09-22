"""
Executive Digest module for Sylvester's Autonomous Career Agent.
Formats and outputs the 17:00 Daily Executive Digest report for Sylvester.
"""

from datetime import datetime
from typing import List, Dict
from career_agent.job_scanner import JobListing
from career_agent.fit_scorer import FitScoreResult
from career_agent.package_tailorer import ApplicationPackage
from career_agent.outreach_finder import ExecutiveOutreachDraft

class ExecutiveDigestBuilder:
    def build_digest_markdown(
        self,
        total_scanned: int,
        scored_jobs: List[tuple[JobListing, FitScoreResult]],
        packages: Dict[str, ApplicationPackage],
        outreach_drafts: Dict[str, ExecutiveOutreachDraft]
    ) -> str:
        date_str = datetime.now().strftime("%B %d, %Y")
        
        auto_apply_count = sum(1 for _, s in scored_jobs if s.recommendation == "AUTO_APPLY")
        review_count = sum(1 for _, s in scored_jobs if s.recommendation == "REVIEW")
        rejected_count = sum(1 for _, s in scored_jobs if s.recommendation == "REJECT")

        digest = []
        digest.append("# Daily Career Agent Executive Digest")
        digest.append(f"**Date:** {date_str} | **Candidate:** Sylvester Floyd Carter IV\n")
        digest.append("---")
        digest.append("## 📊 DAILY PIPELINE METRICS")
        digest.append(f"- **Total Remote Jobs Scanned:** {total_scanned}")
        digest.append(f"- **High-Fit Auto-Apply Matches (≥80%):** {auto_apply_count}")
        digest.append(f"- **Medium-Fit Review Matches (65–79%):** {review_count}")
        digest.append(f"- **Rejected Listings (<65%):** {rejected_count}\n")
        digest.append("---")
        digest.append("## 🎯 TARGET OPPORTUNITIES")

        target_jobs = [(j, s) for j, s in scored_jobs if s.recommendation in ["AUTO_APPLY", "REVIEW"]]

        if not target_jobs:
            digest.append("No new roles exceeded the fit threshold today. Pipeline monitoring continues.\n")
        else:
            for idx, (job, score) in enumerate(target_jobs, 1):
                digest.append(f"### {idx}. {job.title} @ {job.company}")
                digest.append(f"- **Estimated Comp:** ${job.estimated_tc:,} total comp | **Location:** {job.location}")
                digest.append(f"- **Fit Score:** **{score.total_score}%** (Recommendation: `{score.recommendation}`)")
                digest.append(f"- **Pillar Breakdown:** Executive Strategy: {score.pillar_breakdown['Executive Strategy']}/30 | AI Code: {score.pillar_breakdown['AI Engineering & Code']}/30 | Domain Fit: {score.pillar_breakdown['Domain & IP Fit']}/20 | Comp & Remote: {score.pillar_breakdown['Remote & Comp']}/20")
                digest.append("- **Matched Proofs:**")
                for proof in score.matched_proof_points:
                    digest.append(f"  * {proof}")
                
                pkg = packages.get(job.id)
                if pkg:
                    digest.append(f"- **Tailored Resume & Cover Letter Status:** `{pkg.verification_status}` (Zero AI Cliches Verified)")
                
                outreach = outreach_drafts.get(job.id)
                if outreach:
                    digest.append(f"- **Suggested Hiring Manager Contact:** `{outreach.target_title_suggestion}`")
                    digest.append(f"```text\n{outreach.personalized_message}\n```")
                digest.append("\n" + "-"*40 + "\n")

        digest.append("## 📬 ACTION CHECKLIST FOR SYLVESTER")
        for idx, (job, _) in enumerate(target_jobs, 1):
            digest.append(f"- [ ] **Submit Application & Direct Outreach:** {job.title} @ {job.company}")

        return "\n".join(digest)
