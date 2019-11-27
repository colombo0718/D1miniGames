from machine import Pin, SPI, ADC
from tft import TFT_GREEN
import font
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
tft = TFT_GREEN(128, 160, spi, dc, cs, rst, rotate=0)
tft.init()

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
    if adc<100 :
        key='n'
    elif abs(adc-1024)<100:
        key='u'
    elif abs(adc-941)<100:
        key='d'
    elif abs(adc-786)<100:
        key='l'
    elif abs(adc-631)<100:
        key='r'
    elif abs(adc-478)<100:
        key='m'
    elif abs(adc-324)<100:
        key='s'
    elif abs(adc-170)<100:
        key='t'     
    return key

# plot game object functions
def plotRedCar(x0,x1):
    if x0!=x1 :
        tft.rect(x0,140,10,20,tft.rgbcolor(0,0,0))
        #tft.char_b(x0,140,"=", font.terminalfont, tft.rgbcolor(0,0,0))
    tft.rect(x1,140,10,20,tft.rgbcolor(255,0,0))
    #tft.char_b(x1,140,"=", font.terminalfont, tft.rgbcolor(255,0,0))

def plotGreenMissile(x,y):
    tft.rect(x,y+10,5,10,tft.rgbcolor(0,0,0))
    tft.rect(x,y,5,10,tft.rgbcolor(0,255,0))
    #tft.char_b(x1, 108, ">", font.terminalfont, tft.rgbcolor(0,255,0))

def plotBlueCar(x,y):
    tft.rect(x,y-3,10,5,tft.rgbcolor(0,0,0))
    #tft.char_b(x,y-3,"=", font.terminalfont, tft.rgbcolor(0,0,0))
    tft.rect(x,y,10,20,tft.rgbcolor(0,0,255))
    #tft.char_b(x,y,"=", font.terminalfont, tft.rgbcolor(0,0,255))
    #tft.char_b(x,y,">", font.terminalfont, tft.rgbcolor(0,255,0))

# game parameter initialize
end=False
x0=50;x1=50
bx=10;by=0
mx=0;my=-20

tft.clear(tft.rgbcolor(0, 0, 0))
while True:
    key=getKey(adc.read())
    # normal condition    
    if end == False:
        if key=="l" and x1>0  :x1-=5
        elif key=="r" and x1<120 :x1+=5
        elif key=="m" and my<-10 : mx=x1+2;my=140
        plotRedCar(x0,x1)
        
        plotGreenMissile(mx,my)
        if my>-30 : my-=10
        x0=x1
        if by>165 :by=-20;bx=randint(0,11)*10;
        #print(bx,by)
        plotBlueCar(bx,by)
        by+=3
    # collision happened
    if x1==bx and abs(by-140)<20 :
        tft.text(0,10,"Good Game", font.terminalfont,tft.rgbcolor(0,255,0), 2)
        tft.text(0,30,"please press 'RST' ", font.terminalfont,tft.rgbcolor(0,255,0), 1)
        tft.text(0,40,"to restart game.", font.terminalfont,tft.rgbcolor(0,255,0), 1)
        end=True
    # restart game button   
        if key=="m" :
            tft.clear(tft.rgbcolor(0, 0, 0))
            by=-20;
            bx=randint(0,11)*10;
            end=False;
    # necessary time delay    
    time.sleep(.03)
    

