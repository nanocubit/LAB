from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from asl_router.replay import verify_replay


artifact_manifest = (
    Path(__file__).parent
    / "artifacts"
    / "artifact-manifest.json"
)

expected = json.loads(
    artifact_manifest.read_text(encoding="utf-8")
)["result_digest"]

result = verify_replay(
    expected_result_digest=expected,
    seed=7,
    episodes=400,
)

print(json.dumps(result, sort_keys=True))

raise SystemExit(0 if result["ok"] else 1)
