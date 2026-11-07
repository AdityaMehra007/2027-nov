# Local OMNIA Workflow Core — Quickstart

## Requirements
- Python 3.11 or later.
- No third-party Python packages required.
- Works as a local development prototype.

## Run tests
From the project root:

```bash
python -m unittest discover -s tests -v
```

## Run the server
```bash
python -m omnia_core server --host 127.0.0.1 --port 8765
```

Keep the host bound to loopback. Do not expose this unauthenticated prototype to the public internet.

## Create a safe demo task
```bash
curl -X POST http://127.0.0.1:8765/v1/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Summarise a research objective","action":"demo.echo","action_class":"draft","payload":{"objective":"Evaluate a customer workflow"}}'
```

## List tasks
```bash
curl http://127.0.0.1:8765/v1/tasks
```

## Create an approval-gated simulation
```bash
curl -X POST http://127.0.0.1:8765/v1/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Simulated external action","action":"demo.external_simulation","action_class":"approval_required","payload":{"destination":"example-only"}}'
```

Request approval:
```bash
curl -X POST http://127.0.0.1:8765/v1/tasks/TASK_ID/request-approval \
  -H 'Content-Type: application/json' \
  -d '{"requested_by":"local-founder","reason":"Demonstrate approval workflow"}'
```

Approve:
```bash
curl -X POST http://127.0.0.1:8765/v1/tasks/TASK_ID/approve \
  -H 'Content-Type: application/json' \
  -d '{"approved_by":"local-founder","reason":"Approve simulation only"}'
```

Execute:
```bash
curl -X POST http://127.0.0.1:8765/v1/tasks/TASK_ID/execute
```

The external simulation handler does not contact any external service. It only returns a simulated result. The server is unauthenticated, single-node and intended for local testing.

## Production blockers
Before deployment add authentication, authorisation, tenant isolation, rate limiting, TLS, secret management, durable production database, concurrent worker coordination, audit-key management, monitoring, backups, incident response, security testing and privacy review.
