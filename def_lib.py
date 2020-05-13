#Felix Kaelin 
#05.03.2020 
#Library for ltc2983 in python 
#build for IPA 2020

#rpi_ltc2983.gen_transaction(buff,trans_type,address,data) 
#rpi_ltc2983.or_mask_gen(value,bit_pos) 
# WRITE AND READ COMMANDS 
NOP = 0x01 
WRITE = 0x02 
READ = 0x03 

#BASE ADDRESS MAP 
CNV_RSLTS = 0x0010                 #START: 0x010 -> END: 0x05F [Word] 
CHNL_MAP = 0x0200                  #START: 0x200 -> END: 0x24F [Word] 

#TC SE/DIFF VALS 
SNGL = True 
DIFF = False 

#This is the sesnor type selection for the channel 
UNASSIGNED = 0b00000 
TYPE_K = 0b00010 
TYPE_CUST = 0b01001 

#Channel Number to Array Bindings
#CHANNEL = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
CHANNEL_1 = 1 
CHANNEL_2 = 2 
CHANNEL_3 = 3 
CHANNEL_4 = 4 
CHANNEL_5 = 5 
CHANNEL_6 = 6 
CHANNEL_7 = 7 
CHANNEL_8 = 8 
CHANNEL_9 = 9 
CHANNEL_10 = 10 
CHANNEL_11 = 11 
CHANNEL_12 = 12 
CHANNEL_13 = 13 
CHANNEL_14 = 14 
CHANNEL_15 = 15 
CHANNEL_16 = 16 
CHANNEL_17 = 17 
CHANNEL_18 = 18 
CHANNEL_19 = 19 
CHANNEL_20 = 20 

#Input Channel Mapping 
#This is the input channels represented in binary form 
MULTI_CHNL = 0b10000000 
CHNL_1 = 0b10000001 
CHNL_2 = 0b10000010 
CHNL_3 = 0b10000011 
CHNL_4 = 0b10000100 
CHNL_5 = 0b10000101 
CHNL_6 = 0b10000110 
CHNL_7 = 0b10000111 
CHNL_8 = 0b10001000 
CHNL_9 = 0b10001001 
CHNL_10 = 0b10001010 
CHNL_11 = 0b10001011 
CHNL_12 = 0b10001100 
CHNL_13 = 0b10001101 
CHNL_14 = 0b10001110 
CHNL_15 = 0b10001111 
CHNL_16 = 0b10010000 
CHNL_17 = 0b10010001 
CHNL_18 = 0b10010010 
CHNL_19 = 0b10010011 
CHNL_20 = 0b10010100 
CHNL_SLP = 0b10010111 

"""Thermocouple Definitions""" 

#TC Cold Junction Mapping 
#This is the cold junction channels represented in binary form 
NO_CJ = 0b00000 
CJ_CHNL_1 = 0b00001 
CJ_CHNL_2 = 0b00010 
CJ_CHNL_3 = 0b00011 
CJ_CHNL_4 = 0b00100 
CJ_CHNL_5 = 0b00101 
CJ_CHNL_6 = 0b00110 
CJ_CHNL_7 = 0b00111 
CJ_CHNL_8 = 0b01000 
CJ_CHNL_9 = 0b01001 
CJ_CHNL_10 = 0b01010 
CJ_CHNL_11 = 0b01011 
CJ_CHNL_12 = 0b01100 
CJ_CHNL_13 = 0b01101 
CJ_CHNL_14 = 0b01110 
CJ_CHNL_15 = 0b01111 
CJ_CHNL_16 = 0b10000 
CJ_CHNL_17 = 0b10001 
CJ_CHNL_18 = 0b10010 
CJ_CHNL_19 = 0b10011 
CJ_CHNL_20 = 0b10100 
 
#TC Excitation Current ex. EXT, This is the excitation current provided by the LTC2983 
#EXT is the external excitation source will be used 
TC_EXT_C = 0b00 
TC_10UA = 0b00 
TC_100UA = 0b01 
TC_500UA = 0b10 
TC_1000UA = 0b11 
  
#TC SE/DIFF VALS 
SNGL = True 
DIFF = False 
  
#Over current protection 
OC_CHK_ON = True 
OC_CHK_OFF = False 
  
"""DIODE CONFIGURATION""" 
 
#2 or 3 readigs, Diode Readings at 2 or 3 different current levels 
CONV_3 = True 
CONV_2 = False 
  
#Averaging mode enabled *Use this only if diode is stable 
D_AVG_ON = True 
D_AVG_OFF = False 
  
#Excitation Current Settins 
D_10UA = 0b00 
D_20UA = 0b01 
D_40UA = 0b10 
D_80UA = 0b11


"""RTD CONFIGURATION"""

#RTD type
PT_10 = 0b01010
PT_50 = 0b01011
PT_100 = 0b01100
PT_1000 = 0b01111

#RSENSE Assignment
CH2_1 = 0b00010
CH3_2 = 0b00011
CH4_3 = 0b00100
CH5_4 = 0b00101
CH6_5 = 0b00110

#Wire
WIRE_2 = 0b00
WIRE_3 = 0b01

#Mode
Ext = 0b00
Int = 0b01

#Ex_curr
C_EXT = 0b0000
C_5uA = 0b0001
C_10uA = 0b0010
C_25uA = 0b0011
C_50uA = 0b0100
C_100uA = 0b0101
C_250uA = 0b0110
C_500uA = 0b0111
C_1000uA = 0b1000

#Standard
Europa = 0b00
American = 0b01
Japan = 0b10