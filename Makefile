# Makefile

.PHONY: venv activate install db run all

venv:
	python -m venv .venv

activate:
	. .venv/bin/activate

install: venv
	. .venv/bin/activate && pip install -r requirements.txt

db:
	. .venv/bin/activate && python ./src/populate.py

run:
	. .venv/bin/activate && python ./src/main.py

setup: venv activate install

run: db run
