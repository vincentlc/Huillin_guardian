python -m venv .
source bin/activate
python3 -m pip install ebyte-lora-e22-rpi pyserial RPI.GPIO
sudo apt-get install -y python3-rpi.gpio

sudo raspi-config #configure the serial to be enabled

#install node red
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
#enable node-red at boot
sudo systemctl enable nodered.service

sudo systemctl start nodered

sudo systemctl status nodered

#install mosquito for MQTT:
sudo apt install mosquitto mosquitto-clients