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
int rightStart = 112;
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

int baseMicroMid;
int rightMicroMid;
int leftMicroMid;
int clawMicroMid;

int baseMicroMax;
int rightMicroMax;
int leftMicroMax;
int clawMicroMax;

int baseMicroMin;
int rightMicroMin;
int leftMicroMin;
int clawMicroMin;

int baseMin = 64;
int baseMax = 180;

int rightMin = 71;
int rightMax = 180;

int leftMin = 100;
int leftMax = 180;

int baseMinMicro = 1200;
int baseMaxMicro = 2375;

int rightMinMicro = 1280;
int rightMaxMicro = 2385;

int leftMinMicro = 1575;
int leftMaxMicro = 2385;

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
    right.write(180);
    left.write(173);
    claw.write(123);

    delay(1000);

    baseVoltMax = analogRead(basePin);
    rightVoltMax = analogRead(rightPin);
    clawVoltMax = analogRead(clawPin);

    base.writeMicroseconds(2375);
    right.writeMicroseconds(2385);
    left.writeMicroseconds(2315);
    claw.writeMicroseconds(1234);

    delay(300);

    baseMicroMax = analogRead(basePin);
    rightMicroMax = analogRead(rightPin);
    clawMicroMax = analogRead(clawPin);

    base.write(64);
    right.write(71);
    left.write(135);
    claw.write(123);

    delay(1000);

    baseVoltMin = analogRead(basePin);
    rightVoltMin = analogRead(rightPin);
    clawVoltMin = analogRead(clawPin);

    base.writeMicroseconds(1200);
    right.writeMicroseconds(1280);
    left.writeMicroseconds(1930);
    claw.writeMicroseconds(1234);

    delay(300);

    baseMicroMin = analogRead(basePin);
    rightMicroMin = analogRead(rightPin);
    clawMicroMin = analogRead(clawPin);

    //Move Servos To Starting Locations
    base.write(baseStart);
    right.write(rightStart);
    left.write(leftStart);
    claw.write(clawStart);

    delay(1000);

    baseVoltMid = analogRead(basePin);
    rightVoltMid = analogRead(rightPin);
    leftVoltMid = analogRead(leftPin);
    clawVoltMid = analogRead(clawPin);

    base.writeMicroseconds(1680);
    right.writeMicroseconds(1700);
    left.writeMicroseconds(2265);
    claw.writeMicroseconds(1234);

    delay(300);

    baseMicroMid = analogRead(basePin);
    rightMicroMid = analogRead(rightPin);
    leftMicroMid = analogRead(leftPin);
    clawMicroMid = analogRead(clawPin);
    
    base.write(baseStart);
    right.write(rightStart);
    left.write(180);
    claw.write(clawStart);

    delay(1000);

    leftVoltMax = analogRead(leftPin);

    left.writeMicroseconds(2385);

    delay(300);

    leftMicroMax = analogRead(leftPin);

    left.write(100);

    delay(1000);

    leftVoltMin = analogRead(leftPin);

    left.writeMicroseconds(1575);

    delay(300);

    leftMicroMin = analogRead(leftPin);

    left.write(167);

    delay(1000);

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

    if(instr == 'm'){
        getDataMicroPrint();
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

    if(instr == 'u') {
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
                    base.writeMicroseconds(angle);
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
                    right.writeMicroseconds(angle);
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
                    left.writeMicroseconds(angle);
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
            receivedChars[ndx] = '    0';
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
            receivedChars[ndx] = '    0';
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
            receivedChars[ndx] = '    0';
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

void getDataMicroPrint() {
    //Define Variables for Reading Servo Positions
    int basePos;
    int rightPos;
    int leftPos;
    int clawPos;
    int baseMicro;
    int rightMicro;
    int leftMicro;
    String clawMicro = "???";

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
    baseMicro = map(basePos, baseMicroMin, baseMicroMax, baseMinMicro, baseMaxMicro);
    rightMicro = map(rightPos, rightMicroMin, rightMicroMax, rightMinMicro, rightMaxMicro);
    leftMicro = map(leftPos, leftMicroMin, leftMicroMax, leftMinMicro, leftMaxMicro);

    //Print the Servo Angles, in Degrees, to the Serial Monitor
    Serial.print(" ");
    Serial.print(baseMicro);
    Serial.print(" ");
    Serial.print(rightMicro);
    Serial.print(" ");
    Serial.print(leftMicro);
    Serial.print(" ");
    Serial.println(clawMicro);
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
