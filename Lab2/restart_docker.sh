#!/bin/sh
# This is a comment!
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker volume rm $(docker volume ls -q)
sudo rm -rf config
sudo rm -rf database
