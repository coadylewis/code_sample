#!/usr/bin/env python

from threading import Thread
import serial
import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import pandas as pd
import numpy as np
from scipy.fftpack import fft
from tkinter import TclError


CHUNK = 65536 * 2
RATE = 115200
CHANNELS = 2



class serialPlot:
    def __init__(self, serialPort = 'COM5', serialBaud = 115200, plotLength = 150, dataNumBytes = 1):
        self.port = serialPort
        self.baud = serialBaud
        self.plotMaxLength = plotLength
        self.dataNumBytes = dataNumBytes
        self.rawData = bytearray(dataNumBytes)
        self.data = collections.deque([0] * plotLength, maxlen=plotLength)
        self.isRun = True
        self.isReceiving = False
        self.thread = None
        self.plotTimer = 0
        self.previousTimer = 0
        self.csvData = []


        print('Trying to connect to: ' + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')
        try:
            self.serialConnection = serial.Serial(serialPort, serialBaud, timeout=4)
            print('Connected to ' + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')
        except:
            print("Failed to connect with " + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')

    def readSerialStart(self):
        if self.thread == None:
            self.thread = Thread(target=self.backgroundThread)
            self.thread.start()
            # Block till we start receiving values
            while self.isReceiving != True:
                time.sleep(0.1)

    def getSerialData(self, frame, lines, lineValueText, lineLabel, timeText):
        currentTimer = time.perf_counter()
        self.plotTimer = int((currentTimer - self.previousTimer) * 1000)     # the first reading will be erroneous
        self.previousTimer = currentTimer
        timeText.set_text('Plot Interval = ' + str(self.plotTimer) + 'ms')
        value_full = struct.unpack('cxcc', self.rawData)
        float_val=0.0
        for i in range(len(value_full)):
            float_val += int(value_full[i])/ (10**i)
        #value,  = struct.unpack('f', self.rawData)    # use 'h' for a 2 byte integer
        self.data.append(float_val)    # we get the latest data point and append it to our array
        lines.set_data(range(self.plotMaxLength), self.data)
        lineValueText.set_text('[' + lineLabel + '] = ' + str(float_val))
        self.csvData.append(self.data[-1])

    def backgroundThread(self):    # retrieve data
        time.sleep(1.0)  # give some buffer time for retrieving data
        self.serialConnection.reset_input_buffer()
        while (self.isRun):
            self.serialConnection.readinto(self.rawData)
            self.isReceiving = True
            print(self.rawData)
            value_full = struct.unpack('cxcc', self.rawData)
            float_val=0.0
            for i in range(len(value_full)):
                float_val += int(value_full[i])/ (10**i)
            print(float_val)
            print('\n')

    def close(self):
        self.isRun = False
        self.thread.join()
        self.serialConnection.close()
        print('Disconnected...')
        df = pd.DataFrame(self.csvData)
        df.to_csv('/OneDrive/School/Spring 2022/ECEN 404/Project Programs/data.csv')


def main():
    portName = 'COM5'
    baudRate = 115200
    maxPlotLength = 150
    dataNumBytes = 4       # number of bytes of 1 data point
    s = serialPlot(portName, baudRate, maxPlotLength, dataNumBytes)   # initializes all required variables
    s.readSerialStart()                                               # starts background thread

    # plotting starts below
    pltInterval = 50    # Period at which the plot animation updates [ms]
    xmin = 0
    xmax = maxPlotLength
    ymin = -(1)
    ymax = 1
    fig, (ax1, ax2) = plt.subplots(2, figsize=(15,7))

    #variables for plotting
    x = np.arange(0, 2 * CHUNK, 2)
    xf = np.linspace(0, RATE, CHUNK)

    #format wave axes
    ax1.set_title('Arduino Analog Read')
    ax1.set_xlabel("time")
    ax1.set_ylabel("AnalogRead Value")
    ax1.set_ylim(-0.5, 1.5)
    ax1.set_xlim(0, 150)
    #plt.setp(ax1, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])

    #format spectrum axes
    ax2.set_xlim(0, 150)

    lineLabel = 'Output Voltage'
    timeText = ax1.text(0.50, 0.95, '', transform=ax1.transAxes)
    lines = ax1.plot([], [], label=lineLabel)[0]
    lineValueText = ax1.text(0.50, 0.90, '', transform=ax1.transAxes)
    anim = animation.FuncAnimation(fig, s.getSerialData, fargs=(lines, lineValueText, lineLabel, timeText), interval=pltInterval)    # fargs has to be a tuple

    plt.legend(loc="upper left")
    plt.show()

    s.close()

    # for measuring frame rate
    frame_count = 0
    start_time = time.time()


if __name__ == '__main__':
    main()