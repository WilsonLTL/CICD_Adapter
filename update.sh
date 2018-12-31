#!/usr/bin/env bash
sudo docker login -u wilsonloltl -p Vi26151851@
sudo docker pull wilsonloltl/docker_cicd_testing:cicd-demo
sudo docker stop $(sudo docker ps -aq)
sudo docker rm $(sudo docker ps -aq)
sudo docker run -d -p 5000:5000 wilsonloltl/docker_cicd_testing:cicd-demo