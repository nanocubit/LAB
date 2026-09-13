from __future__ import annotations

from .synthetic import Context


class FrozenVectorPolicy:
    policy_id = "frozen-vector-only-v1"

    def select(self, context: Context) -> str:
        return "vector_only"
