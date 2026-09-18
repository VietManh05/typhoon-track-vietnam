PYTHON ?= python

.PHONY: setup clean-data train serve test lint format hooks dvc-init mlflow-ui

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[api,dev,experiment]"
	$(PYTHON) -m pre_commit install

clean-data:
	$(PYTHON) -m typhoon_vn.cli clean-data

train:
	$(PYTHON) -m typhoon_vn.cli train

serve:
	$(PYTHON) -m uvicorn typhoon_vn.api.app:app --reload

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m flake8 src tests
	$(PYTHON) -m isort --check-only src tests
	$(PYTHON) -m black --check src tests

format:
	$(PYTHON) -m isort src tests
	$(PYTHON) -m black src tests

hooks:
	$(PYTHON) -m pre_commit run --all-files

dvc-init:
	$(PYTHON) -m dvc init

mlflow-ui:
	$(PYTHON) -m mlflow ui --backend-store-uri ./mlruns
