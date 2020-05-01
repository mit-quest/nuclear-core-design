sudo apt-get update -qq
sudo apt-get install -y -qq build-essential
sudo apt-get install -y -qq cmake \
	git \
	python3-setuptools \
	python3-dev \
	python3-pip \
	htop \
	tmux \
	tree \
  s3fs \
  vim \
  zip \
  unzip \

#install nvidia drivers
sudo add-apt-repository -y ppa:graphics-drivers
sudo apt-get update -qq
sudo apt-get install -y -qq nvidia-driver-440

#add nvidia package repositories
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-repo-ubuntu1804_10.0.130-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1804_10.0.130-1_amd64.deb
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
sudo apt-get update -qq
wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
sudo apt install -qq ./nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
sudo apt-get update -qq

# install cuda and cuDNN
sudo apt-get install -y -qq --no-install-recommends \
    cuda-10-0 \
    libcudnn7=7.6.2.24-1+cuda10.0  \
    libcudnn7-dev=7.6.2.24-1+cuda10.0

# install TensorRT
sudo apt-get install -y -qq --no-install-recommends libnvinfer5=5.1.5-1+cuda10.0 \
    libnvinfer-dev=5.1.5-1+cuda10.0

export PATH=/usr/local/cuda-10.0/bin${PATH:+:${PATH}}
rm *.deb

#install docker
sudo apt-get install -y -qq \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update -qq
sudo apt-get install -y -qq docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER

#install nvidia container toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update -qq && sudo apt-get install -y -qq nvidia-container-toolkit
sudo systemctl restart docker

#install python packages
python3 -m pip install -q --upgrade pip
sudo python3 -m pip install -q virtualenv
# cd ~/nuclear-core-design && make setup_no_tensorflow
cd ~/nuclear-core-design && make
