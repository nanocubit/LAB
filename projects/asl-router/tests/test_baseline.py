from asl_router.baseline import FrozenVectorPolicy
from asl_router.synthetic import SyntheticWorld


def test_baseline_is_frozen_vector_only() -> None:
    policy = FrozenVectorPolicy()
    world = SyntheticWorld(seed=7)

    assert {
        policy.select(world.context(tick))
        for tick in range(400)
    } == {"vector_only"}
