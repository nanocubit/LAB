# Benchmark reports

Reports are generated artifacts. Canonical truth remains the versioned specification, dataset, workload, and golden answers.

## Correctness

Correctness reports include event precision/recall/F1, status and temporal accuracy, groundedness, EvidencePack coverage/minimality, edge F1, path recall, reachability, hybrid ranking metrics, forbidden hit rate, state equivalence, and failure diagnostics.

## Performance

Performance reports are emitted only after correctness passes and include ingest/index build, cold/warm distributions, throughput, repetitions, RSS, disk footprint, amplification, and runner profile.

## Architecture

Architecture reports list services, artifacts, indexes/materializations, schema objects, adapter LOC, round trips, setup, dual-write, build/startup, and RAM/storage amplification. v0.1 provides no composite architecture score.

## Gaps

Gap reports convert failed correctness gates or expensive workarounds into roadmap evidence: affected queries, symptom/cost, workaround, round trips/candidate pools/glue LOC, candidate primitive/index, priority, and trade-offs. For ToroidalDB, this identifies missing semantic primitives or access paths without redefining the benchmark around current TQL/storage behavior.
