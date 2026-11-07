import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from omnia_foundry.store import Store
from omnia_foundry.audit import verify

db_path = Path(__file__).resolve().parents[1] / "data" / "omnia_foundry.db"
store = Store(db_path)

# Verify tasks status
tasks = store.rows("tasks")
total = len(tasks)
completed = sum(1 for t in tasks if t["status"] == "completed")
print(f"Total tasks: {total}, Completed tasks: {completed}")

events = store.audit_events()
valid = verify(events)
print(f"Audit verification: valid={valid}, event_count={len(events)}")
assert valid is True, "Audit chain invalid!"
assert completed == 50, f"Expected 50 completed tasks, got {completed}"
print("VERIFICATION SUCCESSFUL: 50/50 tasks completed, 100% cryptographic ledger integrity verified.")
