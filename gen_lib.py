#Felix Kaelin 
#05.03.2020 
#Library for ltc2983 in python 
#build for IPA 2020

def gen_transaction(buff, trans_type, address, data):
    buff = 0
    t_buff = [0]*4
    t_buff[3] = trans_type
    t_buff[1] = address & 0xff
    t_buff[2] = (address >> 8) & 0xff
    t_buff[0] = data
    
    for i in range(4):
        buff |= t_buff[i] << (i*8)
    return buff

def or_mask_gen(value, bit_pos):
    return(value << bit_pos)


