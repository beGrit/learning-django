#!/usr/bin/fish

systemctl start docker
docker start mariadb
docker start redis-chat

