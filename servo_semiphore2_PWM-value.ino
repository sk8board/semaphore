// Semiphore operated by servo
// Code for Arduino Uno ATmega328
// Servo is Hitec 32645S HS-645MG High Torque 2BB Metal Gear Servo
// Pin 2 activates two relays which toggle power and ground to the servo so the servo is only powered when moving

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// PWM values are used rather than degrees
int val = 2050;    // variable to read the value from the analog pin
int add = -450;   // variable to increment to the next quadrent
int increment = 18;  // rate of rotation change
int old = 1600;    // previous quadrant

unsigned long previousMillis = 0;
const long interval = 300000; //time in miliseconds, 5 minuted equals 300000 msmyservo.write(0);

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo.write(old);  // set initial position of the servo
  analogWrite(3, 255);  // ground for LED
  pinMode(2, OUTPUT);  // relay control pin
  digitalWrite(2, HIGH);  // activate relays to power and move servo to initial position
  delay(1000);
  digitalWrite(2, LOW);  // remove power and ground to the servo
}

void loop() {

  unsigned long currentMillis = millis();
  

  if (currentMillis - previousMillis >= interval) {
  
      previousMillis = currentMillis;
      
      if (val == 1150){
        add = 450;
      }
      if (val == 2050){
        add = -450;
      }
      if (val == 1600){
        if (old == 1150){
          increment = 18;
        }
        else{
          increment =-18;
        }
      }

      digitalWrite(2, HIGH);
      delay(100);
      
      //val = map(val, 0, 1023, 0, 180);     // scale it to use it with the servo (value between 0 and 180)
      
      while (val != old) {
        old = old + increment;
        myservo.write(old);  // sets the servo position according to the scaled value
        delay(80);
        // red = 170, 2050
        // yellow = 95, 1600
        // green = 20, 1150
      }
      
      old = val;
      digitalWrite(2, LOW);
      
      if (val != 1600){
      val = 1600;
      }
      else{
      val = add + val;
      }
  }
}
