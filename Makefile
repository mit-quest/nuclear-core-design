###########################################################################
# Command Variables
#
# These are usually not overridden by users but can be.
#
PYTHON ?= python3.6
PIP ?= pip3.6
UID := $(shell id -u ${USER})

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

setup_no_tensorflow:
	@echo ${VENV_LOCATION}
	@virtualenv --always-copy --system-site-packages --python=${PYTHON} ${VENV_LOCATION}
	${VENV_PIP} install -q -U https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-0.9.0.dev0-cp36-cp36m-manylinux1_x86_64.whl
	${VENV_PIP} install -q -r requirements.txt

setup: setup_no_tensorflow
	${VENV_PIP} install -q -r tensorflow_requirements.txt

mount:
	@mkdir -p results
	@chmod 600 keys/gcs-auth.txt
	s3fs nuclearcoredesign_sandbox results/ -o umask=0007,uid=${UID} -o passwd_file=keys/gcs-auth.txt -o url=https://storage.googleapis.com -o sigv2 -o nomultipart

unmount:
	sudo umount results/

dockerGPUbuild:
	docker image build -t nuclear_gpu:1.0 .

dockerGPUrun:
	docker run --rm -it --shm-size=20G -p 0.0.0.0:6006:6006 --gpus all nuclear_gpu:1.0

clean:
	rm -rf .venv/
