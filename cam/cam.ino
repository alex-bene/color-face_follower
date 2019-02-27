#include <Servo.h>
Servo myservo;
void setup() {
  Serial.begin(9600);
  myservo.attach(9);
}
int d_position;
int ser_read;
int position = 90;
String inString = "";
void loop() {
  // Read serial input:
  if (Serial.available()>0) {
    int inChar = Serial.read();
    inString += (char)inChar;
    // if you get a newline, print the string, then the string's value:
    if (inChar == '\n') {
      Serial.print("Value:");
      Serial.println(inString.toInt());
      // tou stelno times gyro apo to 8
      d_position = inString.toInt()-4;
      // clear the string for new input:
      inString = "";
      Serial.println(d_position);
      position += d_position;
      //limit for servo movement (0-180 degrees)
      if (position > 175) {
        position = 175;
      }
      if (position < 5) {
        position = 5;
      }
      // END limit for servo movement (0-180 degrees)
      myservo.write(position);
      Serial.println(position);
      delay(1);
    }
  }
}
