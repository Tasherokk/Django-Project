api:
	python3 manage.py runserver

run_linters:
	isort . && \
    black . && \
	bandit . && \
	mypy . --check-untyped-defs --ignore-missing-imports && \
	flake8 . --max-line-length=99 --exclude=.venv,venv
