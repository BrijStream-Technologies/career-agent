"""
Configuration module for Sylvester's Autonomous Career Agent.
Contains verified candidate metrics, search parameters, forbidden AI copy cliches, and scoring weights.
"""

from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class VerifiedCandidateProfile:
    name: str = "Sylvester Floyd Carter IV"
    first_name: str = "Sylvester"
    middle_name: str = "Floyd"
    last_name: str = "Carter"
    suffix: str = "IV"
    title: str = "Executive AI Transformation Leader & Agentic Strategy Director"
    education: str = "BA in Finance, Clark Atlanta University"
    email: str = "sylvesterfcarter@icloud.com"
    phone: str = "Available Upon Request"
    location: str = "Montgomery, TX (Houston Metro / Remote Executive)"
    linkedin: str = "https://linkedin.com/in/sylvestercarter"
    github: str = "https://github.com/BrijStream-Technologies"
    
    # Verified Technical Metrics
    lines_of_code_built: int = 88000
    passing_unit_tests: int = 455
    total_unit_tests: int = 456
    patents: List[str] = field(default_factory=lambda: [
        "Provisional PMG-2025-001 (Autonomous Media Synchronization)",
        "Follow-up Patent Application (Dynamic Soundtrack Substitution & Payment Ledgers)",
        "Provisional (Instant Split Payments & Stablecoin Settlement)"
    ])
    
    # Master Agentic Prompting & System Steering Moat
    agentic_prompting_moat: Dict[str, str] = field(default_factory=lambda: {
        "persona": "Master-Level Executive-Architect & System Steering Director",
        "philosophy": "Ruthless Factual Integrity & Zero AI Slop Tolerance (Directs AI agents to build 88k+ LOC polyglot codebases with 100% test suite pass integrity)",
        "steering_style": "Outcome-Driven Imperative Prompting (Architects data flows, security boundaries, and test criteria without micro-syntax micromanagement)",
        "verification_loop": "Socratic Mechanism Probing & Empirical Audit Verification (Forces 4-layer DOM readback assertions, log evidence, and zero hallucinated metrics)"
    })

    
    # Executive & Domain Background
    executive_experience: List[Dict[str, str]] = field(default_factory=lambda: [
        {
            "role": "Co-Founder & AI Architect",
            "company": "BrijStream / Kyvryn",
            "years": "2019-Present",
            "highlight": "Directed Antigravity & Claude Code agents to build, test, and deploy 88k LOC polyglot multi-tenant microservices across Go (Golang), Python, TypeScript/Node.js, Rust/C++, SQL, and Shell for high-concurrency media streaming and AI governance platforms."
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
    
    # Community-Facing AI Awareness & Advisory Moat
    community_ai_awareness_moat: Dict[str, List[str]] = field(default_factory=lambda: {
        "creative_industry_rights": [
            "Music & Entertainment AI Rights Literacy (Beyoncé/Destiny's Child & Park Bom/2NE1 track record)",
            "Synthetic Media Voice Rights & Fair Creator Split Ledgers (Patent PMG-2025-001)",
            "Catalog Streaming Revenue Decay & Phonorecords IV Statutory Guidance"
        ],
        "zero_slop_verification": [
            "Public AI Literacy on Zero-Slop Factual Verification & Hallucination Elimination",
            "Empirical Testing & 4-Layer DOM Integrity Principles for Business & SMBs"
        ],
        "agentic_workforce_transformation": [
            "Executive & Non-Technical Founder Bootcamps: Force-Multiplying via Agentic Steering",
            "Open-Source Agentic Steering & DOM Verification Standards"
        ],
        "civic_ethics_policy_councils": [
            "Civic & Corporate AI Policy Steering & Governance Advisory Boards",
            "Agent Rate Governance & Responsible AI Deployment Strategy"
        ]
    })
    
    # Domain & Polyglot Technical Expertise Areas
    domain_skills: List[str] = field(default_factory=lambda: [
        "AI System Steering & Meta-Prompt Architecture",
        "Community AI Literacy & Creator Rights Governance",
        "Polyglot Microservices (Go/Golang, Python, TypeScript, Rust, C++, SQL, Shell)",
        "High-Concurrency Platform & API Microservice Architecture",
        "Fintech & Royalty Ledger Split Engines",
        "Phonorecords IV Statutory Compliance",
        "Media Audio Ducking & Feature Extraction Matching",
        "Enterprise AI Governance & Proxy Metering",
        "Reg CF Crowdfunding Strategy"
    ])

@dataclass
class JobSearchConfig:
    target_titles: List[str] = field(default_factory=lambda: [
        # Executive AI Transformation & Enterprise Strategy
        "VP of AI Transformation",
        "Vice President, AI Transformation",
        "Director of AI Transformation",
        "Senior Director, AI Transformation & Innovation",
        "Head of AI Transformation",
        "VP of Enterprise AI Strategy",
        "Director of Digital Innovation",
        "Director of Enterprise Automation",
        "Head of Enterprise AI & Automation",

        # AI Product Strategy & Solutions Leadership
        "Director of AI Product Strategy",
        "Head of AI Product Strategy",
        "Principal AI Product Manager",
        "Group Product Manager - AI & Platform",
        "Director of AI Solutions",
        "Head of Forward Deployed AI",
        "Director of Forward Deployed AI",
        "Principal AI Solutions Architect",
        "Executive Director of Technology & AI Strategy",

        # Media, Entertainment & Rights AI Leadership
        "Head of Creator AI Literacy & Rights Governance",
        "VP of Digital Media Strategy & AI Operations",
        "Director of Media Technology & Platform Strategy"
    ])

    min_base_salary: int = 180000
    min_total_compensation: int = 250000
    require_remote: bool = False  # Allows In-Office, Hybrid, and Remote
    work_arrangements: List[str] = field(default_factory=lambda: ["Remote", "Hybrid", "In-Office"])
    geographic_scope: List[str] = field(default_factory=lambda: ["Greater Houston / The Woodlands", "Domestic (US)", "Global Remote"])
    max_posting_age_days: int = 45
    min_fit_score_for_apply: int = 85
    min_fit_score_for_review: int = 75

# Recruiter Agency / Spam Exclusions to eliminate spam harvester farms
EXCLUDED_AGENCIES = [
    "cybercoders",
    "robert half",
    "teksystems",
    "insight global",
    "kforce",
    "apex systems",
    "hays",
    "motion recruitment",
    "aerotek",
    "beacon hill",
    "addison group",
    "randstad",
    "kelly services",
    "lucas group",
    "jobot"
]

# Do Not Contact / Active Direct Communication Exclusion List
EXCLUDED_CONTACTS = [
    "tim@epicgames.com",
    "timsweeney@epicgames.com"
]

EXCLUDED_COMPANIES = [
    "epic games",
    "epicgames",
    "epic games, inc.",
    "epic games inc",
    "tim sweeney"
]


# Anti-AI Cliché Words (Must be excluded from cover letters & outreach messages)
FORBIDDEN_COPY_TERMS = [
    "delve", "testament", "spearheaded visionary synergy", "tapestry",
    "beacon", "transformative journey", "game-changer", "paradigm shift",
    "leverage cutting-edge", "unwavering commitment", "passionate innovator"
]
