import LCD
from machine import freq,SPI,Pin,PWM,ADC,Timer
import time
from FlagArcade import *

# 螢幕初始設定
spi = SPI(1, baudrate=40000000, polarity=0, phase=0)
screen = LCD.LCD(spi, 15, 5, 0)
screen.init()
screen.clearLCD()

# 設定按鈕感測腳位
adc = ADC(0)

while True:
    val=adc.read()
    key=getKey(val)
    screen.text(10,10,"val : "+str(val)+"    ")
    screen.text(10,30,"key : "+str(key)+"    ")