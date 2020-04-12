.PHONY: help prepare-dev install run run-production

# if a .env file exists load it
# otherwise we are in the CI server variables are already set
-include .env

# directory to store virtual environment
VENV_NAME=venv

# python runtime version
PYTHON_VER=3.7

# python executble
PYTHON=${VENV_NAME}/bin/python${PYTHON_VER}

# gunicorn executable
GUNICORN=$(VENV_NAME)/bin/gunicorn

# pip requirements file
REQUIREMENTS=requirements.txt

help:			## Shows this message.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

prepare-dev:		## Install required debian packages.
	sudo apt-get -y install python${PYTHON_VER} python3-pip
	python3 -m pip install virtualenv
	make venv

venv:			## Recreates the virtual environment if needed.
venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: ${REQUIREMENTS}
	test -d $(VENV_NAME) || virtualenv -p python${PYTHON_VER} $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -r ${REQUIREMENTS}
	touch $@

run:			## Runs local API in development environment.
run: kill venv run-wsgi

run-production:		## Runs local API server.
run-production: kill venv run-wsgi-gunicorn

coverage:		## Runs local API server.
coverage: venv
	coverage run --source=src -m unittest -v
	coverage report --show-missing

run-wsgi:
	${PYTHON} wsgi.py & echo $$! > wsgi.pid

run-wsgi-gunicorn:
	$(GUNICORN) wsgi:app --log-file=- & echo $$! > wsgi.prod.pid

kill:			## Stop running server process
	-kill $(shell cat wsgi.pid) > /dev/null 2>&1; \
	-kill $(shell cat wsgi.prod.pid) > /dev/null 2>&1;

test:			## Runs the test suite.
test: venv
	$(PYTHON) -m pytest tests
