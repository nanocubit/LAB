from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from asl_router.phase_aware_replay import run_experiment


OUTPUT = Path(__file__).parent / "artifacts"
OUTPUT.mkdir(exist_ok=True)

result = run_experiment(
    seed=17,
    episodes=400,
    exploration_rate=0.1,
)

(OUTPUT / "trace.json").write_text(
    json.dumps(
        result["trace"],
        sort_keys=True,
        separators=(",", ":"),
    ),
    encoding="utf-8",
)

(OUTPUT / "metrics.json").write_text(
    json.dumps(
        result["metrics"],
        sort_keys=True,
        separators=(",", ":"),
    ),
    encoding="utf-8",
)

(OUTPUT / "artifact-manifest.json").write_text(
    json.dumps(
        {
            key: result[key]
            for key in (
                "trace_digest",
                "metrics_digest",
                "result_digest",
            )
        },
        sort_keys=True,
        separators=(",", ":"),
    ),
    encoding="utf-8",
)

print(result["result_digest"])
