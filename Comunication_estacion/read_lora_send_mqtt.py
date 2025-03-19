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

# Constants
MQTT_BROKER = "10.3.141.1"
MQTT_TOPIC = 'huillin/data'
SLEEP_TIME = 2  # Configurable sleep time in seconds

# Initialize logger
file = "estacion_read_mqtt_send_lora"
log = logging.getLogger(file)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    #filename=file + ".log",
    encoding="utf-8",
    #filemode="a"
)

GPIO.setwarnings(False) #de activate the GPIO warning to avoir the waring of re-use of port

# I found out that if i config it everytime it was creating conflict, but i leave it in case needed.
# Set the configuration to default values and print the updated configuration to the console
# Not needed if already configured
#configuration_to_set = Configuration('400T22D')
# To enable RSSI, you must also enable RSSI on sender
#configuration_to_set.TRANSMISSION_MODE.enableRSSI = RssiEnableByte.RSSI_ENABLED

#code, confSetted = lora.set_configuration(configuration_to_set)
#log.info("Set configuration: "+ ResponseStatusCode.get_description(code))


def on_connect(client, userdata, flags, rc):
    """Callback for successful MQTT connection."""
    log.info("Conectado al broker MQTT con resultado: " + str(mqtt.connack_string(rc)))

def main() -> None:
    """Main function to read LoRa messages and send them to MQTT."""
    
    try:
        # Initialize the LoRaE22 module
        lora_serial = serial.Serial('/dev/ttyUSB0') #, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
        lora = LoRaE22('400T22D', lora_serial, m0_pin=23, m1_pin=24)
        code = lora.begin()
        log.info("Initialization:"+ ResponseStatusCode.get_description(code))

        # Crear instancia del cliente MQTT
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.on_connect = on_connect
        # Conectar al broker MQTT
        client.connect(MQTT_BROKER, 1883, 60)

        log.info("Waiting for messages...")

        while True:
            if lora.available() > 0: #wait for lora to be available
                try:
                    code, value, rssi = lora.receive_dict(rssi=True) # reading the data
                    
                    # Log RSSI and status code
                    log.debug(f"RSSI: {rssi},Status: {ResponseStatusCode.get_description(code)} ")

                    # Publish to MQTT
                    if isinstance(value, dict) or isinstance(value, str):
                        client.publish(MQTT_TOPIC, str(value))
                        log.debug(f"Published to MQTT: {value}")
                    else:
                        log.warning("Invalid payload type received from LoRa")
                    
                    time.sleep(SLEEP_TIME) #sleep time required in order to not overload the lora module
                except UnicodeDecodeError as e:
                    log.error(f"UnicodeDecodeError: {e}")
                except Exception as e: 
                    log.error(f"An error occurred: {e}")
    except KeyboardInterrupt:
        # Manejar interrupción de teclado
        log.info("Interrupción de teclado detectada. Cerrando conexión.")
        client.disconnect()
    except Exception as e:
        log.error(f"Critical error: {e}")
    finally:
        # Cleanup
        if 'lora_serial' in locals() and lora_serial.is_open:
            lora_serial.close()
            log.info("LoRa serial connection closed.")
        client.disconnect()
        log.info("MQTT client disconnected.")

if __name__ == "__main__":
    main()
