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
  rsync \
  screen

# Set the Kubernetes version as found in the UCP Dashboard or API
k8sversion=v1.14.10-gke.27

# Get the kubectl binary.
curl -LO https://storage.googleapis.com/kubernetes-release/release/$k8sversion/bin/linux/amd64/kubectl

# Make the kubectl binary executable.
chmod +x ./kubectl

# Move the kubectl executable to /usr/local/bin.
mv ./kubectl /usr/local/bin/kubectl


python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
cd /home/nuclear-core-design && make setup_no_tensorflow
