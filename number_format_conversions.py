def int_dec_convert(val):
    # 16 bit BNR
    # Bit count from left(0 bit-MSB) to right(15 bit - LSB)
    
    return '{0:016b}'.format(int(val))
int_dec_convert_vector = np.vectorize(int_dec_convert)  

def partial_converter(value,start_bit,end_bit):
    # Partial BNR
    # Bit count from left(0 bit-MSB) to right(31 bit-LSB)
    # Start bit - MSB
    # End bit - LSB
    
    value_in_bits = '{0:016b}'.format(int(value))[start_bit:end_bit]
    final_value = int(value_in_bits,2)
    return final_value
partial_converter_vector = np.vectorize(partial_converter)     
 
def join_two_16bit_to_32bit(value1,value2):
    # Join two 16 bit strings with value1 on left, value 2 on right
    # 0th bit- LSB - Value1 0th bit, 31st bit - MSB - Value 2 15thbit 
    
    value1_in_16bits = int_dec_convert_vector(value1)
    value2_in_16bits = int_dec_convert_vector(value2)
    value_in_32bits = np.char.add(value1_in_16bits,value2_in_16bits)
    return value_in_32bits;

join_two_16bit_to_32bit_vector = np.vectorize(join_two_16bit_to_32bit)  

def join_four_16bit_to_64bit(value1,value2,value3,value4):
    # Join four 16 bit strings with value1 on left, value 4 on right
    # 0th bit- LSB - Value1 0th bit, 63rd bit - MSB - Value 4 15thbit 
    
    value1_in_16bits = int_dec_convert_vector(value1)
    value2_in_16bits = int_dec_convert_vector(value2)
    value3_in_16bits = int_dec_convert_vector(value3)
    value4_in_16bits = int_dec_convert_vector(value4)
    
    value_5 = np.char.add(value1_in_16bits,value2_in_16bits)
    value_6 = np.char.add(value3_in_16bits,value4_in_16bits)
    value_in_64bits = np.char.add(value_5,value_6)
    return value_in_64bits;

join_four_16bit_to_64bit_vector = np.vectorize(join_four_16bit_to_64bit)  
      
def convert_16bit_2scomp_to_decimal(value,coeff):
    # BC1 Format
    # Input 16 bit binary string, count from left (0) to right (15)
    # Output is decimal number
    # Coeff is to multiple the number to get final engineering value
    
    value_in_16bits = '{0:016b}'.format(int(value))
    if value_in_16bits[0] == '0':
        return value*coeff;
    else:
        return (int(value_in_16bits[1:16],2) -2**15)* coeff;
        
convert_16bit_2scomp_to_decimal_vector = np.vectorize(convert_16bit_2scomp_to_decimal)  

def convert_32bit_2scomp_to_decimal(value,start_bit,end_bit,coeff):
    # BC2 Format
    # Input 32 bit binary string, count from left (0) to right (31)
    # Output is decimal number
    # Coeff is to multiple the number to get final engineering value
    
    if value[0] == '0':
        return int(value[start_bit:end_bit],2)*coeff;
    else:
        return (int(value[start_bit:end_bit],2)-2**(end_bit-1))*coeff;

convert_32bit_2scomp_to_decimal_vector = np.vectorize(convert_32bit_2scomp_to_decimal)

def convert_32bit_ieee754_to_decimal(value):
    # IEEE 754 Single precision Floating Point
    # Input - 32 bit binary string, count from left(0) to right(31)
    # Output is decimal number
    # 0th bit- sign
    # 1-9 th bits (8 bits) - Exponent
    # 10-31 bits (23 bits)- Fraction / Manitssa
    
    sign = pow(-1,int(value[0]))
    exponent=int(value[1:9],2)
    
    s=0;
    for x in range(9,31):
        s=s+2**(-1*(x-8))*int(value[x])
    
    fraction = 1+s;
    final_value = sign * 2**(exponent-127)*fraction;
    return final_value

convert_32bit_ieee754_to_decimal_vector = np.vectorize(convert_32bit_ieee754_to_decimal)


def convert_64bit_ieee754_to_decimal(value):
    # IEEE 754 Double precision Floating Point
    # Input - 64 bit binary string, count from left(0) to right(63)
    # Output is decimal number
    # 0th bit- sign
    # 1-12 th bits (11 bits) - Exponent
    # 13-63 bits (52 bits)- Fraction / Manitssa
    try:
        sign = pow(-1,int(value[0]))
        exponent=int(value[1:12],2)
        
        s=0;
        for x in range(12,63):
            s=s+2**(-1*(x-11))*int(value[x])
        
        fraction = 1+s;
        final_value = sign * 2**(exponent-1023)*fraction
        return final_value
    except:
        print('64 bit exception handled')
        return 0

convert_64bit_ieee754_to_decimal_vector = np.vectorize(convert_64bit_ieee754_to_decimal)
