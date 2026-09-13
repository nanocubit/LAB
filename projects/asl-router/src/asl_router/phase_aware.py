from __future__ import annotations

from hashlib import sha256

from .synthetic import ACTIONS, Context


class PhaseAwareCandidatePolicy:
    policy_id = "phase-aware-candidate-v1"

    def __init__(
        self,
        seed: int = 17,
        exploration_rate: float = 0.1,
    ) -> None:
        if not 0.0 <= exploration_rate <= 1.0:
            raise ValueError("exploration_rate must be between 0 and 1")

        self.seed = seed
        self.exploration_rate = exploration_rate

    def select(self, context: Context) -> str:
        if self._explores(context):
            return self._exploration_action(context)

        return self._rule_action(context)

    def _rule_action(self, context: Context) -> str:
        rules = {
            "semantic": "vector_only",
            "mixed": "hybrid",
            "graph_like": "hybrid_rerank",
            "time_sensitive": "hybrid",
        }

        if context.evidence_requirement == "strict":
            return "hybrid_rerank"

        try:
            return rules[context.query_type]
        except KeyError as exc:
            raise ValueError(
                f"unsupported query type: {context.query_type}"
            ) from exc

    def _explores(self, context: Context) -> bool:
        threshold = int(self.exploration_rate * 1_000_000)
        value = self._stable_int(context, "explore") % 1_000_000
        return value < threshold

    def _exploration_action(self, context: Context) -> str:
        index = self._stable_int(context, "action") % len(ACTIONS)
        return ACTIONS[index]

    def _stable_int(self, context: Context, purpose: str) -> int:
        material = (
            f"{self.seed}:{context.tick}:{context.phase}:"
            f"{context.query_type}:{purpose}"
        ).encode("utf-8")
        return int(sha256(material).hexdigest()[:16], 16)
