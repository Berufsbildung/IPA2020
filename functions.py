# import Libraries
from datetime import datetime
import RPi.GPIO as GPIO 
import ltc2983_hpp 
import def_lib 
import spidev 
import json
import time
import sys

# Load json configuration
f = open("Channel_init.json")
config = json.loads(f.read())


# Print current temperature of one channel
def temp_print(temperature,CHANNEL):
    if temperature == 9000:                                 # If temperature value are 9000, current channel have an error 
        print("Channel", CHANNEL, "have an ERROR")              # Print Error   
        save_temperatur_error()                                 # Save Error to .xls        
    else:                                                   # Else the current channel have an valid temprature vale 
        if temperature[0] == 1:                                 # If temperature value are negative
            temperature[1] = temperature[1] + 10                    # Convert measuret temprature
            print("The temperature of channel", CHANNEL,"is: ", "-","{0:.2f}".format(temperature[1]))
            save_temperatur_negativ(temperature)                    # Save negative temperture value to .xls
        else:                                                   # Else temperature value are positive
            temperature[1] = temperature[1] - 10                    # Convert measuret temprature
            print("The temperature of channel", CHANNEL,"is: ", "{0:.2f}".format(temperature[1]))
            save_temperatur_positiv(temperature)                    # Save negative temperture value to .xls


# Setup all 20 Thermocouples
def init_LTC2983():
    chnl_asgn_map = [0]*20
    chnl_asgn_map[def_lib.CHANNEL_1 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_1, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_2 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_2, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_3 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_3, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_4 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_4, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_5 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_5, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_6 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_6, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_7 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_7, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_8 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_8, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_9 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_9, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_10 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_10, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_11 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_11, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_12 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_12, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_13 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_13, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_14 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_14, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_15 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_15, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_16 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_16, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_17 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_17, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_18 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_18, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_19 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_19, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    chnl_asgn_map[def_lib.CHANNEL_20 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_20, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
    return chnl_asgn_map


# Reading temperature from selected channels
def temperature():
    if config["used_channel"] >= 1:                                                 # If channel 1 is selected:
        save_time()                                                                 # Save current time to .xls
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_1)            # Read temperature from channel 1
        temp_print(temperature,1)                                                   # Print current temperature of channel 1

    if config["used_channel"] >= 2:                                                 # If channel 2 is selected:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_2)            # Read temperature from channel 2
        temp_print(temperature,2)                                                   # Print current temperature of channel 2
    
    if config["used_channel"] >= 3:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_3)
        temp_print(temperature,3)

    if config["used_channel"] >= 4:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_4)
        temp_print(temperature,4)

    if config["used_channel"] >= 5:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_5)
        temp_print(temperature,5)
    
    if config["used_channel"] >= 6:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_6)
        temp_print(temperature,6)

    if config["used_channel"] >= 7:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_7)
        temp_print(temperature,7)

    if config["used_channel"] >= 8:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_8)
        temp_print(temperature,8)

    if config["used_channel"] >= 9:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_9)
        temp_print(temperature,9)

    if config["used_channel"] >= 10:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_10)
        temp_print(temperature,10)

    if config["used_channel"] >= 11:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_11)
        temp_print(temperature,11)

    if config["used_channel"] >= 12:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_12)
        temp_print(temperature,12)

    if config["used_channel"] >= 13:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_13)
        temp_print(temperature,13)

    if config["used_channel"] >= 14:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_14)
        temp_print(temperature,14)

    if config["used_channel"] >= 15:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_15)
        temp_print(temperature,15)

    if config["used_channel"] >= 16:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_16)
        temp_print(temperature,16)

    if config["used_channel"] >= 17:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_17)
        temp_print(temperature,17)

    if config["used_channel"] >= 18:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_18)
        temp_print(temperature,18)

    if config["used_channel"] >= 19:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_19)
        temp_print(temperature,19)

    if config["used_channel"] >= 20:
        temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_20)
        temp_print(temperature,20)


# Save selected channels to .xls
def save_Channel():
    Channel_string = ["Channel_1", "Channel_2", "Channel_3", "Channel_4", "Channel_5", "Channel_6", "Channel_7", "Channel_8", "Channel_9", "Channel_10",
    "Channel_11", "Channel_12", "Channel_13", "Channel_14", "Channel_15", "Channel_16", "Channel_17", "Channel_18", "Channel_19", "Channel_20",]
    
    f = open("Resultate.xls", "a")                  # Open .xls file

    for i in range(config["used_channel"]):         # Save how many channels are selected
        f.write("\t" + Channel_string[i])           # Save Channel_string to .xls

    f.close()                                       # Close .xls file 

# Save current time to .xls
def save_time():
    f = open("Resultate.xls", "a")                              # Open .xls file
    get_time = time.localtime()                                 # get current time
    time_string = time.strftime("%H:%M:%S", get_time)           # Convert current time
    f.write("\n" + time_string)                                 # save converted time to .xls
    f.close()                                                   # Close .xls file 


def save_temperatur_positiv(temperature):
    f = open("Resultate.xls", "a")                                  # Open .xls file
    f.write("\t" + str("{0:.2f}".format(temperature[1])))           # Save positive temprature to .xls
    f.close()                                                       # Close .xls file

def save_temperatur_negativ(temperature):
    f = open("Resultate.xls", "a")                                      # Open .xls file
    f.write("\t" + "-" + str("{0:.2f}".format(temperature[1])))         # Save negative temprature to .xls
    f.close()                                                           # Close .xls file

def save_temperatur_error():
    f = open("Resultate.xls", "a")          # Open .xls file
    f.write("\t" + "ERROR")                 # Save ERROR to .xls
    f.close()                               # Close .xls file