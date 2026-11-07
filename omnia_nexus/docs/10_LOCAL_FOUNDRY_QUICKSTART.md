# OMNIA Foundry — Local Quickstart

## Requirements
- Python 3.11+
- Standard library only; no third-party packages required.

## Tests
From the project root:
```bash
python -m unittest discover -s tests -v
```

## Add the source package to PYTHONPATH
Linux/macOS:
```bash
export PYTHONPATH="$PWD/src"
```
Windows PowerShell:
```powershell
$env:PYTHONPATH = "$PWD/src"
```

## Initialise and inspect
```bash
python -m omnia_foundry init --db data/omnia.db
python -m omnia_foundry report --db data/omnia.db
```

## Create a programme
```bash
python -m omnia_foundry programme-add --db data/omnia.db \
  --name "GODMODE Career OS" --domain "AI workflow product" \
  --owner "Founder" --thesis "Evidence-grounded career execution"
```

## Create a task
```bash
python -m omnia_foundry task-add --db data/omnia.db \
  --title "Interview five target users" --owner "Founder" \
  --priority P0 --acceptance "Five consented interviews documented"
```

## Add an evidence record
```bash
python -m omnia_foundry evidence-add --db data/omnia.db \
  --claim "Users struggle to track applications" \
  --source "Interview synthesis" --classification observation \
  --confidence medium --notes "Only state after interviews are actually conducted"
```

## Verify the audit chain
```bash
python -m omnia_foundry audit-verify --db data/omnia.db
```

## Security limitation
This is a local, single-user prototype. It has no login, tenant isolation, remote API, encrypted database, secure key custody, or production hardening. Do not expose it to the internet or store sensitive personal data.
