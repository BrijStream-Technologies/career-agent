"""
Job Scanner module for Sylvester's Autonomous Career Agent.
Handles sourcing, filtering, deduplication, anti-ghost job validation, and standardization of job listings.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

@dataclass
class JobListing:
    id: str
    title: str
    company: str
    location: str
    is_remote: bool
    base_salary_min: int
    base_salary_max: int
    estimated_tc: int
    posting_date: datetime
    description: str
    source_url: str
    company_funding_stage: str = "Verified Active"
    is_agency_spam: bool = False
    
    @property
    def age_days(self) -> int:
        return (datetime.now() - self.posting_date).days

class JobScanner:
    def __init__(self, config):
        self.config = config

    def normalize_and_filter(self, raw_listings: List[Dict]) -> List[JobListing]:
        """
        Normalizes raw listing dicts into JobListing objects and applies quality & policy filters.
        """
        valid_listings = []
        seen_ids = set()

        for item in raw_listings:
            job_id = item.get("id") or f"{item.get('company')}_{item.get('title')}".lower().replace(" ", "_")
            
            # Deduplication
            if job_id in seen_ids:
                continue
            seen_ids.add(job_id)

            posting_date = item.get("posting_date")
            if isinstance(posting_date, str):
                try:
                    posting_date = datetime.fromisoformat(posting_date)
                except ValueError:
                    posting_date = datetime.now() - timedelta(days=2)
            elif not isinstance(posting_date, datetime):
                posting_date = datetime.now() - timedelta(days=2)

            is_remote = item.get("is_remote", False) or "remote" in item.get("location", "").lower()
            base_min = item.get("base_salary_min", 0)
            base_max = item.get("base_salary_max", 0)
            tc = item.get("estimated_tc", base_max or base_min)
            is_agency = item.get("is_agency_spam", False) or "recruiting firm" in item.get("description", "").lower()

            listing = JobListing(
                id=job_id,
                title=item.get("title", ""),
                company=item.get("company", ""),
                location=item.get("location", "Remote"),
                is_remote=is_remote,
                base_salary_min=base_min,
                base_salary_max=base_max,
                estimated_tc=tc,
                posting_date=posting_date,
                description=item.get("description", ""),
                source_url=item.get("source_url", "https://example.com/job"),
                company_funding_stage=item.get("company_funding_stage", "Verified Active"),
                is_agency_spam=is_agency
            )

            # Apply strict filtering criteria
            if self.is_valid_candidate_job(listing):
                valid_listings.append(listing)

        return valid_listings

    def is_valid_candidate_job(self, listing: JobListing) -> bool:
        """
        Validates job against remote policy, compensation, age, and anti-ghost rules.
        """
        # 1. Must be remote if required by config
        if self.config.require_remote and not listing.is_remote:
            return False

        # 2. Posting age rule (< 45 days)
        if listing.age_days > self.config.max_posting_age_days:
            return False

        # 3. Anti-agency spam rule
        if listing.is_agency_spam:
            return False

        # 4. Compensation threshold (must reach min base or min TC)
        if listing.base_salary_max > 0 and listing.base_salary_max < self.config.min_base_salary:
            if listing.estimated_tc < self.config.min_total_compensation:
                return False

        # 5. Blacklisted role titles / levels (Fellowships, Internships, Junior, Entry Level, Contractors, Trainees)
        FORBIDDEN_LEVELS = ["fellow", "fellowship", "intern", "internship", "junior", "associate", "entry level", "contractor", "trainee", "student"]
        title_lower = listing.title.lower()
        if any(fl in title_lower for fl in FORBIDDEN_LEVELS):
            return False

        # 6. Title relevance filter
        title_matched = any(target.lower() in title_lower or any(word in title_lower for word in target.lower().split()) for target in self.config.target_titles)
        if not title_matched:
            return False

        return True
