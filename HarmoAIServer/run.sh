#!/bin/bash

#values
CONFIG_ROOT="config.json"

# get string of timestamp
get_timestamp() {
    local stamp=$(date +%Y/%m/%d/%H:%M:%S:%6N)
    echo $stamp
}

# ConfigFile Check
check_config() {
    if [ -f $CONFIG_ROOT ]; then
        local timestamp=`get_timestamp`
        echo "[$timestamp] check config file: $CONFIG_ROOT"
    else
        echo "config file: $CONFIG_ROOT is not exist"
        exit 1
    fi
}

# test redis server

# main process
check_config

# Finally Run python code
start_timestamp=`get_timestamp`
echo "[$start_timestamp] starting process..."
python harmoaiserver.py $CONFIG_ROOT &