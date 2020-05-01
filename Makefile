###########################################################################
# Command Variables
#
# These are usually not overridden by users but can be.
#
PYTHON ?= python3.6
PIP ?= pip3.6
UID := $(shell id -u ${USER})

###########################################################################
# Miscellaneous Variables
#
S3FS_PAASSWD_FILE := keys/gcs-auth.txt
GCP_BUCKET_NAME := nuclearcoredesign_sandbox
MOUNT_DIRECTORY := results/

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

unzip:
	@unzip -o bwr6x6env/scaled_objective_func.zip -d bwr6x6env/
	@unzip -o bwr6x6env/raw_objective_func.zip -d bwr6x6env/

setup_no_tensorflow: unzip
	@echo ${VENV_LOCATION}
	@virtualenv --always-copy --system-site-packages --python=${PYTHON} ${VENV_LOCATION}
	${VENV_PIP} install -q -U https://s3-us-west-2.amazonaws.com/ray-wheels/latest/ray-0.9.0.dev0-cp36-cp36m-manylinux1_x86_64.whl
	${VENV_PIP} install -q -r requirements.txt

setup: setup_no_tensorflow
	${VENV_PIP} install -q -r tensorflow_requirements.txt

mount:
	@mkdir -p ${MOUNT_DIRECTORY}
	@chmod 600 ${S3FS_PAASSWD_FILE}
	s3fs ${GCP_BUCKET_NAME} ${MOUNT_DIRECTORY} -o umask=0007,uid=${UID} -o passwd_file=${S3FS_PAASSWD_FILE} -o url=https://storage.googleapis.com -o sigv2 -o nomultipart

unmount:
	sudo umount ${MOUNT_DIRECTORY}

dockerGPUbuild:
	docker image build -t nuclear_gpu:1.0 .

dockerGPUrun:
	docker run --rm -it --shm-size=20G -p 0.0.0.0:6006:6006 --gpus all nuclear_gpu:1.0

clean:
	rm -rf .venv/
	rm -f bwr6x6env/raw_objective_func.p
	rm -f bwr6x6env/scaled_objective_func.p
