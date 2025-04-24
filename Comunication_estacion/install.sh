#!/bin/bash

user_install="estacion" # change if the name of the user is different
folder_project="/home/$user_install/lora_project/"
##### creating work folder if needed
if [ ! -d  $folder_project ]; then
	mkdir $folder_project
fi

##### copying execution file
echo "copying file"
cp ./read_lora_send_mqtt.py $folder_project
cp ./start_lora_broker.sh $folder_project

##### giving execution acces
echo "giving execution acces"
chmod +x $folder_project/start_lora_broker.sh

##### creating virtual environement if needed
if [ ! -d  $folder_project.venv ]; then
	echo "creating virtual environement"
	python3 -m venv $folder_project.venv
fi

##### activate the python virtual environement
echo "activate the python virtual environement"
source $folder_project.venv/bin/activate

##### install wheels
if [[ ! $(python3 -m pip list|grep "ebyte-lora-e22-rpi") ]]; then
	echo "install wheels"
	wget -q --tries=10 --timeout=20 --spider http://google.com  # check if the pi is connected to internet
	if [[ $? -eq 0 ]]; then
		echo "Online"
		python3 -m pip install -r requirements.txt
	else
		echo "Offline installation"
		python3 -m pip install wheels/*
	fi
    
fi

pkgs='mosquitto'
if [ ! dpkg -s $pkgs >/dev/null 2>&1 ]; then
  sudo dpkg -i packages/mosquitto_2.0.11-1.2+deb12u1_arm64.deb
fi

##### add execution of script at start
echo "add execution of script at start"
sudo cp lora_broker.service /etc/systemd/system/lora_broker.service
sudo chmod 744 $folder_project/start_lora_broker.sh
sudo chmod 664 /etc/systemd/system/lora_broker.service

##### enable service
echo "enable service"
sudo systemctl daemon-reload
sudo systemctl enable mosquitto.service
sudo systemctl enable lora_broker.service

##### config mosquitto
valid_config=$(cat /etc/mosquitto/mosquitto.conf | grep -c "listener 1883")
if [ $valid_config -lt 1 ]; then
	echo "config mosquitto"
	sudo chmod +w /etc/mosquitto/mosquitto.conf 
	echo "listener 1883" | sudo tee --append /etc/mosquitto/mosquitto.conf 
	echo "allow_anonymous true" | sudo tee --append /etc/mosquitto/mosquitto.conf 
	sudo systemctl restart mosquitto
fi


##### install node-red:

if [[ ! -x "$(command -v node-red)" ]]; then
	sudo apt-get update
	sudo apt-get install -y build-essential
	sudo apt-get install npm
	
	npm install -g --unsafe-perm node-red
	cp Node-red-flow/flows_estacion.json /home/$user_install/.node-red/flows.json
fi


##### install docker:
if [[ ! -x "$(command -v docker)" ]]; then
	curl -sSL https://get.docker.com | sh
	sudo usermod -aG docker $USER
fi

##### config world map off line: 
cd Map_image #caroeta donde hay archivo
docker run --name maptiler -d -v $(pwd):/data -p 1884:8080 maptiler/tileserver-gl --restart=always -p 8080 --mbtiles osm-2020-02-10-v3.11_south-america_chile.mbtiles
docker start maptiler



