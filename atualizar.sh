#!/bin/sh
cd /volume1/docker/megasena || exit 1
sudo docker compose down
sudo docker compose up -d --build
sudo docker ps | grep mega-flask
