import RPi.GPIO as GPIO 
import ltc2983_hpp 
import def_lib 
import spidev 
import time
import sys

class functions:

    def __init__(self, info = {}):
        self.available_channel = info["available_channel"]
        self.used_channel = info["used_channel"]
        self.time = info["time"]
        self.time_interval = info["time_interval"]

    def init_LTC2983(self):
        self.GPIO.setmode(GPIO.BCM) 
        self.GPIO.setup(26, GPIO.OUT) 
                
        self.spi = spidev.SpiDev()  
        self.spi.open(0,0)  
        self.spi.max_speed_hz = 1000000  
        self.spi.mode = 0b00 
            
        self.d_ideality_f = 0x00101042    #Diode ideality factor of ~ 1.04 
        self.chnl_asgn_map = [0]*20       #Intermap of LTC2983 ADC channel mapping 
        self.spi_tx = [0]*200             #SPI Tansaction buffer, This gets pushed out to the IC and replace with BCM rx spi pin data 
        self.spi_rx = [0]*200             #SPI rx buffer for read data transactions 
        self.trans_buff = 0               #Stores a word containing the transaction (32 bit) 
        self.temperature = [0]*2  
                
        self.ltc2983_hpp.init_ltc2983(0) 
        self.ltc2983_hpp.get_command_status() 
            
        self.chnl_asgn_map[def_lib.CHANNEL_1 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_1, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
        self.chnl_asgn_map[def_lib.CHANNEL_2 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_2, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
        self.chnl_asgn_map[def_lib.CHANNEL_3 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_3, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
        self.chnl_asgn_map[def_lib.CHANNEL_4 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_4, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
        self.chnl_asgn_map[def_lib.CHANNEL_5 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_5, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
        self.chnl_asgn_map[def_lib.CHANNEL_6 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_6, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
        self.chnl_asgn_map[def_lib.CHANNEL_7 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_7, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA)
        self.chnl_asgn_map[def_lib.CHANNEL_8 - 1] = ltc2983_hpp.setup_thermocouple(def_lib.CHANNEL_8, def_lib.TYPE_K, def_lib.NO_CJ, def_lib.SNGL, def_lib.OC_CHK_ON, def_lib.TC_100UA) 
        #self.spi_tx[0] = ltc2983_hpp.write_all_channel_assignments() 


