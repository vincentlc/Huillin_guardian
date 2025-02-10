# Author: Vincent le costaouec
# Code inspired in work of Renzo Mischianti (www.mischianti.org)

# Description:
# This script read messages from Lora Red and send it to the node-red through the MQTT channel

# Note: This code was written and tested using RaspberryPi.
#       when use double check that you are using the correct UART and pins.

import serial
import time

from lora_e22 import LoRaE22, Configuration
from lora_e22_operation_constant import ResponseStatusCode
from lora_e22_constants import FixedTransmission, RssiEnableByte

import paho.mqtt.client as mqtt
import logging
import RPi.GPIO as GPIO

file="estacion_read_mqtt_send_lora"
#innit logger
log = logging.getLogger(file)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    #level=logging.INFO,
    level=logging.DEBUG,
    #filename=file+".log",
    encoding="utf-8",
    #filemode="a"
)

GPIO.setwarnings(False) #de activate the GPIO warning to avoir the waring of re-use of port

# Configuración del servidor MQTT
MQTT_BROKER = "127.0.0.1" #'192.168.1.2'  # Cambia esto a la dirección de tu broker MQTT
MQTT_TOPIC = 'huillin/data'  # Cambia esto al tema MQTT que desees utilizar

# Initialize the LoRaE22 module
loraSerial = serial.Serial('/dev/ttyUSB0') #, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
lora = LoRaE22('400T22D', loraSerial, m0_pin=23, m1_pin=24)
code = lora.begin()
log.info("Initialization:"+ ResponseStatusCode.get_description(code))

# Set the configuration to default values and print the updated configuration to the console
# Not needed if already configured
configuration_to_set = Configuration('400T22D')
# To enable RSSI, you must also enable RSSI on sender
configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED

code, confSetted = lora.set_configuration(configuration_to_set)
log.info("Set configuration: "+ ResponseStatusCode.get_description(code))

# Callback para conexión exitosa al broker MQTT
def on_connect(client, userdata, flags, rc):
    log.info("Conectado al broker MQTT con resultado: " + mqtt.connack_string(rc))

try:
    # Crear instancia del cliente MQTT
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect

    # Conectar al broker MQTT
    client.connect(MQTT_BROKER, 1883, 60)

    log.info("Waiting for messages...")
    while True:
        if lora.available() > 0:
            # If the sender not set RSSI
            # code, value = lora.receive_message()
            # If the sender set RSSI
            #code, value, rssi = lora.receive_message(rssi=True)
            try:
                code, value, rssi = lora.receive_dict(rssi=True)
                
                log.info('RSSI: '+ rssi)

                log.info(ResponseStatusCode.get_description(code))

                client.publish(MQTT_TOPIC, str(value))
                log.info(value)
                time.sleep(2)
            except UnicodeDecodeError as e:
                log.error("UnicodeDecodeError "+str(e))
            except Exception as e: 
                log.error("hubo un error: "+str(e))
except KeyboardInterrupt:
    # Manejar interrupción de teclado
    log.info("Interrupción de teclado detectada. Cerrando conexión.")
    client.disconnect()
