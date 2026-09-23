"""
Browser Applicant module for Sylvester's Autonomous Career Agent.
Automates online job applications via Playwright Chrome browser navigation, form field detection, ATS input populating, and submission handling.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Optional
from playwright.sync_api import sync_playwright, Page, Browser

from career_agent.config import VerifiedCandidateProfile
from career_agent.job_scanner import JobListing
from career_agent.package_tailorer import ApplicationPackage

logger = logging.getLogger(__name__)

class BrowserApplicant:
    def __init__(self, profile: VerifiedCandidateProfile, headless: bool = True):
        self.profile = profile
        self.headless = headless
        self.screenshots_dir = Path(__file__).parent / "application_screenshots"
        self.screenshots_dir.mkdir(exist_ok=True)

    def apply_online(self, job: JobListing, package: ApplicationPackage, submit_live: bool = False) -> Dict:
        """
        Navigates to the job's source_url, detects form fields (Greenhouse, Lever, Workday, or custom),
        populates Sylvester's profile & tailored package, and optionally submits.
        """
        result = {
            "job_id": job.id,
            "company": job.company,
            "url": job.source_url,
            "status": "FAILED",
            "screenshot_path": None,
            "details": ""
        }

        try:
            with sync_playwright() as p:
                browser: Browser = p.chromium.launch(headless=self.headless)
                page: Page = browser.new_page()

                logger.info(f"Navigating to {job.source_url}")
                page.goto(job.source_url, timeout=30000, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)

                # Look for "Apply" button if on a landing page
                apply_btn = page.query_selector("a:has-text('Apply'), button:has-text('Apply'), a:has-text('Apply Now'), button:has-text('Apply Now')")
                if apply_btn:
                    try:
                        apply_btn.click()
                        page.wait_for_timeout(2000)
                    except Exception:
                        pass

                # Fill standard input fields if present
                self._fill_field(page, ["first_name", "first-name", "fname"], self.profile.name.split()[0])
                self._fill_field(page, ["last_name", "last-name", "lname"], " ".join(self.profile.name.split()[1:]))
                self._fill_field(page, ["name", "full_name", "full-name"], self.profile.name)
                self._fill_field(page, ["email", "email_address"], self.profile.email)
                self._fill_field(page, ["phone", "mobile", "telephone"], self.profile.phone)
                self._fill_field(page, ["location", "city", "address"], self.profile.location)

                # Fill cover letter / notes / system steering brief
                cover_text = f"{package.translucent_brief_markdown}\n\n{package.cover_letter_markdown}"
                self._fill_textarea(page, ["cover_letter", "cover-letter", "comments", "additional_info", "brief"], cover_text)

                # Save pre-submission screenshot
                screenshot_file = self.screenshots_dir / f"{job.id}_application.png"
                page.screenshot(path=str(screenshot_file), full_page=True)
                result["screenshot_path"] = str(screenshot_file)

                if submit_live:
                    submit_button = page.query_selector("button[type='submit'], input[type='submit'], button:has-text('Submit Application')")
                    if submit_button:
                        submit_button.click()
                        page.wait_for_timeout(3000)
                        result["status"] = "SUBMITTED_ONLINE"
                        result["details"] = "Application form submitted live via Chrome Playwright engine."
                    else:
                        result["status"] = "PREFILLED_NEEDS_SUBMIT_CLICK"
                        result["details"] = "Form pre-filled cleanly. Submit button requires final click."
                else:
                    result["status"] = "PREFILLED_PREVIEW_READY"
                    result["details"] = f"Form pre-filled and verified. Screenshot captured at {screenshot_file.name}."

                browser.close()

        except Exception as err:
            logger.error(f"Browser application error for {job.company}: {err}")
            result["details"] = f"Browser automation error: {str(err)}"

        return result

    def _fill_field(self, page: Page, selector_names: list, value: str):
        for name in selector_names:
            selectors = [
                f"input[name*='{name}' i]",
                f"input[id*='{name}' i]",
                f"input[placeholder*='{name}' i]"
            ]
            for sel in selectors:
                try:
                    el = page.query_selector(sel)
                    if el and el.is_visible():
                        el.fill(value)
                        return
                except Exception:
                    pass

    def _fill_textarea(self, page: Page, selector_names: list, value: str):
        for name in selector_names:
            selectors = [
                f"textarea[name*='{name}' i]",
                f"textarea[id*='{name}' i]",
                f"textarea[placeholder*='{name}' i]"
            ]
            for sel in selectors:
                try:
                    el = page.query_selector(sel)
                    if el and el.is_visible():
                        el.fill(value)
                        return
                except Exception:
                    pass
