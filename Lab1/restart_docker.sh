#! /bin/bash
docker container stop $(docker ps -q)
docker container rm $(docker ps -aq)
docker run -dit -p 2345:1234 -p 1234:22 --privileged rastasheep/ubuntu-sshd /usr/sbin/sshd -D -E /var/log/sshd
