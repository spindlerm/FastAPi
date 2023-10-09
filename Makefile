format:
	black .
lint:
	pylint  app/ --disable=E Makefile
run:
	 uvicorn app.main:app --reload

test:
	pytest



all: format lint run