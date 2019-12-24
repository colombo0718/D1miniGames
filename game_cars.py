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
    elif abs(adc-922)<50:
        key='u'
    elif abs(adc-740)<50:
        key='d'
    elif abs(adc-555)<80:
        key='l'
    elif abs(adc-370)<50:
        key='r'
    elif abs(adc-188)<80:
        key='m'    
    return key

# plot game object functions
def plotRedCar(x0,x1):
    if x0!=x1 :
        tft.rect(x0,140,10,20,tft.rgbcolor(0,0,0))
    tft.rect(x1,140,10,20,tft.rgbcolor(255,0,0))


def plotBlueCar(x,y0,y1):
    tft.rect(x,y0,10,20,tft.rgbcolor(0,0,0))
    tft.rect(x,y1,10,20,tft.rgbcolor(0,0,255))

def plotYelloHeart(n):
    h=150
    tft.rect(113,0,15,160,tft.rgbcolor(0,0,0))
    for _ in range(n):
        tft.rect(115,h,3,6,tft.rgbcolor(255,255,0))
        tft.rect(118,h+2,2,6,tft.rgbcolor(255,255,0))
        tft.rect(120,h,3,6,tft.rgbcolor(255,255,0))
        h-=10 

# game parameter initialize
end=False
x0=50;x1=50
bx=10;by0=0;by1=0

tft.clear(tft.rgbcolor(0, 0, 0))
#tft.line(112, 0, 112, 160,tft.rgbcolor(255,255,255))
life=0
#plotYelloHeart(life)
while True:
    key=getKey(adc.read())
    # normal condition    
    if end == False:
        if key=="l" and x1>0  :x1-=5;toot()
        elif key=="r" and x1<120 :x1+=5;toot()
        plotRedCar(x0,x1)   
        x0=x1
        #print(bx,by)
        by1=by0+3+life
        plotBlueCar(bx,by0,by1)
        by0=by1
        
        # pass one car 
        if by1>180 :
            life+=1
            #plotYelloHeart(life)
            by0=-20;
            bx=randint(0,11)*10;
        
    

    
    # collision happened
    if abs(x1-bx)<10 and abs(by1-140)<20:
        end=True
        buzz()

        
        
    # restart game button   
        if key=="m":
            tft.clear(tft.rgbcolor(0, 0, 0))
            by0=-20;
            bx=randint(0,11)*10;
            life=0
            end=False;
    # necessary time delay    
    time.sleep(.03)
    

