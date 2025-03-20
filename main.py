import time
import numpy as np
import RPi.GPIO as io
from app import FlaskServer

readSequence = [(0,0,0),
                (0,0,1),
                (0,1,0),
                (0,1,1),
                (1,0,0),
                (1,0,1)]

def configure():
    try:
        # Pin definitions
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
        io.setup(pinDict['col2'], io.OUT, initial = io.HIGH) 
        io.setup(pinDict['col3'], io.OUT, initial = io.LOW) 
        
        print('finished setup')
        return pinDict
    except Exception as e:
        print('encountered error during board startup')

def sense(pinDict):
    inputV = np.zeros(6)
    for i, vals in enumerate(readSequence):
        io.output(pinDict['rowSelect1'],vals[0])
        io.output(pinDict['rowSelect2'],vals[1])
        io.output(pinDict['rowSelect3'],vals[2])
        #print('vals set')
        time.sleep(.15)
        inputV[i-1] = io.input(pinDict['voltageRead'])
        #print(f'Read: {inputV[i-1]}')
        time.sleep(.15)
    print(f'READ: {inputV}')

    if inputV[1] == 0:
        return 0
    else:
        return -1

def main():
    # create server object
    flask = FlaskServer()
    
    # start server in discrete thread
    flask.run()

    print("Flask application running...")

    # configure board layout
    pinDict = configure()

    print("Board has been cofigured")
    # main app loop, placeholder for sensor arbitration
    try:
        count = 0
        while True:
            time.sleep(1)
            result = sense(pinDict)
            message = f"{result}"
            print(f"Sample {count} Pressure: {message}")
            flask.send_message("update_zone", {"data": message})
            count += 1
    except KeyboardInterrupt:
        print("Shutting down...") # expand to ensure clean shutdown
        for pin in pinDict:
            if pin=='voltageRead':
                continue
            io.output(pinDict[pin], io.LOW)

if __name__ == "__main__":
    main()