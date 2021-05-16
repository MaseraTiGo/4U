#!/bin/bash

source ./utils/base_tools.sh
source ./utils/array_tools.sh


# initialize flag parameters
if [ "$1" = "online" ]; then
	flag="online"
	log "environment" "to initialize online environment parameters."
	source ./conf/project_online_env.sh
elif [ "$1" = "test" ]; then
	flag="test"
	log "environment" "to initialize test environment parameters."
	source ./conf/project_test_env.sh
elif [ "$1" = "reddeer" ]; then
	flag="reddeer"
	log "environment" "to initialize reddeer environment parameters."
	source ./conf/project_reddeer_env.sh
else
	flag="local"
	log "environment" "to initialize test environment parameters."
	source ./conf/project_local_env.sh
fi

# network
sys_network="oc_net"
