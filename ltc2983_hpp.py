#Felix Kaelin 
#09.04.2020 
#Library for ltc2983 in python 
#build for IPA 2020

import RPi.GPIO as GPIO
import def_lib
import gen_lib
import spidev
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)

spi = spidev.SpiDev() 
spi.open(0,0) 
spi.max_speed_hz = 1000000 
spi.mode = 0b00

chnl_asgn_map = [0]*20

def init_ltc2983(spi_channel):
    spi_tx = [0]*4 
    trans_buff = 0
    try:
        if (spi_channel > 1) | (spi_channel < 0): 
            raise 2
        else:
            spi_channel = spi_channel
    except:
        pass
        #print("SPI channel is invalid, 0 and 1 are Supported")

    try:
        if spi_channel < 0: 
            raise 1     
    except: 
        pass
        #print("SPI Setup failed")
    trans_buff = gen_lib.gen_transaction(trans_buff, def_lib.WRITE, 0x00F0, 0b00000100)
    for k in range(4):
        spi_tx[3-k] = (trans_buff >> (8*k)) & 0xff
    trans_buff = spi.xfer(spi_tx)
   
        
def read_data(address, result, b):
    results = [0]*4
    tx_buff = 0              #Stores the complete transaction
    tx = [0]*4            #you could use your results pointer but mem is cheap
    for i in range(b):
        tx_buff = 0
        tx_buff = gen_lib.gen_transaction(tx_buff, def_lib.READ, (address+i), 0x00)
        #time.sleep(0.1)
        for j in range(4):
            tx[3-j] = (tx_buff >> (8*j)) & 0xff            
        tx_buff = spi.xfer(tx)
        results[i] = tx_buff[3]
    return results


def get_command_status():
    status_reg = 0
    status_reg = read_data(0x0000, status_reg, 1)
    #print("Command register read and") 
    #if status_reg[0] == 128:
        #print("LTC2983 is initialized with no channel configuration.") 
    #elif status_reg[0] == 64: 
        #print("LTC2983 is ready for use") 
    #else:
        #print("was not defined as a valid response")


     
def setup_thermocouple(channel, tc_type, cj_assignment, snl_ended, oc_chk, oc_curr):
    dat_buff = 0x0000
    dat_buff |= gen_lib.or_mask_gen(oc_curr, 18)
    dat_buff |= gen_lib.or_mask_gen(oc_chk, 20)
    dat_buff |= gen_lib.or_mask_gen(snl_ended, 21)
    dat_buff |= gen_lib.or_mask_gen(cj_assignment, 22)
    dat_buff |= gen_lib.or_mask_gen(tc_type, 27)
    chnl_asgn_map[channel - 1] = dat_buff
    return chnl_asgn_map[channel - 1]

    
def write_all_channel_assignments():
    trans_buff = 0        #Buffers the full tranaction byte to be written to the LTC2983
    byte_buff = [0]*4     #Used to buffer a word into a byte
    byte_null = [0]*4     #Null byte buffer used for transactions
    address = 0           #Address Storage
    #Generate SPI Transactions
    for i in range(20):
        #print("\nChannel", i+1, "data written.")
        #Convert the channel assignment into a 4 byte array for DEBUG read back
        for j in range(4):
            byte_buff[3-j] = (chnl_asgn_map[i] >> (8*j)) & 0xff
        for j in range(4):
            for k in range(4):
                byte_null[k] = byte_buff[k]
            address = (0x200 + i*4 + j)
            #print("Contents of byte[", j, "] transaction = ", byte_buff[j])
            trans_buff = gen_lib.gen_transaction(trans_buff, def_lib.WRITE, address, byte_null[j])
            for k in range(4):
                byte_null[3-k] = (trans_buff >> (8*k)) & 0xff
                byte_null[3] = byte_null[3]
            spi.xfer(byte_null)
            

def all_channel_conversion():
    temp = 0
    tx_buff = [0]*4
    dat_buff = 0
    all_mask = 0x000fffff
    address = 0x00F4
    #GPIO.setup(19, GPIO.IN)
    #print("\n")
    for i in range(4):
        dat_buff = ((all_mask >> (24-(8*i))) & 0xff)
        temp = gen_lib.gen_transaction(temp, def_lib.WRITE, (address+i), dat_buff)
        #print("Writing multi channel conversion mask byte", i,":",dat_buff)
        
        for j in range(4):
            tx_buff[3-j] = (temp >> (8*j)) & 0xff
            
        temp = spi.xfer(tx_buff)
        
    temp = gen_lib.gen_transaction(temp, def_lib.WRITE, 0x0000, 0x80)
    for i in range(4):
        tx_buff[3-i] = (temp >> (8*i)) & 0xff
        
    temp = spi.xfer(tx_buff)
    
    #print("\nconversion_complete")
    
    
def read_channel_double(channel_number):
    result = 0
    temperature = [0]*2
    sign = 0
    chnl_dat_buff = [0]*4
    conversion_result_address = (0x0010 + (4 * (channel_number - 1)))
    #time.sleep(0.01)
    #Read out the channel information from the SPI bus.
    chnl_dat_buff = read_data(conversion_result_address, chnl_dat_buff[0], 4)
    #Now that the channel data buffer is filled check for errors
    if (chnl_dat_buff[0] != 1):
        #print("Result on channel ", channel_number, " is invalid.")
        return 9000
    else:
        #for i in range(4):
            #print("Raw read value of channel ", channel_number, " byte ", i, " = ", chnl_dat_buff[i])
        result = 0
        if (chnl_dat_buff[1] >= 128):
            chnl_dat_buff[1] = chnl_dat_buff[1]^0xff
            chnl_dat_buff[2] = chnl_dat_buff[2]^0xff
            chnl_dat_buff[3] = chnl_dat_buff[3]^0xff
            temperature[0] = 1
        result = result | (chnl_dat_buff[1]<<16)
        result = result | (chnl_dat_buff[2]<<8)
        result = result | (chnl_dat_buff[3])
        #temperature[0] = 0
        #print("Raw bin of result = ", result)
        
        #Convert a 24bit 2s compliment into a 32bit 2s compliment number
        if ((chnl_dat_buff[1]&0b10000000)==128):
            sign = True
        else:
            sign = False
        #append 1s to the MSB 8 bits
        if (sign == 1):
            result = result | 0xFF000000
        #Compensate for precision
        temperature[1] = result / 1024
        return temperature
    
GPIO.cleanup() #delet the GPIO setup
