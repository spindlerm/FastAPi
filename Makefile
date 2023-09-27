format:
	black .
lint:
	pylint  app/ --disable=E Makefile
run:
	 uvicorn app.main:app --reload


all: format lint run