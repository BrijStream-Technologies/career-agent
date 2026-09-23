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
    location: str = "Montgomery, TX (Targeting Remote US / Global)"
    
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
            "role": "Senior Director of Operations (Records, Publishing, Touring, Merch)",
            "company": "Music World / Sanctuary Group",
            "years": "2004-2006",
            "highlight": "Managed 4 core operational divisions for global #1 Urban artist management enterprise (Roster: Destiny's Child/Beyoncé [32x Grammy Winner], Mary J. Blige, Earth Wind & Fire, Chaka Khan)."
        },
        {
            "role": "Founder & CEO / Artist Manager",
            "company": "Yysman, Inc.",
            "years": "1999-2004",
            "highlight": "Managed premier artist management enterprise representing Mary Mary (4x Grammy Winners), Myron Butler & Levi, Ted & Sheri, and Platinum Producers."
        },
        {
            "role": "Executive Strategic Advisor",
            "company": "Brij Brands",
            "years": "2018-Present",
            "highlight": "Executive Advisor to Park Bom of K-Pop group 2NE1 (Billboard 200 pioneers, MAMA Daesang Winners, 66M+ digital downloads)."
        },
        {
            "role": "Artist Manager",
            "company": "Left Eye Management / Independent",
            "years": "1997-2002",
            "highlight": "Managed Lisa 'Left Eye' Lopes of TLC (5x Grammy Winner, RIAA 12x Diamond Certified, 65M+ records sold)."
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
