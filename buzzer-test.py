from machine import Pin, SPI, ADC,PWM
import time 

buzzer=PWM(Pin(12,Pin.OUT),duty=500)
print(buzzer)


buzzer.freq(500)
time.sleep(.05)
buzzer.freq(1000)
time.sleep(.05)
buzzer.freq(500)
time.sleep(.05)


buzzer.duty(0)