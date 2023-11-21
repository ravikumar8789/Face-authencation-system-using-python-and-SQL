#include <Servo.h>

Servo myservo;  // Create a Servo object

#define led 6
#define led1 7
int data, flag = 2;

void setup()
{
  pinMode(led, OUTPUT);
  pinMode(led1, OUTPUT);
  digitalWrite(led, LOW);
  digitalWrite(led1, LOW);
  myservo.attach(9); // Attach the servo to pin 9 (you can change this to the appropriate pin)
  Serial.begin(9600);
}

void loop()
{
  while (Serial.available())
  {
    data = Serial.read();

    if (data == '0')
    {
      flag = 0;
    }
    else if (data == '1')
    {
      flag = 1;
    }
  }
  if (flag == 1)
  {
    digitalWrite(led, HIGH);
    digitalWrite(led1, LOW);
    
    myservo.write(90); // Rotate servo 90 degrees clockwise
    delay(3000);       // Wait for 3 seconds
    
    myservo.write(0);  // Rotate servo back to 0 degrees (counterclockwise)
    delay(2000);       // Wait for 2 seconds
    
    digitalWrite(led, LOW);
    digitalWrite(led1, LOW);
  }
  else if (flag == 0)
  {
    digitalWrite(led, LOW);
    digitalWrite(led1, HIGH);
    delay(2000);
    digitalWrite(led1, LOW);
  }
}