#!/bin/bash

source ./deploy_project.sh


log "server" "to start project is starting ..."
if [ -e ${deploydir} ]
then
	start_services=(`echo ${server_names[@]}`)
	start_paths=(`echo ${server_paths[@]}`)

	server_len=${#start_services[@]} 
	for((i=0;i<${server_len};i++))
	do
		cd ${deploydir}${start_paths[i]}
		sudo docker-compose -f ${docker_compose_file} up -d
	done
else
	log "server" " ${deploydir} is not existed, to deploy is failed!"
fi
log "server" "to start project have finished ..."



if [ "${flag}" = "test" ]; then
    # update project
    sudo cp -rf ${deploydir}/balance/nginx/cdn/* ${datadir}/balance/nginx/cdn/
    
    # sync table struct
    # docker exec -it web /bin/bash -c "python3 manage.py migrate"
    
    # exec to auto transfer data script
    
    
elif [ "${flag}" = "agent" ]; then
    sudo cp -rf ${deploydir}/balance/nginx/cdn/* ${datadir}/balance/nginx/cdn/
fi
