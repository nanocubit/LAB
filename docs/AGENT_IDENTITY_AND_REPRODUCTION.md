# Agent Identity and Reproduction

Every receipt MUST declare:

```yaml
executor:
  principal: solo
  agent:
    provider: example
    model: example-model
    agent_instance_id: null
  session_id: T-042-uuid
  commission_ref: agents/task-queue/T-042.yaml
  execution_mode: supervised
```

Cost is attributed to `principal`; agent cost data is declared with a verification level.

## Reproduction independence

| Level | Name | Meaning |
|---|---|---|
| L0 | `same_agent_same_session` | Rerun; not reproduction |
| L1 | `same_agent_fresh_context` | Weak reproduction |
| L2 | `same_model_different_prompt` | Moderate reproduction |
| L3 | `different_model` | Independent agent reproduction |
| L4 | `different_model_different_infrastructure` | Strong independent reproduction |

`agent_reproduced` MUST require L3 or L4. The same agent instance MUST NOT reproduce itself as L3.
