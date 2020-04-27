setup-venv:
	rm -rf .venv
	python3 -m venv .venv
	.venv/bin/python3 -m pip install .

test: setup-venv
	.venv/bin/python3 -m pip install -e .[dev]
	.venv/bin/python3 -m pytest
