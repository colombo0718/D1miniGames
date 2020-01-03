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

dinosaur1_pixels=(
b"           11111111 "
b"          11 1111111"
b"          1111111111"
b"          1111111111"
b"          1111111111"
b"          11111     "
b"          11111111  "
b"         11111      "
b"1       111111      "
b"1      111111111    "
b"11    11111111 1    "
b"111  111111111      "
b"11111111111111      "
b" 111111111111       "
b"  1111111111        "
b"   11111111         "
b"    1111 11         "
b"     11   1         "
b"     1    11        "
b"    11     11       "
)

dinosaur2_pixels=(
b"          11111111  "
b"         11 1111111 "
b"         1111111111 "
b"         1111111111 "
b"         1111111111 "
b"         11111      "
b"         11111111   "
b"         11111      "
b"   1     111111     "
b"  11    111111111   "
b"  11   11111111 1   "
b" 111  111111111     "
b"11111111111111      "
b" 111111111111       "
b"  1111111111        "
b"   11111111         "
b"    1111 11         "
b"     11   1         "
b"      1   1         "
b"      11 11         "
)

cactus_pixels=(
b"    1111    "
b"   111111   "
b"   111111   "
b"   111111   "
b"   111111   "
b"   111111   "
b"11 111111 11"
b"11 111111 11"
b"11 111111 11"
b"11 111111 11"
b"11 111111 11"
b"11 111111 11"
b" 1111111111 "
b"  11111111  "
b"   111111   "
b"   111111   "
b"   111111   "
b"   111111   "
b"   111111   "
b"   111111   "
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

# 背景音樂
# timer = Timer(-1)
# rtttl_defaults = 'd=4,o=4,b=100'
# rtttl_tune = b'16e5,16e5,32p,8e5,16c5,8e5,8g5,8p,8g,8p,8c5,16p,8g,16p,8e,16p,8a,8b,16a#,8a,16g.,16e5,16g5,8a5,16f5,8g5,8e5,16c5,16d5,8b,16p,8c5,16p,8g,16p,8e,16p,8a,8b,16a#,8a,16g.,16e5,16g5,8a5,16f5,8g5,8e5,16c5,16d5,8b,8p,16g5,16f#5,16f5,16d#5,16p,16e5,16p,16g#,16a,16c5,16p,16a,16c5,16d5,8p,16g5,16f#5,16f5,16d#5,16p,16e5,16p,16c6,16p,16c6,16c6,p,16g5,16f#5,16f5,16d#5,16p,16e5,16p,16g#,16a,16c5,16p,16a,16c5,16d5,8p,16d#5,8p,16d5,8p,16c5'
# music = RTTTL(buzzer, rtttl_defaults, rtttl_tune)
# music.play_background(timer)
# music.repeat_play = True
# music.repeat_play_startidx = 32

# 初始化變數
end = False
jump = False   
x0 = 140; x1 = x0
y0 = 140; y1 = y0
v = 0
running_time = 0
running_dist = 0

cactus = Character(cactus_pixels, 12, 20, lcd, LCD.GREEN)
# 用兩個 bitmap 來建立 dinosaur 物件. 預設會自動換圖產生動作效果
dinosaur = Character(
    (dinosaur1_pixels, dinosaur2_pixels), 20, 20, lcd, lcd.rgbcolor(255,255,0))

dinosaur.show(10, y0)
cactus.y = y0

lcd.text(10, 10, "KM:")
lcd.text(10, 20, "Level:")

while True:
    if not end:
        speed_level = running_time//100 
        lcd.text(34, 10, running_dist//100)
        lcd.text(58, 20, speed_level)

    key=getKey(adc.read())
    
    # 讓恐龍的顏色越來越紅
    color_g = 255-speed_level*25
    if color_g < 0:
        color_g = 0
    dinosaur.color = lcd.rgbcolor(255, color_g, 0)
    
    # normal condition    
    if end == False:

        # Cactus forward
        if x0<-50:
            x0=130
        # speed_level 越高, 仙人掌速度越快
        x1 = x0-3-speed_level
        running_dist += 3+speed_level
        
        # dinosaur jumping
        if jump:
            y1=y0+v 
            v+=1
            
        # fall on ground    
        if y1>140:
            v=0
            y1=140
            #y0=140
            jump=False
            
        # press to jump
        if key=='m' and jump==False:
        # if button.value() == 0 and y0>=100:
            if not jump:
                toot()
            if v==0:
                v=-6
                #import gc;print(gc.mem_free())
                #import micropython;print(micropython.mem_info(111))
            elif v>-6:
                v-=1
            jump=True
        dinosaur.yplot(y0,y1)
        if running_time//1000 >= 10: print(x0,x1)
        cactus.xplot(x0,x1)
        
    # collision happened
    #print(abs(x1-10))
    if not end and 0<x1<32:
        if y1>125:
            end=True
            music.play_background_stop()
            buzz()
            lcd.text(30, 60, "GAME OVER", color=LCD.YELLOW)
    
    # restart game button
    if end and key=='m':       
    #if end and button.value() == 0:
        lcd.clearLCD()
        lcd.text(10, 10, "KM: ")
        lcd.text(10, 20, "Level: ")
        music.play_background_restart()
        
        # 初始化變數
        end = False
        jump = False   
        x0 = 140; x1 = x0
        y0 = 140; y1 = y0
        v = 0
        running_time = 0
        running_dist = 0       
                       
    x0=x1
    y0=y1
    
    running_time += 1