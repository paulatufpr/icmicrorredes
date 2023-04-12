#!/bin/bash

echo "instalando dependencias do linux(ubuntu)"
sudo apt install can-utils -y
sudo apt install net-tools -y
echo "dependencias python" 
sudo pip install python-can 

echo "ligando interface CAN FISICA" 
sudo modprobe vcan0
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
echo "Checagem se a rede realmente está ligada"
ifconfig vcan0
