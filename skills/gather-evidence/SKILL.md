---
name: gather-evidence
description: Cache-first evidence gathering for a workflow. Use when a workflow's gather stage runs, before any writer skill. Resolves each source connector through connectors.json, reuses a fresh cache, fetches only on a miss or an explicit refresh, writes one evidence.json with a content hash and a sources list, and never interprets or writes prose.
---

# Gather evidence

Inputs: the workflow's `sources` (connector, ref, notes), the connectors file (connector to server and tool), the
cache path and its `ttl_hours`, and a `refresh` flag.

1. **Cache check.** If `<cache>/last-evidence.json` exists, is younger than `ttl_hours`, and
   `refresh` is false, copy it to the run's `evidence.json` and stop.
2. **Fetch by connector.** For each source, call the tool the connectors file binds to its connector with the `ref`
   and `notes` as argument hints. Read bodies; never mark mail as read; never post, write or
   react. One keyword per chat search call. If a connector has no binding, record
   `{"connector": ..., "status": "unmapped"}` and continue.
3. **Distil, do not interpret.** Keep facts as they appear: names, dates, statuses, counts,
   quotes with their source id. Drop formatting and boilerplate. Do not infer status, do not
   resolve conflicts (record both values with their sources).
4. **Write** `evidence.json` with `gathered_at`, `sources` (connector, ref, item count, status),
   and `items`. Compute `evidence_hash` as the sha256 of the sorted items and store it in the
   file.
5. **Refresh the cache** by copying `evidence.json` to `<cache>/last-evidence.json` after the
   workflow's diff stage has read the previous copy.

The writer that runs next receives `evidence.json` and nothing else. If gathering fails for
every source, write an `evidence.json` with an empty `items` list and `status: "empty"` so the
workflow can stop cleanly instead of writing from memory.
