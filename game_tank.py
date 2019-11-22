from machine import Pin, SPI, ADC
from tft import TFT_GREEN
#import font
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
    elif abs(adc-1024)<50:
        key='u'
    elif abs(adc-941)<50:
        key='d'
    elif abs(adc-786)<50:
        key='l'
    elif abs(adc-631)<50:
        key='r'
    elif abs(adc-478)<50:
        key='m'
    elif abs(adc-324)<50:
        key='s'
    elif abs(adc-170)<50:
        key='t'     
    return key
Vb=10
# plot game object functions
def plotBluTank(x0,x1,y):
    if x0!=x1 :
        tft.rect(x0,y-5,10,20,tft.rgbcolor(0,0,0))
    tft.rect(x1+4,y-5,2,10,tft.rgbcolor(0,0,255))
    tft.rect(x1,y,10,8,tft.rgbcolor(0,0,255))

def plotCyanBullet(x,y):
    tft.rect(x,y+Vb,2,5,tft.rgbcolor(0,0,0))
    tft.rect(x,y,2,5,tft.rgbcolor(0,255,255))

def plotRedTank(x0,x1,y):
    if x0!=x1 :
        tft.rect(x0,y,10,20,tft.rgbcolor(0,0,0))
    tft.rect(x1+4,y+5,2,10,tft.rgbcolor(255,0,0))
    tft.rect(x1,y,10,8,tft.rgbcolor(255,0,0))
    
def plotMageBullet(x,y):
    tft.rect(x,y-Vb,2,5,tft.rgbcolor(0,0,0))
    tft.rect(x,y,2,5,tft.rgbcolor(255,0,255))


# game parameter initialize
end=False
Bx0=60;Bx1=60;By=150
Cx=60;Cy=-10
Rx0=60;Rx1=0;Ry=0
Mx=60;My=170
dx=3


tft.clear(tft.rgbcolor(0, 0, 0))
tft.rect(115,150,3,6,tft.rgbcolor(255,255,0))
tft.rect(118,152,2,6,tft.rgbcolor(255,255,0))
tft.rect(120,150,3,6,tft.rgbcolor(255,255,0))

while True:
    key=getKey(adc.read())
    # normal condition    
    if end == False:
        if key=="l" and Bx1>0  :Bx1-=3
        elif key=="r" and Bx1<100 :Bx1+=3
        # fire Cyan bullet 
        elif key=="m" and Cy<=-10 : Cx=Bx1+4;Cy=150
        Cy-=Vb
        if Cy<=-10 : Cy=-10
        plotCyanBullet(Cx,Cy)
        # move My tank 
        plotBluTank(Bx0,Bx1,By)
        Bx0=Bx1
        # fire Mage bullet
        if My>=170 : Mx=Rx1+4;My=5
        My+=Vb
        plotMageBullet(Mx,My)
        # move Enemy tank
        Rx1+=dx
        if Rx1>100 : dx=-3
        elif Rx1<0 : dx=3
        plotRedTank(Rx0,Rx1,Ry)
        Rx0=Rx1
        
        





    # necessary time delay
    time.sleep(.01)
    

