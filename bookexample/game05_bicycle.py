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
b"                    "    
b"                    "
b"         111        "    
b"         111        "    
b"         111        "    
b"         1          "
b"        111   1     "
b"       11  111      "
b"      11    1 1     "
b"    11111      1    "
b" 111    11    11111 "
b"1 1 1  11    1 1 1 1"
b"11111 1111111  11111"
b"1 1 1          1 1 1"
b" 111            111 "
)

bicycle_pixels_2=(
b"                    "    
b"                    "    
b"          111       "
b"          111       "    
b"          111       "    
b"         1          "
b"        111   1     "
b"       11  111      "
b"      11    1 1     "
b"    1111111    11   "
b" 111   1  1   11111 "
b"11 11   1 11 1 11 11"
b"1 1 1 1111111  1 1 1"
b"11 11 11       11 11"
b" 111            111 "
)
#----------------
bicycle_pixels_1=(
b"         111        "    
b"         111        "    
b"         111        "    
b"         1          "
b"        111    1    "
b"       11 111 1     "
b"      11     1 1    "
b"      1111111  1    "
b"  111   1  1   111  "
b" 1 1 1   11   1 1 1 "
b"1  1  1   1  1  1  1"
b"1111111   1  1111111"
b"1  1  1   11 1  1  1"
b" 1 1 1        1 1 1 "
b"  111          111  "
)

bicycle_pixels_2=(
b"          111       "    
b"          111       "    
b"          111       "    
b"         1          "
b"        111    1    "
b"       11 111 1     "
b"      11     1 1    "
b"      111      1    "
b"  111    11    111  "
b" 1   1     11 1   1 "
b"1 1 1 1  11  1 1 1 1"
b"1  1  1 111  1  1  1"
b"1 1 1 1      1 1 1 1"
b" 1   1        1   1 "
b"  111          111  "
)

hydrant_pixels=(
b"    1111    "
b"   111111   "
b"    1111    "
b"  11111111  "
b"  11111111  "
b"    1111    "
b"    1111    "
b"    1111    "
b"    1111    "
b"    1111    "
)

def toot():
    buzzer.duty(500)
    buzzer.freq(1000)
    ### 背景音樂播放時的音效不要 sleep 也不要 duty(0) ###
    time.sleep(.05)
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
v = 0
running_time = 0
running_dist = 0
score=0

hydrant = Character(hydrant_pixels, 12, 10, lcd, LCD.RED)
# 用兩個 bitmap 來建立 bicycle 物件. 預設會自動換圖產生動作效果
bicycle = Character(
    (bicycle_pixels_1,bicycle_pixels_2), 20, 15, lcd, lcd.rgbcolor(255,255,0))

bicycle.show(10, y0)
hydrant.y = 150

lcd.text(10, 10, "score:")
lcd.text(74, 10,score)
while True:
    key=getKey(adc.read())
    if not end:

        # Cactus forward
        if x0<-50:
            x0=130
            score+=1
            lcd.text(74, 10,score)
        # speed_level 越高, 仙人掌速度越快
        x1 = x0-6-score//5
        
        # dinosaur jumping
        if jump:
            y1=y0+v 
            v+=1
            
        # fall on ground    
        if y1>145:
            v=0
            y1=145
            jump=False
            
        # press to jump
        if key=='m' and jump==False:
            jump=True
            toot()
            if v==0:
                v=-6

        bicycle.yplot(y0,y1)
        hydrant.xplot(x0,x1)
        x0=x1
        y0=y1
        
    # collision happened
    if not end and 0<x1<30:
        if y1>137:
            end=True
            buzz()
            lcd.text(30, 60, "GAME OVER", color=LCD.YELLOW)
    
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