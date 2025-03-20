import time
import numpy as np
import RPi.GPIO as io

io.setmode(io.BOARD)

pinDict = { 'rowSelect1' : 8,
            'rowSelect2' : 10,
            'rowSelect3' : 12,
            'voltageRead' : 21,
            'muxEnable': 13,
            'col1': 36,
            'col2': 38,
            'col3': 40,
            'motorSelect1': 18,
            'motorSelect2': 22,
            'motorSelect3': 24,
            'motorSelect4': 26
        }

# General setup
io.setmode(io.BOARD)
io.setwarnings(False)

# Pin configurations
io.setup(pinDict['rowSelect1'], io.OUT, initial = io.LOW) 
io.setup(pinDict['rowSelect2'], io.OUT, initial = io.LOW) 
io.setup(pinDict['rowSelect3'], io.OUT, initial = io.LOW) 
io.setup(pinDict['voltageRead'], io.IN, pull_up_down = io.PUD_DOWN) # Default LOW (0)
io.setup(pinDict['muxEnable'], io.OUT, initial = io.LOW) 
io.setup(pinDict['motorSelect1'], io.OUT, initial = io.LOW) 
io.setup(pinDict['motorSelect2'], io.OUT, initial = io.LOW) 
io.setup(pinDict['motorSelect3'], io.OUT, initial = io.LOW)
io.setup(pinDict['motorSelect4'], io.OUT, initial = io.LOW)
io.setup(pinDict['col1'], io.OUT, initial = io.LOW) 
io.setup(pinDict['col2'], io.OUT, initial = io.LOW) 
io.setup(pinDict['col3'], io.OUT, initial = io.LOW) 
 
print('finished setup')

readSequence = [(0,0,0),
                (0,0,1),
                (0,1,0),
                (0,1,1),
                (1,0,0),
                (1,0,1)]

motorSequence = [(0,0,0),
                (0,0,1),
                (0,1,0),
                (1,0,0)]

inputV = np.zeros(6)
motorStatus = np.zeros(4)

try:
    while True:
        for j, column in enumerate(['col1', 'col2', 'col3']):
            io.output(pinDict[column], io.HIGH)
            time.sleep(.05)
            for i, vals in enumerate(readSequence):
                io.output(pinDict['rowSelect1'],vals[0])
                io.output(pinDict['rowSelect2'],vals[1])
                io.output(pinDict['rowSelect3'],vals[2])
                #print('vals set')
                time.sleep(.1)
                inputV[i-1] = io.input(pinDict['voltageRead'])
                #print(f'Read: {inputV[i-1]}')
                time.sleep(.1)
            print(f'READ: {inputV}')
            io.output(pinDict[column], io.LOW)
        for j, motor in enumerate(['motorSelect1','motorSelect4','motorSelect3','motorSelect4']):
            if (inputV[1] != 0):
                io.output(pinDict[motor],io.HIGH)
                motorStatus[j] = 1
                print(f'Vals set {motorStatus}')
                time.sleep(1)
                io.output(pinDict[motor],io.LOW)
                motorStatus[j] = 0
        time.sleep(.2)
        
except KeyboardInterrupt:
    print('Process ended')
