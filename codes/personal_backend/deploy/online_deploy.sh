#!/bin/bash

sudo mkdir -p /data
sudo docker-compose -f /deploy/production.yml down
sudo docker rmi deploy_web
sudo rm -rf /deploy/**
sudo rm -rf /project/crm-be/tuoen/settings_local.py
sudo rm -rf /project/crm-be/tuoen/settings_local.pyc
sudo cp -rf /project/crm-be/deploy/** /deploy/
sudo cp -rf /project/crm-be/** /deploy/web/
sudo docker-compose -f /deploy/production.yml up -d

sudo chmod -R 777 /data
sudo chmod -R 777 /deploy/nginx/

# 停止10s保证mysql服务启动起来
sleep 10s
