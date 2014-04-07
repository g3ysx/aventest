import serial
import matplotlib.pyplot as plt
import numpy as np
import re

def getATT(ser):
    ser.write(b'ATT?\r\n')
    s = str(ser.read(20).decode('utf8'))
    print('1',s)
    s = re.sub('[\x11\x13\r\n AT]','',s)
    print ('2',s)
    s = 'ATT:' + str(int(float(s)))
    print(s)
    return s


ser = serial.Serial('COM10', 9600)

print('--' + getATT(ser) + '--\n')

#Ref = REF? then decode hdr for units
#/div = 0:10, 1:5, 2:2, 3:1 WARNING when peak is on or multi marker mult double db
#Atten = ATT?
#start = SRT?
#Stop = STP?
#Center = CF
#Span =  SP?
#RBW = RBW?
#VBW = VBW?
#SWP = SWP?


