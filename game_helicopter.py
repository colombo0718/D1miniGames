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


bicycle_pixels_1=(
b"        1   1111    "    
b"       1    1       "    
b"      1111111111111 "    
b"            1    1  "
b"         1111   1   "
b"1           1       "
b"  1     1111111111  "
b" 1 11111111     1 1 "
b" 1   1111 1     1  1"
b"       1111     1  1"
b"       1111     1  1"
b"        111111111111"
b"          1    1    "
b"          1    1  1 "
b"        1111111111  "
)

bicycle_pixels_2=(
b"        1111   11   "    
b"         11   11 1  "    
b"      1    111    1 "    
b"       1 11   11    "
b"        11   1111   "
b"1           1       "
b" 1      1111111111  "
b"  111111111     1 1 "
b" 1   1111 1     1  1"
b"       1111     1  1"
b"       1111     1  1"
b"        111111111111"
b"          1    1    "
b"          1    1  1 "
b"        1111111111  "
)

hydrant_pixels_1=(
b"                 "
b"         1       "
b"         1       "
b"       11111     "
b"     11     11   "
b"    11       11  "
b"    11       11  "
b"   1111111111111 "
b"  111 11 11 11 11"
b"   1111111111111 "
b"    111 1 1 111  "
b"     1   1   1   "
)

hydrant_pixels_2=(
b"         1       "
b"        1 1      "
b"         1       "
b"       11111     "
b"     11     11   "
b"    11       11  "
b"    11       11  "
b"   1111111111111 "
b"  11 11 11 11 111"
b"   1111111111111 "
b"    1 1 111 1 1  "
b"     1   1   1   "
)

fire_pixels=(
b"11   11   11 "
b" 11   11   11"
b"11   11   11 "
)

def toot():
    buzzer.duty(500)
    buzzer.freq(1000)
    ### 背景音樂播放時的音效不要 sleep 也不要 duty(0) ###
    time.sleep(.05)
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
    time.sleep(.1)
    buzzer.duty(0)
toot()

# 初始化變數
end = False
jump = False   
x0 = 145; x1 = x0
y0 = 145; y1 = y0
fx0=0;fx1=0
v = 0
running_time = 0
running_dist = 0
score=0

hydrant = Character((hydrant_pixels_1,hydrant_pixels_2), 17, 11, lcd, LCD.BLUE)
# 用兩個 bitmap 來建立 bicycle 物件. 預設會自動換圖產生動作效果
bicycle = Character(
    (bicycle_pixels_1,bicycle_pixels_2), 20, 15, lcd, lcd.rgbcolor(255,255,0))

fire = Character(fire_pixels,13,3, lcd, LCD.RED)
fire.x=130

bicycle.show(0, y0)
hydrant.y = 140

lcd.text(10, 10, "score:")
lcd.text(74, 10,score)
while True:
    key=getKey(adc.read())
    if not end:

        # Cactus forward
        if x0<-20:
            x0=130
            hydrant.y = randint(30,150)
            score-=1
            lcd.text(74, 10,score)
        # speed_level 越高, 仙人掌速度越快
        x1 = x0-2
        
        # dinosaur jumping
        y1=y0+2
            
        # fall on ground    
        if y1>145:
            v=0
            y1=145
            
            
        # press to jump
        if key=='u' :
            y1=y0-3
            toot()
        if key=='d' :
            y1=y0+5
            toot()
        if key=='m' and fire.x>140:
            ding()
            fire.x=bicycle.x+10
            fire.y=bicycle.y+10
        # fire shoot


        bicycle.yplot(y0,y1)
        hydrant.xplot(x0,x1)
        fire.xplot(fire.x,fire.x+10)
        x0=x1
        y0=y1
        
        # ufo hited
        if hydrant.x-10<fire.x<hydrant.x+17 :
            if hydrant.y<fire.y<hydrant.y+10 :
                buzz()
                hydrant.hide()
                x0=130
                hydrant.y = randint(30,150)
                fire.hide()
                fire.x=140
                score+=1
                lcd.text(74, 10,score)
          
        if bicycle.x-17<hydrant.x<bicycle.x+20 : 
            if bicycle.y-10<hydrant.y<bicycle.y+15 :
                buzz()
                end=True
    
    # restart game button
    if end and key=='m':
        lcd.clearLCD()
        score=0
        lcd.text(10, 10, "score: ")
        lcd.text(74, 10,score)
        # initialize
        end = False
        jump = False   
        x0 = 140; x1 = x0
        y0 = 147; y1 = y0
        v = 0
        running_time = 0
        running_dist = 0          

    
    running_time += 1