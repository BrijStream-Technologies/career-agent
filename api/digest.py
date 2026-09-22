import json
from http.server import BaseHTTPRequestHandler
from career_agent.agent_orchestrator import CareerAgentOrchestrator
from career_agent.live_job_fetcher import LiveJobFetcher

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Fallback sample target listings
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
                "description": "Lead strategic AI music initiatives, rights registry, audio synchronization, and ad-tech monetization.",
                "source_url": "https://wmg.com/careers/director-ai-strategy"
            }
        ]

        # 2. Try fetching live jobs from public APIs
        try:
            fetcher = LiveJobFetcher()
            live_jobs = fetcher.fetch_live_remote_jobs()
            if live_jobs:
                sample_listings.extend(live_jobs)
        except Exception:
            pass

        orchestrator = CareerAgentOrchestrator()
        digest_md = orchestrator.run_daily_pipeline(sample_listings)

        payload = {
            "candidate": orchestrator.profile.name,
            "title": orchestrator.profile.title,
            "scanned_count": len(sample_listings),
            "digest_markdown": digest_md
        }

        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
