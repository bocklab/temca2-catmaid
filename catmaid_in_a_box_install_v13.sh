#!/bin/bash

git clone https://github.com/catmaid/catmaid-docker.git
wget -O temca2/v13.sql https://www.dropbox.com/s/0c7q8gafqywct5u/v13.sql?dl=1
wget -O /tmp/level_8.tar https://www.dropbox.com/s/qfhxoxfu9ib0cug/level_8.tar?dl=1
tar -xf /tmp/level_8.tar -C pyramid_top
wget -O /tmp/level_7.tar https://www.dropbox.com/s/2s2r7imvjwtkhy2/level_7.tar?dl=1
tar -xf /tmp/level_7.tar -C pyramid_top

git clone https://www.github.com/catmaid/catmaid-docker
docker-compose -f catmaid-docker/docker-compose.yml -f temca2_catmaid_docker.yml build
