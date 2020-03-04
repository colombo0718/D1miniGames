import LCD
from machine import freq,SPI,Pin,PWM,ADC,Timer
import time
from flaglib import *


# 按鈕與蜂鳴器感測腳位設定
adc = ADC(0)
buzzer = PWM(Pin(12))
buzzer.freq(1000)

# 螢幕初始設定
spi = SPI(1, baudrate=40000000, polarity=0, phase=0)
screen = LCD.LCD(spi, 15, 5, 0)
screen.init()
screen.clearLCD()

# 搖桿音效設計
def bee():
    buzzer.duty(500)
    time.sleep(.05)
    buzzer.duty(0)

# 賽車造型設計
c1=(
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
c2=(
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

car= Character([c1,c2], 13, 17, screen, LCD.RED)
car.show(60,140)

    
while True:
    key=getKey(adc.read())
    print(key)
    if key== "r":
        car.move(3,0)
        bee()
    elif key== "l":
        car.move(-3,0)
        bee()
    else :
        car.plot()
