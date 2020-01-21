sudo apt-get update
sudo apt-get install -y build-essential

#install nvidia drivers
sudo add-apt-repository -y ppa:graphics-drivers
sudo apt-get update
sudo apt-get install -y nvidia-driver-440

#add nvidia package repositories
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-repo-ubuntu1804_10.0.130-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1804_10.0.130-1_amd64.deb
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
sudo apt-get update
wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
sudo apt install ./nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
sudo apt-get update

# install cuda and cuDNN
sudo apt-get install -y --no-install-recommends \
    cuda-10-0 \
    libcudnn7=7.6.2.24-1+cuda10.0  \
    libcudnn7-dev=7.6.2.24-1+cuda10.0

# install TensorRT
sudo apt-get install -y --no-install-recommends libnvinfer5=5.1.5-1+cuda10.0 \
    libnvinfer-dev=5.1.5-1+cuda10.0

export PATH=/usr/local/cuda-10.0/bin${PATH:+:${PATH}}

sudo apt-get install -y cmake \
	git \
	python3-setuptools \
	python3-dev \
	python3-pip \
	htop \
	tmux \
	tree \
  s3fs \

python3 -m pip install --upgrade pip
sudo python3 -m pip install virtualenv
cd ~/nuclear-core-design && make
