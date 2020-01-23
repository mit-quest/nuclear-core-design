FROM ubuntu:18.04

WORKDIR /home/nuclear-core-design
COPY . .
RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils
RUN scripts/docker_setup.sh
