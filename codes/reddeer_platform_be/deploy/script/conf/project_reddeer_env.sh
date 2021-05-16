#!/bin/bash


# base directory parameters
currentdir=${PWD}
confdir=${currentdir}/../
codedir=${confdir}/../

# deployment directory
deploydir=/deploy


# data directory
datadir=/data

volume_dir=/data/application/web/pycodes

# database to backup of path
backup_dir=/data/databases/mysql-master/backup


# docker
docker_compose_file=reddeer_production.yml
docker_backup_dir=/var/lib/backup


# invalide project files
invalide_files=(
    "${deploydir}/application/web/tuoen/settings_local.py" 
    "${deploydir}/application/web/tuoen/settings_local.pyc"
)

# services config
server_names=('mysql' 'redis' 'web' 'nginx')
server_paths=('/database/mysql' '/cache/redis' '/application/web' '/balance/nginx')

