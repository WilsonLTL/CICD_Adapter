#!/usr/bin/env bash
sudo apt-get update -qy
sudo apt install python-pip -qy
sudo apt install docker.io -qy
#sudo apt install nodejs npm -qy
#sudo apt install npm -qy
sudo pip install -r requirements.txt
