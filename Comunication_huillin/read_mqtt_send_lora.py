# Author: Renzo Mischianti
# Website: www.mischianti.org
#
# Description:
# This script demonstrates how to use the E22 LoRa module with RaspberryPi.
# Sending dictionary
#
# Note: This code was written and tested using RaspberryPi on an ESP32 board.
#       It works with other boards, but you may need to change the UART pins.

import serial
import time

from lora_e22 import LoRaE22, Configuration
from lora_e22_constants import RssiAmbientNoiseEnable, RssiEnableByte
from lora_e22_operation_constant import ResponseStatusCode

import paho.mqtt.client as mqtt

# Initialize the LoRaE22 module
loraSerial = serial.Serial('/dev/ttyUSB1') #, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
lora = LoRaE22('400T22D', loraSerial, m0_pin=23, m1_pin=24)
code = lora.begin()
print("Initialization: {}", ResponseStatusCode.get_description(code))

# Set the configuration to default values and print the updated configuration to the console
# Not needed if already configured
configuration_to_set = Configuration('400T22D')
# To enable RSSI, you must also enable RSSI on receiver
configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED
code, confSetted = lora.set_configuration(configuration_to_set)
print("Set configuration: {}", ResponseStatusCode.get_description(code))

def on_connect(client, userdata, flags, rc):
  print("Connected with result code " + str(rc))
  client.subscribe("huillin/data")
  
def on_message(client, userdata, msg):
  print(msg.topic + " " + str(msg.payload))
  code = lora.send_transparent_dict(msg.payload.decode('utf-8'))
  print("Send message: {}", ResponseStatusCode.get_description(code))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("10.3.141.1", 1883, 60)

client.loop_forever()


# Send a dictionary message (transparent)
#data = {'key1': 'value1', 'key2': 'value2'}
#while 1:
#     code = lora.send_transparent_dict(data)
#     print("Send message: {}", ResponseStatusCode.get_description(code))
#     time.sleep(5)
