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

int stepsize = 100;
int varDelay = 0;

void setup() {
    pinMode(X_ENABLE_PIN, OUTPUT);
    pinMode(Y_ENABLE_PIN, OUTPUT);
    digitalWrite(X_ENABLE_PIN, HIGH);
    digitalWrite(Y_ENABLE_PIN, HIGH);

    Serial.begin(9600);
    printHelp();
}

void stepX(int steps, int dir) {
    digitalWrite(X_ENABLE_PIN, LOW);
    digitalWrite(Y_ENABLE_PIN, LOW);
  
    if (dir == 0) {
        digitalWrite(X_DIR_PIN, LOW);
    } else {
        digitalWrite(X_DIR_PIN, HIGH);
    }

    for (int x = 0; x < steps; x++) {
        digitalWrite(X_STEP_PIN, HIGH);
        //delay(varDelay);
        digitalWrite(X_STEP_PIN, LOW);
        //delay(varDelay);

        if(x%50==0)Serial.println(x);
    }

    digitalWrite(X_ENABLE_PIN, HIGH);
    digitalWrite(Y_ENABLE_PIN, HIGH);
}

void stepY(int steps, int dir) {
    digitalWrite(X_ENABLE_PIN, LOW);
    digitalWrite(Y_ENABLE_PIN, LOW);

    if (dir == 0) {
        digitalWrite(Y_DIR_PIN, LOW);
    } else {
        digitalWrite(Y_DIR_PIN, HIGH);
    }

    for (int x = 0; x < steps; x++) {
        digitalWrite(Y_STEP_PIN, HIGH);
        //delay(varDelay);
        digitalWrite(Y_STEP_PIN, LOW);
        //delay(varDelay);

        if(x%50==0)Serial.println(x);
    }

    digitalWrite(X_ENABLE_PIN, HIGH);
    digitalWrite(Y_ENABLE_PIN, HIGH);
}


void printHelp(){
      Serial.println("? Print this help ");
      Serial.println("1 Enable Motors ");
      Serial.println("0 Disable Motors ");
      Serial.println("");
      Serial.println("2  - 9 stepsize from 1 to 1000");
      Serial.println("w up");
      Serial.println("s down");
      Serial.println("a left");
      Serial.println("d right");
}

void loop() {
    if (Serial.available()) {
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

            default:
                break;
        }
    }
}
