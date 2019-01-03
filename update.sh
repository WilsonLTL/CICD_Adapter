#!/usr/bin/env bash
docker login registry.gitlab.com -u wilsonlo1997@gmail.com -p Vi26151851@
sudo docker pull registry.gitlab.com/asiabots/wilson/cantonese-nlp
sudo docker stop $(sudo docker ps -aq)
sudo docker rm $(sudo docker ps -aq)
sudo docker run -d -p 5000:5000 registry.gitlab.com/asiabots/wilson/cantonese-nlp


