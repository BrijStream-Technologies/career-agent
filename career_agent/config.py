"""
Configuration module for Sylvester's Autonomous Career Agent.
Contains verified candidate metrics, search parameters, forbidden AI copy cliches, and scoring weights.
"""

from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class VerifiedCandidateProfile:
    name: str = "Sylvester Floyd Carter IV"
    title: str = "AI Systems Architect & Executive Strategy Leader"
    education: str = "BA in Finance, Clark Atlanta University"
    email: str = "sylvesterfcarter@icloud.com"
    location: str = "Atlanta, GA (Targeting Remote US / Global)"
    
    # Verified Technical Metrics
    lines_of_code_built: int = 88000
    passing_unit_tests: int = 455
    total_unit_tests: int = 456
    patents: List[str] = field(default_factory=lambda: [
        "Provisional PMG-2025-001 (Autonomous Media Synchronization)",
        "Follow-up Patent Application (Dynamic Soundtrack Substitution & Payment Ledgers)",
        "Provisional (Instant Split Payments & Stablecoin Settlement)"
    ])
    
    # Executive & Domain Background
    executive_experience: List[Dict[str, str]] = field(default_factory=lambda: [
        {
            "role": "Co-Founder & AI Architect",
            "company": "BrijStream / Kyvryn",
            "years": "2019-Present",
            "highlight": "Directed Antigravity & Claude Code agents to build, test, and deploy 88k LOC multi-sided media streaming and AI governance SaaS platforms."
        },
        {
            "role": "Director of Strategy",
            "company": "Music World / Sanctuary Group",
            "years": "2004-2006",
            "highlight": "Multi-million dollar P&L responsibility, strategic licensing, artist catalogue management."
        },
        {
            "role": "Founder & CEO",
            "company": "Yysman, Inc.",
            "years": "1999-2004",
            "highlight": "Founded and successfully navigated tech acquisition."
        }
    ])
    
    # Domain Expertise Areas
    domain_skills: List[str] = field(default_factory=lambda: [
        "AI Prompt Architecture & Orchestration",
        "Multi-Sided Platform Design",
        "Fintech & Royalty Ledger Systems",
        "Phonorecords IV Statutory Compliance",
        "Media Audio ducking & Energy Matching",
        "Enterprise AI Governance & Proxy Metering",
        "Reg CF Crowdfunding Strategy"
    ])

@dataclass
class JobSearchConfig:
    target_titles: List[str] = field(default_factory=lambda: [
        "Principal AI Product Manager",
        "Senior AI Product Manager",
        "Forward Deployed AI Lead",
        "Forward Deployed AI Engineer",
        "VP of AI Product Strategy",
        "Director of AI Product Strategy",
        "AI Systems Architect",
        "Prompt Engineering Lead"
    ])
    min_base_salary: int = 180000
    min_total_compensation: int = 250000
    require_remote: bool = True
    max_posting_age_days: int = 45
    min_fit_score_for_apply: int = 80
    min_fit_score_for_review: int = 65

# Anti-AI Cliché Words (Must be excluded from cover letters & outreach messages)
FORBIDDEN_COPY_TERMS = [
    "delve", "testament", "spearheaded visionary synergy", "tapestry",
    "beacon", "transformative journey", "game-changer", "paradigm shift",
    "leverage cutting-edge", "unwavering commitment", "passionate innovator"
]
