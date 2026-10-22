"""Count saved submissions and collect brief native-agent records into runs.csv.

Run from the experiment directory with /opt/anaconda3/envs/p314/bin/python.
Usage: scripts/collect.py [RESULTS_ROOT] (default: ./results)
"""
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

RESULTS = Path(sys.argv[1] if len(sys.argv) > 1 else "results").expanduser()
FIELDS = [
    "run_id", "harness", "interface", "requested_model", "actual_model", "prompt",
    "rep", "agent_id", "status", "start", "end", "wall_min", "n_figures",
    "answer_words", "n_work_files", "input_tokens", "cache_write_tokens",
    "cache_read_tokens", "output_tokens", "output_tokens_est", "cost_usd_est",
    "debrief", "notes",
]
# USD per million tokens: (input, cache write, cache read, output). Anthropic first-party list
# prices as of 2026-10-06 (cache write = 1.25x input, 5-minute cache). Runs actually go
# through a cloud provider, not Anthropic's API, so these are API-equivalent estimates.
# Codex estimates are configured separately below.
PRICES = {
    "claude-opus-5-5": (4.00, 5.00, 0.20, 20.00),
    "claude-sonnet-5-5": (2.00, 2.50, 0.20, 10.00),
}


def transcript_usage(folder):
    """Token totals from a Claude Code subagent transcript (agent-*.jsonl) in folder.

    The transcript's output_tokens undercounts (it records usage from the start of each
    streamed message), so output_tokens_est also estimates output from the visible content
    at ~4 characters per token and takes the larger. Hidden thinking is not counted in
    either, so both are lower bounds."""
    usage, chars, models = {}, 0, set()
    for path in folder.glob("agent-*.jsonl"):
        messages = {}
        for line in path.open():
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            message = entry.get("message") or {}
            if entry.get("type") != "assistant" or not message.get("id"):
                continue
            messages[message["id"]] = message
            for block in message.get("content") or []:
                kind = block.get("type")
                if kind == "text":
                    chars += len(block.get("text", ""))
                elif kind == "thinking":
                    chars += len(block.get("thinking", ""))
                elif kind == "tool_use":
                    chars += len(json.dumps(block.get("input")))
        for message in messages.values():
            models.add(message.get("model", ""))
            for key, value in (message.get("usage") or {}).items():
                if isinstance(value, int):
                    usage[key] = usage.get(key, 0) + value
    if not usage:
        return None
    totals = {
        "input_tokens": usage.get("input_tokens", 0),
        "cache_write_tokens": usage.get("cache_creation_input_tokens", 0),
        "cache_read_tokens": usage.get("cache_read_input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
    }
    totals["output_tokens_est"] = max(totals["output_tokens"], chars // 4)
    models.discard("")
    price = PRICES.get(models.pop()) if len(models) == 1 else None
    if price:
        totals["cost_usd_est"] = round(
            (totals["input_tokens"] * price[0] + totals["cache_write_tokens"] * price[1]
             + totals["cache_read_tokens"] * price[2]
             + totals["output_tokens_est"] * price[3]) / 1e6, 2)
    return totals


def codex_usage(folder):
    """Token totals from a copied Codex session log (*.jsonl with token_count events)."""
    last = None
    models = set()
    for path in folder.glob("*.jsonl"):
        for line in path.open():
            if '"turn_context"' in line:
                try:
                    model = (json.loads(line).get("payload") or {}).get("model")
                    if model:
                        models.add(model)
                except ValueError:
                    pass
            if "total_token_usage" not in line:
                continue
            try:
                info = (json.loads(line).get("payload") or {}).get("info") or {}
            except ValueError:
                continue
            last = info.get("total_token_usage") or last
    if not last:
        return None
    cached = last.get("cached_input_tokens", 0)
    totals = {
        "input_tokens": last.get("input_tokens", 0) - cached,
        "cache_read_tokens": cached,
        "output_tokens": last.get("output_tokens", 0),
        "output_tokens_est": last.get("output_tokens", 0),
    }
    prices = None
    if models == {"openai.gpt-6-luna"}:
        prices = (.10, .125, .01, .50)
    elif models == {"openai.gpt-6.1-sol"} and folder.name.startswith("Sol-"):
        # Preserve historical Codex-* accounting; estimate the new Sol-* trials.
        prices = (2.00, 2.50, .10, 10.00)
    if prices:
        # API-equivalent estimate, Standard tier, 30-minute cache writes.
        # Official pricing fetched 2026-10-22:
        # https://developers.openai.com/api/docs/pricing
        # USD/MTok: (ordinary input, cache write, cache read, output).
        writes = last.get("cache_write_input_tokens", 0)
        totals["input_tokens"] -= writes
        totals["cache_write_tokens"] = writes
        totals["cost_usd_est"] = round(
            (totals["input_tokens"] * prices[0] + writes * prices[1]
             + cached * prices[2] + totals["output_tokens"] * prices[3]) / 1e6, 6)
    return totals
FIGURE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".pdf"}


def read_text(path):
    return path.read_text() if path.is_file() else ""


previous_notes = {}
if Path("runs.csv").is_file():
    with Path("runs.csv").open(newline="") as source:
        previous_notes = {
            row["run_id"]: row.get("notes", "") for row in csv.DictReader(source)
        }

with Path("plan.csv").open(newline="") as source:
    plan = list(csv.DictReader(source))

rows = []
for planned in plan:
    run_id = planned["run_id"]
    folder = RESULTS / run_id
    if not folder.is_dir():
        continue
    record_path = folder / "run.json"
    try:
        record = json.loads(read_text(record_path) or "{}")
        if not isinstance(record, dict):
            raise ValueError("expected a JSON object")
    except (ValueError, OSError) as error:
        sys.exit(f"Cannot collect {record_path}: {error}")

    row = {field: "" for field in FIELDS}
    row.update({key: planned[key] for key in ("run_id", "harness", "prompt", "rep")})
    row["requested_model"] = record.get("requested_model", planned["model"])
    for key in ("interface", "actual_model", "agent_id", "status", "start", "end"):
        row[key] = record.get(key, "")
    notes = previous_notes.get(run_id, "")
    record_notes = record.get("notes", "")
    if record_notes and record_notes not in notes:
        notes = "; ".join(filter(None, (notes, record_notes)))
    if not record_path.is_file():
        warning = "missing run.json"
        if warning not in notes:
            notes = "; ".join(filter(None, (notes, warning)))
    if row["start"] and row["end"]:
        try:
            duration = datetime.fromisoformat(row["end"]) - datetime.fromisoformat(row["start"])
            row["wall_min"] = round(duration.total_seconds() / 60, 1)
        except (ValueError, TypeError):
            warning = "unreadable timestamps"
            if warning not in notes:
                notes = "; ".join(filter(None, (notes, warning)))
    frozen = folder / "frozen"
    row["n_figures"] = sum(
        file.is_file() and file.suffix.lower() in FIGURE_SUFFIXES
        for file in (frozen / "figures").rglob("*")
    )
    row["answer_words"] = len(read_text(frozen / "answer.md").split())
    row["n_work_files"] = sum(file.is_file() for file in (folder / "work").rglob("*"))
    tokens = (transcript_usage if planned["harness"] == "claude" else codex_usage)(folder)
    if tokens:
        row.update(tokens)
    elif "no token data" not in notes:
        notes = "; ".join(filter(None, (notes, "no token data (optional telemetry unavailable)")))
    row["debrief"] = "yes" if (folder / "debrief" / "ABOUT.md").is_file() else "no"
    row["notes"] = notes
    rows.append(row)

with Path("runs.csv").open("w", newline="") as output:
    writer = csv.DictWriter(output, FIELDS)
    writer.writeheader()
    writer.writerows(rows)
print(f"{len(rows)} runs written to runs.csv")
