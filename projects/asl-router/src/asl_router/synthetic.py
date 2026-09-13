from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

ACTIONS = (
    "vector_only",
    "bm25_only",
    "hybrid",
    "hybrid_rerank",
)


@dataclass(frozen=True)
class Context:
    tick: int
    phase: str
    query_type: str
    freshness: str
    graph_density: str
    evidence_requirement: str


class SyntheticWorld:
    def __init__(self, seed: int = 7) -> None:
        self.seed = seed

    def phase(self, tick: int) -> str:
        if tick < 100:
            return "A"
        if tick < 200:
            return "B"
        if tick < 300:
            return "C"
        return "D"

    def context(self, tick: int) -> Context:
        phase = self.phase(tick)

        values = {
            "A": ("semantic", "low", "low", "standard"),
            "B": ("mixed", "medium", "medium", "standard"),
            "C": ("graph_like", "high", "high", "strict"),
            "D": ("time_sensitive", "high", "medium", "strict"),
        }[phase]

        return Context(tick, phase, *values)

    def utilities(self, phase: str) -> dict[str, float]:
        return {
            "A": {
                "vector_only": 0.82,
                "hybrid": 0.76,
                "bm25_only": 0.67,
                "hybrid_rerank": 0.73,
            },
            "B": {
                "vector_only": 0.61,
                "hybrid": 0.79,
                "bm25_only": 0.58,
                "hybrid_rerank": 0.74,
            },
            "C": {
                "vector_only": 0.58,
                "hybrid": 0.75,
                "bm25_only": 0.49,
                "hybrid_rerank": 0.86,
            },
            "D": {
                "vector_only": 0.80,
                "hybrid": 0.81,
                "bm25_only": 0.62,
                "hybrid_rerank": 0.78,
            },
        }[phase]

    def outcome(self, context: Context, action: str) -> dict[str, object]:
        if action not in ACTIONS:
            raise ValueError(f"unknown action: {action}")

        base = self.utilities(context.phase)

        raw = f"{self.seed}:{context.tick}:{action}".encode("utf-8")
        noise = int(sha256(raw).hexdigest()[:8], 16) / 0xFFFFFFFF

        utility = round(
            max(0.0, min(1.0, base[action] + (noise - 0.5) * 0.02)),
            12,
        )

        optimal_action = max(base, key=base.get)

        return {
            "tick": context.tick,
            "phase": context.phase,
            "action": action,
            "utility": utility,
            "quality": utility,
            "evidence_coverage": {
                "vector_only": 0.72,
                "bm25_only": 0.69,
                "hybrid": 0.84,
                "hybrid_rerank": 0.93,
            }[action],
            "risk": {
                "vector_only": 0.08,
                "bm25_only": 0.09,
                "hybrid": 0.06,
                "hybrid_rerank": 0.05,
            }[action],
            "cost": {
                "vector_only": 0.01,
                "bm25_only": 0.01,
                "hybrid": 0.02,
                "hybrid_rerank": 0.05,
            }[action],
            "latency_ms": {
                "vector_only": 600,
                "bm25_only": 700,
                "hybrid": 1200,
                "hybrid_rerank": 3000,
            }[action],
            "optimal_action": optimal_action,
            "oracle_utility": base[optimal_action],
        }
