.PHONY: install run test build

install:
	pip install -r requirements.txt

run:
	uvicorn vellum_grid.api.main:app --host 0.0.0.0 --port 8000 --reload

test:
	pytest tests/test_engine.py

build:
	python setup.py sdist bdist_wheel
