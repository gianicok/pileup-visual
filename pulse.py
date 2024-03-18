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
        f = ((self.volt/self.tau)*((t-dx)*(math.exp(-(t-dx)/self.tau))))
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

def create_peaks(freq,x2): 
    volt = 12
    tau = 8 # this is in microseconds
    
    peaks = []
    num = int((freq*1e6)/x2)

    print("Simulating",num,"peaks at",num/x2,"MHz")
    for i in range(num):
        peaks.append(_pulse(volt,tau))
    return peaks
    
def create_data(peaks,x2):  
    data = []
    res = 10000
    x1 = 0     # this is in microseconds
    for peak in peaks:
        peak.generate(x1,x2,res,random.uniform(0,x2))
        data.append(peak.dataframe())
    return data

def create_pileup(data):
    sum = 0
    for peak in data:
        sum += peak['y']
    pileup = pd.DataFrame({'x': peaks[0].df['x'], 'y': sum})
    return pileup

def plotter(peaks):
    fig, (ax1, ax2) = plt.subplots(2, 1)

    for peak in peaks:
        peak = peak.df
        ax1.plot(peak['x'],peak['y'])

    ax1.set_xlabel('Time (us)')
    ax1.set_ylabel('Output (Volts)')
    ax1.set_title('Individual Peaks')

    ax2.plot(pileup['x'], pileup['y'],color='red')
    ax2.set_xlabel('Time (us)')
    ax2.set_ylabel('Output (Volts)')
    ax2.set_title('Sum-Peaks "Pulse-Pileup"')

    plt.tight_layout()
    plt.show()

# ----------------------------------------------------------------------------------------------------------

#peaks = create_peaks(int(sys.argv[1]),1000)
peaks = create_peaks(1,1000) #hardcode for now
data = create_data(peaks,1000)
pileup = create_pileup(data)

plotter(peaks)
