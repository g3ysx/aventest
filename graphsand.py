import serial
import matplotlib.pyplot as plt
import numpy as np



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

plt.title('Ref = xdB   xxdB/    Atten = ydB')

plt.xlabel('Start:xxxxxxMHz, Stop:yyyyyyMHz\n'+
          'Center:xxxxxxMHz, Span:yyyyyyMHz\n'+
          'RBW:xxxKHz VBW:yyyKHz SWP:zzms')

          


##plt.scatter([ x/70.1 for x in range(len(y))] ,y,s=1)
#plt.plot([ x/70.1 for x in range(len(y))] ,y)

plt.show()
