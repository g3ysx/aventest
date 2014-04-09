import serial
import matplotlib.pyplot as plt
import numpy as np
import re

def getParam(ser,paramStr,regStr):
    ser.write((paramStr + '?\r\n').encode('utf8'))
    s = ser.read(40).decode('utf8')
    s = re.sub('[\x11\x13\r\n ' + regStr + ']', '', s)
    return s

def getATT(ser):
    s = 'Atten:' + str(int(float(getParam(ser, 'ATT', 'AT')))) + 'dB'
    return s

def getREF(ser):
    s = getParam(ser, 'REF', 'R')
    if s[1] == 'B':
        u = 'dBm'
    elif s[1] == 'M':
        u = 'dBmV'
    elif s[1] == 'U':
        u = 'dBuV'
    elif s[1] == 'E':
        u = 'dBuVemf'
    elif s[1] == 'P':
        u = 'dBpW'
    elif s[1] == 'V':
        u = 'V'
    elif s[1] == 'W':
        u = 'W'
    else:
        u = 'UNDEFINED'
    s = s.replace(s[:2], '')
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
    s = getParam(ser, 'SRT', 'FA')   
    s = 'Start:' + f2fu(s)
    return s

def getSTP(ser):
    s = getParam(ser, 'STP', 'FB')       
    s = 'Stop:' + f2fu(s)
    return s

def getCF(ser):
    s = getParam(ser, 'CF', 'CF')       
    s = 'Center:' + f2fu(s)
    return s

def getSP(ser):
    s = getParam(ser, 'SP', 'SP')     
    s = 'Span:' + f2fu(s)
    return s

def getRBW(ser):
    s = getParam(ser, 'RBW', 'RB')       
    s = 'RBW:' + f2fu(s)
    return s

def getVBW(ser):
    s = getParam(ser, 'VBW', 'VB')     
    s = 'VBW:' + f2fu(s)
    return s

def getSWP(ser):
    s = getParam(ser, 'SWP', 'SW')   
    sw = float(s)
    if sw >= 1:
        return 'Sweep:' + str(sw) + 's'
    else:
        return 'Sweep:' + str(sw*1000) + 'ms'

def getDIV(ser):
    su = getParam(ser, 'UNIT', '')
    su = int(su)
    if su==6 or su==7:
        return 'LIN'
    s = getParam(ser, 'DIV', '')
    s = int(s)
    if s==0:
        return '10dB/'
    if s==1:
        return '5dB/'
    if s==2:
        return '2db/'
    if s==3:
        return '1db/'
    return 'UNKNOWN'


ser = serial.Serial('COM10', 9600)

print('--' + getATT(ser) + '--')
print('--' + getREF(ser) + '--')
print('--' + getSRT(ser) + '--')
print('--' + getSTP(ser) + '--')
print('--' + getCF(ser) + '--')
print('--' + getSP(ser) + '--')
print('--' + getRBW(ser) + '--')
print('--' + getVBW(ser) + '--')
print('--' + getSWP(ser) + '--')
print('--' + getDIV(ser) + '--')


#/div = 0:10, 1:5, 2:2, 3:1 WARNING when peak is on or multi marker mult double db
##need the date

