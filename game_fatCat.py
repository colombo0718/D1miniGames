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

left_pixels_1=(
b"   1   1         11 "
b"  11   11        11 "
b" 111111111        1 "
b" 11 111 11       11 "
b"111 111 11111 1 11  "
b" 1111 1111 11 1 111 "
b"1111   111111111111 "
b"  1111111 111111111 "
b"         1111111111 "
b"      111111111111  "
b"      11       11   "
)
left_pixels_2=(
b"  1     1       11  "
b"  11   11       11  "
b" 111111111       1  "
b" 11 111 11       1  "
b"111 111 11111 1 11  "
b" 1111 1111 11 1 111 "
b"1111   111111111111 "
b"  1111111 111111111 "
b"         1111111111 "
b"      111111111111  "
b"     1  1     1  1  "
)
# ------------------

righ_pixels_1=(
b" 11        1     1  "
b" 11        11   11  "
b" 1        111111111 "
b"  1       11 111 11 "
b"  11 1 11111 111 111"
b" 111 1 11 1111 1111 "
b" 111111111111   1111"
b" 111111111 1111111  "
b" 1111111111         "
b"  111111111111      "
b"   11       11      "
)

righ_pixels_2=(
b"  11        1   1   "
b"  11       11   11  "
b"  1       111111111 "
b"  1       11 111 11 "
b"  11 1 11111 111 111"
b" 111 1 11 1111 1111 "
b" 111111111111   1111"
b" 111111111 1111111  "
b" 1111111111         "
b"  111111111111      "
b"  1  1     1  1     "
)
# ------------------
mouse_pixels_1=(
b"    1    "    
b"    1    " 
b"     1   "    
b"     1   " 
b"    1    "    
b"   111   "
b"  11111  "
b"  11111  "    
b"  11111  "
b" 1 111 1 "
b"111111111"
b" 11 1 11 "
b"   111   "
b"   111   "
b"   111   "
b"    1    "
b"    1    "
)
mouse_pixels_2=(
b"    1    "    
b"    1    " 
b"   1     "    
b"   1     " 
b"    1    "    
b"   111   "
b"  11111  "
b"  11111  "    
b"  11111  "
b" 1 111 1 "
b"111111111"
b" 11 1 11 "
b"   111   "
b"   111   "
b"   111   "
b"    1    "
b"    1    "
)
def toot():
    buzzer.duty(500)
    buzzer.freq(1000)
    time.sleep(.01)
    buzzer.duty(0)

def ding():
    buzzer.duty(500)
    buzzer.freq(1000)
    time.sleep(.02)
    buzzer.freq(500)
    time.sleep(.05)
    buzzer.freq(1000)
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
righ = Character(
    (righ_pixels_1,righ_pixels_2), 20, 11, lcd, LCD.RED)
left = Character(
    (left_pixels_1,left_pixels_2), 20, 11, lcd, LCD.RED)
cat=righ

rat = Character(
    (mouse_pixels_1,mouse_pixels_2), 9, 17, lcd, LCD.BLUE)

left.y=140
righ.y=140
x0=0;x1=0
y0=0;y1=0

score=0
lcd.text(10, 5, "score:")
lcd.text(74, 5,score)

while True:
    # red cat control 
    key=getKey(adc.read())
    if key=='r':
        x1=x0+2+score//2
        cat=righ
        toot()
    if key=='l':
        x1=x0-2-score//2
        cat=left
        toot()
    cat.xplot(x0,x1)
    x0=x1
    
    # blue rat moving 
    y1=y0+3+score
    rat.yplot(y0,y1)
    y0=y1
    if y0>170 :
        y0=20
        rat.x=randint(0,110)
        score-=1
        lcd.text(10, 5, "score:")
        lcd.fillRect(74,5,40,10,LCD.BLACK)
        lcd.text(74, 5,score)

    # collision happend
    if cat.y-17<rat.y<cat.y+11:
        if cat.x-10<rat.x<cat.x+20:
            ding()
            rat.hide()
            y0=20
            rat.x=randint(0,110)
#             if score<10:
            score+=1
            lcd.text(10, 5, "score:")
            lcd.fillRect(74,5,40,10,LCD.BLACK)
            lcd.text(74, 5,score)

    
    
