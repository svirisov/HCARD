import os, time, traceback
import RPi.GPIO as io


def configure(self):
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
        io.setup(pinDict['voltageRead1'], io.IN, pull_up_down = io.PUD_UP) # Default high (1)
        io.setup(pinDict['voltageRead2'], io.IN, pull_up_down = io.PUD_UP) # Default high (1)
        io.setup(pinDict['voltageRead3'], io.IN, pull_up_down = io.PUD_UP) # Default high (1)

        return pinDict
    except Exception as ex:
        print('Device failed initial setup')
        print(traceback.format_exc())
    finally:
        io.cleanup() # Clean exit


def main(self):
    try:
        pinDict = configure()
        t = 0
        tlim = 100 # 5min timout

        while(t<tlim):
            io.output(pinDict['col1'], io.HIGH)
            io.output(pinDict['col2'], io.HIGH)
            io.output(pinDict['col3'], io.HIGH)

            time.sleep(5)

            io.output(pinDict['col1'], io.LOW)
            io.output(pinDict['col2'], io.LOW)
            io.output(pinDict['col3'], io.LOW)
    

    except Exception as ex:
        traceback.print_exc()

    finally:
        io.cleanup() #this ensures a clean exit


if __name__=='__main__':
    main()