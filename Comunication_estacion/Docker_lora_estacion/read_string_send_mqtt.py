# Author: Renzo Mischianti
# Website: www.mischianti.org
#
# Description:
# This script demonstrates how to use the E22 LoRa module with RaspberryPi.
# It includes examples of sending and receiving string using both transparent and fixed transmission modes.
# The code also configures the module's address and channel for fixed transmission mode.
# Address and channel of this receiver:
# ADDH = 0x00
# ADDL = 0x01
# CHAN = 23
#
# Can be used with the send_fixed_string and send_transparent_string scripts
#
# Note: This code was written and tested using RaspberryPi on an ESP32 board.
#       It works with other boards, but you may need to change the UART pins.

import serial
import time

from lora_e22 import LoRaE22, Configuration
from lora_e22_operation_constant import ResponseStatusCode
from lora_e22_constants import FixedTransmission, RssiEnableByte

import paho.mqtt.client as mqtt

# Configuración del servidor MQTT
MQTT_BROKER = "127.0.0.1" #'192.168.1.2'  # Cambia esto a la dirección de tu broker MQTT
MQTT_TOPIC = 'huillin/data'  # Cambia esto al tema MQTT que desees utilizar

# Initialize the LoRaE22 module
loraSerial = serial.Serial('/dev/ttyUSB0') #, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
lora = LoRaE22('400T22D', loraSerial, m0_pin=23, m1_pin=24)
code = lora.begin()
print("Initialization: {}", ResponseStatusCode.get_description(code))

# Set the configuration to default values and print the updated configuration to the console
# Not needed if already configured
configuration_to_set = Configuration('400T22D')
# To enable RSSI, you must also enable RSSI on sender
configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED

code, confSetted = lora.set_configuration(configuration_to_set)
print("Set configuration: {}", ResponseStatusCode.get_description(code))

# Callback para conexión exitosa al broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con resultado: " + mqtt.connack_string(rc))

# Crear instancia del cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect

# Conectar al broker MQTT
client.connect(MQTT_BROKER, 1883, 60)


print("Waiting for messages...")
while True:
    if lora.available() > 0:
        # If the sender not set RSSI
        # code, value = lora.receive_message()
        # If the sender set RSSI
        #code, value, rssi = lora.receive_message(rssi=True)
        try:
        
            code, value, rssi = lora.receive_dict(rssi=True)
            
            print('RSSI: ', rssi)

            print(ResponseStatusCode.get_description(code))

            client.publish(MQTT_TOPIC, str(value))
            print(value)
            time.sleep(2)
        
        except UnicodeDecodeError:
            print("UnicodeDecodeError")
        except KeyboardInterrupt:
            # Manejar interrupción de teclado
            print("Interrupción de teclado detectada. Cerrando conexión.")
            ser.close()
            client.disconnect()
        except: 
            print("Otro error")
            
#except KeyboardInterrupt:
    # Manejar interrupción de teclado
#    print("Interrupción de teclado detectada. Cerrando conexión.")
#    ser.close()
#    client.disconnect()
