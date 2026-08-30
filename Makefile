SHELL := /bin/sh

.DEFAULT_GOAL := help
.DELETE_ON_ERROR:

QUARTO ?= quarto
PYTHON ?= python3
VENV ?= .ids
REQUIREMENTS ?= requirements.txt
QUARTO_ARGS ?=

VENV_PYTHON := $(VENV)/bin/python

.PHONY: help check-tools check render preview render-one install upgrade req \
	packages publish clean clean-output clean-cache

help: ## Show the available targets.
	@awk 'BEGIN {FS = ":.*## "; printf "Usage: make <target>\n\nTargets:\n"} \
		/^[a-zA-Z0-9_-]+:.*## / {printf "  %-14s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check-tools: ## Verify that required command-line tools are available.
	@command -v "$(QUARTO)" >/dev/null 2>&1 || { \
		echo "Error: Quarto executable not found: $(QUARTO)" >&2; exit 1; }
	@command -v "$(PYTHON)" >/dev/null 2>&1 || { \
		echo "Error: Python executable not found: $(PYTHON)" >&2; exit 1; }

check: check-tools ## Run Quarto's installation and environment checks.
	$(QUARTO) check

render: check-tools ## Render the complete book.
	$(QUARTO) render $(QUARTO_ARGS)

preview: check-tools ## Preview the book with live reload.
	$(QUARTO) preview $(QUARTO_ARGS)

render-one: check-tools ## Render FILE, for example: make render-one FILE=chapter.qmd
	@test -n "$(FILE)" || { \
		echo "Error: set FILE to a Quarto source file." >&2; exit 2; }
	@test -f "$(FILE)" || { \
		echo "Error: file not found: $(FILE)" >&2; exit 2; }
	$(QUARTO) render "$(FILE)" $(QUARTO_ARGS)

$(VENV_PYTHON):
	$(PYTHON) -m venv "$(VENV)"
	$(VENV_PYTHON) -m pip install --upgrade pip

install: $(VENV_PYTHON) ## Install Python dependencies in the project environment.
	@test -f "$(REQUIREMENTS)" || { \
		echo "Error: requirements file not found: $(REQUIREMENTS)" >&2; exit 2; }
	$(VENV_PYTHON) -m pip install -r "$(REQUIREMENTS)"

upgrade: $(VENV_PYTHON) ## Upgrade packages allowed by the requirements file.
	@test -f "$(REQUIREMENTS)" || { \
		echo "Error: requirements file not found: $(REQUIREMENTS)" >&2; exit 2; }
	$(VENV_PYTHON) -m pip install --upgrade -r "$(REQUIREMENTS)"

req: $(VENV_PYTHON) ## Freeze the selected environment into requirements.txt.
	@if "$(VENV_PYTHON)" -c 'import pip' >/dev/null 2>&1; then \
		"$(VENV_PYTHON)" -m pip freeze > "$(REQUIREMENTS)"; \
	elif grep -q '^uv = ' "$(VENV)/pyvenv.cfg" 2>/dev/null && \
		command -v uv >/dev/null 2>&1; then \
		uv pip freeze --python "$(VENV_PYTHON)" > "$(REQUIREMENTS)"; \
	else \
		echo "Error: pip is unavailable in this environment." >&2; \
		echo "Install pip or use uv for an environment created by uv." >&2; exit 2; \
	fi

packages: $(VENV_PYTHON) ## Print the installed Python package versions.
	$(VENV_PYTHON) -m pip freeze

publish: check-tools ## Publish interactively to GitHub Pages.
	$(QUARTO) publish gh-pages $(QUARTO_ARGS)

clean-output: ## Remove the rendered book.
	rm -rf -- _book

clean-cache: ## Remove Quarto caches and frozen computations.
	rm -rf -- .quarto _freeze

clean: clean-output clean-cache ## Remove all generated Quarto files.
