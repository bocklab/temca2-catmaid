#!/bin/bash

git clone https://github.com/catmaid/catmaid-docker.git
wget -O temca2/v14.sql https://www.dropbox.com/s/n981husya0mdswo/v14.sql?dl=0
wget -O /tmp/level_8.tar https://www.dropbox.com/s/14ryl0ln5qvxjxm/level_8.tar?dl=1
tar -xf /tmp/level_8.tar -C pyramid_top/v14_align_tps
wget -O /tmp/level_7.tar https://www.dropbox.com/s/41x48a3fjswzphm/level_7.tar?dl=0
tar -xf /tmp/level_7.tar -C pyramid_top/v14_align_tps

docker pull catmaid/catmaid:latest
docker-compose -f catmaid-docker/docker-compose.yml -f temca2_catmaid_docker.yml build
