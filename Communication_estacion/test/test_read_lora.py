# Author: Vincent le costaouec
# Code inspired in work of Renzo Mischianti (www.mischianti.org)

# Description:
# This script read messages from Lora Red and send it to the node-red through the MQTT channel

# Note: This code was written and tested using RaspberryPi.
#       when use double check that you are using the correct UART and pins.

import serial
import time
from datetime import datetime

from lora_e22 import LoRaE22, Configuration
from lora_e22_operation_constant import ResponseStatusCode
from lora_e22_constants import FixedTransmission, RssiEnableByte

import paho.mqtt.client as mqtt
import logging
import RPi.GPIO as GPIO

file="estacion_read_mqtt_send_lora"
#innit logger
log = logging.getLogger(file)
logging.basicConfig( #logging into a local file
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    #level=logging.INFO,
    level=logging.DEBUG,
    #filename=file+".log",
    encoding="utf-8",
    #filemode="a"
)

GPIO.setwarnings(False) #de activate the GPIO warning to avoir the waring of re-use of port

# Configuración del servidor MQTT
MQTT_BROKER = "127.0.0.1" # Direccion de broker MQTT
MQTT_TOPIC = 'huillin/data'  # Tema MQTT utilizado

# Initialize the LoRaE22 module
loraSerial = serial.Serial('/dev/ttyUSB0') #, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
lora = LoRaE22('400T22D', loraSerial, m0_pin=23, m1_pin=24)
code = lora.begin()
log.info("Initialization:"+ ResponseStatusCode.get_description(code))

list_received_data = []
list_received_time = []
list_received_valid = []
verif_dictionnary = {'la': -40.0, 'lo': -72.99999999, 'ph': 7.33, 'ec': 3.66, 'od': 7.0, 'sa': 88.88, 'tp': '28.09', 'sp': 0.21, 'e1': 13000, 'e2': 0, 'e3': 1200, 'e4': 0, 'ue': 13000, 'up': 'start', 'p4': 4.0, 'p7': 7.0}
try:
    log.info("Waiting for messages...")
    while True:
        if lora.available() > 0: #wait for lora to be available
            try:
                code, value, rssi = lora.receive_dict(rssi=True) # reading the data
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S") # H - hour, M- minute, S - second
                print("Current Time =", current_time)
                # print debug message
                log.debug('RSSI: '+ str(rssi) + " -" + str(ResponseStatusCode.get_description(code))) 
                #log.debug(value)
                reduce_value = value["ts"]-1000000000000
                if len(list_received_time) >1:
                    time_difference=(now-list_received_time[-1]).total_seconds()
                else:
                    time_difference=0
                value.pop("ts") #remove the ts from value
                if verif_dictionnary==value:
                    check_valid_dic = True
                else:
                    check_valid_dic = False
                
                log.debug("current_time="+str(current_time)+", diff="+str(time_difference)+ ", value=" +str(reduce_value)+ ", valid="+str(check_valid_dic))
                list_received_data.append(reduce_value)
                list_received_time.append(now)
                list_received_valid.append(check_valid_dic)
                #log.debug(list_received_data)
                #log.debug(list_received_time)
                #log.debug(list_received_valid)
                
                time.sleep(2) #sleep time required in order to not overload the lora module
            except UnicodeDecodeError as e:
                log.error("UnicodeDecodeError "+str(e))
            except Exception as e: 
                log.error("hubo un error: "+str(e))
except KeyboardInterrupt:
    # Manejar interrupción de teclado
    log.info("Interrupción de teclado detectada. Cerrando conexión.")
    log.debug(list_received_data)
    log.debug(list_received_time)
    log.debug(list_received_valid)
