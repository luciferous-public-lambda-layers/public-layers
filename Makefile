SHELL = /usr/bin/env bash -xeuo pipefail

codes:=app.py public_layers/

format: \
	fmt-isort \
	fmt-black

fmt-isort:
	poetry run isort ${codes}

fmt-black:
	poetry run black ${codes}

lint: \
	lint-isort \
	lint-black \
	lint-flake8

lint-isort:
	poetry run isort --check ${codes}

lint-black:
	poetry run black --check ${codes}

lint-flake8:
	poetry run flake8 ${codes}

generate-install-scripts:
	poetry run generate-install-scripts

.PHONY: \
	message \
	fmt-isort \
	fmt-black \
	lint \
	lint-isort \
	lint-black \
	lint-flake8 \
	generate-install-scripts
