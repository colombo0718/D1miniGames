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

# plot game object functions
def plotRedCar(x0,x1):
    if x0!=x1:
        tft.rect(x0,140,10,20,tft.rgbcolor(0,0,0))
    tft.rect(x1,140,10,20,tft.rgbcolor(255,0,0))
def plotGreenBasket(x,y,color):
    tft.text(x,y,"U",font.terminalfont,color,2)

def plotBlueCar(x,y):
    tft.rect(x,y-5,10,5,tft.rgbcolor(0,0,0))
    tft.rect(x,y,10,20,tft.rgbcolor(0,0,255))
    
def plotRedApple(x,y,color):
    tft.text(x,y,"@",font.terminalfont,color,1)
    #tft.text(0,30,"please press 'RST' ", font.terminalfont,tft.rgbcolor(0,255,0), 1)
    

# game parameter initialize
end=False;score=0

# apple position
ax=100;ay0=0;ay1=0
# basket position 
bx0=50;bx1=50;by=140

tft.clear(tft.rgbcolor(0, 0, 0))
plotGreenBasket(bx1,140,tft.rgbcolor(0,255,0))
tft.text(110,0,str(score), font.terminalfont,tft.rgbcolor(255,255,255), 1)
while True:
    key=getKey(adc.read())
    # normal condition    
    if end == False:
        # get control 
        if key=="l" and bx1>0   :bx1=bx0-5
        if key=="r" and bx1<120 :bx1=bx0+5
        # plotBasket
        if bx1!=bx0:
            plotGreenBasket(bx0,140,tft.rgbcolor(0,0,0))
            plotGreenBasket(bx1,140,tft.rgbcolor(0,255,0))
            bx0=bx1
        # plotApple
        ay1=ay0+6
        plotRedApple(ax,ay0,tft.rgbcolor(0,0,0))
        plotRedApple(ax,ay1,tft.rgbcolor(255,0,0))
        ay0=ay1
        if ay1>165: ay0=-10;ax=randint(0,11)*10;
        print(ax,ay1,bx1,by)
    # collision happened
    
    if ay1>140 and ay1<150 and ax-bx1<20 and ax-bx1>-5 :
        tft.text(110,0,str(score), font.terminalfont,tft.rgbcolor(0,0,0), 1)
        score+=1
        tft.text(110,0,str(score), font.terminalfont,tft.rgbcolor(255,255,255), 1)
    # restart game button   
        if key=="t" :
            tft.clear(tft.rgbcolor(0, 0, 0))
            by=-20;
            bx=randint(0,11)*10;
            end=False;
    
    # necessary time delay    
    time.sleep(.05)
    

