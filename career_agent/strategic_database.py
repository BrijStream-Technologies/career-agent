"""
Strategic Database module for Sylvester's Autonomous Career Agent.
Manages persistent SQLite enterprise knowledge graph storing Agentic Economy intelligence dossiers,
decision-maker directory, opportunities, and outreach logs.
"""

import sqlite3
import json
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent / "agentic_economy_intelligence.db"

@dataclass
class EnterpriseDossier:
    id: str
    company_name: str
    domain: str
    agentic_score: int  # 0-100 Agentic Intensity Index
    tech_stack_gaps: List[str]
    funding_telemetry: str
    sector: str
    created_at: str = ""

@dataclass
class ExecutiveContact:
    id: str
    enterprise_id: str
    name: str
    title: str
    email: str
    mx_verified: bool
    confidence_score: int

@dataclass
class StrategicOpportunity:
    id: str
    enterprise_id: str
    company_name: str
    role_title: str
    source_type: str  # "DIRECT_SITE", "EXECUTIVE_PITCH", "API_ENDPOINT"
    url: str
    status: str       # "DISCOVERED", "PREFILLED_PREVIEW_READY", "DRAFTED_TO_ICLOUD", "HOLD_UNVERIFIED"
    screenshot_path: Optional[str] = None
    created_at: str = ""

class StrategicDatabase:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS enterprises (
                id TEXT PRIMARY KEY,
                company_name TEXT UNIQUE NOT NULL,
                domain TEXT NOT NULL,
                agentic_score INTEGER NOT NULL,
                tech_stack_gaps TEXT NOT NULL,
                funding_telemetry TEXT NOT NULL,
                sector TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS executives (
                id TEXT PRIMARY KEY,
                enterprise_id TEXT NOT NULL,
                name TEXT NOT NULL,
                title TEXT NOT NULL,
                email TEXT NOT NULL,
                mx_verified BOOLEAN NOT NULL,
                confidence_score INTEGER NOT NULL,
                FOREIGN KEY (enterprise_id) REFERENCES enterprises (id)
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS opportunities (
                id TEXT PRIMARY KEY,
                enterprise_id TEXT NOT NULL,
                company_name TEXT NOT NULL,
                role_title TEXT NOT NULL,
                source_type TEXT NOT NULL,
                url TEXT NOT NULL,
                status TEXT NOT NULL,
                screenshot_path TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (enterprise_id) REFERENCES enterprises (id)
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS outreach_ledger (
                id TEXT PRIMARY KEY,
                enterprise_id TEXT NOT NULL,
                recipient_email TEXT NOT NULL,
                subject TEXT NOT NULL,
                status TEXT NOT NULL,
                dispatch_timestamp TEXT NOT NULL,
                FOREIGN KEY (enterprise_id) REFERENCES enterprises (id)
            )
            """)

            conn.commit()

    def upsert_enterprise(self, dossier: EnterpriseDossier):
        now = datetime.now().isoformat()
        gaps_json = json.dumps(dossier.tech_stack_gaps)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO enterprises (id, company_name, domain, agentic_score, tech_stack_gaps, funding_telemetry, sector, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(company_name) DO UPDATE SET
                agentic_score=excluded.agentic_score,
                tech_stack_gaps=excluded.tech_stack_gaps,
                funding_telemetry=excluded.funding_telemetry,
                sector=excluded.sector
            """, (dossier.id, dossier.company_name, dossier.domain, dossier.agentic_score, gaps_json, dossier.funding_telemetry, dossier.sector, dossier.created_at or now))
            conn.commit()

    def add_executive(self, exec_contact: ExecutiveContact):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO executives (id, enterprise_id, name, title, email, mx_verified, confidence_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (exec_contact.id, exec_contact.enterprise_id, exec_contact.name, exec_contact.title, exec_contact.email, exec_contact.mx_verified, exec_contact.confidence_score))
            conn.commit()

    def upsert_opportunity(self, opp: StrategicOpportunity):
        now = datetime.now().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO opportunities (id, enterprise_id, company_name, role_title, source_type, url, status, screenshot_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                status=excluded.status,
                screenshot_path=excluded.screenshot_path
            """, (opp.id, opp.enterprise_id, opp.company_name, opp.role_title, opp.source_type, opp.url, opp.status, opp.screenshot_path, opp.created_at or now))
            conn.commit()

    def record_outreach(self, opp_id: str, enterprise_id: str, recipient_email: str, subject: str, status: str):
        now = datetime.now().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO outreach_ledger (id, enterprise_id, recipient_email, subject, status, dispatch_timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (opp_id, enterprise_id, recipient_email, subject, status, now))
            conn.commit()

    def get_high_intensity_enterprises(self, min_score: int = 70) -> List[EnterpriseDossier]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM enterprises WHERE agentic_score >= ? ORDER BY agentic_score DESC", (min_score,))
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append(EnterpriseDossier(
                    id=row["id"],
                    company_name=row["company_name"],
                    domain=row["domain"],
                    agentic_score=row["agentic_score"],
                    tech_stack_gaps=json.loads(row["tech_stack_gaps"]),
                    funding_telemetry=row["funding_telemetry"],
                    sector=row["sector"],
                    created_at=row["created_at"]
                ))
            return results

    def get_executives_for_enterprise(self, enterprise_id: str) -> List[ExecutiveContact]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM executives WHERE enterprise_id = ?", (enterprise_id,))
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append(ExecutiveContact(
                    id=row["id"],
                    enterprise_id=row["enterprise_id"],
                    name=row["name"],
                    title=row["title"],
                    email=row["email"],
                    mx_verified=bool(row["mx_verified"]),
                    confidence_score=row["confidence_score"]
                ))
            return results

    def get_all_opportunities(self) -> List[StrategicOpportunity]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM opportunities ORDER BY created_at DESC")
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append(StrategicOpportunity(
                    id=row["id"],
                    enterprise_id=row["enterprise_id"],
                    company_name=row["company_name"],
                    role_title=row["role_title"],
                    source_type=row["source_type"],
                    url=row["url"],
                    status=row["status"],
                    screenshot_path=row["screenshot_path"],
                    created_at=row["created_at"]
                ))
            return results
