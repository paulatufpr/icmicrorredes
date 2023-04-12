#!/bin/bash

echo "instalando dependencias do linux(ubuntu)
sudo apt install can-utils -y
sudo apt install modprobe -y

echo "dependencias python" 
sudo pip install python-can 

echo "ligando interface CAN FISICA" 
sudo modprobe can0
sudo ip link add dev can0 type can bitrate 500000
sudo ip link set up can0
