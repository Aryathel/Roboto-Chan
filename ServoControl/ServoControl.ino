//Including Servo Library
#include <Servo.h>

//Defining Servos
Servo base;
Servo right;
Servo left;
Servo claw;

//Servo Position Defaults, in Degrees
int baseStart = 131;
int rightStart = 120;
int leftStart = 120;
int clawStart = 48;

//Define Analog Input Servo Pins

const char basePin = A1;
const char leftPin = A2;
const char rightPin = A3;
const char clawPin = A4;

void setup() {
  //Start Serial Monitor
  Serial.begin(9600);
  
  //Define Pin States
  pinMode(basePin, INPUT);
  pinMode(leftPin, INPUT);
  pinMode(rightPin, INPUT);
  pinMode(clawPin, INPUT);
  
  //Define Servo Control Pins
  base.attach(3);
  right.attach(5);
  left.attach(6);
  claw.attach(9);
  
  //Move Servos To Starting Locations
  base.write(baseStart);
  right.write(rightStart);
  left.write(leftStart);
  claw.write(clawStart);
}

void loop() {
  //Define Variables for Reading Servo Positions
  int basePos;
  int rightPos;
  int leftPos;
  int clawPos;
  int baseAngle;
  int rightAngle;
  int leftAngle;
  int clawAngle;
  
  //Read the Current Position of the Servos in Voltage
  basePos = analogRead(basePin);
  rightPos = analogRead(rightPin);
  leftPos = analogRead(leftPin);
  clawPos = analogRead(clawPin);

  //Print the Servo Angles, in Voltage, to the Serial Monitor
  Serial.print("BVP: ");
  Serial.print(basePos);
  Serial.print("   RVP: ");
  Serial.print(rightPos);
  Serial.print("   LVP: ");
  Serial.print(leftPos);
  Serial.print("   CVP: ");
  Serial.print(clawPos);

  //Read the Current Position of the Servos in Voltage
  baseAngle = map(basePos, 247, 494, 64, 180);
  rightAngle = map(rightPos, 297, 485, 90, 180);
  leftAngle = map(leftPos, 213, 440, 51, 160);
  clawAngle = "???";

  //Print the Servo Angles, in Degrees, to the Serial Monitor
  Serial.print("   BAA: ");
  Serial.print(baseAngle);
  Serial.print("   RAA: ");
  Serial.print(rightAngle);
  Serial.print("   LAA: ");
  Serial.print(leftAngle);
  Serial.print("   CAA: ");
  Serial.println(clawAngle);
}
