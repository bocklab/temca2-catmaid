#!/bin/bash

git clone https://github.com/catmaid/catmaid-docker.git
wget -O temca2/v14.sql https://www.temca2data.org/install/v14/v14.sql
wget -O /tmp/level_8.tar https://www.temca2data.org/install/v14/level_8.tar
tar -xf /tmp/level_8.tar -C pyramid_top/v14_align_tps
wget -O /tmp/level_7.tar https://www.temca2data.org/install/v14/level_7.tar
tar -xf /tmp/level_7.tar -C pyramid_top/v14_align_tps

docker-compose -f catmaid-docker/docker-compose.yml -f temca2_catmaid_docker.yml build
