import json
from http.server import BaseHTTPRequestHandler
from career_agent.agent_orchestrator import CareerAgentOrchestrator
from career_agent.live_job_fetcher import LiveJobFetcher

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
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
            },
            {
                "id": "job_004",
                "title": "Senior AI Product Manager",
                "company": "Spotify",
                "location": "Hybrid - New York, NY / Austin, TX",
                "is_remote": False,
                "base_salary_min": 160000,
                "base_salary_max": 210000,
                "estimated_tc": 210000,
                "description": "Drive AI recommendations, music audio metadata, prompt orchestration, and multi-sided artist platform features.",
                "source_url": "https://spotifyjobs.com/careers"
            },
            {
                "id": "job_005",
                "title": "AI Systems Architect",
                "company": "Soundcloud",
                "location": "In-Office - London, UK / Global",
                "is_remote": False,
                "base_salary_min": 130000,
                "base_salary_max": 160000,
                "estimated_tc": 160000,
                "description": "Architect AI content governance, audio feature extraction microservices, python system steering, and royalty ledger splits.",
                "source_url": "https://soundcloud.com/jobs"
            },
            {
                "id": "job_006",
                "title": "AI Solutions Lead",
                "company": "Epidemic Sound",
                "location": "Hybrid - Global / US",
                "is_remote": False,
                "base_salary_min": 105000,
                "base_salary_max": 125000,
                "estimated_tc": 125000,
                "description": "Lead customer AI implementations, soundtrack matching, audio ducking workflows, and Python orchestration pipelines.",
                "source_url": "https://epidemicsound.com/careers"
            }
        ]

        try:
            fetcher = LiveJobFetcher()
            live_jobs = fetcher.fetch_live_remote_jobs()
            if live_jobs:
                sample_listings.extend(live_jobs)
        except Exception:
            pass

        orchestrator = CareerAgentOrchestrator(auto_dispatch=False)
        valid_listings = orchestrator.scanner.normalize_and_filter(sample_listings)
        
        parsed_jobs = []
        for j in valid_listings:
            score = orchestrator.scorer.score_job(j)
            if score.recommendation in ["AUTO_APPLY", "REVIEW"]:
                pkg = orchestrator.tailorer.build_tailored_package(j, score)
                draft = orchestrator.outreach_finder.create_outreach_draft(j)

                parsed_jobs.append({
                    "id": j.id,
                    "title": j.title,
                    "company": j.company,
                    "location": j.location,
                    "estimated_tc": f"${j.estimated_tc:,} Total Comp",
                    "score": score.total_score,
                    "recommendation": score.recommendation,
                    "pillar_breakdown": score.pillar_breakdown,
                    "matched_proofs": score.matched_proof_points,
                    "audit_details": score.audit_details,
                    "contact_target": draft.target_title_suggestion,
                    "inmail_text": draft.personalized_message,
                    "full_resume": pkg.tailored_resume_markdown,
                    "full_cover_letter": pkg.cover_letter_markdown,
                    "translucent_note": pkg.translucent_brief_markdown
                })

        payload = {
            "candidate": orchestrator.profile.name,
            "title": orchestrator.profile.title,
            "email": orchestrator.profile.email,
            "scanned_count": len(sample_listings),
            "jobs": parsed_jobs
        }

        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
