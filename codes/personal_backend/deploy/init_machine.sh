sudo apt-get update

sudo apt-get remove docker docker-engine docker.io
sudo apt install docker.io

sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo docker-compose --version

sudo apt-get install vim
sudo apt-get install git

sudo mkdir -p /data/
sudo chmod -R 777 /data/

sudo mkdir -p /deploy/
sudo chmod -R 777 /deploy/

sudo mkdir -p /project/
sudo chmod -R 777 /project/
