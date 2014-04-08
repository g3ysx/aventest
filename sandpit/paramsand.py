import serial
import matplotlib.pyplot as plt
import numpy as np
import re

def getATT(ser):
    ser.write(b'ATT?\r\n')
    s = str(ser.read(30).decode('utf8'))
    print('1',s)
    s = re.sub('[\x11\x13\r\n AT]','',s)
    print ('2',s)
    s = 'ATT:' + str(int(float(s))) + 'dB'
    print(s)
    return s

def getREF(ser):
    ser.write(b'REF?\r\n')
    s = str(ser.read(30).decode('utf8'))
    print('1',s)
    s = re.sub('[\x11\x13\r\n R]','',s)
    if s[1] == 'B':
        u = ' dBm'
    elif s[1] == 'M':
        u = ' dBmV'
    elif s[1] == 'U':
        u = ' dBuV'
    elif s[1] == 'E':
        u = ' dBuVemf'
    elif s[1] == 'P':
        u = ' dBpW'
    elif s[1] == 'V':
        u = ' V'
    elif s[1] == 'W':
        u = ' W'
    else:
        u = 'UNDEFINED'
    print('units = ', u)
    s = s.replace(s[:2], '')
    print('2', s)
    s = 'REF:' + str(float(s)) + u
    return s

ser = serial.Serial('COM10', 9600)

print('--' + getATT(ser) + '--\n')
print('--' + getREF(ser) + '--\n')


#/div = 0:10, 1:5, 2:2, 3:1 WARNING when peak is on or multi marker mult double db
#start = SRT?
#Stop = STP?
#Center = CF
#Span =  SP?
#RBW = RBW?
#VBW = VBW?
#SWP = SWP?


