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

stop_pixels_1=(
b"     111     "
b"     111     "
b"     111     "
b"      1      "
b"   1111111   "
b"   1 111 1   "
b"   1 111 1   "
b"   1 111 1   "
b"     1 1     "
b"     1 1     "
b"     1 1     "
b"     1 1     "
)
stop_pixels_2=(
b"             "
b"     111     "
b"     111     "
b"     111     "
b"      1      "
b"   1111111   "
b"   1 111 1   "
b"   1 111 1   "
b"   1 111 1   "
b"     1 1     "
b"     1 1     "
b"     1 1     "
)
# -----------------

fall_pixels_1=(
b"     111     "
b"   1 111 1   "
b"   1 111 1   "
b"   1  1  1   "
b"   1111111   "
b"     111     "
b"     111     "
b"     111     "
b"     1 1     "
b"     1 1     "
b"     1 1     "
b"     1 1     "
)
fall_pixels_2=(
b"     111     "
b"  1  111  1  "
b"  1  111  1  "
b"   1  1  1   "
b"   1111111   "
b"     111     "
b"     111     "
b"     111     "
b"     1 1     "
b"     1 1     "
b"    1   1    "
b"    1   1    "
)
# -----------------

righ_pixels_1=(
b"     111     "
b"     1111    "
b"     111     "
b"      1      "
b"    11111    "
b"   1 111 1 1 "
b"  1  111  1  "
b"   1 111     "
b"     1  1    "
b"    1    1   "
b"  11     1   "
b"         1   "
)
righ_pixels_2=(
b"             "
b"     111     "
b"     1111    "
b"     111     "
b"     111     "
b"    1111     "
b"     11111   "
b"     111     "
b"     1 1     "
b"      1 1    "
b"      1 1    "
b"     1 1     "
)
# -----------------

left_pixels_1=(
b"     111     "
b"    1111     "
b"     111     "
b"      1      "
b"    11111    "
b" 1 1 111 1   "
b"  1  111  1  "
b"     111 1   "
b"    1  1     "
b"   1    1    "
b"   1     11  "
b"   1         "
)
left_pixels_2=(
b"             "
b"     111     "
b"    1111     "
b"     111     "
b"     111     "
b"     1111    "
b"   11111     "
b"     111     "
b"     1 1     "
b"    1 1      "
b"    1 1      "
b"     1 1     "
)
# ---------------
floor_pixels=(
b" 1111 1111 1111 1111 1111 1111 1111 1111"
b" 1111 1111 1111 1111 1111 1111 1111 1111"
b" 1111 1111 1111 1111 1111 1111 1111 1111"
b" 1111 1111 1111 1111 1111 1111 1111 1111"
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
stop = Character((stop_pixels_1,stop_pixels_2), 13, 12, lcd, LCD.RED)
fall = Character((fall_pixels_1,fall_pixels_2), 13, 12, lcd, LCD.RED)
left = Character((left_pixels_1,left_pixels_2), 13, 12, lcd, LCD.RED)
righ = Character((righ_pixels_1,righ_pixels_2), 13, 12, lcd, LCD.RED)



x0=55;y0=50;x1=55;y1=50
stop.x=x0;stop.y=y0
left.x=x0;left.y=y0
righ.x=x0;righ.y=y0

man=stop

floor = [
    Character(floor_pixels,40,4, lcd, LCD.BLUE),
    Character(floor_pixels,40,4, lcd, LCD.BLUE),
    Character(floor_pixels,40,4, lcd, LCD.BLUE),
    Character(floor_pixels,40,4, lcd, LCD.BLUE),
    Character(floor_pixels,40,4, lcd, LCD.BLUE),
#     Character(floor_pixels,40,2, lcd, LCD.BLUE),
#     Character(floor_pixels,40,2, lcd, LCD.BLUE),
]

floor[0].x=40;floor[0].y=160
floor[1].x=40;floor[1].y=130
floor[2].x=40;floor[2].y=100
floor[3].x=40;floor[3].y= 70
floor[4].x=40;floor[4].y= 40
# floor[5].x=40;floor[5].y=60
# floor[6].x=40;floor[6].y=40

score=0
lcd.text(10, 5, "score:")
lcd.text(74, 5,score)

state=''

while True:
    key=getKey(adc.read())
    if not end :    
        # floors move
        state='down'
        for i in range(5):
            fx=floor[i].x;fy=floor[i].y
            floor[i].plot(floor[i].x,floor[i].y,floor[i].x,floor[i].y-1)
            if fy<20 :
                floor[i].hide();
                floor[i].x=randint(0,80);
                floor[i].y=170
                score+=1
                lcd.text(10, 5, "score:")
                lcd.text(74, 5,score)
            if fy-18<man.y<fy-12 :
                if fx-10<man.x<fx+37:
                    print('raise')
                    state="up"
                    y1=fy-14
                    
        if state == "up":
#             man=stop
#             y1=y0-1
            a=1
        else :
#             man=fall
            y1=y0+3
            
                # red man control
        x0=x1
        if key=="r":
            toot()
            man=righ
            if x0<106:
                x1=x0+4
        if key=="l":
            toot()
            man=left
            if x0>2:
                x1=x0-4
        if key=="d":
            y1=y0+4
            man=fall
        if key=="n":
            man=stop
            if state != "up" :
                man=fall

        if y1<20 or y1> 150 :
            end = True
            buzz()
        
        man.plot(x0,y0,x1,y1)
        
        x0=x1; y0=y1
    if end :
        if key=="m" :
            end = False
            score=0
            lcd.text(10, 5, "score:")
            lcd.text(74, 5,score)
            man.hide()
            man.y=70
            y0=70

        