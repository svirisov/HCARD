import time
import RPi.GPIO as io

io.setmode(io.BOARD)

io.setup(8, io.IN, initial=io.LOW)

print('finished setup')

for i in range(0,5):
    io.output(8,1)
    print('high')
    time.sleep(5)
    io.output(8,0)
    print('low')