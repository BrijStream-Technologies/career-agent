"""
Live Job Fetcher module for Sylvester's Autonomous Career Agent.
Fetches real-time remote job listings from public APIs (Remotive, Arbeitnow, etc.) without requiring paid API keys.
"""

import urllib.request
import json
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class LiveJobFetcher:
    REMOTIVE_URL = "https://remotive.com/api/remote-jobs?category=software-dev&limit=25"
    ARBEITNOW_URL = "https://www.arbeitnow.com/api/job-board-api"

    def fetch_live_remote_jobs(self) -> List[Dict]:
        """
        Fetches live remote listings from public APIs and normalizes them into dictionary records.
        """
        listings = []
        
        # 1. Fetch from Remotive API
        remotive_jobs = self._fetch_remotive()
        listings.extend(remotive_jobs)

        # 2. Fetch from Arbeitnow API
        arbeitnow_jobs = self._fetch_arbeitnow()
        listings.extend(arbeitnow_jobs)

        return listings

    def _fetch_remotive(self) -> List[Dict]:
        results = []
        try:
            req = urllib.request.Request(self.REMOTIVE_URL, headers={"User-Agent": "Mozilla/5.0 (CareerAgent/1.0)"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for job in data.get("jobs", []):
                    title = job.get("title", "")
                    # Estimate comp if not explicitly stated
                    salary_str = job.get("salary", "")
                    results.append({
                        "id": f"remotive_{job.get('id')}",
                        "title": title,
                        "company": job.get("company_name", "Remote Enterprise"),
                        "location": "Remote",
                        "is_remote": True,
                        "base_salary_min": 180000 if "senior" in title.lower() or "lead" in title.lower() or "architect" in title.lower() or "manager" in title.lower() else 140000,
                        "base_salary_max": 280000 if "lead" in title.lower() or "director" in title.lower() or "architect" in title.lower() else 220000,
                        "estimated_tc": 320000 if "principal" in title.lower() or "lead" in title.lower() or "architect" in title.lower() or "director" in title.lower() else 220000,
                        "description": job.get("description", title),
                        "source_url": job.get("url", "https://remotive.com")
                    })
        except Exception as e:
            logger.warning(f"Failed to fetch Remotive jobs: {e}")
        return results

    def _fetch_arbeitnow(self) -> List[Dict]:
        results = []
        try:
            req = urllib.request.Request(self.ARBEITNOW_URL, headers={"User-Agent": "Mozilla/5.0 (CareerAgent/1.0)"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for job in data.get("data", []):
                    if job.get("remote", False):
                        title = job.get("title", "")
                        results.append({
                            "id": f"arbeitnow_{job.get('slug')}",
                            "title": title,
                            "company": job.get("company_name", "Remote Tech"),
                            "location": "Remote",
                            "is_remote": True,
                            "base_salary_min": 180000 if "lead" in title.lower() or "senior" in title.lower() else 150000,
                            "base_salary_max": 260000,
                            "estimated_tc": 300000 if "lead" in title.lower() or "architect" in title.lower() else 210000,
                            "description": job.get("description", title),
                            "source_url": job.get("url", "https://arbeitnow.com")
                        })
        except Exception as e:
            logger.warning(f"Failed to fetch Arbeitnow jobs: {e}")
        return results
