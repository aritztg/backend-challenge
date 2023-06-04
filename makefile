run:
	python app/backend.py

test:
	python -m unittest discover app

lint:
	ruff check app
	isort app --check-only
	pylint app