import time
import board
import analogio
import digitalio
import neopixel

a5 = analogio.AnalogIn(board.AIN5) #P0_29
a7 = analogio.AnalogIn(board.AIN7) #P0_31

gpout = digitalio.DigitalInOut(board.P0_02).switch_to_output(True) # row0
gpin = digitalio.DigitalInOut(board.P0_24) #col0
gpin.switch_to_input(pull=digitalio.Pull.DOWN)

printtype = 'neopixel'

if printtype == 'neopixel':
    pixel_pin = board.P0_06
    num_pixels = 29
    npx = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=.05)

i = 0
while True:
    if printtype == 'v':
        a5v = a5.reference_voltage*a5.value*2**-16
        a7v = a7.reference_voltage*a7.value*2**-16
        print(f'a5,7: {a5v:.3f} {a7v:.3f}')
    elif printtype == '12bit':
        a5v = a5.value//16
        a7v = a7.value//16
        print(f'a5,7: {a5v:04} {a7v:04}')
    elif printtype == 'raw':
        print(f'a5,7: {a5.value:05} {a7.value:05}')
    elif printtype == 'neopixel':
        if i % 2 == 0:
            print('npx on')
            npx.fill((100, 0, 255))
        else:
            print('npx off')
            npx.fill((0, 0, 0))
    else:
        print('gpio is', gpin.value)
    time.sleep(.1)
    i += 1

# 5/29 is Y, observed range in 12bit is roughly 4030 - ~0 for down-up
# 7/31 is X, observed range in 12bit is roughly 0 - 4040 for left-right
# for both it seems like 4000 is more the limit unless you brush around a bit