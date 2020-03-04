import LCD
from machine import freq,SPI,Pin,PWM,ADC,Timer 
import time
# from FlagArcade import *

spi = SPI(1, baudrate=40000000, polarity=0, phase=0)
screen = LCD.LCD(spi, 15, 5, 0)
screen.init()
screen.clearLCD()

buzzer = PWM(Pin(12))
buzzer.freq(1000)

while True:
    buzzer.duty(100)
    time.sleep(.05)
    buzzer.duty(0)
    time.sleep(.95)
