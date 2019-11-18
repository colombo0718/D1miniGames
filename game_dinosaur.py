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
tft = TFT_GREEN(128, 160, spi, dc, cs, rst, rotate=90)
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
    err=20
    key='n'
    if adc<30 :
        key='n'
    elif abs(adc-1024)<err:
        key='u'
    elif abs(adc-941)<err:
        key='d'
    elif abs(adc-786)<err:
        key='l'
    elif abs(adc-631)<err:
        key='r'
    elif abs(adc-478)<err:
        key='m'
    elif abs(adc-324)<err:
        key='s'
    elif abs(adc-170)<err:
        key='t'     
    return key

# plot game object functions
def plotRedDinosaur(y0,y1):
    #tft.rect(30,y0,10,20,tft.rgbcolor(0,0,0))
    #tft.rect(30,y1,10,20,tft.rgbcolor(255,0,0))
    #tft.text(30,y0,"?",font.terminalfont,tft.rgbcolor(0,0,0),1)
    #tft.text(30,y1,"?",font.terminalfont,tft.rgbcolor(255,0,0),1)
    
    #tft.char_b(30, y0, "A", font.terminalfont, tft.rgbcolor(0,0,0))
    tft.char_b(30, y1, "?", font.terminalfont, tft.rgbcolor(255,0,0))
    
def plotGreenCactus(x0,x1):
    #tft.rect(x0,108,10,20,tft.rgbcolor(0,0,0))
    #tft.rect(x1,108,10,20,tft.rgbcolor(0,255,0))
    #tft.text(x0,108,">",font.terminalfont,tft.rgbcolor(0,0,0),1)
    #tft.text(x1,108,">",font.terminalfont,tft.rgbcolor(0,255,0),1)
    
    #tft.char_b(x0, 108, ">", font.terminalfont, tft.rgbcolor(0,0,0))
    tft.char_b(x1, 108, ">", font.terminalfont, tft.rgbcolor(0,255,0))
    
# game parameter initialize
tft.clear(tft.rgbcolor(0, 0, 0))
#tft.line(0,100,160,100,tft.rgbcolor(255,255,255))
end=False
jump=False   

x0=140;x1=140
y0=108; y1=108
v=0

plotRedDinosaur(y0,y1)
plotGreenCactus(x0,x1)
'''
while True:
    key=getKey(adc.read())
    # normal condition    
    if end == False:
        # Cactus forward
        if(x0==-20):
            x0=160
        x1=x0-5 
        # dinosaur jumping
        if(jump):
            y1=y0+v 
            v+=1
        # fall on ground    
        if(y0>128):
            v=0
            y1=108
            y0=108
            jump=False
        # press to jump
        if key=='m':
            v=-8
            jump=True
        plotRedDinosaur(y0,y1)
        plotGreenCactus(x0,x1)
    # collision happened
    if x1==25 or x1==30 or x1==35 :
        if y1>88:
            end=True
    # restart game button   
    if key=='m':
        end=False
    # necessary time delay    
    time.sleep(.05)
    x0=x1
    y0=y1
'''   