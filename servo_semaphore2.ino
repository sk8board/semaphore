#include <Servo.h>

Servo myservo;  // create servo object to control a servo

int val = 170;    // variable to read the value from the analog pin
int add = -75;   // variable to increment to the next quadrent
int increment = 3;  // rate of rotation change
int old = 95;    // previous quadrant

unsigned long previousMillis = 0;
const long interval = 10000; //time in miliseconds, 5 minuted equals 300000 msmyservo.write(0);

void setup() {
  myservo.attach(9, 1000, 2000);  // attaches the servo on pin 9 to the servo object
  myservo.write(old);
  analogWrite(3, 255);
  pinMode(2, OUTPUT);
}

void loop() {

  unsigned long currentMillis = millis();
  

  if (currentMillis - previousMillis >= interval) {
  
      previousMillis = currentMillis;
      
      if (val == 20){
        add = 75;
      }
      if (val == 170){
        add = -75;
      }
      if (val == 95){
        if (old == 20){
          increment = 3;
        }
        else{
          increment =-3;
        }
      }

      digitalWrite(2, HIGH);
      delay(100);
      
      //val = map(val, 0, 1023, 0, 180);     // scale it to use it with the servo (value between 0 and 180)
      
      while (val != old) {
        old = val;//old + increment;
        myservo.write(old);  // sets the servo position according to the scaled value
        delay(800);
        // green 180, 20
        // yellow 105, 95
        // red 30, 170
      }
      
      old = val;
      digitalWrite(2, LOW);
      //digitalWrite(9, HIGH);
      
      if (val != 95){
      val = 95;
      }
      else{
      val = add + val;
      }
  }
}
