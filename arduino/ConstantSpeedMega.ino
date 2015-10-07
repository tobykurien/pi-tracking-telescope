// ConstantSpeed.pde
// -*- mode: C++ -*-
//
// Shows how to run AccelStepper in the simplest,
// fixed speed mode with no accelerations
/// \author  Mike McCauley (mikem@open.com.au)
// Copyright (C) 2009 Mike McCauley
// $Id: ConstantSpeed.pde,v 1.1 2011/01/05 01:51:01 mikem Exp mikem $

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
#include <AccelStepper.h>

//AccelStepper stepper; // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
AccelStepper stepper(AccelStepper::FULL2WIRE,X_STEP_PIN, X_DIR_PIN  );
AccelStepper stepper1(AccelStepper::FULL2WIRE, Y_STEP_PIN , Y_DIR_PIN);
float stepsize = 50;

void setup()
{  pinMode(X_ENABLE_PIN,OUTPUT);
   pinMode(Y_ENABLE_PIN,OUTPUT);
   digitalWrite(X_ENABLE_PIN,LOW);
   digitalWrite(Y_ENABLE_PIN,LOW);
   //stepper.setMinPulseWidth(100);
//   stepper.setMaxSpeed(100);
   
   //stepper1.setMaxSpeed(100);
   
 //   stepper.setAcceleration(200);
   //  stepper1.setAcceleration(200);
  //stepper.moveTo(5000);
//  stepper1.moveTo(5000);
   stepper.setAcceleration(200);
   stepper.setMaxSpeed(1000000);
   stepper.setSpeed(10000);
   
   stepper1.setAcceleration(200000);
   stepper1.setMaxSpeed(100000);
   stepper1.setSpeed(10000);
   
   
   Serial.begin(9600);
  
}

void loop()
{     
    if(Serial.available()){
        byte r = Serial.read();
        switch (r) {
        case '1':
           digitalWrite(X_ENABLE_PIN,LOW);
           digitalWrite(Y_ENABLE_PIN,LOW);
           break;   
        case '0':
           digitalWrite(X_ENABLE_PIN,HIGH);
           digitalWrite(Y_ENABLE_PIN,HIGH);
           break;   
          
        case 'w':    
          stepper.moveTo(stepper.currentPosition()-stepsize);
          break;
        case 's':    
          stepper.moveTo(stepper.currentPosition()+stepsize);
          break;
        case 'a':    
          stepper1.moveTo(stepper1.currentPosition()-stepsize*2);
          break;
        case 'd':    
          stepper1.moveTo(stepper1.currentPosition()+stepsize*2);
          break;
        case '2':
          stepsize = 1;
          break;
        case '3':
          stepsize = 2;
          break;
        case '4':
          stepsize = 5;
          break;
        case '5':
          stepsize = 10;
          break;
        case '6':
          stepsize = 20;
          break;
        case '7':
          stepsize = 50;
          break;
        case '8':
          stepsize = 100;
          break;

        case '9':
          stepsize = 200;
          break;
         case '?':
          Serial.println(stepsize);
          break;         
          
        default:
          break;
          // turn all the LEDs off:
          }
        } 
        
       
    stepper.run();
    stepper1.run();
  
}
