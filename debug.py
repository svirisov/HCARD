import time
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
            'motorSelect1': 27,
            'motorSelect2': 29,
            'motorSelect3': 31
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
#io.setup(pinDict['motorSelect1'], io.OUT, initial = io.LOW) 
io.setup(pinDict['motorSelect2'], io.OUT, initial = io.LOW) 
io.setup(pinDict['motorSelect3'], io.OUT, initial = io.LOW) 
io.setup(pinDict['col1'], io.OUT, initial = io.LOW) 
io.setup(pinDict['col2'], io.OUT, initial = io.HIGH) 
io.setup(pinDict['col3'], io.OUT, initial = io.LOW) 
 
print('finished setup')

readSequence = [(0,0,0),
                (0,0,1),
                (0,1,0),
                (0,1,1),
                (1,0,0),
                (1,0,1),
                (1,1,1)]

motorSequence = [(0,0,0),
                 (0,0,1),
                 (0,1,0),
                 (0,1,1),
                 (0,1,0),
                 (0,0,1),
                 (0,0,0)]

try:
    while True:
        for i, vals in enumerate(readSequence):
            io.output(pinDict['rowSelect1'],vals[0])
            io.output(pinDict['rowSelect2'],vals[1])
            io.output(pinDict['rowSelect3'],vals[2])
            print('vals set')
            time.sleep(.1)
            input = io.input(pinDict['voltageRead'])
            print(f'Read: {input}')
            time.sleep(.2)
            io.output(pinDict['motorSelect2'],motorSequence[i,1])
            io.output(pinDict['motorSelect3'],motorSequence[i,2])
except KeyboardInterrupt:
    print('Process ended')
