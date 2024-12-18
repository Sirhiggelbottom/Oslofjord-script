#!/bin/bash

check_if_running(){
	
	local script_name=$1
	if pgrep -f $script_name > /dev/null
	then
		echo "$script_name is already running"
		return 1
	else
		return 0
	fi
}

script_dir="$(dirname "$0")"

script1="Temperatur_varsel.py"
check_if_running $script1
if [ $? -eq 0 ]; then
	/usr/bin/python3 "$script_dir/$script1" &
	echo "Started $script1."
fi

script2="Sjekk_for_oppdateringer.py"
check_if_running $script2
if [ $? -eq 0 ]; then
	/usr/bin/python3 "$script_dir"/$script2 & 
	echo "Started $script2."
fi

script3="start_backend.py"
check_if_running $script3
if [ $? -eq 0 ]; then
	/usr/bin/python3 "$script_dir"/$script3 & 
	echo "Started $script3."
fi

script4="start_host.py"
check_if_running $script4
if [ $? -eq 0 ]; then
	/usr/bin/python3 "$script_dir"/$script4 & 
	echo "Started $script4."
fi