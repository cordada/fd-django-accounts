SHELL = /usr/bin/env bash

# Sources Root
SOURCES_ROOT = $(CURDIR)/src

# Python
PYTHON = python3
PYTHON_PIP = $(PYTHON) -m pip
PYTHON_PIP_VERSION_SPECIFIER = ==24.2
PYTHON_VIRTUALENV_DIR = venv

# Tox
TOXENV ?= py310

.DEFAULT_GOAL := help
.PHONY: help
.PHONY: clean clean-build clean-pyc clean-test
.PHONY: install-dev install-deps-dev
.PHONY: lint test test-all test-coverage
.PHONY: test-coverage-report test-coverage-report-console test-coverage-report-xml test-coverage-report-html
.PHONY: docs build dist deploy upload-release
.PHONY: docker-compose-run-test
.PHONY: python-virtualenv
.PHONY: python-pip-install

help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc clean-test ## remove all build, test, lint, coverage and Python artifacts

clean-build: ## remove build artifacts (dist, docs, etc)
	${RM} -r .eggs/
	${RM} -r build/
	${RM} -r docs/_build/
	${RM} docs/fd_dj_accounts.rst
	${RM} docs/modules.rst
	${RM} -r dist/
	find . -name '*.egg-info' -exec ${RM} -r {} +
	find . -name '*.egg' -exec ${RM} -r {} +

clean-pyc: ## remove Python file artifacts
	find . -iname '*.py[cod]' -delete
	find . -name '*~' -exec ${RM} {} +
	find . -iname __pycache__ -type d -prune -exec ${RM} -r {} \;

clean-test: ## remove test, lint and coverage artifacts
	${RM} -r .cache/
	${RM} -r .tox/
	${RM} -f .coverage
	${RM} -r htmlcov/
	${RM} -r test-reports/
	${RM} -r .mypy_cache/

install-dev: install-deps-dev
install-dev: ## Install for development
	python -m pip install --editable .
	python -m pip check

install-deps-dev: python-pip-install
install-deps-dev: ## Install dependencies for development
	python -m pip install -r requirements.txt
	python -m pip check

	python -m pip install -r requirements_test.txt
	python -m pip check

	python -m pip install -r requirements_release.txt
	python -m pip check

lint: FLAKE8_FILES = *.py "$(SOURCES_ROOT)"
lint: ## run tools for code style analysis, static type check, etc
	flake8 $(FLAKE8_FILES)
	mypy

test: ## run tests quickly with the default Tox Python
	tox -e "$(TOXENV)"

test-all: ## run tests on every Python version with tox
	tox

test-coverage: ## run tests and record test coverage
	coverage run --rcfile=.coveragerc.test.ini runtests.py tests

test-coverage-report: test-coverage-report-console
test-coverage-report: test-coverage-report-xml
test-coverage-report: test-coverage-report-html
test-coverage-report: ## Run tests, measure code coverage, and generate reports

test-coverage-report-console: ## print test coverage summary
	coverage report --rcfile=.coveragerc.test.ini -m

test-coverage-report-xml: ## Generate test coverage XML report
	coverage xml --rcfile=.coveragerc.test.ini

test-coverage-report-html: ## generate test coverage HTML report
	coverage html --rcfile=.coveragerc.test.ini

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/fd_dj_accounts.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ "$(SOURCES_ROOT)/fd_dj_accounts"
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

build: ## Build Python package
	$(PYTHON) setup.py build

dist: build ## builds source and wheel package
	python -m build --sdist
	python -m build --wheel
	twine check dist/*
	twine check --strict dist/*
	ls -l dist

upload-release: ## upload dist packages
	python -m twine upload 'dist/*'

deploy: upload-release
deploy: ## Deploy or publish

python-virtualenv: ## Create virtual Python environment
	$(PYTHON) -m venv "$(PYTHON_VIRTUALENV_DIR)"

python-pip-install: ## Install Pip
	$(PYTHON_PIP) install 'pip$(PYTHON_PIP_VERSION_SPECIFIER)'

docker-compose-run-test: export COMPOSE_FILE = docker-compose.yml:docker-compose.test.yml
docker-compose-run-test:  ## Run tests with Docker Compose
	docker compose run --rm --env TOXENV=py39 -- app-python3.9
	docker compose run --rm --env TOXENV=py310 -- app-python3.10
