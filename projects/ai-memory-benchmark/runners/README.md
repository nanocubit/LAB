# Runners and GitHub Actions

GitHub Actions is the benchmark control plane for reproducibility, reviewable goldens, and conformance.

## Execution tiers

| Tier | Trigger | Environment | Purpose |
|---|---|---|---|
| PR correctness | pull request | GitHub-hosted | schema, fixture, oracle/scorer, property, targeted adapter checks |
| Public smoke | main/manual | GitHub-hosted | deterministic 10K data and public adapter correctness |
| Nightly matrix | schedule/manual | hosted or controlled containers | wider public matrix and mutations |
| Holdout conformance | protected manual/schedule | isolated controlled runner | private goldens and rotating seeds |
| Performance | manual/release | pinned self-hosted hardware | comparable tail latency and resources |

## Phase 0 workflow

The initial PR workflow validates all implemented Phase 0 artifacts. It runs oracle, golden reproducibility, scorer, and negative-adapter commands only when the expected implementation files exist. Once those files land, their failures are not suppressed.

## Holdout isolation

Holdout goldens are never committed, passed to adapter jobs, or written in adapter-visible workspaces. Oracle/scorer and adapter execution are separated; adapter jobs receive no benchmark master secret.

## Performance

GitHub-hosted timings are diagnostic only. Comparative claims require pinned self-hosted hardware with captured CPU, RAM, storage, filesystem, kernel, OS, runtime, backend/adapter/generator commits, and power profile. Correctness must pass before measured samples begin.
