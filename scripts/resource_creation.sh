sudo apt-get -y update
sudo apt-get -y install build-essential
sudo apt-get -y install python3-pip
python3 -m pip install --upgrade pip
sudo python3 -m pip install virtualenv
cd ~/nuclear-core-design && make
