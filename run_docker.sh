#!/usr/bin/env bash
sudo docker stop $(sudo docker ps -aq)
sudo docker rm $(sudo docker ps -aq)
sudo docker run -d -p 5000:5000 registry.gitlab.com/asiabots/wilson/cantonese-nlp