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
def plotGreenBasket(x0,x1):
    tft.rect(x0-8,150-10,17,20,tft.rgbcolor(0,0,0))
    tft.rect(x1-5,155,10,3,tft.rgbcolor(0,255,0))
    tft.rect(x1-8,150,3,5,tft.rgbcolor(0,255,0))
    tft.rect(x1+6,150,3,5,tft.rgbcolor(0,255,0))
  
def plotRedApple(x,y0,y1):
    tft.rect(x-4,y0-8,8,12,tft.rgbcolor(0,0,0))
    tft.rect(x-4,y1-3,8,6,tft.rgbcolor(255,0,0))
    tft.rect(x-3,y1-4,6,8,tft.rgbcolor(255,0,0))
    tft.rect(x,y1-7,1,3,tft.rgbcolor(255,0,0))
    tft.rect(x,y1-8,4,1,tft.rgbcolor(255,0,0))
 
def plotYelloHeart(n):
    h=150
    tft.rect(113,0,15,160,tft.rgbcolor(0,0,0))
    for _ in range(n):
        tft.rect(115,h,3,6,tft.rgbcolor(255,255,0))
        tft.rect(118,h+2,2,6,tft.rgbcolor(255,255,0))
        tft.rect(120,h,3,6,tft.rgbcolor(255,255,0))
        h-=10 

# game parameter initialize
end=False;score=0

# apple position
ax=100;ay0=0;ay1=0
# basket position 
bx0=50;bx1=50;by=140

tft.clear(tft.rgbcolor(0, 0, 0))
plotGreenBasket(bx0,bx1)
tft.line(112, 0, 112, 160,tft.rgbcolor(255,255,255))
life=0
plotYelloHeart(life)

while True:
    key=getKey(adc.read())
    # normal condition    
    if end == False:
        # get control 
        if key=="l" and bx1>10  :bx1=bx0-5;toot()
        if key=="r" and bx1<100 :bx1=bx0+5;toot()
        # plotBasket
        if bx1!=bx0:
            #plotGreenBasket(bx0,140,tft.rgbcolor(0,0,0))
            plotGreenBasket(bx0,bx1)
            bx0=bx1
        # plotApple
        ay1=ay0+3+life
        plotRedApple(ax,ay0,ay1)
        ay0=ay1
        if ay1>170:
            ay0=-20;
            ax=randint(10,100);
            print(ax)
        #print(ax,ay1,bx1,by)
        
    # collision happened   
    if ay1>150 and ax-bx1<10 and ax-bx1>-10 :
        ding()
        ding()
        score+=1
        ay0=-10;ax=randint(10,100);
        plotGreenBasket(bx0,bx1)
        if life<10 :life+=1
        plotYelloHeart(life)
        
    # restart game button   
        if key=="t" :
            tft.clear(tft.rgbcolor(0, 0, 0));
            by=-20;
            bx=randint(0,11)*10;
            end=False;
    
    # necessary time delay    
    time.sleep(.05)
    

