"""Collect one row per run into runs.csv from the results folders. Best-effort: fields a
harness doesn't report are left blank. Usage: python3 scripts/collect.py [RESULTS_ROOT]"""
import csv, json, os, sys, glob, datetime
RES = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/de4-2-results")
plan = {r["run_id"]: r for r in csv.DictReader(open("plan.csv"))}
FIELDS = ["run_id","harness","model","prompt","rep","start","end","wall_min","exit",
          "num_turns","tool_calls","input_tokens","cached_input_tokens","output_tokens",
          "models_used","cost_usd_reported","n_figures","answer_words","sources_listed",
          "snapshots","debrief","notes"]
def rd(p):
    try: return open(p).read().strip()
    except OSError: return ""
rows = []
for rid, p in plan.items():
    o = os.path.join(RES, rid)
    if not os.path.isdir(o): continue
    row = {k: "" for k in FIELDS}; row.update({k: p[k] for k in ["run_id","harness","model","prompt","rep"]})
    row["start"], row["end"], row["exit"] = rd(f"{o}/start.txt"), rd(f"{o}/end.txt"), rd(f"{o}/turn1.exit")
    try:
        t = lambda s: datetime.datetime.fromisoformat(s)
        row["wall_min"] = round((t(row["end"]) - t(row["start"])).total_seconds() / 60, 1)
    except Exception: pass
    if p["harness"] == "claude" and os.path.exists(f"{o}/turn1.json"):
        try:
            j = json.load(open(f"{o}/turn1.json"))
            u = j.get("usage", {})
            row["num_turns"] = j.get("num_turns", "")
            row["input_tokens"] = u.get("input_tokens", "")
            row["cached_input_tokens"] = (u.get("cache_read_input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0)
            row["output_tokens"] = u.get("output_tokens", "")
            row["cost_usd_reported"] = j.get("total_cost_usd", "")
            mu = j.get("modelUsage") or {}
            row["models_used"] = ";".join(f"{m}:{v.get('costUSD','')}" for m, v in mu.items())
        except Exception as e: row["notes"] += f"turn1.json unreadable ({e}); "
    if p["harness"] == "codex" and os.path.exists(f"{o}/turn1.jsonl"):
        last, tools = None, 0
        for l in open(f"{o}/turn1.jsonl"):
            try: e = json.loads(l)
            except Exception: continue
            s = json.dumps(e)
            if "token" in s and "usage" in s: last = e
            if '"exec_command' in s or '"tool_call' in s or '"function_call' in s: tools += 1
        row["tool_calls"] = tools or ""
        if last: row["notes"] += "codex usage event: " + json.dumps(last)[:300] + "; "
    fr = f"{o}/frozen"
    row["n_figures"] = len(glob.glob(f"{fr}/figures/*"))
    row["answer_words"] = len(rd(f"{fr}/answer.md").split())
    row["sources_listed"] = len([l for l in rd(f"{fr}/sources.txt").splitlines() if l.strip()])
    row["snapshots"] = ";".join(sorted(os.path.basename(x) for x in glob.glob(f"{o}/snapshots/t*")))
    row["debrief"] = "yes" if os.path.exists(f"{o}/debrief/ABOUT.md") else "no"
    rows.append(row)
with open("runs.csv", "w", newline="") as f:
    w = csv.DictWriter(f, FIELDS); w.writeheader(); w.writerows(rows)
print(f"{len(rows)} runs written to runs.csv")
