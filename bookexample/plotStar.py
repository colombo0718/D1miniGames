from machine import freq,SPI,Pin,PWM,ADC,Timer
import time
import LCD
from flaglib import *

# 螢幕初始設定
spi = SPI(1, baudrate=40000000, polarity=0, phase=0)
screen = LCD.LCD(spi, 15, 5, 0)
screen.init()
screen.clearLCD()

while True :
    x=randint(0,120)
    y=randint(0,160)
    color=screen.rgbcolor(randint(0,255),randint(0,255),randint(0,255))
    screen.drawPixel(x,y,color)
    time.sleep(.1)
