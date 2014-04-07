import serial
import matplotlib.pyplot as plt
import numpy as np

ser = serial.Serial('COM10', 9600)
print(str(ser) + '\n')

print('--', getATT(ser), '--\n')

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

def getATT(ser):
    ser.write(b'ATT?\r\n')
    return(ser.read(20,1))
