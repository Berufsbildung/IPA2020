"""!
Felix Kaelin \n
IPA 2020 \n
14.04.2020 \n 
V1.3
"""

# import Libraries
import RPi.GPIO as GPIO
import ltc2983_hpp
import subprocess
import threading
import functions
import def_lib
import spidev
import signal
import shlex
import json
import time
import sys

# Stop programm with Keyboardinterrupt
signal.signal(signal.SIGINT, signal.SIG_DFL)
signal.signal(signal.SIGTERM, signal.SIG_DFL)

## Load json configuration
f = open("Channel_init.json")
config = json.loads(f.read())

# SW Information
print("Mehrkanaliges Temperaturmessmodul")
print("IPA_2020")
print("Felix Kaelin")

# Slected setting from json file
print("\nThe selected settings are:")
print(config["used_channel"], "Channels are selected for the measurement")
print("The hole measurement time is:", config["time"], "seconds ")
print("A measurement is taken after every", config["time_interval"], "seconds ")

# Start measurement
print("\nPress ENTER to start the measurement")
input()                                                 # Wait until Enter will pressed
print("START")

# Setup GPIO
GPIO.setmode(GPIO.BCM) 
GPIO.setup(26, GPIO.OUT) 

## Setup SPI               
spi = spidev.SpiDev()  
spi.open(0,0)
## 1'000'000 Hz 
spi.max_speed_hz = 1000000 
## 0b00         
spi.mode = 0b00

## Used for SPI communication          
chnl_asgn_map = [0]*20          ## Intermap of LTC2983 ADC channel mapping
spi_tx = [0]*200                ## SPI Tansaction buffer, This gets pushed out to the IC and replace with BCM rx spi pin data 

# Setup LTC2983
ltc2983_hpp.init_ltc2983(0) 
ltc2983_hpp.get_command_status()

# Setup all 20 Thermocouples
chnl_asgn_map = functions.init_LTC2983()
ltc2983_hpp.write_all_channel_assignments()

# Write using Channel to .xsl
functions.save_Channel()

## function to stop programm after the hole measurement time 
def stop():     
    print("")                           # Make a space line 
    befehl = "pkill -f main.py"         # Command to close this program
    cmd = shlex.split(befehl)           # Type the comand in to the cmd
    subprocess.run(cmd)                 # Run the command

## Start Timer for the hole measurement time  
st = threading.Timer((config["time"]+1), stop)              # Setup Timer for the hole measurement time
st.start()                                                  # Start Timer for the hole measurement time

## Main rutin 0
def main_interval0():
    mi0 = threading.Timer(config["time_interval"], main_interval1)          # Setup Timer for the repeat interval time
    mi0.start()                                                             # Start Timer for the repeat interval time
    print("")                                                               # Make a space line
    functions.temperature()                                                 # Print and save current temperature
    ltc2983_hpp.all_channel_conversion()                                    # Get Current temprature    

## Main rutin 1 
def main_interval1():
    mi1 = threading.Timer(config["time_interval"], main_interval0)          # Setup Timer for the repeat interval time
    mi1.start()                                                             # Start Timer for the repeat interval time
    print("")                                                               # Make a space line
    functions.temperature()                                                 # Print and save current temperature
    ltc2983_hpp.all_channel_conversion()                                    # Get Current temprature

# First Main rutin without printing temprature
threading.Timer(config["time_interval"], main_interval0).start()            # Start Timer for the repeat interval time
ltc2983_hpp.all_channel_conversion()                                        # Get Current temprature

GPIO.cleanup()          #delete the GPIO setup