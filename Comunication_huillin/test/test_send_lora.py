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
    #filename=file+".log",
    encoding="utf-8",
    #filemode="a"
)

GPIO.setwarnings(False) #de activate the GPIO warning to avoir the waring of re-use of port

# Initialize the LoRaE22 module
loraSerial = serial.Serial('/dev/ttyS0') #, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
lora = LoRaE22('400T22D', loraSerial, m0_pin=23, m1_pin=24)
code = lora.begin()
log.info("Initialization: {}"+ResponseStatusCode.get_description(code))
  
def send_message(iterator):
    msg_decode={"ts":1000000000000+iterator,"la":-40.000000,"lo":-72.99999999,"ph":7.33,"ec":3.66,"od":7.00,"sa":88.88,"tp":"28.09","sp":0.210,"e1":13000,"e2":0,"e3":1200,"e4":0,"ue":13000,"up":"start","p4":4.00,"p7":7.00}
    code = lora.send_transparent_dict(msg_decode) 
    log.info(",len="+str(len(msg_decode))+  " " + str(msg_decode)) 
    log.info("Send message: "+ResponseStatusCode.get_description(code))
    
try:
    iterator = 0; 
    while 1:
        send_message(iterator);
        time.sleep(5)
        iterator+=1;
    
except KeyboardInterrupt:
    # Manejar interrupción de teclado
    log.info("Interrupción de teclado detectada. Cerrando conexión.")
    client.disconnect()
except Exception as e: 
    log.error("hubo un error: "+str(e))
