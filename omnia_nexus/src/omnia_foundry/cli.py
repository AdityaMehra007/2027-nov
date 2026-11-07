from __future__ import annotations
import argparse, json
from .store import Store
from .audit import verify
from .models import identifier

def main():
    p = argparse.ArgumentParser(prog="omnia-foundry", description="Local programme, task, experiment and evidence tracker.")
    p.add_argument("--db", default="data/omnia_foundry.db")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init")
    q = sub.add_parser("programme-add")
    q.add_argument("--name", required=True); q.add_argument("--domain", required=True)
    q.add_argument("--owner", required=True); q.add_argument("--thesis", required=True)

    q = sub.add_parser("task-add")
    q.add_argument("--title", required=True); q.add_argument("--priority", choices=["P0","P1","P2","P3"], default="P1")
    q.add_argument("--owner", required=True); q.add_argument("--acceptance", required=True)
    q.add_argument("--programme-id")

    q = sub.add_parser("task-set")
    q.add_argument("--task-id", required=True)
    q.add_argument("--status", choices=["not_started","researching","specified","in_progress","in_review","testing","blocked","completed","rejected","deferred"], required=True)

    q = sub.add_parser("evidence-add")
    q.add_argument("--claim", required=True); q.add_argument("--source", required=True)
    q.add_argument("--source-date", default=""); q.add_argument("--classification", choices=["fact","estimate","hypothesis","observation","opinion"], required=True)
    q.add_argument("--confidence", choices=["low","medium","high"], default="medium")
    q.add_argument("--notes", default="")

    q = sub.add_parser("experiment-add")
    q.add_argument("--programme-id"); q.add_argument("--hypothesis", required=True); q.add_argument("--protocol", required=True)

    q = sub.add_parser("experiment-complete")
    q.add_argument("--experiment-id", required=True); q.add_argument("--outcome", required=True); q.add_argument("--evidence-id", required=True)

    q = sub.add_parser("approval-request")
    q.add_argument("--action", required=True); q.add_argument("--details", required=True); q.add_argument("--requested-by", required=True)

    q = sub.add_parser("approval-decide")
    q.add_argument("--approval-id", required=True); q.add_argument("--approved-by", required=True)
    q.add_argument("--reason", required=True); q.add_argument("--decision", choices=["approve","reject"], required=True)

    q = sub.add_parser("report")
    q.add_argument("--table", choices=["programmes","tasks","experiments","evidence","approvals"], default=None)

    sub.add_parser("audit-verify")
    args = p.parse_args()
    store = Store(args.db)

    if args.cmd == "init":
        print(json.dumps({"status":"initialised","database":args.db}))
    elif args.cmd == "programme-add":
        pid = identifier("PRG")
        store.add_programme(pid,args.name,args.domain,args.owner,args.thesis)
        print(json.dumps({"programme_id":pid}))
    elif args.cmd == "task-add":
        tid = identifier("TSK")
        store.add_task(tid,args.programme_id,args.title,args.priority,args.owner,args.acceptance)
        print(json.dumps({"task_id":tid}))
    elif args.cmd == "task-set":
        store.set_task_status(args.task_id,args.status)
        print(json.dumps({"status":"updated","task_id":args.task_id}))
    elif args.cmd == "evidence-add":
        eid = identifier("EVD")
        store.add_evidence(eid,args.claim,args.source,args.source_date,args.classification,args.confidence,args.notes)
        print(json.dumps({"evidence_id":eid}))
    elif args.cmd == "experiment-add":
        xid = identifier("EXP")
        store.add_experiment(xid,args.programme_id,args.hypothesis,args.protocol)
        print(json.dumps({"experiment_id":xid}))
    elif args.cmd == "experiment-complete":
        store.complete_experiment(args.experiment_id,args.outcome,args.evidence_id)
        print(json.dumps({"status":"completed","experiment_id":args.experiment_id}))
    elif args.cmd == "approval-request":
        aid = identifier("APR")
        store.request_approval(aid,args.action,args.details,args.requested_by)
        print(json.dumps({"approval_id":aid,"status":"pending"}))
    elif args.cmd == "approval-decide":
        store.decide_approval(args.approval_id,args.approved_by,args.reason,args.decision=="approve")
        print(json.dumps({"approval_id":args.approval_id,"status":args.decision+"d"}))
    elif args.cmd == "report":
        tables = [args.table] if args.table else ["programmes","tasks","experiments","evidence","approvals"]
        print(json.dumps({t:store.rows(t) for t in tables},indent=2))
    elif args.cmd == "audit-verify":
        events = store.audit_events()
        print(json.dumps({"valid":verify(events),"event_count":len(events)}))
        if not verify(events):
            raise SystemExit(1)

if __name__ == "__main__":
    main()
