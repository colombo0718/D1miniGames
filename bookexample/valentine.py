from machine import freq,SPI,Pin,PWM,ADC,Timer
import time
import LCD
from flaglib import *

# 螢幕初始設定
spi = SPI(1, baudrate=40000000, polarity=0, phase=0)
screen = LCD.LCD(spi, 15, 5, 0)
screen.init()
screen.clearLCD()

h1=(
b"  111   111  "
b" 1   1 1   1 "
b"1     1     1"
b"1           1"
b"1           1"
b" 1         1 "
b"  1       1  "
b"   1     1   "
b"    1   1    "
b"     1 1     "
b"      1      "
)
h2=(
b"             "
b"  111   111  "
b" 1   1 1   1 "
b" 1    1    1 "
b" 1         1 "
b"  1       1  "
b"   1     1   "
b"    1   1    "
b"     1 1     "
b"      1      "
b"             "
)

h3=(
b"             "
b"             "
b"   11   11   "
b"  1  1 1  1  "
b"  1   1   1  "
b"   1     1   "
b"    1   1    "
b"     1 1     "
b"      1      "
b"             "
b"             "
)

heartA= Character([h1,h2], 13, 11, screen, LCD.RED)
heartB= Character([h1,h3], 13, 11, screen, LCD.RED)
heartC= Character([h1,h2,h3], 13, 11, screen, LCD.RED)

heartA.show(25,15)
heartB.show(55,25)
heartC.show(85,20)

m1=(
b"   111   "
b"  11111  "
b"  11111  "
b"   111   "
b"    1    "
b"   111   "
b"  11111  "
b"  11111  "
b"  111111 "
b"  111111 "
b"  111111 "
b"  1111111"
b"  11111 1"
b"   111  1"
b"   111   "
b"   111   "
b"   111   "
b"   111   "
b"   11    "
b"   11    "
b"   11    "
b"   11    "
b"   11    "
b"   1111  "
)

m2=(
b"    111  "
b"   11111 "
b"   11111 "
b"    111  "
b"    1    "
b"   111   "
b"  11111  "
b"  11111  "
b"  111111 "
b"  111111 "
b"  111111 "
b"  1111111"
b"  11111 1"
b"   111  1"
b"   111   "
b"   111   "
b"   111   "
b"   111   "
b"   11    "
b"   11    "
b"   11    "
b"   11    "
b"   11    "
b"   1111  "
)

w1=(
b"   111    "
b" 1111111  "
b"  11111   "
b"  11111   "
b"   11111  "
b"    1 11  "
b"   111 11 "
b"  11111 1 "
b" 111111 1 "
b" 111111   "
b" 111111   "
b"11 111    "
b"1  111    "
b"1  111    "
b"  11111   "
b"  11111   "
b"  11111   "
b"  11111   "
b"  11111   "
b"  11111   "
b"  11111   "
b"    11    "
b"    11    "
b"  1111    "
)

w2=(
b"  111     "
b"1111111   "
b" 11111    "
b" 11111    "
b"  11111   "
b"    1111  "
b"   111 11 "
b"  11111  1"
b" 111111  1"
b" 111111   "
b" 111111   "
b"11 111    "
b"1  111    "
b"1  111    "
b"  11111   "
b"  11111   "
b"  11111   "
b"  11111   "
b"  11111   "
b"  11111   "
b"  11111   "
b"    11    "
b"    11    "
b"  1111    "
)
man=Character([m1,m2,m2,m2], 9, 24, screen, LCD.CYAN)
wom=Character([w1,w2,w2,w2], 10, 24, screen, LCD.PURPLE)

man.show(51,100)
wom.show(60,100)

screen.text(20,60,"Love You ^^")

while True:
    heartA.plot()
    heartB.plot()
    heartC.plot()
    man.plot()
    wom.plot()