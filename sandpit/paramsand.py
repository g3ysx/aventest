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
    s = 'Attenuation:' + str(int(float(s))) + 'dB'
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
    s = 'Reference:' + str(float(s)) + u
    return s

def f2fu(s):
    f = float(s)
    if f<1000:
       u = 'Hz'
    elif f<1000000:
        f = f/1000
        u = 'KHz'
    elif f<1000000000:
        f = f/1000000
        u = 'MHz'
    else:
        f = f/1000000000
        u = 'GHz'
    return str(f)+u

def getSRT(ser):
    ser.write(b'SRT?\r\n')
    s = str(ser.read(40).decode('utf8'))
    print('1',s)
    s = re.sub('[\x11\x13\r\n FA]','',s)
    print ('2',s)    
    s = 'Start:' + f2fu(s)
    print(s)
    return s

def getSTP(ser):
    ser.write(b'STP?\r\n')
    s = str(ser.read(40).decode('utf8'))
    print('1',s)
    s = re.sub('[\x11\x13\r\n FB]','',s)
    print ('2',s)    
    s = 'Stop:' + f2fu(s)
    print(s)
    return s

def getCF(ser):
    ser.write(b'CF?\r\n')
    s = str(ser.read(40).decode('utf8'))
    print('1',s)
    s = re.sub('[\x11\x13\r\n CF]','',s)
    print ('2',s)    
    s = 'Center:' + f2fu(s)
    print(s)
    return s

def getSP(ser):
    ser.write(b'SP?\r\n')
    s = str(ser.read(40).decode('utf8'))
    print('1',s)
    s = re.sub('[\x11\x13\r\n SP]','',s)
    print ('2',s)    
    s = 'Span:' + f2fu(s)
    print(s)
    return s

def getRBW(ser):
    ser.write(b'RBW?\r\n')
    s = str(ser.read(40).decode('utf8'))
    print('1',s)
    s = re.sub('[\x11\x13\r\n RB]','',s)
    print ('2',s)    
    s = 'RBW:' + f2fu(s)
    print(s)
    return s

def getVBW(ser):
    ser.write(b'VBW?\r\n')
    s = str(ser.read(40).decode('utf8'))
    print('1',s)
    s = re.sub('[\x11\x13\r\n VB]','',s)
    print ('2',s)    
    s = 'VBW:' + f2fu(s)
    print(s)
    return s

def getSWP(ser):
    ser.write(b'SWP?\r\n')
    s = str(ser.read(40).decode('utf8'))
    print('1',s)
    s = re.sub('[\x11\x13\r\n SW]','',s)
    print ('2',s)
    sw = float(s)
    if sw >= 1:
        return 'Sweep:' + str(sw) + 's'
    else:
        return 'Sweep:' + str(sw*1000) + 'ms'


ser = serial.Serial('COM10', 9600)

print('--' + getATT(ser) + '--\n')
print('--' + getREF(ser) + '--\n')
print('--' + getSRT(ser) + '--\n')
print('--' + getSTP(ser) + '--\n')
print('--' + getCF(ser) + '--\n')
print('--' + getSP(ser) + '--\n')
print('--' + getRBW(ser) + '--\n')
print('--' + getVBW(ser) + '--\n')
print('--' + getSWP(ser) + '--\n')


#/div = 0:10, 1:5, 2:2, 3:1 WARNING when peak is on or multi marker mult double db



