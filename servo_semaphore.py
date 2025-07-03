# Semaphore operated by servo
# Servo code is for Pico
# Servo is Hitec 32645S HS-645MG High Torque 2BB Metal Gear Servo
# Pin 2 activates two relays which toggle power and ground to the servo so the servo is powered only when moving

from machine import Pin, PWM
import time

def setup():
# servo pulse width time
    val = high = 2_050_000      # 2,050,000 nanoseconds or 2050 microseconds (red)
    old = mid = 1_600_000       # time in nanoseconds (yellow)
    low = 1_150_000             # time in nanoseconds (green)
    step = pos_step = 450_000   # time in nanoseconds (change to next color)
    neg_step = pos_step * -1
    increment = pos_inc 18_000  # time in nanoseconds (servo increment during movement)
    neg_inc = pos_inc * -1

# time intervals    
    interval = 300_000  #time in miliseconds, 5 minuted equals 300,000
    prev_time = time.ticks_ms()

# pin assignment
    slice_freq = 50 # if servo and LED use the same slice (RP2040), then use slice_freq when assigning servo and LED
    servo = PWM(Pin(0), freq=slice_freq, duty_ns=mid)
    LED = PWM(Pin(1), freq=slice_freq, duty_u16=duty_percent(50))
    relay = Pin(Pin(2), Pin.OUT)
    relay.off()

def duty_percent(x):  # convert duty cycle percent to u16
    y = x / 100 * 65535
    return y

def init_servo():   # initialize servo to mid position
    servo.duty_ns(mid)
    relay.on()
    time.sleep(1)
    relay.off()
    
def main():
    curr_time = time.ticks_ms()
    
    if time.ticks_diff(prev_time,curr_time) >= interval:
        prev_time = curr_time
        if val == low:
            step = pos_step  # low --> mid (green to yellow)
        elif val == high:
            step = neg_step  # high --> mid (red to yellow)
        else:  # val equal mid
            if old == high:  
                increment = neg_inc  # mid --> low (yellow to green)
            else:
                increment = pos_inc  # mid --> high (yellow to red)
        
        relay.on()
        
        # incremently movement of servo to new color position
        while val != old:
            old = old + increment
            servo.duty_ns(old)
            time.sleep_ms(80)
        
        relay.off()
        
        old = val
        
        if val == mid:
            val = step + val # next step is red or green
        else:
            val = mid # next step is to mid position (yellow)


setup()
init_servo()
while True:
    main()
