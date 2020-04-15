#!/bin/bash

# get string of timestamp
get_timestamp() {
    local stamp=$(date +%Y/%m/%d/%H:%M:%S:%6N)
    echo $stamp
}

CONFIG_ROOT="config.json"

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

# main process
check_config

# Finally Run python code
start_timestamp=`get_timestamp`
echo "[$start_timestamp] starting process..."
python harmoaiserver.py $CONFIG_ROOT