#Felix Kaelin
#IPA 2020
#07.04.2020
#V1.0

import RPi.GPIO as GPIO
import ltc2983_hpp
import functions
import def_lib
import spidev
import json
import time
import sys


# load configuration
f = open("Channel_init.json")
config = json.loads(f.read())

print(config["Name"])
print(config["Description"])
print(config["Author"])

print("\nDrueken Sie ENTER um die Temperaturmessung zu starten")
input()
print("START")

ltc2983_hpp.all_channel_conversion()
temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_1)
print("\nThe temperature of channel", def_lib.CHANNEL_1,"is: ", "{0:.2f}".format(temperature[1])) 

#GPIO.cleanup() #delete the GPIO setup