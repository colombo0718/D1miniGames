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
    if adc<80 :
        key='n'
    elif abs(adc-1024)<80:
        key='u'
    elif abs(adc-941)<50:
        key='d'
    elif abs(adc-786)<80:
        key='l'
    elif abs(adc-631)<50:
        key='r'
    elif abs(adc-478)<80:
        key='m'
    elif abs(adc-324)<80:
        key='s'
    elif abs(adc-170)<80:
        key='t'     
    return key

# plot game object functions
def plotTile(i,j,color):
    tft.rect(i*5,j*5,4,4,color)

def plotSnake(s):
    for n in range(len(s)):
        plotTile(s[n][0],s[n][1],tft.rgbcolor(0,255,0))
    
def plotYelloHeart(n):
    h=150
    tft.rect(113,0,15,160,tft.rgbcolor(0,0,0))
    for i in range(n):
        tft.rect(115,h,3,6,tft.rgbcolor(255,255,0))
        tft.rect(118,h+2,2,6,tft.rgbcolor(255,255,0))
        tft.rect(120,h,3,6,tft.rgbcolor(255,255,0))
        h-=10

life=3


# game parameter initialize
end=False

tft.clear(tft.rgbcolor(0, 0, 0))
tft.line(112, 0, 112, 160,tft.rgbcolor(255,255,255))
plotYelloHeart(life)

direction="d"
snake=[[1,1],[1,2],[1,3],[1,4],[1,5]]
dt=.4
plotSnake(snake)

food = [10,10]
plotTile(food[0],food[1],tft.rgbcolor(255,0,0))
    
while True:
    key=getKey(adc.read())
    # normal condition    
    if end == False:
        # press key change direction 
        if key=="u" and direction!="d":
            direction="u"
        if key=="d" and direction!="u":
            direction="d"
        if key=="r" and direction!="l":
            direction="r" 
        if key=="l" and direction!="r":
            direction="l"
            
        # get new head by its direction
        if direction=="u" :
            head=[snake[-1][0],snake[-1][1]-1]
        if direction=="d" :
            head=[snake[-1][0],snake[-1][1]+1]
        if direction=="r" :
            head=[snake[-1][0]+1,snake[-1][1]]
        if direction=="l" :
            head=[snake[-1][0]-1,snake[-1][1]]
         
        # head touch wall
        if head[0]==-1 : head[0]=21
        if head[0]==22 : head[0]=0
        if head[1]==-1 : head[1]=31
        if head[1]==32 : head[1]=0
        
        # head touch body 
        if head in snake :
            tft.rect(0,0,110,160,tft.rgbcolor(0,0,0))
            direction="d"
            snake=[[1,1],[1,2],[1,3],[1,4],[1,5]]
            head=[1,6]
            dt=.4
            plotSnake(snake)
        # erase tail add new head
        if head!=food :
            plotTile(snake[0][0],snake[0][1],tft.rgbcolor(0,0,0))
            snake=snake[1:]
        snake.append(head)
        plotTile(snake[-1][0],snake[-1][1],tft.rgbcolor(0,255,0))
        print(len(snake))
        
        # random set new food
        if head==food :
            dt*=.9 # faster 
            food[0]=randrange(0,21)
            food[1]=randrange(0,31)
            plotTile(food[0],food[1],tft.rgbcolor(255,0,0))
        
        
    # reset condition
    if end == True:
        if key=="s":
            end=False

    # necessary time delay
    time.sleep(dt)
    

