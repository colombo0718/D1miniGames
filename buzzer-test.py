from machine import Pin, SPI, ADC,PWM
import time 

buzzer=PWM(Pin(12,Pin.OUT),duty=500)
print(buzzer)

def toot():
    buzzer.duty(500)
    buzzer.freq(1000)
    time.sleep(.05)
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
    time.sleep(1)
    buzzer.duty(0)
 
toot()
time.sleep(1)   
ding()