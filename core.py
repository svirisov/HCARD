import os, time, traceback
import RPi.GPIO as io

def configure():
    try:
        # Pin definitions
        

        pinDict = { 'col1' : 23,
                    'col2' : 24,
                    'col3' : 25,
                    'rowSelect1' : 4,
                    'rowSelect2' : 5,
                    'rowSelect3' : 6,
                    'voltageRead1' : 26,
                    'voltageRead2' : 19,
                    'voltageRead3' : 16,
                    'motorSelect1' : 12,
                    'motorSelect2' : 13
                }

        # General setup
        io.setmode(io.BCM)
        io.setwarnings(False)

        # Pin configurations
        io.setup(pinDict['col1'], io.OUT, initial = io.LOW) 
        io.setup(pinDict['col2'], io.OUT, initial = io.LOW) 
        io.setup(pinDict['col3'], io.OUT, initial = io.LOW) 
        io.setup(pinDict['rowSelect1'], io.OUT, initial = io.LOW) 
        io.setup(pinDict['rowSelect2'], io.OUT, initial = io.LOW) 
        io.setup(pinDict['rowSelect3'], io.OUT, initial = io.LOW) 
        io.setup(pinDict['motorSelect1'], io.OUT, initial = io.LOW) 
        io.setup(pinDict['motorSelect2'], io.OUT, initial = io.LOW) 
        io.setup(pinDict['voltageRead1'], io.IN, pull_up_down = io.PUD_DOWN) # Default LOW (0)
        io.setup(pinDict['voltageRead2'], io.IN, pull_up_down = io.PUD_DOWN) # Default LOW (0)
        io.setup(pinDict['voltageRead3'], io.IN, pull_up_down = io.PUD_DOWN) # Default LOW (0)

        return pinDict
    except Exception as ex:
        print('Device failed initial setup')
        print(traceback.format_exc())

def readSensorMatrix(pinDict, pressureHist):
    warningZone = -1

    # Pin select values for multiplexer
    readSequence = [(0,0,0),
                    (0,0,1),
                    (0,1,0),
                    (0,1,1),
                    (1,0,0),
                    (1,0,1),
                    (1,1,1)]

    v1,v2,v3 = 0 # Voltage readings
    measurements = []

    # Take readings
    for j, column in enumerate(['col1', 'col2', 'col3']):
        io.output(pinDict['col1'], io.HIGH)

        time.sleep(.1) # Allow for voltage rise time (tbd)

        for i, values in enumerate(readSequence): # Inline conditionals to be confirmed functionally
            io.output(pinDict['rowSelect1'], io.HIGH if (values(0)==1) else io.LOW)
            io.output(pinDict['rowSelect2'], io.HIGH if (values(1)==1) else io.LOW)
            io.output(pinDict['rowSelect3'], io.HIGH if (values(2)==1) else io.LOW)
        
            time.sleep(.1) # Allow for voltage rise time (tbd)
            
            v1 = io.input(pinDict['voltageRead1'])
            v2 = io.input(pinDict['voltageRead2'])
            v3 = io.input(pinDict['voltageRead3'])
            vValue = f'{v1}{v2}{v3}' # 3-bit breakdown of voltage value
            voltLevel = int(vValue) # Convert to numeric voltage level 

            measurements[i,j] = voltLevel
    
    # Compare to history
    
    for j, _ in enumerate(['col1', 'col2', 'col3']): 
        for i, _ in enumerate(readSequence):
            for meas in pressureHist[-10:]: # last 10 pressure meas, needs confirmation for which part of matrix is pulled
                if (abs(measurements[i,j]-meas[i,j])>2):
                    continue # Detected non-static pressure, check next sample point
            warningZone = [i,j] # Log warning if no pressure change detected

    pressureHist.append(measurements) # Add to end of history

    return pressureHist, warningZone

def main():
    try:
        pinDict = configure()
        t = 0
        tlim = 100 # 5min timout

        pressureHist = []

        ## TEST CODE FOR PIN VALIDATION
        while(t<tlim): # while(True):
            io.output(pinDict['col1'], io.HIGH)
            io.output(pinDict['col2'], io.HIGH)
            io.output(pinDict['col3'], io.HIGH)

            time.sleep(5)

            io.output(pinDict['col1'], io.LOW)
            io.output(pinDict['col2'], io.LOW)
            io.output(pinDict['col3'], io.LOW)

            t += 1 # Increment to hit timeout

            # pressureHist, warningZone = readSensorMatrix(pinDict, pressureHist)
            # buzzHaptics(warningZone)
            # time.sleep(1)

    except Exception as ex:
        traceback.print_exc()

    finally:
        io.cleanup() #this ensures a clean exit
        # file delete for pressure hist if storing in .csv


if __name__=='__main__':
    main()