import sys
import math
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class _pulse:
    # class that stores data for a pulse

    def __init__(self,volt,tau):
        self.volt = volt
        self.tau = tau 

    def func(self,t,dx):
        f = ((self.volt/self.tau)*((t-dx)*(math.e**(-(t-dx)/self.tau))))
        if f < 0: f = 0
        return f
    
    def generate(self,x1,x2,res,dx):
        self.x = np.arange(x1,x2,(x2-x1)/res)
        self.y = []
        for i in np.arange(0,x2-x1,(x2-x1)/res):
            self.y.append(self.func(i,dx))

    def plot(self):
        plt.plot(self.x,self.y)

    def dataframe(self):
        data = {'x':self.x,'y':self.y}
        self.df = pd.DataFrame(data)
        return self.df
    
# ----------------------------------------------------------------------------------------------------------

# params
volt = 12
tau = 1
num = int(sys.argv[1])
res = 1000
x1 = 0
x2 = 100

# create list of objects
peaks = []
for i in range(num):
    peaks.append(_pulse(volt,tau))

# generate data for each
data = []
for peak in peaks:
    peak.generate(x1,x2,res,random.randint(0,int(x2*0.7)))
    data.append(peak.dataframe())

sum = 0
for peak in data:
    sum += peak['y']
pileup = pd.DataFrame({'x': peaks[0].df['x'], 'y': sum})

# ----------------------------------------------------------------------------------------------------------

fig, (ax1, ax2) = plt.subplots(2, 1)

for peak in peaks:
    peak = peak.df
    ax1.plot(peak['x'],peak['y'])

ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Output (Volts)')
ax1.set_title('Individual Peaks')

ax2.plot(pileup['x'], pileup['y'],color='red')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Output (Volts)')
ax2.set_title('Sum-Peaks "Pulse-Pileup"')

plt.tight_layout()
plt.show()
