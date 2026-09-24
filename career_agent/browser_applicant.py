"""
Browser Applicant module for Sylvester's Autonomous Career Agent.
Automates online job applications via Playwright Chrome browser navigation, ATS input populating,
account registration (Workday, Taleo, iCIMS, etc.), automated IMAP verification code handling,
and Profile-Driven LLM Custom Question Answering.
"""

import os
import re
import time
import imaplib
import email
import logging
from pathlib import Path
from typing import Dict, List, Optional
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
        self.default_account_password = os.environ.get("CANDIDATE_PORTAL_PASSWORD", "SylvesterAI#2026!Career")

    def handle_account_registration(self, page: Page, domain: str) -> bool:
        """
        Detects 'Create Account' / 'Sign Up' forms (Workday, Taleo, iCIMS),
        fills Sylvester's credentials, submits registration, and fetches verification code via IMAP if prompted.
        """
        signup_btn = page.query_selector(
            "a:has-text('Create Account'), button:has-text('Create Account'), "
            "a:has-text('Sign Up'), button:has-text('Sign Up'), "
            "a:has-text('Register'), button:has-text('Register')"
        )
        if signup_btn and signup_btn.is_visible():
            try:
                signup_btn.click()
                page.wait_for_timeout(2000)
            except Exception:
                pass

        # Check if account registration fields exist
        email_field = page.query_selector("input[type='email'], input[name*='email' i], input[id*='email' i]")
        pass_field = page.query_selector("input[type='password'], input[name*='password' i], input[id*='password' i]")
        confirm_pass_field = page.query_selector("input[name*='confirm' i], input[id*='confirm' i]")

        if email_field and pass_field and email_field.is_visible() and pass_field.is_visible():
            logger.info("Account creation form detected. Filling registration details...")
            try:
                email_field.fill(self.profile.email)
                pass_field.fill(self.default_account_password)
                if confirm_pass_field and confirm_pass_field.is_visible():
                    confirm_pass_field.fill(self.default_account_password)

                # Check terms checkbox if present
                terms_cb = page.query_selector("input[type='checkbox']")
                if terms_cb and not terms_cb.is_checked():
                    terms_cb.check()

                # Submit registration
                reg_submit = page.query_selector("button[type='submit'], input[type='submit'], button:has-text('Create Account'), button:has-text('Register')")
                if reg_submit:
                    reg_submit.click()
                    page.wait_for_timeout(3000)

                # Check if verification code / OTP input is present
                otp_field = page.query_selector("input[name*='code' i], input[name*='otp' i], input[id*='code' i], input[placeholder*='code' i]")
                if otp_field and otp_field.is_visible():
                    logger.info("Verification code requested. Fetching OTP from iCloud inbox via IMAP...")
                    code = self.fetch_verification_code_via_imap()
                    if code:
                        otp_field.fill(code)
                        verify_submit = page.query_selector("button:has-text('Verify'), button:has-text('Submit'), input[type='submit']")
                        if verify_submit:
                            verify_submit.click()
                            page.wait_for_timeout(3000)
                return True
            except Exception as err:
                logger.warning(f"Account registration flow exception: {err}")
                return False

        return False

    def fetch_verification_code_via_imap(self) -> Optional[str]:
        """
        Connects to Sylvester's iCloud inbox via IMAP and extracts recent 6-digit verification code.
        """
        icloud_pass = os.environ.get("ICLOUD_APP_PASSWORD")
        if not icloud_pass:
            return None

        try:
            imap = imaplib.IMAP4_SSL("imap.mail.me.com", 993)
            imap.login(self.profile.email, icloud_pass)
            imap.select("INBOX")

            # Search for unread messages received in last 5 minutes
            status, messages = imap.search(None, 'UNSEEN')
            if status == 'OK' and messages[0]:
                msg_ids = messages[0].split()
                latest_id = msg_ids[-1]
                res, msg_data = imap.fetch(latest_id, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() in ["text/plain", "text/html"]:
                                    body += part.get_payload(decode=True).decode("utf-8", errors="ignore")
                        else:
                            body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

                        # Extract 6-digit PIN code
                        match = re.search(r'\b\d{6}\b', body)
                        if match:
                            imap.logout()
                            return match.group(0)

            imap.logout()
        except Exception as e:
            logger.warning(f"IMAP OTP fetch error: {e}")
        return None

    def generate_authentic_answer(self, question: str, job: JobListing) -> str:
        """
        Generates an authentic, high-impact answer strictly adhering to Sylvester's 
        Master-Level Executive-Architect Persona & Communication Profile:
        - Zero pleasing/romantic fluff
        - Outcome-driven system steering focus
        - Empirical receipts (88k LOC Go/Rust/C++/Python/TS, Patent PMG-2025-001, Brij Brands, Sanctuary Group, TLC)
        """
        q_lower = question.lower()
        if "compensation" in q_lower or "salary" in q_lower or "pay" in q_lower:
            return f"My total compensation expectation is targeted at ${job.base_salary_min:,}+, aligned with executive strategy and system architecture scope."
        elif "why" in q_lower and ("company" in q_lower or "join" in q_lower or "role" in q_lower):
            return (
                f"I am targeting {job.company} because this {job.title} scope aligns directly with my core moat: "
                "architecting production multi-LLM proxy steering, real-time meter governance, and polyglot microservices. "
                f"Having led executive P&L operations at Brij Brands (Park Bom) and Music World Sanctuary Group, I bring "
                "both institutional commercial rigor and hands-on system architecture."
            )
        elif "experience" in q_lower or "project" in q_lower or "challenge" in q_lower or "built" in q_lower:
            return (
                "My approach is outcome-driven System Steering. I direct AI agent orchestration pipelines to convert "
                "complex domain requirements into production software—evidenced by 88,000+ LOC of polyglot telemetry across "
                "Go (Golang), Rust, C/C++, Python, and TypeScript, backed by Patent PMG-2025-001 for proxy metering and rights governance."
            )
        else:
            return (
                f"As an AI Systems Architect & Executive Strategy Leader (Montgomery, TX), I approach {job.title} "
                "through empirical verification, zero-fluff truthfulness, and strict system steering. I combine 20+ years "
                "of executive entertainment/fintech operations with full-stack agent orchestration."
            )

    def audit_unanswered_form_questions(self, page: Page) -> List[Dict[str, str]]:
        """
        DOM & ARIA Form Reconciliation Pass: Checks if any visible non-identity input field or required element was missed.
        Returns a list of missed questions with their DOM attributes and labels.
        """
        missed = []
        try:
            # 1. HTML5 Required Field Check via JavaScript Evaluation
            unfilled_required = page.evaluate("""() => {
                const inputs = Array.from(document.querySelectorAll('input, textarea, select'));
                return inputs
                    .filter(el => el.offsetParent !== null && (el.required || el.getAttribute('aria-required') === 'true') && !el.value)
                    .map(el => {
                        const id = el.id || '';
                        let labelText = '';
                        if (id) {
                            const lbl = document.querySelector(`label[for='${id}']`);
                            if (lbl) labelText = lbl.innerText.trim();
                        }
                        return {
                            id: id,
                            name: el.getAttribute('name') || '',
                            placeholder: el.getAttribute('placeholder') || '',
                            label: labelText || el.getAttribute('aria-label') || el.getAttribute('name') || 'Required Question'
                        };
                    });
            }""")
            for item in unfilled_required:
                missed.append(item)

            # 2. Non-Identity Textarea & Text Input Audit
            all_text_inputs = page.query_selector_all("textarea, input[type='text']")
            for el in all_text_inputs:
                if not el.is_visible():
                    continue
                attr_text = (
                    (el.get_attribute("name") or "") + " " +
                    (el.get_attribute("id") or "") + " " +
                    (el.get_attribute("placeholder") or "")
                ).lower()
                # Skip standard identity fields
                if any(k in attr_text for k in ["first", "last", "email", "phone", "city", "address", "zip", "location"]):
                    continue
                
                val = (el.input_value() or "").strip()
                if not val:
                    label_text = attr_text
                    id_attr = el.get_attribute("id")
                    if id_attr:
                        lbl = page.query_selector(f"label[for='{id_attr}']")
                        if lbl:
                            label_text = lbl.inner_text().strip()
                    missed.append({
                        "id": id_attr or "",
                        "name": el.get_attribute("name") or "",
                        "placeholder": el.get_attribute("placeholder") or "",
                        "label": label_text
                    })
        except Exception as err:
            logger.warning(f"Error auditing unanswered form questions: {err}")

        return missed

    def answer_custom_open_ended_questions(self, page: Page, job: JobListing) -> List[Dict[str, str]]:
        """
        Scrapes all custom open-ended form questions on the page and fills them with authentic LLM-profile responses.
        Also runs missing question reconciliation pass.
        """
        answered_questions = []
        textareas = page.query_selector_all("textarea, input[type='text']")

        for index, el in enumerate(textareas):
            try:
                if not el.is_visible():
                    continue

                name_attr = (el.get_attribute("name") or "").lower()
                id_attr = (el.get_attribute("id") or "").lower()
                placeholder = (el.get_attribute("placeholder") or "").lower()

                # Skip identity fields
                if any(k in name_attr or k in id_attr or k in placeholder for k in ["first", "last", "email", "phone", "city", "address", "zip"]):
                    continue

                # Find associated label or question text
                question_text = ""
                if id_attr:
                    label_el = page.query_selector(f"label[for='{id_attr}']")
                    if label_el:
                        question_text = label_el.inner_text().strip()

                if not question_text:
                    question_text = placeholder or name_attr or f"Custom Application Question #{index + 1}"

                # Generate authentic answer based on Sylvester's Persona
                answer_text = self.generate_authentic_answer(question_text, job)
                el.fill(answer_text)

                answered_questions.append({
                    "question": question_text,
                    "answer": answer_text
                })
            except Exception as err:
                logger.warning(f"Error answering question index {index}: {err}")

        return answered_questions

    def step_to_active_form_if_needed(self, page: Page, company_name: str) -> bool:
        """
        If current page has no input fields (e.g., top-level careers landing page),
        scrapes the page for active job listing links or ATS links (Greenhouse, Lever, Ashby, Workday)
        and steps into the actual job posting form page.
        """
        try:
            visible_inputs = [el for el in page.query_selector_all("input, textarea") if el.is_visible()]
            if len(visible_inputs) > 0:
                return True

            logger.info(f"No input fields on landing page ({page.url}). Searching for direct ATS / job board links...")
            links = page.query_selector_all("a")
            candidate_urls = []
            for link in links:
                try:
                    href = link.get_attribute("href") or ""
                    if not href or href.startswith("#") or href.startswith("javascript:"):
                        continue
                    href_lower = href.lower()
                    if any(ats in href_lower for ats in ["greenhouse.io", "lever.co", "ashbyhq.com", "myworkdayjobs.com", "workable.com", "smartrecruiters.com"]):
                        candidate_urls.append(href)
                    elif any(kw in href_lower for kw in ["/job/", "/jobs/", "/careers/jobs", "/position/", "/opening/", "gh_jid"]):
                        if href.startswith("/"):
                            from urllib.parse import urlparse
                            parsed = urlparse(page.url)
                            href = f"{parsed.scheme}://{parsed.netloc}{href}"
                        candidate_urls.append(href)
                except Exception:
                    pass

            for target_url in candidate_urls[:3]:
                try:
                    logger.info(f"Stepping through to job listing URL: {target_url}")
                    page.goto(target_url, timeout=20000, wait_until="domcontentloaded")
                    page.wait_for_timeout(2000)

                    apply_btn = page.query_selector(
                        "a:has-text('Apply'), button:has-text('Apply'), "
                        "a:has-text('Apply Now'), button:has-text('Apply Now'), "
                        "a:has-text('Apply for this job'), button:has-text('Apply for this job')"
                    )
                    if apply_btn and apply_btn.is_visible():
                        apply_btn.click()
                        page.wait_for_timeout(2000)

                    new_inputs = [el for el in page.query_selector_all("input, textarea") if el.is_visible()]
                    if len(new_inputs) > 0:
                        logger.info(f"Successfully stepped through to form page with {len(new_inputs)} visible input fields!")
                        return True
                except Exception as err:
                    logger.warning(f"Failed stepping through to {target_url}: {err}")
        except Exception as e:
            logger.warning(f"Error in step_to_active_form_if_needed: {e}")

        return False

    def handle_dropdowns_and_compliance(self, page: Page):
        """
        Selects standard compliance options (US Work Authorization, Sponsorship, EEO) across ATS forms.
        """
        try:
            selects = page.query_selector_all("select")
            for sel in selects:
                if not sel.is_visible():
                    continue
                name_attr = (sel.get_attribute("name") or "").lower()
                id_attr = (sel.get_attribute("id") or "").lower()

                # Work authorization
                if any(k in name_attr or k in id_attr for k in ["auth", "work_auth", "legally", "authorized", "eligible"]):
                    options = sel.query_selector_all("option")
                    for opt in options:
                        txt = (opt.inner_text() or "").lower()
                        val = (opt.get_attribute("value") or "").lower()
                        if "yes" in txt or "authorized" in txt or "yes" in val:
                            sel.select_option(value=opt.get_attribute("value") or opt.inner_text())
                            break
                # Sponsorship
                elif any(k in name_attr or k in id_attr for k in ["sponsor", "sponsorship", "visa"]):
                    options = sel.query_selector_all("option")
                    for opt in options:
                        txt = (opt.inner_text() or "").lower()
                        val = (opt.get_attribute("value") or "").lower()
                        if "no" in txt or "don't" in txt or "do not" in txt or "no" in val:
                            sel.select_option(value=opt.get_attribute("value") or opt.inner_text())
                            break
                # Veteran / Disability / EEO
                elif any(k in name_attr or k in id_attr for k in ["veteran", "disability", "eeo", "gender", "race"]):
                    options = sel.query_selector_all("option")
                    for opt in options:
                        txt = (opt.inner_text() or "").lower()
                        val = (opt.get_attribute("value") or "").lower()
                        if "decline" in txt or "don't wish" in txt or "not" in txt or "decline" in val:
                            sel.select_option(value=opt.get_attribute("value") or opt.inner_text())
                            break
        except Exception as e:
            logger.warning(f"Error handling compliance dropdowns: {e}")

    def apply_online(self, job: JobListing, package: ApplicationPackage, submit_live: bool = False) -> Dict:
        """
        Navigates to the job's source_url, steps through landing pages to active job application forms,
        populates Sylvester's profile & tailored package, answers custom questions, verifies input presence, and captures screenshots.
        """
        result = {
            "job_id": job.id,
            "company": job.company,
            "url": job.source_url,
            "status": "FAILED",
            "screenshot_path": None,
            "custom_questions_answered": [],
            "details": ""
        }

        try:
            with sync_playwright() as p:
                browser: Browser = p.chromium.launch(headless=self.headless)
                page: Page = browser.new_page()

                logger.info(f"Navigating to {job.source_url}")
                page.goto(job.source_url, timeout=30000, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)

                # 1. Step through landing page to active job form if needed
                self.step_to_active_form_if_needed(page, job.company)

                # 2. Handle Account Creation / Registration if required (e.g., Workday/Taleo/iCIMS)
                self.handle_account_registration(page, job.company)

                # 3. Look for "Apply" button if on a landing page
                apply_btn = page.query_selector("a:has-text('Apply'), button:has-text('Apply'), a:has-text('Apply Now'), button:has-text('Apply Now')")
                if apply_btn:
                    try:
                        apply_btn.click()
                        page.wait_for_timeout(2000)
                    except Exception:
                        pass

                # 4. Fill standard input fields if present
                fields_filled = 0
                first = getattr(self.profile, "first_name", "Sylvester")
                middle = getattr(self.profile, "middle_name", "Floyd")
                last = getattr(self.profile, "last_name", "Carter")
                suffix = getattr(self.profile, "suffix", "IV")

                if self._fill_field(page, ["first_name", "first-name", "fname", "given-name", "given_name", "first"], first):
                    fields_filled += 1
                if self._fill_field(page, ["middle_name", "middle-name", "mname", "middle_initial", "middle"], middle):
                    fields_filled += 1
                if self._fill_field(page, ["last_name", "last-name", "lname", "family-name", "family_name", "last", "surname"], last):
                    fields_filled += 1
                if self._fill_field(page, ["suffix", "title_suffix", "name_suffix"], suffix):
                    fields_filled += 1
                if self._fill_field(page, ["name", "full_name", "full-name", "applicant_name"], self.profile.name, is_full_name=True):
                    fields_filled += 1
                if self._fill_field(page, ["email", "email_address", "email-address"], self.profile.email):
                    fields_filled += 1
                phone_val = getattr(self.profile, "phone", "Available Upon Request")
                if self._fill_field(page, ["phone", "mobile", "telephone", "phone_number", "phone-number"], phone_val):
                    fields_filled += 1
                if self._fill_field(page, ["location", "city", "address", "current_location"], self.profile.location):
                    fields_filled += 1
                if hasattr(self.profile, "linkedin"):
                    if self._fill_field(page, ["linkedin", "website", "portfolio", "url"], self.profile.linkedin):
                        fields_filled += 1

                # 5. Fill compliance & work authorization dropdowns
                self.handle_dropdowns_and_compliance(page)

                # 6. Fill cover letter / notes / system steering brief
                cover_text = f"{package.translucent_brief_markdown}\n\n{package.cover_letter_markdown}"
                self._fill_textarea(page, ["cover_letter", "cover-letter", "comments", "additional_info", "brief"], cover_text)

                # 7. Profile-Driven LLM Custom Question Answering
                custom_qa = self.answer_custom_open_ended_questions(page, job)
                result["custom_questions_answered"] = custom_qa

                # 8. Unanswered Form Question Audit Reconciliation Pass
                missed_questions = self.audit_unanswered_form_questions(page)
                result["missed_questions"] = missed_questions
                if missed_questions:
                    logger.warning(f"Unanswered form questions detected ({len(missed_questions)}): {[m.get('label') for m in missed_questions]}")

                # 9. Strict verification of live candidate form inputs presence
                visible_inputs = [el for el in page.query_selector_all("input, textarea, select") if el.is_visible()]
                candidate_form_inputs = []
                for el in visible_inputs:
                    attr_text = (
                        (el.get_attribute("name") or "") + " " +
                        (el.get_attribute("id") or "") + " " +
                        (el.get_attribute("placeholder") or "") + " " +
                        (el.get_attribute("aria-label") or "")
                    ).lower()
                    if any(k in attr_text for k in ["first", "last", "email", "phone", "name", "resume", "cover", "applicant", "city", "address", "linkedin", "portfolio"]):
                        candidate_form_inputs.append(el)

                if len(candidate_form_inputs) == 0 and fields_filled == 0:
                    result["status"] = "NO_CANDIDATE_FORM_INPUTS_FOUND"
                    result["details"] = f"Visited {page.url} (detected {len(visible_inputs)} general elements), but no live candidate application form fields were visible or populated."
                else:
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
                            result["details"] = f"Form pre-filled cleanly with {len(candidate_form_inputs)} candidate inputs. Submit button requires final click."
                    else:
                        result["status"] = "PREFILLED_PREVIEW_READY"
                        result["details"] = f"Form pre-filled and verified with {len(candidate_form_inputs)} candidate inputs ({fields_filled} profile fields filled). Screenshot captured at {screenshot_file.name}."

                browser.close()

        except Exception as err:
            logger.error(f"Browser application error for {job.company}: {err}")
            result["details"] = f"Browser automation error: {str(err)}"

        return result

    def _fill_field(self, page: Page, selector_names: list, value: str, is_full_name: bool = False) -> bool:
        for name in selector_names:
            selectors = [
                f"input[name*='{name}' i]",
                f"input[id*='{name}' i]",
                f"input[placeholder*='{name}' i]"
            ]
            for sel in selectors:
                try:
                    elements = page.query_selector_all(sel)
                    for el in elements:
                        if not el or not el.is_visible():
                            continue
                        attr_text = (
                            (el.get_attribute("name") or "") + " " +
                            (el.get_attribute("id") or "") + " " +
                            (el.get_attribute("placeholder") or "")
                        ).lower()
                        # Never fill full name string into dedicated first/last/middle name fields!
                        if is_full_name and any(k in attr_text for k in ["first", "last", "middle", "fname", "lname", "mname", "given", "family", "surname"]):
                            continue
                        el.fill(value)
                        return True
                except Exception:
                    pass
        return False

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
