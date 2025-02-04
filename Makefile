install: requirements.txt
	pip install --upgrade pip &&\
	pip install -r requirements.txt

setup: 
	# python setup.py install
	pip install . 

lint:
	pylint --disable=R,C *.py &&\
	pylint --disable=R,C dp_app/*.py &&\
	pylint --disable=R,C dp_app/tests/*.py

test:
	# python -m pytest -vv --cov=dp_app dp_app/tests

format:
	black *.py &&\
	black dp_app/*.py &&\
	black dp_app/tests/*.py

all: install setup lint format test
