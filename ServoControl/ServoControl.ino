//Including Servo Library
#include <Servo.h>

const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

//Defining Servos
Servo base;
Servo right;
Servo left;
Servo claw;

//Servo Position Defaults, in Degrees
int baseStart = 111; 
int rightStart = 87; 
int leftStart = 167; 
int clawStart = 48;

//Define Analog Input Servo Pins

const char basePin = A1;
const char rightPin = A2;
const char leftPin = A3;
const char clawPin = A4;

//Defining String variable to take commands
String string;

int baseVoltMid;
int rightVoltMid;
int leftVoltMid;
int clawVoltMid;

int baseVoltMax;
int rightVoltMax;
int leftVoltMax;
int clawVoltMax;

int baseVoltMin;
int rightVoltMin;
int leftVoltMin;
int clawVoltMin;

int baseMin = 64;
int baseMax = 180;

int rightMin = 46;
int rightMax = 156;

int leftMin = 100;
int leftMax = 180;


void setup() {
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
  
  base.write(180);
  right.write(156);
  left.write(175);
  claw.write(123);
  
  delay(1500);
  
  baseVoltMax = analogRead(basePin);
  rightVoltMax = analogRead(rightPin);
  clawVoltMax = analogRead(clawPin);
  
  base.write(64);
  right.write(46);
  left.write(135);
  claw.write(123);
  
  delay(1500);
  
  baseVoltMin = analogRead(basePin);
  rightVoltMin = analogRead(rightPin);
  clawVoltMin = analogRead(clawPin);
  
  //Move Servos To Starting Locations
  base.write(baseStart);
  right.write(rightStart);
  left.write(leftStart);
  claw.write(clawStart);
  
  delay(1500);
  
  baseVoltMid = analogRead(basePin);
  rightVoltMid = analogRead(rightPin);
  leftVoltMid = analogRead(leftPin);
  clawVoltMid = analogRead(clawPin);
  
  left.write(180);
  
  delay(1500);
  
  leftVoltMax = analogRead(leftPin);
  
  left.write(100);
  
  delay(1500);
  
  leftVoltMin = analogRead(leftPin);
  
  left.write(167);
  
  delay(500);
  
  //Start Serial Monitor
  Serial.begin(9600);
}

void loop() {
  while (Serial.available()==0) {}

  byte instr = Serial.read();

  if(instr == 'd'){
    while(Serial.available() == 0) {}
    
    byte whichServos = Serial.read();
    
    if((whichServos & 'a') == 'a') {
      getBaseAngle();
    }

    if((whichServos & 'b') == 'b') {
      getRightAngle();
    }

    if((whichServos & 'd') == 'd') {
      getLeftAngle();
    }

    if((whichServos & 'h') == 'h') {
      getClawAngle();
    }
  }

  if(instr == 'a'){
    getDataPrint();
  }
  
  if(instr == 's') {
    boolean Loop = true;
    while(Serial.available() == 0) {}
    
    char whichServo = Serial.read();
    
    if(whichServo == '1') {
      while(Loop) {
        readNewBase();
        if(newData == true) {
          int angle = atoi(receivedChars);
          newData = false;
          Loop = false;
          base.write(angle);
        }
      }
    }
    
    if(whichServo == '2') {
      while(Loop) {
        readNewBase();
        if(newData == true) {
          int angle = atoi(receivedChars);
          newData = false;
          Loop = false;
          right.write(angle);
        }
      }
    }
    
    if(whichServo == '3') {
      while(Loop) {
        readNewBase();
        if(newData == true) {
          int angle = atoi(receivedChars);
          newData = false;
          Loop = false;
          left.write(angle);
        }
      }
    }
  }
}

void readNewBase() {
  static byte ndx = 0;
  char endMarker = ',';
  char data;

  while(Serial.available() > 0 && newData == false) {
    data = Serial.read();
    
    if(data != endMarker) {
      receivedChars[ndx] = data;
      ndx++;
      if(ndx >= numChars) {
        ndx = numChars-1;
      }
    } else {
      receivedChars[ndx] = '\0';
      ndx = 0;
      newData = true;
    }
  }
}

