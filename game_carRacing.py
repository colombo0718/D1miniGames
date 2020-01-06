import LCD
from machine import freq,SPI,Pin,PWM,ADC,Timer
import time
from flaglib import *

freq(160000000)

spi = SPI(1, baudrate=40000000, polarity=0, phase=0)
lcd = LCD.LCD(spi, 15, 5, 0)
lcd.init()
lcd.setRotation(4)
lcd.clearLCD()

adc = ADC(0)
button = Pin(4, Pin.IN, Pin.PULL_UP)
buzzer = PWM(Pin(12))

car_pixels_1=(
b"   1111111   "
b" 11111111111 "
b"     111     "
b" 1   111   1 "
b"1 1  111  1 1"
b" 1 1111111 1 "
b"1 1  111  1 1"
b" 1   1 1   1 "
b"    11 11    "
b"1 1 1   1 1 1"
b" 1  1   1  1 "
b"1 111 1 111 1"
b" 1  11111  1 "
b"1 1 11111 1 1"
b"    1   1    "
b"  111111111  "
b"1111111111111"
)
car_pixels_2=(
b"   1111111   "
b" 11111111111 "
b"     111     "
b"1 1  111  1 1"
b" 1   111   1 "
b"1 111111111 1"
b" 1   111   1 "
b"1 1  1 1  1 1"
b"    11 11    "
b" 1  1   1  1 "
b"1 1 1   1 1 1"
b" 1 11 1 11 1 "
b"1 1 11111 1 1"
b" 1  11111  1 "
b"    1   1    "
b"  111111111  "
b"1111111111111"
)



def toot():
    buzzer.duty(500)
    buzzer.freq(1000)
    time.sleep(.01)
    buzzer.duty(0)

def ding():
    buzzer.duty(500)
    buzzer.freq(500)
    time.sleep(.02)
    buzzer.freq(1000)
    time.sleep(.05)
    buzzer.freq(500)
    time.sleep(.03)
    buzzer.duty(0)
    
def buzz():
    buzzer.duty(500)
    buzzer.freq(200)
    time.sleep(.5)
    buzzer.duty(0)

toot()


# game parameter initialize
end=False
redCar = Character(
    (car_pixels_1,car_pixels_2), 13, 17, lcd, LCD.RED)
redCar.x=0
redCar.y=140
x0=0;x1=0
life=0

while True:
    redCar.xplot(x0,x1)
    key=getKey(adc.read())
    if key=='r':
        x1=x0+1
    if key=='l':
        x1=x0-1
    print(key)
    

    

