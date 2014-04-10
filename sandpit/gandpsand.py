import serial
import matplotlib.pyplot as plt
import numpy as np
import re
import time
import datetime


def getParam(ser,paramStr,regStr):
    ser.write((paramStr + '?\r\n').encode('utf8'))
    s = ser.read(50).decode('utf8')
    s = re.sub('[\x11\x13\r\n ' + regStr + ']', '', s)
    return s

def getATT(ser):
    p = getParam(ser, 'ATT', 'AT')
    s = 'Atten:' + str(int(float(p))) + 'dB'
    print(s)
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
    print(s)
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
    s = str(f)+u
    return(s)


def getSRT(ser):
    s = getParam(ser, 'SRT', 'FA')   
    s = 'Start:' + f2fu(s)
    print(s)
    return s

def getSTP(ser):
    s = getParam(ser, 'STP', 'FB')       
    s = 'Stop:' + f2fu(s)
    print(s)
    return s

def getCF(ser):
    s = getParam(ser, 'CF', 'CF')       
    s = 'Center:' + f2fu(s)
    print(s)
    return s

def getSP(ser):
    s = getParam(ser, 'SP', 'SP')     
    s = 'Span:' + f2fu(s)
    print(s)
    return s

def getRBW(ser):
    s = getParam(ser, 'RBW', 'RB')       
    s = 'RBW:' + f2fu(s)
    print(s)
    return s

def getVBW(ser):
    s = getParam(ser, 'VBW', 'VB')     
    s = 'VBW:' + f2fu(s)
    print(s)
    return s

def getSWP(ser):
    s = getParam(ser, 'SWP', 'SW')   
    sw = float(s)
    if sw >= 1:
        s = 'Sweep:' + str(sw) + 's'
    else:
        s = 'Sweep:' + str(sw*1000) + 'ms'
    print(s)
    return(s)

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
ser.flush()

when = datetime.datetime.now().strftime('%d-%m-%y@%H:%M')

fig = plt.figure()
fig.subplots_adjust(bottom=0.2)
ax = fig.gca()
plt.xlim(xmin=0)
plt.xlim(xmax=10)
plt.ylim(ymin=-10)
plt.ylim(ymax=0)
ax.set_xticks(np.arange(0,11,1))
ax.set_yticks(np.arange(-10,1,1))
plt.grid()

refStr = getREF(ser)
attStr = getATT(ser)
divStr = getDIV(ser)
print(divStr)
srtStr = getSRT(ser)
stpStr = getSTP(ser)
cfStr  = getCF(ser)
spStr  = getSP(ser)
rbwStr = getRBW(ser)
vbwStr = getVBW(ser)
swpStr = getSWP(ser)

plt.title('Time:' + when + '\n' +
          refStr + ', ' + attStr + '   ' + divStr)

plt.xlabel(srtStr + ', ' + stpStr + '\n' +
           cfStr  + ', ' + spStr  + '\n' +
           rbwStr + ', ' + vbwStr + ', ' + swpStr)

plt.show()


