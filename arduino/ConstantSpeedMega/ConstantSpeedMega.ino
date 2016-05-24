// PiScope Arduino firmware
// Using an Arduino Mega with a stepper motor shield
#include "TimerOne.h"
#include "TimerThree.h"

#define X_STEP_PIN         54
#define X_DIR_PIN          55
#define X_ENABLE_PIN       38
#define X_MIN_PIN           3
#define X_MAX_PIN           2

#define Y_STEP_PIN         60
#define Y_DIR_PIN          61
#define Y_ENABLE_PIN       56
#define Y_MIN_PIN          14
#define Y_MAX_PIN          15

#define MIN_DELAY          20 // minimum timer tick

// these are initialized in reset()
int stepsize;
int varDelayX;
int varDelayY;
int moveX;
int moveY;

// interrupt variables
boolean stateX;
boolean stateY;
boolean interruptXBusy;
boolean interruptYBusy;

// variables for reading in speed
String str;
int number;
 
void setup() {
    pinMode(X_ENABLE_PIN, OUTPUT);
    pinMode(Y_ENABLE_PIN, OUTPUT);
    digitalWrite(X_ENABLE_PIN, HIGH);
    digitalWrite(Y_ENABLE_PIN, HIGH);

    Timer1.initialize(1000000); // will be reset once stepping begins
    Timer3.initialize(1000000); // will be reset once stepping begins

    Serial.begin(9600);
    printHelp();
    reset();
}

void reset() {
    stepsize = 500;
    varDelayX = MIN_DELAY;
    varDelayY = MIN_DELAY;
    moveX = -1;
    moveY = -1; 
     
    stateX = false;
    stateY = false;
    interruptXBusy = false;
    interruptYBusy = false;
}

void stepperInterruptX(void) {
    if (moveX >= 0) {
            if (interruptXBusy) return;
            interruptXBusy = true;
            stateX = !stateX;
            digitalWrite(X_DIR_PIN, moveX == 0 ? LOW : HIGH);
            digitalWrite(X_STEP_PIN, stateX);
            interruptXBusy = false;
    }
}

void stepperInterruptY(void) {
    if (moveY >= 0) {
          if (interruptYBusy) return;
          interruptYBusy = true;
          stateY = !stateY;
          digitalWrite(Y_DIR_PIN, moveY == 0 ? LOW : HIGH);
          digitalWrite(Y_STEP_PIN, stateY);
          interruptYBusy = false;
    }
}

void stepX(int steps, int dir) {
    if (varDelayX < MIN_DELAY) varDelayX = MIN_DELAY; 
    digitalWrite(X_ENABLE_PIN, LOW);
  
    if (dir == 0) {
        digitalWrite(X_DIR_PIN, LOW);
    } else {
        digitalWrite(X_DIR_PIN, HIGH);
    }

    for (int x = 0; x < steps; x++) {
        digitalWrite(X_STEP_PIN, HIGH);
        delayMicroseconds(varDelayX);
        digitalWrite(X_STEP_PIN, LOW);
        delayMicroseconds(varDelayX);

        if(x%50==0)Serial.println(x);
    }

    digitalWrite(X_ENABLE_PIN, HIGH);
}

void stepY(int steps, int dir) {
    if (varDelayY < MIN_DELAY) varDelayY = MIN_DELAY; 
    digitalWrite(Y_ENABLE_PIN, LOW);

    if (dir == 0) {
        digitalWrite(Y_DIR_PIN, LOW);
    } else {
        digitalWrite(Y_DIR_PIN, HIGH);
    }

    for (int x = 0; x < steps; x++) {
        digitalWrite(Y_STEP_PIN, HIGH);
        delayMicroseconds(varDelayY);
        digitalWrite(Y_STEP_PIN, LOW);
        delayMicroseconds(varDelayY);

        if(x%50==0)Serial.println(x);
    }

    digitalWrite(X_ENABLE_PIN, HIGH);
}


void printHelp(){
      Serial.println("? Print this help ");
      Serial.println("1 Enable Motors ");
      Serial.println("0 Disable Motors ");
      Serial.println("");
      Serial.println("2  - 9 stepsize from 1 to a lot");
      Serial.println("w up");
      Serial.println("s down");
      Serial.println("a left");
      Serial.println("d right");
      Serial.println("");
      Serial.println("u const. up");
      Serial.println("j const. down");
      Serial.println("h const. left");
      Serial.println("k const. right");
      Serial.println("");
      Serial.println("m[0-9]. set base speed");
      Serial.println("n[0-9]. set incl. speed");
      Serial.println("");
      Serial.println("r reset");
}

void readNumber() {
    str = "";
    while (true) {
      if (Serial.available()) {
        byte c = Serial.read();
        if (c >= '0' && c <= '9') str += (c - '0');
        else break;
      }
    }
}

void loop() {  
    if (Serial.available()) {
        Timer1.detachInterrupt();
        Timer3.detachInterrupt();
        byte r = Serial.read();

        switch (r) {
            case '?':
              printHelp();
              break;
          
            case '1':
                digitalWrite(X_ENABLE_PIN, LOW);
                digitalWrite(Y_ENABLE_PIN, LOW);
                break;
                
            case '0':
                digitalWrite(X_ENABLE_PIN, HIGH);
                digitalWrite(Y_ENABLE_PIN, HIGH);
                break;

            case 'a':
                Serial.print("A  ");
                Serial.println(stepsize);
                stepX(stepsize, 1);
                break;
            case 'd':
                Serial.print("D  ");
                Serial.println(stepsize);
                stepX(stepsize, 0);
                break;
            case 'w':
                Serial.print("W  ");
                Serial.println(stepsize);
                stepY(stepsize, 1);
                break;
            case 's':
                Serial.print("S  ");
                Serial.println(stepsize);
                stepY(stepsize, 0);
                break;

            case '2':
                Serial.println("stepsize = 1");
                stepsize = 1;
                break;
            case '3':
                Serial.println("stepsize = 10");
                stepsize = 10;
                break;
            case '4':
                Serial.println("stepsize = 100");
                stepsize = 100;
                break;
            case '5':
                Serial.println("stepsize = 500");
                stepsize = 500;
                break;
            case '6':
                Serial.println("stepsize = 1,000");
                stepsize = 1000;
                break;
            case '7':
                Serial.println("stepsize = 5,000");
                stepsize = 5000;
                break;
            case '8':
                Serial.println("stepsize = 10,000");
                stepsize = 10000;
                break;
            case '9':
                Serial.println("stepsize = 20,000");
                stepsize = 20000;
                break;

            case 'u':
                if (moveY == 0) moveY = -1; else moveY = 1;
                break;
            case 'j':
                if (moveY == 1) moveY = -1; else moveY = 0;
                break;
            case 'k':
                if (moveX == 0) moveX = -1; else moveX = 1;
                break;
            case 'h':
                if (moveX == 1) moveX = -1; else moveX = 0;
                break;

            case 'm':
                readNumber();
                number = str.toInt();
                varDelayX = number;
                if (varDelayX < MIN_DELAY) varDelayX = MIN_DELAY; 
                Serial.print("speedX = ");
                Serial.println(varDelayX);
                break;

            case 'n':
                readNumber();
                number = str.toInt();
                varDelayY = number;
                if (varDelayY < MIN_DELAY) varDelayY = MIN_DELAY; 
                Serial.print("speedY = ");
                Serial.println(varDelayY);
                break;

            case 'r':
                reset();
                break;

            default:
                break;
        }

        Timer1.attachInterrupt(stepperInterruptX, varDelayX);
        Timer3.attachInterrupt(stepperInterruptY, varDelayY);
    }
}
