###########################################################################
# Command Variables
#
# These are usually not overridden by users but can be.
#
PYTHON ?= python3.6
PIP ?= pip3.6

###########################################################################
# Virtual Environment Locations
#
# Should not really be changed
#
VENV_LOCATION_BASENAME := .venv/
VENV_LOCATION := $(shell realpath ${VENV_LOCATION_BASENAME})
VENV_PYTHON := ${VENV_LOCATION}/bin/python
VENV_PIP := ${VENV_LOCATION}/bin/pip

###########################################################################
# Virtual Environment Setup
#
.DEFAULT_GOAL := setup

setup:
	@echo ${VENV_LOCATION}
	@virtualenv --always-copy --python=${PYTHON} ${VENV_LOCATION}
	${VENV_PIP} install -U https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-0.9.0.dev0-cp36-cp36m-manylinux1_x86_64.whl
	${VENV_PIP} install -r requirements.txt

clean:
	rm -rf .venv/
