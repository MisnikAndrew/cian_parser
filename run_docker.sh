#!/bin/bash

sudo systemctl start docker
sudo docker build -t bot-image .
sudo docker run --rm  --name bot-container bot-image