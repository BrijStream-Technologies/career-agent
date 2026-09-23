"""
Runner script for Sylvester's Autonomous Career Agent with strict verification standards.
"""

import os
from career_agent.agent_orchestrator import CareerAgentOrchestrator
from career_agent.live_job_fetcher import LiveJobFetcher

def run():
    os.environ["ICLOUD_APP_PASSWORD"] = "oqpx-ebgr-cioh-ajtg"
    os.environ["SAVE_AS_DRAFT"] = "true"

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

    fetcher = LiveJobFetcher()
    live_jobs = fetcher.fetch_live_remote_jobs()
    sample_listings.extend(live_jobs)

    orchestrator = CareerAgentOrchestrator(auto_dispatch=True)
    digest = orchestrator.run_daily_pipeline(sample_listings)
    print("DAILY PIPELINE COMPLETED")
    print(digest[:500])

if __name__ == "__main__":
    run()
