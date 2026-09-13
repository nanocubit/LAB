# Evidence Levels

Evidence level describes verification strength and permitted governance influence; it is not a quality score or proof that an interpretation is correct.

| Level | Meaning | May influence |
|---|---|---|
| `spike` | Exploratory work without manifest obligations | Author only; active TTL 30 days |
| `registered` | Hypothesis, protocol, and manifest preregistered | Intra-experiment iteration |
| `replay_verified` | Tier-1 replay matches declared result digest | ADR input; memory only through human PR |
| `agent_reproduced` | `replay_verified` plus independent reproduction L3+ | Stronger ADR input |
| `human_verified` | Human reviewed claim, protocol, and interpretation | Curated memory and permitted promotion inputs |

`replay_verified` means the declared protocol reproduced the declared result. It does **not** prove causal interpretation, external validity, or hypothesis truth.

A Tier-2 Colab/Kaggle receipt is capped at `registered` until a new Tier-1 receipt replays the exported artifact bundle.
