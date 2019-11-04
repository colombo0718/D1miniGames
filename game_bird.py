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
    if adc<30 :
        key='n'
    elif abs(adc-1024)<5:
        key='u'
    elif abs(adc-941)<5:
        key='d'
    elif abs(adc-786)<5:
        key='l'
    elif abs(adc-631)<5:
        key='r'
    elif abs(adc-478)<5:
        key='m'
    elif abs(adc-324)<5:
        key='s'
    elif abs(adc-170)<5:
        key='t'     
    return key

def plotRedBird(x0,x1):
    tft.rect(x0,120,10,10,tft.rgbcolor(0,0,0))
    tft.rect(x1,120,10,10,tft.rgbcolor(255,0,0))
    
def plotBluePiller(x,y):
    tft.rect(0,y-5,x,5,tft.rgbcolor(0,0,0))
    tft.rect(x+40,y-5,128-(x+40),5,tft.rgbcolor(0,0,0))
    tft.rect(0,y,x,5,tft.rgbcolor(0,0,255))
    tft.rect(x+40,y,128-(x+40),5,tft.rgbcolor(0,0,255))

end=False
x0=50;x1=50
bx=60;by=0

tft.clear(tft.rgbcolor(0, 0, 0))
while True:
    key=getKey(adc.read())
    
    if not end:
        x1+=5
        if key=="m":# and x1>0 and x1<120 :
            x1-=10
        print(key)
        plotRedBird(x0,x1)
        x0=x1
        
        plotBluePiller(bx,by)
        by+=5
        if by>165:
            bx=randint(0,128-40)
            by=0
    
    if by==125 or by==130 :
        if x1<bx or x1>bx+30:
            tft.text(0,10,"Good Game", font.terminalfont,tft.rgbcolor(0,255,0), 2)
            tft.text(0,30,"please press 'RST' ", font.terminalfont,tft.rgbcolor(0,255,0), 1)
            tft.text(0,40,"to restart game.", font.terminalfont,tft.rgbcolor(0,255,0), 1)
            end=True 
            if key=="t":
                tft.clear(tft.rgbcolor(0, 0, 0))
                bx=randint(0,128-40)
                x1=50
                by=0;
                end=False
    
    
    time.sleep(.1)
    

