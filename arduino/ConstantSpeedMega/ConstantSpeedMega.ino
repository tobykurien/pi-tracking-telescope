// PiScope Arduino firmware
// Using an Arduino Mega with a stepper motor shield


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

float stepsize = 500;
int varDelay = 10;

void setup() {
    pinMode(X_ENABLE_PIN, OUTPUT);
    pinMode(Y_ENABLE_PIN, OUTPUT);
    digitalWrite(X_ENABLE_PIN, LOW);
    digitalWrite(Y_ENABLE_PIN, LOW);

    Serial.begin(115200);
    printHelp();
}

void stepX(int steps, int dir) {
    if (dir == 0) {
        digitalWrite(X_DIR_PIN, LOW);
    } else {
        digitalWrite(X_DIR_PIN, HIGH);
    }

    for (int x = 0; x < steps; x++) {
        digitalWrite(X_STEP_PIN, HIGH);
        delay(varDelay);
        digitalWrite(X_STEP_PIN, LOW);
        delay(varDelay);

        if(x%50==0)Serial.println(x);
    }
}


void printHelp(){
      Serial.println("? Print this help ");
      Serial.println("1 Enable Motors ");
      Serial.println("0 Disable Motors ");
      Serial.println("");
      Serial.println("2  - 9 delay from 20 to 90 ms");
      Serial.println("u Motor 1 - CW  ");
      Serial.println("n Motor 1 - CCW ");
      Serial.println("t 5000 steps ");
      Serial.println("b -5000 steps ");
      Serial.println("o 100 steps ");
      Serial.println("l -100 steps ");
      Serial.println("i 10 steps");
      Serial.println("k -10 steps");
}

void loop() {
    if (Serial.available()) {
        byte r = Serial.read();

        switch (r) {
            case '?':
              printHelp();
          
            case '1':
                digitalWrite(X_ENABLE_PIN, LOW);
                digitalWrite(Y_ENABLE_PIN, LOW);
                break;
                
            case '0':
                digitalWrite(X_ENABLE_PIN, HIGH);
                digitalWrite(Y_ENABLE_PIN, HIGH);
                break;
    
            case 'u':
                Serial.print("U  ");
                Serial.println(stepsize);
                stepX(stepsize, 1);
                break;
            case 'n':
                Serial.print("N  ");
                Serial.println(stepsize);
                stepX(stepsize, 0);
                break;
            case 't':
                Serial.println("T  5000");
                stepX(5000, 0);
                break;
    
            case 'b':
                Serial.println("B -5000");
                stepX(5000, 1);
                break;
    
            case 'o':
                Serial.println("O 100 ");
                stepX(1000, 0);
                break;
    
            case 'l':
                Serial.println("L -100 ");
                stepX(1000, 1);
                break;
    
    
            case 'i':
              Serial.println("I 10 ");
              stepX(50, 0);
              break;
        
            case 'k':
              Serial.println("K -10 ");
              stepX(50, 1);
              break;

            case '2':
                Serial.println("delay = 20");
                varDelay = 20;
                break;
            case '3':
                Serial.println("delay = 30");
                varDelay = 30;
                break;
            case '4':
                Serial.println("delay = 40");
                varDelay = 40;
                break;
            case '5':
                Serial.println("delay  =  50");
                varDelay = 50;
                break;
            case '6':
                Serial.println("delay  =  60");
                varDelay = 60;
                break;
            case '7':
                Serial.println("delay  =  70");
                varDelay = 70;
                break;
            case '8':
                Serial.println("delay  =  80");
                varDelay = 80;
                break;
            case '9':
                Serial.println("delay  =  90");
                varDelay = 90;
                break;

            default:
                break;
        }
    }
}