void readNewRight() {
  static byte ndx = 0;
  char endMarker = ',';
  char data;

  while(Serial.available() > 0 && newData == false) {
    data = Serial.read();
    
    if(data != endMarker) {
      receivedChars[ndx] = data;
      ndx++;
      if(ndx >= numChars) {
        ndx = numChars-1;
      }
    } else {
      receivedChars[ndx] = '\0';
      ndx = 0;
      newData = true;
    }
  }
}

void readNewLeft() {
  static byte ndx = 0;
  char endMarker = ',';
  char data;

  while(Serial.available() > 0 && newData == false) {
    data = Serial.read();
    
    if(data != endMarker) {
      receivedChars[ndx] = data;
      ndx++;
      if(ndx >= numChars) {
        ndx = numChars-1;
      }
    } else {
      receivedChars[ndx] = '\0';
      ndx = 0;
      newData = true;
    }
  }
}

void getDataPrint() {
  //Define Variables for Reading Servo Positions
  int basePos;
  int rightPos;
  int leftPos;
  int clawPos;
  int baseAngle;
  int rightAngle;
  int leftAngle;
  String clawAngle = "???";
  
  //Read the Current Position of the Servos in Voltage
  basePos = analogRead(basePin);
  rightPos = analogRead(rightPin);
  leftPos = analogRead(leftPin);
  clawPos = analogRead(clawPin);

  //Print the Servo Angles, in Voltage, to the Serial Monitor
  Serial.print(basePos);
  Serial.print(" ");
  Serial.print(rightPos);
  Serial.print(" ");
  Serial.print(leftPos);
  Serial.print(" ");
  Serial.print(clawPos);

  //Read the Current Position of the Servos in Voltage
  baseAngle = map(basePos, baseVoltMin, baseVoltMax, baseMin, baseMax);
  rightAngle = map(rightPos, rightVoltMin, rightVoltMax, rightMin, rightMax);
  
  leftAngle = map(leftPos, leftVoltMin, leftVoltMax, leftMin, leftMax);

  //Print the Servo Angles, in Degrees, to the Serial Monitor
  Serial.print(" ");
  Serial.print(baseAngle);
  Serial.print(" ");
  Serial.print(rightAngle);
  Serial.print(" ");
  Serial.print(leftAngle);
  Serial.print(" ");
  Serial.println(clawAngle);
}

void getBaseAngle() {
  //Define Variables for Reading Servo Positions
  int basePos;
  int baseAngle;
  
  //Read the Current Position of the Servos in Voltage
  basePos = analogRead(basePin);

  //Read the Current Position of the Servos in Voltage
  baseAngle = map(basePos, baseVoltMin, baseVoltMax, baseMin, baseMax);

  Serial.println(baseAngle);
}

void getRightAngle() {
  //Define Variables
  int rightPos;
  int rightAngle;

  rightPos = analogRead(rightPin);
  
  //Read the Current Position of the Servos in Voltage
  rightAngle = map(rightPos, rightVoltMin, rightVoltMax, rightMin, rightMax);
    
  Serial.println(rightAngle);
}

void getLeftAngle() {
  //Define Variables for Reading Servo Positions
  int leftPos;
  int leftAngle;
  
  //Read the Current Position of the Servos in Voltage
  leftPos = analogRead(leftPin);

  //Read the Current Position of the Servos in Voltage
  leftAngle = map(leftPos, leftVoltMin, leftVoltMax, leftMin, leftMax);
  leftAngle = map(leftPos, 247, 494, 64, 180);

  Serial.println(leftAngle);
}

void getClawAngle() {
  int clawPos;

  clawPos = analogRead(clawPin);
  
  Serial.println("???");
}
