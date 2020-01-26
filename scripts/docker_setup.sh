apt-get update
apt-get install -y build-essential

apt-get install -y cmake \
	git \
	python3-setuptools \
	python3-dev \
	python3-pip \
	htop \
	tmux \
	tree \
  vim \
  s3fs \

python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
cd /home/nuclear-core-design && make setup_no_tensorflow
