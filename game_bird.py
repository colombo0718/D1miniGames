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
#------------------
buzzer=PWM(Pin(12,Pin.OUT),duty=500)
def toot():
    buzzer.duty(500)
    buzzer.freq(1000)
    time.sleep(.01)
    buzzer.duty(0)
    
def buzz():
    buzzer.duty(500)
    buzzer.freq(200)
    time.sleep(1)
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
        x1+=2
        if key=="m":# and x1>0 and x1<120 :
            toot()
            x1-=6
        plotRedBird(x0,x1)
        x0=x1
        
        plotBluePiller(bx,by)
        by+=4
        if by>165:
            bx=randint(0,128-40)
            by=0
    
    if by>120 and by<130 :
        if x1<bx or x1>bx+30:
            buzz()
            end=True 
            if key=="l":
                tft.clear(tft.rgbcolor(0,0,0))
                bx=randint(0,128-40)
                x1=50
                by=0;
                end=False
    
    
    time.sleep(.01)
    

