#!/bin/bash

echo "instalando dependencias do linux(ubuntu)"
sudo apt install can-utils -y
sudo apt install net-tools
echo "dependencias python" 
sudo pip install python-can 

echo "ligando interface CAN FISICA" 
sudo ip link set can0 type can bitrate 500000
sudo ip link set up can0
echo "Checagem se a rede realmente está ligada"
ifconfig can0
