import os, time, traceback
import RPi.GPIO as io

def configure():
    try:
        # Pin definitions
        

        pinDict = { 'col1' : 8,
                    'col2' : 10,
                    'col3' : 12,
                    'rowSelect1' : 3,
                    'rowSelect2' : 5,
                    'rowSelect3' : 7,
                    'voltageRead1' : 29,
                    'voltageRead2' : 31,
                    'voltageRead3' : 33,
                    'motorSelect1' : 38,
                    'motorSelect2' : 40,
                    'muxEnable': 16
                }

        # General setup
        io.setmode(io.BOARD)
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
        io.setup(pinDict['muxEnable'], io.OUT, initial = io.LOW) 

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

def readVoltage(pinDict):
    v1 = io.input(pinDict['voltageRead1'])
    v2 = io.input(pinDict['voltageRead2'])
    v3 = io.input(pinDict['voltageRead3'])
    voltage = f'Read - {v1}{v2}{v3}'
    return voltage

def main():
    try:
        pinDict = configure()
        t = 0
        tlim = 20 # 1min timout
        print('Completed setup')

        pressureHist = []

        readSequence = [(0,0,0),
                        (0,0,1),
                        (0,1,0),
                        (0,1,1),
                        (1,0,0),
                        (1,0,1),
                        (1,1,1)]

        ## TEST CODE FOR PIN VALIDATION
        for _ in range(0,60): # while(True):
            for entry in readSequence:
                io.output(pinDict['col1'], entry[0])
                io.output(pinDict['col2'], entry[1])
                io.output(pinDict['col3'], entry[2])
                time.sleep(.1)
                print(f'set select to  {entry[0]}{entry[1]}{entry[2]}')
                print(readVoltage(pinDict))
                time.sleep(10)

            #t += 1 # Increment to hit timeout

            # pressureHist, warningZone = readSensorMatrix(pinDict, pressureHist)
            # buzzHaptics(warningZone)
            # time.sleep(1)

    except KeyboardInterrupt:
        print('Performance terminated by user')

    except Exception as ex:
        traceback.print_exc()

    finally:
        io.cleanup() #this ensures a clean exit
        # file delete for pressure hist if storing in .csv


if __name__=='__main__':
    main()