#!/bin/bash

source ./project_env.sh


log "server" "to stop project is starting ..."
if [ -e ${deploydir} ]
then
	stop_services=(`reverse ${server_names[@]}`)
	stop_paths=(`reverse ${server_paths[@]}`)

	server_len=${#stop_services[@]} 
	for((i=0;i<${server_len};i++))
	do
		cd ${deploydir}${stop_paths[i]}
		sudo docker-compose -f ${docker_compose_file} down
	done
else
	log "server" "${deploydir} is not existed, it is not need to stop."
fi
log "server" "to stop project have finished ..."
