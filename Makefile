install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

lint:
	pylint --disable=R,C *.py &&\
	pylint --disable=R,C dp_app/*.py &&\
	pylint --disable=R,C dp_app/tests/*.py
	# pylint --disable=R,C dp_app.py

test:
	# python -m pytest -vv --cov=dp_app_core dp_app/tests/test_dp_app_core.py

format:
	black *.py &&\
	black dp_app/*.py &&\
	black dp_app/tests/*.py

all:
	install lint format test
	