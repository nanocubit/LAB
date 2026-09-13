#!/usr/bin/env python3
"""Run EXP-ASL-0003 and write a canonical paired-comparison artifact."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXP_DIR = Path(__file__).resolve().parent
RESULT_PATH = EXP_DIR / "results" / "result.json"
SEED = 17
EPISODES = 400
CANDIDATE_EXPLORATION_RATE = 0.1

def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()

def digest(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()

def run_policy(policy: str, exploration_rate: float | None) -> dict:
    command = [
        sys.executable,
        "-m",
        "asl_router.run_synthetic",
        "--policy",
        policy,
        "--seed",
        str(SEED),
        "--episodes",
        str(EPISODES),
        "--json",
    ]
    if exploration_rate is not None:
        command.extend(["--exploration-rate", str(exploration_rate)])
    completed = subprocess.run(command, cwd=ROOT, check=True, text=True, capture_output=True)
    payload = json.loads(completed.stdout)
    return {
        "policy": policy,
        "seed": SEED,
        "episodes": EPISODES,
        "exploration_rate": exploration_rate,
        "metrics": payload,
    }

def main() -> None:
    baseline = run_policy("frozen-vector-only-v1", None)
    candidate = run_policy("phase-aware-candidate-v1", CANDIDATE_EXPLORATION_RATE)
    baseline_utility = baseline["metrics"]["mean_utility"]
    candidate_utility = candidate["metrics"]["mean_utility"]
    result = {
        "experiment_id": "EXP-ASL-0003",
        "status": "completed",
        "configuration": {
            "seed": SEED,
            "episodes": EPISODES,
            "candidate_exploration_rate": CANDIDATE_EXPLORATION_RATE,
            "primary_metric": "mean_utility",
        },
        "baseline": baseline,
        "candidate": candidate,
        "baseline_digest": digest(baseline),
        "candidate_digest": digest(candidate),
        "delta_17": candidate_utility - baseline_utility,
        "hypothesis_supported": candidate_utility > baseline_utility,
    }
    result["result_digest"] = digest(result)
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
