from machine import Pin, SPI, ADC, PWM
from tft import TFT_GREEN
import time
from urandom import *

# setting TFT pings and init --------------
# DC       - RS/DC data/command flag
# CS       - Chip Select, enable communication
# RST/RES  - Reset
dc  = Pin(5, Pin.OUT)
cs  = Pin(15, Pin.OUT)
rst = Pin(0, Pin.OUT)
# SPI Bus (CLK/MOSI/MISO)
# check your port docs to see which Pins you can use
spi = SPI(1, baudrate=8000000, polarity=1, phase=0)
# TFT object, this is ST7735R green tab version
tft = TFT_GREEN(128, 160, spi, dc, cs, rst, rotate=180)
tft.init()

buzzer=PWM(Pin(12,Pin.OUT),duty=500)
def toot():
    buzzer.duty(500)
    buzzer.freq(1000)
    time.sleep(.05)
    buzzer.duty(0)
def buzz():
    buzzer.duty(500)
    buzzer.freq(200)
    time.sleep(.1)
    buzzer.duty(0)
toot()
# low level random generator -------------- 
def randrange(start, stop=None):
    if stop is None:
        stop = start
        start = 0
    upper = stop - start
    bits = 0
    pwr2 = 1
    while upper > pwr2:
        pwr2 <<= 1
        bits += 1
    while True:
        r = getrandbits(bits)
        if r < upper:
            break
    return r + start

def randint(start, stop):
    return randrange(start, stop + 1)

# from adc value to keyname --------------
adc = ADC(0)
def getKey(adc):
    key='n'
    if adc<80 :
        key='n'
    elif abs(adc-1024)<50:
        key='u'
    elif abs(adc-964)<50:
        key='d'
    elif abs(adc-730)<80:
        key='l'
    elif abs(adc-489)<50:
        key='r'
    elif abs(adc-246)<80:
        key='m'    
    return key


# plot game object functions
def plotRedDinosaur(y0,y1):
    tft.rect(10-10,y0,20,20,tft.rgbcolor(0,0,0))
    tft.rect(10,y1,7,7,tft.rgbcolor(255,0,0))
    tft.rect(10-3,y1,4,15,tft.rgbcolor(255,0,0))
    tft.rect(10-9,y1+13,6,2,tft.rgbcolor(255,0,0))
    tft.rect(10-3,y1+15,2,5,tft.rgbcolor(255,0,0))
    tft.rect(10,y1+15,2,5,tft.rgbcolor(255,0,0))
    tft.rect(10,y1+3,2,2,tft.rgbcolor(0,0,0))
    tft.rect(10,y1+8,5,1,tft.rgbcolor(255,0,0))
    tft.rect(10,y1+10,3,2,tft.rgbcolor(255,0,0))
    tft.rect(10+3,y1+10,1,3,tft.rgbcolor(255,0,0))
    

    
def plotGreenCactus(x0,x1):
    tft.rect(x0-6,140,13,20,tft.rgbcolor(0,0,0))
    tft.rect(x1-1,140,3,20,tft.rgbcolor(0,255,0))
    tft.rect(x1-6,140+5,2,5,tft.rgbcolor(0,255,0))
    tft.rect(x1+5,140+3,2,7,tft.rgbcolor(0,255,0))
    tft.rect(x1-5,140+10,11,2,tft.rgbcolor(0,255,0))

    
# game parameter initialize
tft.clear(tft.rgbcolor(0, 0, 0))
#tft.line(0,100,160,100,tft.rgbcolor(255,255,255))
end=False
jump=False   

x0=140;x1=140
y0=140; y1=140
v=0

plotRedDinosaur(y0,y1)
plotGreenCactus(x0,x1)



while True:
    key=getKey(adc.read())
    # normal condition    
    if end == False:
        # Cactus forward
        if(x0<-20):
            x0=130
        x1=x0-5
        # dinosaur jumping
        if(jump):
            y1=y0+v 
            v+=1
        # fall on ground    
        if(y0>160):
            v=0
            y1=140
            y0=140
            jump=False
        # press to jump
        if key=='m' and jump==False:
            toot()
            v=-8
            jump=True
        plotRedDinosaur(y0,y1)
        print(x1)
        plotGreenCactus(x0,x1)
    # collision happened
    print(abs(x1-10))
    if abs(x1-10)<10:
        if y1>120:
            buzz()
            end=True
    # restart game button
    if end == True:
        if key=='m':
            end=False
            
    # necessary time delay    
    time.sleep(.001)
    x0=x1
    y0=y1
  