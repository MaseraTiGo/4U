#!/bin/bash


reverse(){
	local current_array
	current_array=(` echo "$@" `)
	max_index=`expr ${#current_array[@]} - 1`

	reverse_array=()
	for((i=0;i<=${max_index};i++));
	do
		result_index=`expr ${max_index} - ${i}`
		reverse_array[$i]=${current_array[${result_index}]}
	done
	echo ${reverse_array[@]}
}

