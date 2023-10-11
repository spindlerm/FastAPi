format:
	black .
lint:
	pylint  app/ 
run:
	 uvicorn app.main:app --reload

test:
	pytest



all: format lint run