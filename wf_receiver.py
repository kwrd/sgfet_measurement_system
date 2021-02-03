from ctypes import *
from dwfconstants import *
import time
import matplotlib.pyplot as plt
import sys

import numpy
import datetime
import csv

def receiver_run(wavefrq, trglevel):
    if sys.platform.startswith("win"):
        dwf = cdll.dwf
    elif sys.platform.startswith("darwin"):
        dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
    else:
        dwf = cdll.LoadLibrary("libdwf.so")

    hdwf = c_int()
    sts = c_byte()
    rgdSamples = (c_double*8192)()
    acqhz = 100000000.0
    
    version = create_string_buffer(16)
    dwf.FDwfGetVersion(version)
    print("DWF Version: "+str(version.value))

    print("Opening first device")
    dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))
  
    if hdwf.value == hdwfNone.value:
        szError = create_string_buffer(512)
        dwf.FDwfGetLastErrorMsg(szError);
        print("failed to open device\n"+str(szError.value))
        quit()
    
    dwf.FDwfAnalogInFrequencySet(hdwf, c_double(acqhz))
    dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(8192)) 
    dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_bool(True))
    dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(0), c_double(5))

    dwf.FDwfAnalogInTriggerAutoTimeoutSet(hdwf, c_double(0))
    dwf.FDwfAnalogInTriggerSourceSet(hdwf, trigsrcDetectorAnalogIn)
    dwf.FDwfAnalogInTriggerTypeSet(hdwf, trigtypeEdge)
    dwf.FDwfAnalogInTriggerChannelSet(hdwf, c_int(0))
    dwf.FDwfAnalogInTriggerLevelSet(hdwf, c_double(trglevel))
    dwf.FDwfAnalogInTriggerConditionSet(hdwf, trigcondRisingPositive) 

    time.sleep(2)

    print("Starting repeated acquisitions")
    dwf.FDwfAnalogInConfigure(hdwf, c_bool(False), c_bool(True))
    
    for iTrigger in range(10):
        while True:
            dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
            if sts.value == DwfStateDone.value :
                break
            time.sleep(0.001)
        
        dwf.FDwfAnalogInStatusData(hdwf, 0, rgdSamples, 8192)
        dc = sum(rgdSamples)/len(rgdSamples)
        print("Acquisition #"+str(iTrigger)+" average: "+str(dc)+"V")
    _create_graph(rgdSamples, wavefrq, acqhz)
    _create_csv(rgdSamples, wavefrq, acqhz)
    dwf.FDwfDeviceCloseAll()

def _create_graph(rgdSamples, wavefrq, acqhz):
    fig = plt.figure(figsize = (6, 6))
    ax = fig.add_subplot(111,xlabel="time(s)", ylabel='voltage(V)')
    ax.set_title(_hz_name_formater(wavefrq), size = 16)
    ax.plot([(t/acqhz) for t in range(8192) ],numpy.fromiter(rgdSamples, dtype=numpy.float))
    samplelim = (acqhz/wavefrq)*2.4
    ax.set_xlim(0, samplelim/acqhz)
    name =  _hz_name_formater(wavefrq) + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fig.savefig("graph/{}.jpg".format(name))
    print("save graph/{}".format(name))
    
def _create_csv(rgdSamples, wavefrq, acqhz):
    name = _hz_name_formater(wavefrq) + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('csv/{}.csv'.format(name), 'w') as f:
        writer = csv.writer(f)
        for i,v in enumerate(rgdSamples):
            writer.writerow([i/acqhz,v])
        print("Complete save the CSV {}".format(name))

def _hz_name_formater(wavefrq):
    if wavefrq//1000000 >= 1:
        return "{}MHz".format(str(wavefrq//1000000))
    if wavefrq//1000 >= 1:
        return "{}kHz".format(str(wavefrq//1000))
    return "{}Hz".format(str(wavefrq))
