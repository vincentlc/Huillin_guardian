# Author: Vincent le costaouec
# Code inspired in work of Renzo Mischianti (www.mischianti.org)

# Description:
# This script read messages from the node-red that send it on a MQTT channel
# And send the data read to lora 
#
# Note: This code was written and tested using RaspberryPi.
#       when use double check that you are using the correct UART and pins.

import serial
import time

from lora_e22 import LoRaE22, Configuration
from lora_e22_constants import RssiAmbientNoiseEnable, RssiEnableByte
from lora_e22_operation_constant import ResponseStatusCode

import paho.mqtt.client as mqtt
import logging
import RPi.GPIO as GPIO

file="huillin_read_mqtt_send_lora"
#innit logger
log = logging.getLogger(file)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename=file+".log",
    encoding="utf-8",
    filemode="a"
)

GPIO.setwarnings(False) #de activate the GPIO warning to avoir the waring of re-use of port

# Initialize the LoRaE22 module
loraSerial = serial.Serial('/dev/ttyS0') #, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
lora = LoRaE22('400T22D', loraSerial, m0_pin=23, m1_pin=24)
code = lora.begin()
log.info("Initialization: {}"+ResponseStatusCode.get_description(code))

client_ID = "400T22D" #id of the mqtt

# Set the configuration to default values and print the updated configuration to the console
# Not needed if already configured
configuration_to_set = Configuration('400T22D')
# To enable RSSI, you must also enable RSSI on receiver
configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED
code, confSetted = lora.set_configuration(configuration_to_set)
log.info("Set configuration: {}"+str(ResponseStatusCode.get_description(code)))

def on_connect(client, userdata, flags, rc, properties):
  log.info("Connected with result code " + str(rc))
  if rc == 0 : #mean success
    client.subscribe("huillin/data")
  
def on_message(client, userdata, msg):
  log.info(msg.topic + " " + str(msg.payload))
  log.info(len(msg.payload.decode('utf-8')))                                                              
  code = lora.send_transparent_dict(msg.payload.decode('utf-8'))
  log.info("Send message: {}"+ResponseStatusCode.get_description(code))

try:
    # connect client to MQTT
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("10.3.141.1", 1883, 60)

    client.loop_forever()
    
except KeyboardInterrupt:
    # Manejar interrupción de teclado
    log.info("Interrupción de teclado detectada. Cerrando conexión.")
    client.disconnect()
except Exception as e: 
    log.error("hubo un error: "+str(e))
