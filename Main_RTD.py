#Felix Kaelin 
#15.05.2020 
#Library for ltc2983 in python 
#build for IPA 2020

import RPi.GPIO as GPIO
import ltc2983_hpp
import def_lib
import spidev
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)

spi = spidev.SpiDev() 
spi.open(0,0) 
spi.max_speed_hz = 100000 
spi.mode = 0b00

d_ideality_f = 0x00101042    #Diode ideality factor of ~ 1.04
chnl_asgn_map = [0]*20       #Intermap of LTC2983 ADC channel mapping
spi_tx = [0]*200             #SPI Tansaction buffer, This gets pushed out to the IC and replace with BCM rx spi pin data
spi_rx = [0]*200             #SPI rx buffer for read data transactions
trans_buff = 0               #Stores a word containing the transaction (32 bit)


ltc2983_hpp.init_ltc2983(0)

ltc2983_hpp.get_command_status()

chnl_asgn_map[def_lib.CHANNEL_5 -1] = ltc2983_hpp.setup_Sense_R(def_lib.CHANNEL_5)
chnl_asgn_map[def_lib.CHANNEL_6 -1] = ltc2983_hpp.setup_RTD(def_lib.CHANNEL_6, def_lib.PT_100, def_lib.CH5_4, def_lib.WIRE_3, def_lib.Int, def_lib.C_250uA, def_lib.Europa)

ltc2983_hpp.write_all_channel_assignments()


for i in range(1): #BSP range(1800)
    temperature = 0
    ltc2983_hpp.all_channel_conversion()

    temperature = ltc2983_hpp.read_channel_double(def_lib.CHANNEL_6)

    
    if temperature == 9000:
        print("The temperature of channel", def_lib.CHANNEL_6, "= ERROR")
    else:
        if temperature == 1:
            temperature = temperature + 10
            print("The temperature of channel", def_lib.CHANNEL_6,"is: ", "-","{0:.2f}".format(temperature))
        else:
            temperature = temperature - 10
            print("The temperature of channel", def_lib.CHANNEL_6,"is: ", "{0:.2f}".format(temperature))

    
GPIO.cleanup() #delete the GPIO setup