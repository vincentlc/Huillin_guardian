# Author: Vincent le costaouec
# Code inspired in work of Renzo Mischianti (www.mischianti.org)

# Description:
# This script read messages from Lora Red and send it to the node-red through the MQTT channel

# Note: This code was written and tested using RaspberryPi.
#       when use double check that you are using the correct UART and pins.

import serial
import time
from datetime import datetime
import json
import os

from lora_e22 import LoRaE22, Configuration
from lora_e22_operation_constant import ResponseStatusCode
from lora_e22_constants import FixedTransmission, RssiEnableByte

import paho.mqtt.client as mqtt
import logging
import RPi.GPIO as GPIO

file="test_batch_lora"
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

# Initialize variables
expected_start_value = 1000000000000
received_messages = []
lost_messages = 0
time_differences = []
time_greater_than_3s = 0
test_batch_file = "test_batch_number.txt"

# Function to read the last test batch number
def read_test_batch_number():
    if os.path.exists(test_batch_file):
        with open(test_batch_file, 'r') as f:
            return int(f.read().strip())
    return 1  # Start from batch 1 if the file does not exist

# Function to write the current test batch number
def write_test_batch_number(batch_number):
    with open(test_batch_file, 'w') as f:
        f.write(str(batch_number))

# Function to check the integrity of the message
def check_integrity(message, expected_message):
    try:
        # Check if the message is a dictionary
        if not isinstance(message, dict):
            return False
        
        # Check required fields and their types
        required_fields = {
            'ts': int,
            'la': float,
            'lo': float,
            'ph': float,
            'ec': float,
            'od': float,
            'sa': float,
            'tp': str,
            'sp': float,
            'e1': int,
            'e2': int,
            'e3': int,
            'e4': int,
            'ue': int,
            'up': str,
            'p4': float,
            'p7': float
        }
        
        for field, field_type in required_fields.items():
            if field not in message or not isinstance(message[field], field_type):
                return False
        
        # Check if 'ts' is greater than or equal to the expected start value
        if message['ts'] < expected_start_value:
            return False
        
        # Check if the received message matches the expected message (except for 'ts')
        for field in expected_message:
            if field != 'ts' and message[field] != expected_message[field]:
                return False
        
        return True
    except Exception as e:
        print(f"Integrity check error: {e}")
        return False

# Function to log statistics
def log_statistics(batch_number, received_count, lost_count, time_diff_stats):
    log_file = f"test_batch_{batch_number}.txt"
    with open(log_file, 'a') as f:
        f.write(f"Test Batch: {batch_number}\n")
        f.write(f"Received Messages: {received_count}\n")
        f.write(f"Lost Messages: {lost_count}\n")
        f.write(f"Time Differences: {time_diff_stats}\n")
        f.write(f"Messages with Time Difference > 3s: {time_greater_than_3s}\n")
        f.write("\n")
        
# Main loop to receive messages
def main():
    global lost_messages, time_differences, time_greater_than_3s
    last_received_time = None
    expected_message = {
            'ts': None,  # Placeholder for the timestamp
            'la': -40.0,'lo': -72.99999999,'ph': 7.33,'ec': 3.66,'od': 7.0,'sa': 88.88,'tp': '28.09','sp': 0.21,'e1': 13000,'e2': 0,'e3': 1200,'e4': 0,'ue': 13000,'up': 'start','p4': 4.0,'p7': 7.0
    }
    # Initialize the LoRaE22 module
    loraSerial = serial.Serial('/dev/ttyUSB0') #, baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
    lora = LoRaE22('400T22D', loraSerial, m0_pin=23, m1_pin=24)
    code = lora.begin()
    log.info("Initialization:"+ ResponseStatusCode.get_description(code))
    
    # Read the current test batch number
    test_batch = read_test_batch_number()

    try:
        while True:
            # Simulate receiving a message (replace with actual lora.receive_dict())
            code, value, rssi = lora.receive_dict(rssi=True)  # Replace with actual receive method
            if lora.available() > 0: #wait for lora to be available

try:
    log.info("Waiting for messages...")
    while True:
        if lora.available() > 0: #wait for lora to be available
            try:
                code, value, rssi = lora.receive_dict(rssi=True) # reading the data
                # Update the expected timestamp for the next message
                if expected_message['ts'] is None:
                    expected_message['ts'] = expected_start_value
                else:
                    expected_message['ts'] += 1  # Increment the expected timestamp

                # Check the integrity of the received message
                if check_integrity(value, expected_message):
                    received_messages.append(value)
                    current_received_time = time.time()  # Get the actual reception time
                    
                    # Check time difference
                    if last_received_time is not None:
                        time_diff = current_received_time - last_received_time
                        time_differences.append(time_diff)
                        
                        if time_diff > 3:
                            time_greater_than_3s += 1
                    
                    last_received_time = current_received_time
                else:
                    lost_messages += 1
            else:
                lost_messages += 1
            
            # Sleep for 2 seconds (or adjust as needed)
            time.sleep(2)

            # Log statistics every 10 messages (or adjust as needed)
            if len(received_messages) % 10 == 0:
                log_statistics(test_batch, len(received_messages), lost_messages, time_differences)

    except KeyboardInterrupt:
        print("Keyboard interrupt received. Saving data...")
        log_statistics(test_batch, len(received_messages), lost_messages, time_differences)
        print("Data saved. Exiting program.")
    except Exception as e:
        print(f"An error occurred: {e}")
        log_statistics(test_batch, len(received_messages), lost_messages, time_differences)
        print("Data saved. Exiting program.")
    finally:
        # Increment and save the test batch number for the next run
        test_batch += 1
        write_test_batch_number(test_batch)

if __name__ == "__main__":
    main()

