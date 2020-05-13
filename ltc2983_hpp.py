#Felix Kaelin 
#05.03.2020 
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
spi.max_speed_hz = 100000
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
        print("SPI channel is invalid, 0 and 1 are Supported")
       
    GPIO.output(26, GPIO.LOW) 
    time.sleep(0.1) 
    GPIO.output(26, GPIO.HIGH) 
    time.sleep(0.3)

    try:
        if spi_channel < 0: 
            raise 1     
    except: 
        print("SPI Setup failed")
    trans_buff = gen_lib.gen_transaction(trans_buff, def_lib.WRITE, 0x00F0, 0b00000100)
    for k in range(4):
        spi_tx[3-k] = (trans_buff >> (8*k)) & 0xff
    trans_buff = spi.xfer(spi_tx)
   
        
def read_data(address, result, b):
    results = [0]*4
    tx_buff = 0              #Stores the complete transaction
    byte = b*4
    tx = [0]*4            #you could use your results pointer but mem is cheap
    for i in range(b):
        tx_buff = 0
        tx_buff = gen_lib.gen_transaction(tx_buff, def_lib.READ, (address+i), 0x00)
        time.sleep(0.2)
        for j in range(4):
            tx[3-j] = (tx_buff >> (8*j)) & 0xff            
        tx_buff = spi.xfer(tx)
        results[i] = tx_buff[3]
    return results


def get_command_status():
    status_reg = 0
    status_reg = read_data(0x0000, status_reg, 1)
    print("Command register read and") 
    if status_reg[0] == 128:
        print("LTC2983 is initialized with no channel configuration.") 
    elif status_reg[0] == 64: 
        print("LTC2983 is ready for use") 
    else:
        print("was not defined as a valid response")


     
def setup_thermocouple(channel, tc_type, cj_assignment, snl_ended, oc_chk, oc_curr):
    dat_buff = 0x0000
    dat_buff |= gen_lib.or_mask_gen(oc_curr, 18)
    dat_buff |= gen_lib.or_mask_gen(oc_chk, 20)
    dat_buff |= gen_lib.or_mask_gen(snl_ended, 21)
    dat_buff |= gen_lib.or_mask_gen(cj_assignment, 22)
    dat_buff |= gen_lib.or_mask_gen(tc_type, 27)
    chnl_asgn_map[channel - 1] = dat_buff
    return chnl_asgn_map[channel - 1]


def setup_RTD(channel, rtd_type, Rsens_assignment, wire, mode, Ex_curr, standard):
    dat_buff = 0x0000
    dat_buff |= gen_lib.or_mask_gen(standard, 12)
    dat_buff |= gen_lib.or_mask_gen(Ex_curr, 14)
    dat_buff |= gen_lib.or_mask_gen(mode, 18)
    dat_buff |= gen_lib.or_mask_gen(wire, 20)
    dat_buff |= gen_lib.or_mask_gen(Rsens_assignment, 22)
    dat_buff |= gen_lib.or_mask_gen(rtd_type, 27)
    chnl_asgn_map[channel - 1] = dat_buff
    return chnl_asgn_map[channel - 1]

def setup_Sense_R(channel):
    dat_buff = 0x0000
    dat_buff = 3893338112
    #dat_buff |= gen_lib.or_mask_gen(0b00, 10)
    #dat_buff |= gen_lib.or_mask_gen(0b1010, 12)
    #dat_buff |= gen_lib.or_mask_gen(0b10, 14)
    #dat_buff |= gen_lib.or_mask_gen(0b11111010, 14)
    #dat_buff |= gen_lib.or_mask_gen(0b11, 18)
    #dat_buff |= gen_lib.or_mask_gen(0b11101, 26)
    chnl_asgn_map[channel - 1] = dat_buff
    return chnl_asgn_map[channel - 1]

def setup_diode(channel, snl_ended, three_readings, averaging, exc_current, ideality_f):
    dat_buff = 0x0000
    dat_buff |= gen_lib.or_mask_gen(ideality_f, 0)
    dat_buff |= gen_lib.or_mask_gen(exc_current, 22)
    dat_buff |= gen_lib.or_mask_gen(averaging, 24)
    dat_buff |= gen_lib.or_mask_gen(three_readings, 25)
    dat_buff |= gen_lib.or_mask_gen(snl_ended, 26)
    dat_buff |= gen_lib.or_mask_gen(0b11100, 27)
    chnl_asgn_map[channel - 1] = dat_buff
    
    
