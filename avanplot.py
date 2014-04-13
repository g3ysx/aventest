##<Plots the output from an Avantest U4342 Spectrum
##Analyser (C) <2014  Stewart Bryant
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import serial
import matplotlib.pyplot as plt
import numpy as np
import re
import time
import datetime
    
def printLic():
    print("Avanplot Copyright (C) 2014 Stewart Bryant")
    print("This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.")
    print("This is free software, and you are welcome to redistribute it")
    print("under certain conditions.")
    print()

## Open the serial port - the name of the serial port is text
## file serialport.txt which must be in the current directory.
    
def serialOpen():
    sf = 'serialport.txt'
    f=open(sf, 'r')
    sp = f.readline().strip('\n')
    f.close()
    print('Serial Port is:' + sp)
    f.close()
    ser = serial.Serial(sp, 9600)
    print(ser)
    return ser


## Get the parameter specified in paramStr. This will be in bytes
## so convert to 16 bit chars now used by Python.
## Then strip the control chars, and in some cases the header
## returned by the instrument.           

def getParam(ser,paramStr,regStr):
    ser.write((paramStr + '?\r\n').encode('utf8'))
    s = ser.read(50).decode('utf8')
    s = re.sub('[\x11\x13\r\n ' + regStr + ']', '', s)
    return s
            
## Get Atenuation
            
def getATT(ser):
    p = getParam(ser, 'ATT', 'AT')
    s = 'Atten:' + str(int(float(p))) + 'dB'
    print(s)
    return s

## Get the reference level, then parse it to find the units
            
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

## Convert the frequency in Hz to more readable
## KHz, MHz, or GHz if appropriate
            
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

## Get Start Frequency

def getSRT(ser):
    s = getParam(ser, 'SRT', 'FA')   
    s = 'Start:' + f2fu(s)
    print(s)
    return s

## Get Stop Frequency
            
def getSTP(ser):
    s = getParam(ser, 'STP', 'FB')       
    s = 'Stop:' + f2fu(s)
    print(s)
    return s

## Get Center Frequency
            
def getCF(ser):
    s = getParam(ser, 'CF', 'CF')       
    s = 'Center:' + f2fu(s)
    print(s)
    return s

## Get Frequency Span
            
def getSP(ser):
    s = getParam(ser, 'SP', 'SP')     
    s = 'Span:' + f2fu(s)
    print(s)
    return s

## Get Resolution Bandwidth
            
def getRBW(ser):
    s = getParam(ser, 'RBW', 'RB')       
    s = 'RBW:' + f2fu(s)
    print(s)
    return s

## Get Video Bandwidth
            
def getVBW(ser):
    s = getParam(ser, 'VBW', 'VB')     
    s = 'VBW:' + f2fu(s)
    print(s)
    return s

## Get Sweep time and convert to ms if appropriate
            
def getSWP(ser):
    s = getParam(ser, 'SWP', 'SW')   
    sw = float(s)
    if sw >= 1:
        s = 'Sweep:' + str(sw) + 's'
    else:
        s = 'Sweep:' + str(sw*1000) + 'ms'
    print(s)
    return(s)

## Get the y units

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


## Start of main
            
printLic()

## Open serial port
            
ser = serialOpen()
ser.flush()

## Get test parameters startng with the time
            
when = datetime.datetime.now().strftime('%d-%m-%y@%H:%M')

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

## Get Trace A
## This is 701 x points with values 0..340
## This will be plotted on a fixed 0..10 to match the
## instrument screen.
##
            
x = 1
y = []
getA = b'TAA?\r\n'
ser.write(getA)
s = ser.read(701*6+40)

## Remove the pseky xon/xoff bytes
## We do this by hand becsue we are operating on a byte string
## in a future version must try converting to 16bit chars and
## using reg exp           

for fc in range(0,40):
    if ((s[fc] != 17) and (s[fc] != 19)):
        break

## fc is the first non-xon-xoff
## we convert this to an arry of y values for plotting
## The -10 offsets the display which has 0 at the top
## and -10 at the bottom
            
for i in range(0,701):
    y.append(float((s[i*6+0+fc]-48)*1000 +
                   (s[i*6+1+fc]-48)*100 +
                   (s[i*6+2+fc]-48)*10 +
                   (s[i*6+3+fc]-48))/34 -10)

## Create the graph, set up the limits, labels and ticks and then
## add the grid           
            
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

## Now plot the graph scalling the 701 points on the 0..10
## x axis
            
plt.plot([ x/70.1 for x in range(len(y))], y)

## Now print out the title bar
            
plt.title('Time:' + when + '\n' +
          refStr + ', ' + attStr + '   ' + divStr)

## Now put the rest of the parameters at the bottom of the display
            
plt.xlabel(srtStr + ', ' + stpStr + '\n' +
           cfStr  + ', ' + spStr  + '\n' +
           rbwStr + ', ' + vbwStr + ', ' + swpStr)

## Now plot the output to a pop-up window.
## The plot window will give the opportunity to save the display
## to disk
            
plt.show()









plt.show()
