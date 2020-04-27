.PHONY: setup-venv test-setup test

setup-venv:
	rm -rf .venv
	python3 -m venv .venv
	.venv/bin/python3 -m pip install .

test-setup: setup-venv
	.venv/bin/python3 -m pip install -e .[dev]

test:
	.venv/bin/python3 -m pytest -vv --cov=mailanalysis
