#!/bin/bash
# Authors: David Hu, Jean Martial Mari & Chat GPT
# Date: 2023-12

# Exit on error
set -e 

# Predefined options
PRODUCT_TYPE="LD06"
COMM_MODE="serial"
PORT_PATH="/dev/ttyUSB0"
SERVER_IP_ADDR="None"
SERVER_PORT_ADDR="0"

# Check if a filename parameter is passed
if [ -z "$1" ]
then
  echo "No filename provided. Output will be displayed on stdout."
  USE_STDOUT=true
else
  FILENAME=$1
  LOG_NAME="${FILENAME}" #_`date +%Y%m%d-%H-%M`.log"
  echo "Saving to File: $LOG_NAME"
  USE_STDOUT=false
fi

echo "Starting with the following settings:"
echo "  Product Type: $PRODUCT_TYPE"
echo "  Communication Mode: $COMM_MODE"
echo "  Port Path: $PORT_PATH"
echo "  Server IP: $SERVER_IP_ADDR"
echo "  Server Port: $SERVER_PORT_ADDR"

execute_command() {
  if [ $COMM_MODE == "network" ]
  then
    echo "Start network execution"
    ./ldlidar_stl_sdk/build/ldlidar_stl_node ${PRODUCT_TYPE} networkcom_tcpclient ${SERVER_IP_ADDR} ${SERVER_PORT_ADDR}
  elif [ $COMM_MODE == "serial" ]
  then
    sudo chmod 777 ${PORT_PATH}
    echo "Start serial execution"
    ./ldlidar_stl_sdk/build/ldlidar_stl_node ${PRODUCT_TYPE} serialcom ${PORT_PATH}
  else
    echo "Input [communication_mode] is error."
    exit 1
  fi
}

if [ "$USE_STDOUT" = true ]; then
  execute_command
else
  execute_command > ${LOG_NAME}
fi
