export APP := 3.5.1-delta-4.0.0rc1-hadoop-3-java-17-scala-2.13-python-3.9
export TAG := 0.0.1
export DOCKER_FILE_PATH := tools/docker
export CONTEXT := .
export DOCKER_BUILD := buildx build

setup-environment: clean-environment install-environment install-linter

.PHONY: build-container-image
build-container-image:
	docker $(DOCKER_BUILD) -t $(APP):$(TAG) -f $(DOCKER_FILE_PATH)/Dockerfile $(CONTEXT)

.PHONY: clean-environment
clean-environment:
	rm -rf build dist .eggs *.egg-info
	rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	find . -type d -name '.mypy_cache' -exec rm -rf {} +
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	find . -type f -name "*.py[co]" -exec rm -rf {} +

.PHONY: install-environment
install-environment:
	poetry env use 3.9
	poetry install --no-root

.PHONY: info-environment
info-environment:
	poetry env info
	poetry show --tree

.PHONY: update-environment
update-environment:
	poetry update

.PHONY: install-linter
install-linter:
	poetry run pre-commit clean
	poetry run pre-commit install

.PHONY: run-shell
run-shell:
	pyspark --packages $(PACKAGES)

.PHONY: poetry-path
poetry-path:
	@echo $(shell eval poetry show -v 2> /dev/null | head -n1 | cut -d ' ' -f 3)

.PHONY: linter
linter:
	poetry run pre-commit run --all-files
