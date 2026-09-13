from __future__ import annotations

from .canonical import digest
from .phase_aware import PhaseAwareCandidatePolicy
from .synthetic import SyntheticWorld


def run_experiment(
    seed: int = 17,
    episodes: int = 400,
    exploration_rate: float = 0.1,
) -> dict[str, object]:
    if episodes <= 0:
        raise ValueError("episodes must be positive")

    world = SyntheticWorld(seed)
    policy = PhaseAwareCandidatePolicy(
        seed=seed,
        exploration_rate=exploration_rate,
    )

    trace: list[dict[str, object]] = []

    for tick in range(episodes):
        context = world.context(tick)
        action = policy.select(context)
        trace.append(world.outcome(context, action))

    phase_metrics: dict[str, dict[str, float | int]] = {}

    for phase in ("A", "B", "C", "D"):
        rows = [row for row in trace if row["phase"] == phase]

        if not rows:
            continue

        phase_metrics[phase] = {
            "episodes": len(rows),
            "mean_utility": round(
                sum(float(row["utility"]) for row in rows) / len(rows),
                12,
            ),
            "mean_oracle_regret": round(
                sum(
                    float(row["oracle_utility"]) - float(row["utility"])
                    for row in rows
                )
                / len(rows),
                12,
            ),
        }

    metrics = {
        "experiment_id": "EXP-ASL-0002-phase-aware-candidate",
        "seed": seed,
        "episodes": episodes,
        "policy_id": policy.policy_id,
        "exploration_rate": exploration_rate,
        "phase_metrics": phase_metrics,
        "mean_utility": round(
            sum(float(row["utility"]) for row in trace) / len(trace),
            12,
        ),
    }

    trace_digest = digest(trace)
    metrics_digest = digest(metrics)
    result_digest = digest(
        {
            "trace_digest": trace_digest,
            "metrics_digest": metrics_digest,
        }
    )

    return {
        "trace": trace,
        "metrics": metrics,
        "trace_digest": trace_digest,
        "metrics_digest": metrics_digest,
        "result_digest": result_digest,
    }


def verify_replay(
    expected_result_digest: str,
    seed: int = 17,
    episodes: int = 400,
    exploration_rate: float = 0.1,
) -> dict[str, object]:
    actual = run_experiment(
        seed=seed,
        episodes=episodes,
        exploration_rate=exploration_rate,
    )["result_digest"]

    return {
        "ok": actual == expected_result_digest,
        "expected_result_digest": expected_result_digest,
        "actual_result_digest": actual,
    }
