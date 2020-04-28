# FROM nvcr.io/nvidia/tensorflow:19.12-tf2-py3
FROM rayproject/autoscaler

WORKDIR /home/nuclear-core-design
COPY . .
RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils
RUN DEBIAN_FRONTEND=noninteractive scripts/docker_setup.sh