def write_all_channel_assignments():
    trans_buff = 0        #Buffers the full tranaction byte to be written to the LTC2983
    byte_buff = [0]*4     #Used to buffer a word into a byte
    byte_null = [0]*4     #Null byte buffer used for transactions
    address = 0           #Address Storage
    #Generate SPI Transactions
    for i in range(20):
        print("\nChannel", i+1, "data written.")
        #Convert the channel assignment into a 4 byte array for DEBUG read back
        for j in range(4):
            byte_buff[3-j] = ((chnl_asgn_map[i] >> (8*j)) & 0xff)
        for j in range(4):
            for k in range(4):
                byte_null[k] = byte_buff[k]
            address = (0x0200 + i*4 + j)
            print("Contents of byte[", j, "] transaction = ", byte_buff[j])
            trans_buff = gen_lib.gen_transaction(trans_buff, def_lib.WRITE, address, byte_null[j])
            for k in range(4):
                byte_null[3-k] = ((trans_buff >> (8*k)) & 0xff)
                byte_null[3] = byte_null[3]
            trans_buff = spi.xfer(byte_null)
    return trans_buff
            

def all_channel_conversion():
    x = 0
    temp = 0
    tx_buff = [0]*4
    dat_buff = 0
    all_mask = 0x000fffff
    address = 0x00F4
    #GPIO.setup(19, GPIO.IN)
    print("\n")
    for i in range(4):
        dat_buff = ((all_mask >> (24-8*i)) & 0xff)
        temp = gen_lib.gen_transaction(temp, def_lib.WRITE, (address+i), dat_buff)
        #print("Writing multi channel conversion mask byte", i,":",dat_buff)
        
        for j in range(4):
            tx_buff[3-j] = (temp >> (8*j)) & 0xff  
        temp = spi.xfer(tx_buff)
        
    temp = gen_lib.gen_transaction(temp, def_lib.WRITE, 0x0000, 0x80)
    for i in range(4):
        tx_buff[3-i] = (temp >> (8*i)) & 0xff  
    temp = spi.xfer(tx_buff)
    #x = GPIO.input(19)
    #while(x == 1):
        #x = GPIO.input(19)
    #print("\nconversion_complete")

    
def channel_err_decode(channel_number):
    status = 0
    sensor_type = 0
    conversion_status = 0
    conversion_result_address = (0x0010 + (4 * (channel_number - 1)))
    error_bit_pos = 0
    error_string = ["VALID", "ADC OUT OF RANGE", "SENSOR UNDER RANGE", "SENSOR OVER RANGE", "CJ SOFT FAULT", "CJ HARD FAULT", "HARD ADC OUT OF RANGE", "SENSOR HARD FAULT"]
    #Readback the channel configuration
    conversion_status = read_data(conversion_result_address, conversion_status, 1)

    if conversion_status[0] == 255:
        print ("\nSensor conversion on channel", channel_number, "status byte returned 0xFF: ALL ERROR BITS AND VALID FLAGGED")
    
    elif conversion_status[0] == 1:
        print ("\nConversion on channel", channel_number, "is valid.")
        
    elif conversion_status[0] == 0:
        print ("\nNo conversion on channel", channel_number, "occoured.")
        
    else:
        print ("\nConversion on channel", channel_number, "contained the following errors.")
        for i in range(7):
            if(((conversion_status[0] >> i) & 0x01) == 1):
                print(error_string[i])
    
    
def read_channel_double(channel_number):
    status = 0
    result = 0
    #temperature = [0]*2
    temperature = 0
    sign = 0
    chnl_dat_buff = [0]*4
    conversion_result_address = (0x0010 + (4 * (channel_number - 1)))
    #time.sleep(0.2)
    #Read out the channel information from the SPI bus.
    chnl_dat_buff = read_data(conversion_result_address, chnl_dat_buff[0], 4)
    #Now that the channel data buffer is filled check for errors
    channel_err_decode(channel_number)
    if (chnl_dat_buff[0] == 0):
        #print("Result on channel ", channel_number, " is invalid.")
        return 9000
    else:
        for i in range(4):
            print("Raw read value of channel ", channel_number, " byte ", i, " = ", hex(chnl_dat_buff[i]))
        result = 0;
        if (chnl_dat_buff[1] >= 128):
            chnl_dat_buff[1] = chnl_dat_buff[1]^0xff
            chnl_dat_buff[2] = chnl_dat_buff[2]^0xff
            chnl_dat_buff[3] = chnl_dat_buff[3]^0xff
            #temperature[0] = 1
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
        #temperature[1] = result / 1024
        temperature = result / 1024
        return temperature
    
GPIO.cleanup() #delet the GPIO setup
