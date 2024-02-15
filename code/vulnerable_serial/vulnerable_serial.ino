// the pin
const char PIN[4] = {'1', '3', '3', '7'};

// state LEDs
const int rejectLed = A0;
const int inputLed = A1;
const int acceptLed = A2;


// init serial and LEDs
void setup() {
    Serial.begin(9600);
    pinMode(inputLed, OUTPUT);
    pinMode(acceptLed, OUTPUT);
    pinMode(rejectLed, OUTPUT);
}

// link the LEDs
void blink(int led, int times) {
    for (int i = 0; i < times; i++) {
        digitalWrite(led, HIGH);
        print(led);
        delay(500);
        digitalWrite(led, LOW);
    }
}

// print to serial console
void print(int led) {
    if (led == rejectLed) {
        Serial.println("red LED");
    }
    if (led == acceptLed) {
        Serial.println("green LED");
    }
}

// check the entered PIN
bool check_key(String key) {
    for (int i = 0; i < 4; i++) {
        if (PIN[i] != key[i]) {
            blink(rejectLed, 1);
            return false;
        }
    }
    blink(acceptLed, 1);
    return true;
}

void loop() {
    String key = "";
    while (Serial.available() == 0) {
        // wait till input
    }
    key = Serial.readString();
    Serial.print(key);

    Serial.println("#");
    blink(inputLed, 1);
    check_key(key);
}
