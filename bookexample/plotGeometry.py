from machine import freq,SPI,Pin,PWM,ADC,Timer
import time
import LCD
from flaglib import *

# 螢幕初始設定
spi = SPI(1, baudrate=40000000, polarity=0, phase=0)
screen = LCD.LCD(spi, 15, 5, 0)
screen.init()
screen.clearLCD()

# 畫點
screen.drawPixel(20,20,LCD.WHITE)
# 畫線
screen.drawLine(60,10,10,60,LCD.PURPLE)
# 畫框
screen.drawRect(40,60,30,50,LCD.YELLOW)
# 畫圓
screen.drawCircle(100,120,10,LCD.CYAN)



