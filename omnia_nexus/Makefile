PYTHON ?= python3
.PHONY: test init report audit
test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v
init:
	PYTHONPATH=src $(PYTHON) -m omnia_foundry init
report:
	PYTHONPATH=src $(PYTHON) -m omnia_foundry report
audit:
	PYTHONPATH=src $(PYTHON) -m omnia_foundry audit-verify
