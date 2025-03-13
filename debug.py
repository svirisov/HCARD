import time
import RPi.GPIO as io

io.setmode(io.BOARD)

pinDict = { 'rowSelect1' : 8,
            'rowSelect2' : 10,
            'rowSelect3' : 12,
            'voltageRead' : 3,
            'muxEnable': 22,
            'col1': 16
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

io.setup(pinDict['col1'], io.OUT, initial = io.HIGH) 

print('finished setup')

readSequence = [(0,0,0),
                (0,0,1),
                (0,1,0)]

for i, vals  in enumerate(readSequence):
    io.output(pinDict['rowSelect1'],vals[0])
    io.output(pinDict['rowSelect2'],vals[1])
    io.output(pinDict['rowSelect3'],vals[2])
    print('vals set')
    time.sleep(30)
    input = io.input(pinDict['voltageRead'])
    print(f'{input}')
    time.sleep(5)