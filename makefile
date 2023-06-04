run:
	python app/backend.py

tests:
	python -m unittest discover app

lint:
	ruff check app
	isort app --check-only
	pylint app