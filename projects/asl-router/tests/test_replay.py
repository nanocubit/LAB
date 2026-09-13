from asl_router.replay import run_experiment, verify_replay


def test_same_inputs_produce_same_result_digest() -> None:
    assert (
        run_experiment()["result_digest"]
        == run_experiment()["result_digest"]
    )


def test_replay_accepts_expected_digest() -> None:
    result = run_experiment()

    assert verify_replay(
        str(result["result_digest"])
    )["ok"]


def test_seed_changes_run_identity() -> None:
    assert (
        run_experiment(seed=7)["result_digest"]
        != run_experiment(seed=8)["result_digest"]
    )
