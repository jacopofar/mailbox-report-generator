.PHONY: help
help:
	@echo 'Usage: make <subcommand>'
	@echo ''
	@echo 'Subcommands:'
	@echo '    install       Install locally'

.PHONY: install
install:
	python3 -m pip install .


.PHONY: test
test:
	python3 -m pip install -e ".[testing]"
	python3 -m pytest --cov=mailanalysis --cov-report html tests/

.PHONY: test-fe
test-fe:
	cd frontend && npm install && npm test


.PHONY: lint
lint:
	python3 -m pip install -e ".[testing]"
	python3 -m black mailanalysis
	python3 -m mypy --strict --explicit-package-bases mailanalysis
