# Semaphore operated by servo
# Servo code is for Pico RP2040 or RP2350
# Servo is Hitec 32645S HS-645MG High Torque 2BB Metal Gear Servo
# Pin 2 activates two relays which toggle power and ground to the servo so the servo is powered only when moving

from machine import Pin, PWM
import time

class semaphore:

    def __init__(self):
    # servo pulse width time
        self.val = self.high = 2_050_000        # 2,050,000 nanoseconds or 2050 microseconds (red)
        self.old = self.mid = 1_600_000         # time in nanoseconds (yellow)
        self.low = 1_150_000                    # time in nanoseconds (green)
        self.step = self.pos_step = 450_000     # time in nanoseconds (change to next color)
        self.neg_step = self.pos_step * -1
        self.increment = self.pos_inc = 18_000  # time in nanoseconds (servo increment during movement)
        self.neg_inc = self.pos_inc * -1

    # time intervals    
        self.interval = 300_000  # time in miliseconds, 5 minutes equals 300,000
        self.prev_time = time.ticks_ms()

    # pin assignment
        self.slice_freq = 50     # if servo and LED use the same slice (RP2040), then use slice_freq when assigning servo and LED
        self.servo = PWM(Pin(0), freq=self.slice_freq, duty_ns=self.mid)
        self.LED = PWM(Pin(1), freq=self.slice_freq, duty_u16=int(self.duty_percent(50)))
        self.relay = Pin(Pin(2), Pin.OUT)
        self.relay.off()

    def duty_percent(self,x):    # convert duty cycle percent to u16
        y = x / 100 * 65535
        return y

    def init_servo(self):        # initialize servo to mid position
        self.servo.duty_ns(self.mid)
        self.relay.on()
        time.sleep(1)
        self.relay.off()
        
    def main(self):
        curr_time = time.ticks_ms()
        if time.ticks_diff(curr_time,self.prev_time) >= self.interval:
            self.prev_time = curr_time
            if self.val == self.low:
                self.step = self.pos_step  # low --> mid (green to yellow)
            elif self.val == self.high:
                self.step = self.neg_step  # high --> mid (red to yellow)
            else:  # val equal mid
                if self.old == self.high:  
                    self.increment = self.neg_inc  # mid --> low (yellow to green)
                else:
                    self.increment = self.pos_inc  # mid --> high (yellow to red)
            
            self.relay.on()
            
            # incremently movement of servo to new color position
            while self.val != self.old:
                self.old = self.old + self.increment
                self.servo.duty_ns(self.old)
                time.sleep_ms(80)
            
            self.relay.off()
            
            self.old = self.val
            
            if self.val == self.mid:
                self.val = self.step + self.val # next step is red or green
            else:
                self.val = self.mid             # next step is to mid position (yellow)

run = semaphore()
run.init_servo()
while True:
    run.main()
