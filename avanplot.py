import serial
import matplotlib.pyplot as plt
import numpy as np

ser = serial.Serial('COM10', 9600)
ser.flush()
print(str(ser) + '\n')

getA = b'TAA?\r\n'
print (getA)

x = 1
y = []
ser.write(getA)
s = ser.read(701*6+20)

for fc in range(0,20):
     print(s[fc],'\n')
     if ((s[fc] != 17) and (s[fc] != 19)):
        break

print(fc, s[fc], '\n')
     
for i in range(0,701):
    y.append(float((s[i*6+0+fc]-48)*1000 +
                   (s[i*6+1+fc]-48)*100  +
                   (s[i*6+2+fc]-48)*10   +
                   (s[i*6+3+fc]-48))/34)

print(y[0], '\n')
print(y[1], '\n')
print(y[2], '\n')
print(y[700], '\n')

fig = plt.figure()
ax = fig.gca()
plt.xlim(xmin=0)
plt.ylim(ymin=0)
ax.set_xticks(np.arange(0,11,1))
ax.set_yticks(np.arange(0,11,1))
plt.grid()

##plt.scatter([ x/70.1 for x in range(len(y))] ,y,s=1)
plt.plot([ x/70.1 for x in range(len(y))] ,y)

plt.show()
