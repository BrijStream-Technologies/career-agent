"""
Market Scoring Model module for Sylvester's Autonomous Career Agent.
Defines the 100-Point Market Hiring Alignment & Strength Score Model evaluating C-suite strategic resonance,
empirical proof integrity, system steering moat differentiation, and anti-fluff authority.
"""

from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class MarketStrengthEvaluation:
    strategic_resonance_score: int  # Max 25
    empirical_proof_score: int      # Max 25
    steering_moat_score: int       # Max 25
    anti_fluff_tone_score: int       # Max 25
    detailed_critique: List[str] = field(default_factory=list)

    @property
    def total_score(self) -> int:
        return (
            self.strategic_resonance_score
            + self.empirical_proof_score
            + self.steering_moat_score
            + self.anti_fluff_tone_score
        )

    @property
    def is_certified_95_plus(self) -> bool:
        return self.total_score >= 95

class MarketScoringModel:
    def __init__(self):
        pass

    def evaluate_brief_strength(
        self,
        company_name: str,
        exec_name: str,
        brief_markdown: str,
        cover_letter_markdown: str
    ) -> MarketStrengthEvaluation:
        """
        Evaluates strategic brief quality across 4 25-point pillars.
        """
        critique = []
        res_score = 25
        proof_score = 25
        moat_score = 25
        tone_score = 25

        brief_lower = brief_markdown.lower()
        cover_lower = cover_letter_markdown.lower()

        # Pillar 1: Strategic Resonance (Max 25)
        if company_name.lower() not in brief_lower:
            res_score -= 10
            critique.append("Missing explicit enterprise name customization.")
        if "machine economy" not in brief_lower and "strategic transformation" not in brief_lower:
            res_score -= 5
            critique.append("Lacks high-level Machine Economy strategic framing.")

        # Pillar 2: Empirical Proof Integrity (Max 25)
        if "88,000" not in brief_lower and "88k" not in brief_lower:
            proof_score -= 10
            critique.append("Missing 88,000 LOC polyglot telemetry receipt.")
        if "pmg-2025-001" not in brief_lower:
            proof_score -= 5
            critique.append("Missing Patent PMG-2025-001 citation.")
        if "brij brands" not in brief_lower and "music world" not in brief_lower:
            proof_score -= 5
            critique.append("Missing verified executive track record (Brij Brands / Music World).")

        # Pillar 3: System Steering Moat Differentiation (Max 25)
        if "system steering" not in brief_lower and "steering officer" not in brief_lower:
            moat_score -= 10
            critique.append("Fails to emphasize System Steering Officer persona over raw coding.")
        if "10x" not in brief_lower and "100% test" not in brief_lower:
            moat_score -= 5
            critique.append("Lacks 10x output velocity & 100% test integrity mandate.")

        # Pillar 4: Anti-Fluff Tone & Authority (Max 25)
        forbidden_cliches = ["delve", "testament", "visionary synergy", "passionate developer", "thrilled to apply"]
        for cliche in forbidden_cliches:
            if cliche in brief_lower or cliche in cover_lower:
                tone_score -= 10
                critique.append(f"Forbidden AI cliche detected: '{cliche}'.")

        return MarketStrengthEvaluation(
            strategic_resonance_score=max(0, res_score),
            empirical_proof_score=max(0, proof_score),
            steering_moat_score=max(0, moat_score),
            anti_fluff_tone_score=max(0, tone_score),
            detailed_critique=critique
        )
