import json
from pathlib import Path
from collections import Counter

events_file = Path("artifacts/telemetry/events.jsonl")
audit_file = Path("artifacts/telemetry/audit_events.jsonl")

print("--- TELEMETRY VERIFICATION ---")
if events_file.exists():
    with open(events_file, "r", encoding="utf-8") as f:
        events = [json.loads(line) for line in f if line.strip()]
    print(f"Total events in {events_file}: {len(events)}")
    event_counts = Counter(e.get("event_name") for e in events)
    for k, v in event_counts.items():
        print(f"  {k}: {v}")
    print("Sample event:", json.dumps(events[-1], indent=2))
else:
    print(f"MISSING: {events_file}")

if audit_file.exists():
    with open(audit_file, "r", encoding="utf-8") as f:
        audit_events = [json.loads(line) for line in f if line.strip()]
    print(f"\nTotal audit events in {audit_file}: {len(audit_events)}")
    hub_counts = Counter(e.get("hub") for e in audit_events)
    print("Audit events per hub:", dict(hub_counts))
    print("Sample audit event:", json.dumps(audit_events[-1], indent=2))
else:
    print(f"MISSING: {audit_file}")
