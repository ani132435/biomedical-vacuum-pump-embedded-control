from machine import PWM,Pin

led=PWM(Pin(15))
led.freq(1000)
led.duty_u16(30000)

led.value(0)
