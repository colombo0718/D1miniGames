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

tankUp_pixels_1=(
b"     111     "
b"     111     "
b"      1      "
b"11    1    11"
b"      1      "
b"11111 1 11111"
b"  111 1 111  "
b"1111 111 1111"
b"  1 11 11 1  "
b"111 1   1 111"
b"  1 11111 1  "
b"1111 111 1111"
b"  111   111  "
b"1111111111111"
b"             "
b"11         11"
b"             "
)
tankUp_pixels_2=(
b"     111     "
b"     111     "
b"      1      "
b"      1      "
b"11    1    11"
b"  111 1 111  "
b"11111 1 11111"
b"  11 111 11  "
b"111 11 11 111"
b"  1 1   1 1  "
b"111 11111 111"
b"  11 111 11  "
b"11111   11111"
b"  111111111  "
b"11         11"
b"             "
b"11         11"
)
fireUp_pixels=(
b"      1      "
b"     111     "
b"     111     "
b"     1 1     "
)
# -----------------
tankDn_pixels_1=(
b"             "
b"11         11"
b"             "
b"1111111111111"
b"  111   111  "
b"1111 111 1111"
b"  1 11111 1  "
b"111 1   1 111"
b"  1 11 11 1  "
b"1111 111 1111"
b"  111 1 111  "
b"11111 1 11111"
b"      1      "
b"11    1    11"
b"      1      "
b"     111     "
b"     111     "
)
tankDn_pixels_2=(
b"11         11"
b"             "
b"11         11"
b"  111111111  "
b"11111   11111"
b"  11 111 11  "
b"111 11111 111"
b"  1 1   1 1  "
b"111 11 11 111"
b"  11 111 11  "
b"11111 1 11111"
b"  111 1 111  "
b"11    1    11"
b"      1      "
b"      1      "
b"     111     "
b"     111     "
)
fireDn_pixels=(
b"     1 1     "
b"     111     "
b"     111     "
b"      1      "
)
# ---------------
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
redTank = Character(
    (tankUp_pixels_1,tankUp_pixels_2), 13, 17, lcd, LCD.RED)
purFire = Character(fireUp_pixels, 13, 4, lcd, LCD.PURPLE)

bluTank = Character(
    (tankDn_pixels_1,tankDn_pixels_2), 13, 17, lcd, LCD.BLUE)
cyaFire = Character(fireDn_pixels, 13, 4, lcd, LCD.CYAN)

redTank.x=0
redTank.y=140
bluTank.y=20
rx0=0;rx1=0
bx0=0;br1=0
score=0
d=3

py0=-20;py1=0
cy0=180;cy1=0


score=5
lcd.text(10, 5, "score:")
lcd.text(74, 5,score)

while True:
    key=getKey(adc.read())
    if not end :
        # blue car moving
        bx1=bx0+d
        bluTank.xplot(bx0,bx1)
        bx0=bx1
        if bx1>120:
            d=-3
        if bx1<0:
            d=3
            
        # red car control
        if key=='r':
            toot()
            rx1=rx0+3
            toot()
        if key=='l':
            toot()
            rx1=rx0-3
            toot()
        redTank.xplot(rx0,rx1)
        rx0=rx1
        
        # bullet fire
        if -20<purFire.y<0:
            lcd.text(10, 5, "score:")
            lcd.text(74, 5,score)
        
        if key=="m" and purFire.y<-10:
            ding()
            purFire.x=rx1
            py0=140
        py1=py0-10
        purFire.yplot(py0,py1)
        py0=py1
        
        if cyaFire.y>160 :
            cyaFire.x=bx1
            cy0=34
        cy1=cy0+10
        cyaFire.yplot(cy0,cy1)
        cy0=cy1
        
        # collision happen
        print(abs(cyaFire.x-redTank.x)<6 ,cyaFire.y)
        if abs(cyaFire.x-redTank.x)<7 and 140<cyaFire.y<164:
            cy0=170
            score-=1
            buzz()
            lcd.text(10, 5, "score:")
            lcd.text(74, 5,score)
        if abs(purFire.x-bluTank.x)<7 and 16<purFire.y<37:
            py0=-10
            score+=1
            buzz()
            lcd.text(10, 5, "score:")
            lcd.text(74, 5,score)
        