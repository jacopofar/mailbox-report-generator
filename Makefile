setup-venv:
	rm -rf .venv
	python3 -m venv .venv
	.venv/bin/python3 -m pip install .
