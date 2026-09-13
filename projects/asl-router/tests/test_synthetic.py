from asl_router.synthetic import SyntheticWorld


def test_phase_optima() -> None:
    world = SyntheticWorld(seed=7)

    assert max(
        world.utilities("A"),
        key=world.utilities("A").get,
    ) == "vector_only"

    assert max(
        world.utilities("B"),
        key=world.utilities("B").get,
    ) == "hybrid"

    assert max(
        world.utilities("C"),
        key=world.utilities("C").get,
    ) == "hybrid_rerank"

    assert max(
        world.utilities("D"),
        key=world.utilities("D").get,
    ) == "hybrid"


def test_frozen_baseline_has_positive_regret_after_drift() -> None:
    world = SyntheticWorld(seed=7)
    regret = 0.0

    for tick in range(100, 300):
        outcome = world.outcome(
            world.context(tick),
            "vector_only",
        )

        regret += (
            float(outcome["oracle_utility"])
            - float(outcome["utility"])
        )

    assert regret > 0
