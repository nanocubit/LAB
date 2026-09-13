# nanocubit/LAB

`LAB` is a research operating system for a solo researcher and bounded agent executors.

It stores projects, experiments, receipts, artifacts, protocols, decisions, and curated research memory in one GitHub-native workspace.

## Core rule

```text
Replaceable compute; durable evidence.
```

Read [LAB_CONTRACT_v0.1.md](LAB_CONTRACT_v0.1.md) before adding experiments or automation.

## Quick start

```bash
cd lab_sdk
python -m pip install -e .[dev]
pytest -q
lab canonicalize ../../example.json
```

Create a new project from `projects/_template/`. Each registered experiment belongs to an `experiment/<project>/<experiment-id>/<slug>` branch until human merge into `main`.
