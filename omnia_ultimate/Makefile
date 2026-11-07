PYTHON ?= python3
.PHONY: test demo serve
test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v
demo:
	PYTHONPATH=src $(PYTHON) -m omnia_core demo
serve:
	PYTHONPATH=src $(PYTHON) -m omnia_core server
