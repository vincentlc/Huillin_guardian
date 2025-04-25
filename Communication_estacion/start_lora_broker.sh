#!/bin/bash
user="estacion" # if user on the board is different please change the line
cd /home/$user/lora_project/ 
source .venv/bin/activate
python3 read_lora_send_mqtt.py