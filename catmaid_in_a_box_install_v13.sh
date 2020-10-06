#!/bin/bash

git clone https://github.com/catmaid/catmaid-docker.git
wget -O https://www.temca2data.org/install/v13/v13.sql
wget -O https://www.temca2data.org/install/v13/level_8.tar
tar -xf /tmp/level_8.tar -C pyramid_top
wget -O https://www.temca2data.org/install/v13/level_7.tar
tar -xf /tmp/level_7.tar -C pyramid_top

docker-compose -f catmaid-docker/docker-compose.yml -f temca2_catmaid_docker.yml build
