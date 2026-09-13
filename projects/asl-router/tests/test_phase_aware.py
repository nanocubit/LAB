from __future__ import annotations

import unittest

from asl_router.phase_aware import PhaseAwareCandidatePolicy
from asl_router.phase_aware_replay import run_experiment, verify_replay
from asl_router.synthetic import Context


class PhaseAwareCandidatePolicyTests(unittest.TestCase):
    def context(
        self,
        tick: int,
        query_type: str,
        evidence_requirement: str = "standard",
    ) -> Context:
        return Context(
            tick=tick,
            phase="A",
            query_type=query_type,
            freshness="medium",
            graph_density="medium",
            evidence_requirement=evidence_requirement,
        )

    def test_context_rules_without_exploration(self) -> None:
        policy = PhaseAwareCandidatePolicy(exploration_rate=0.0)

        self.assertEqual(
            policy.select(self.context(0, "semantic")),
            "vector_only",
        )
        self.assertEqual(
            policy.select(self.context(1, "mixed")),
            "hybrid",
        )
        self.assertEqual(
            policy.select(self.context(2, "graph_like")),
            "hybrid_rerank",
        )
        self.assertEqual(
            policy.select(self.context(3, "time_sensitive")),
            "hybrid",
        )

    def test_strict_evidence_overrides_query_type(self) -> None:
        policy = PhaseAwareCandidatePolicy(exploration_rate=0.0)

        self.assertEqual(
            policy.select(
                self.context(
                    0,
                    "semantic",
                    evidence_requirement="strict",
                )
            ),
            "hybrid_rerank",
        )

    def test_exploration_is_deterministic(self) -> None:
        first = PhaseAwareCandidatePolicy(
            seed=17,
            exploration_rate=1.0,
        )
        second = PhaseAwareCandidatePolicy(
            seed=17,
            exploration_rate=1.0,
        )
        context = self.context(42, "semantic")

        self.assertEqual(first.select(context), second.select(context))

    def test_invalid_exploration_rate_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            PhaseAwareCandidatePolicy(exploration_rate=-0.01)

        with self.assertRaises(ValueError):
            PhaseAwareCandidatePolicy(exploration_rate=1.01)


class PhaseAwareReplayTests(unittest.TestCase):
    def test_replay_matches_result_digest(self) -> None:
        result = run_experiment(
            seed=17,
            episodes=40,
            exploration_rate=0.1,
        )

        verification = verify_replay(
            expected_result_digest=str(result["result_digest"]),
            seed=17,
            episodes=40,
            exploration_rate=0.1,
        )

        self.assertTrue(verification["ok"])

    def test_episode_count_must_be_positive(self) -> None:
        with self.assertRaises(ValueError):
            run_experiment(episodes=0)


if __name__ == "__main__":
    unittest.main()
