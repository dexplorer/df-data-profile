install: pyproject.toml
	pip install --upgrade pip &&\
	pip install --editable . &&\
	pip install --editable .[cli] &&\
	pip install --editable .[api] &&\
	pip install --editable .[test]

	python -m spacy download en_core_web_sm
	
lint:
	pylint --disable=R,C src/dp_app/*.py &&\
	pylint --disable=R,C tests/*.py

test:
	python -m pytest -vv --cov=src/dp_app tests

format:
	black src/dp_app/*.py &&\
	black tests/*.py

all:
	install lint format test