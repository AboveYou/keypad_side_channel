#include <Keypad.h>

// the pin
const int PIN_LEN = 4;
const char PIN[PIN_LEN] = {'1', '3', '3', '7'};

// state LEDs
const int rejectLed = A0;
const int inputLed = A1;
const int acceptLed = A2;

// keypad configuration
const byte ROWS = 4;
const byte COLS = 3;
char keys[ROWS][COLS] = {
    {'1', '2', '3'},
    {'4', '5', '6'},
    {'7', '8', '9'},
    {'*', '0', '#'}};
// keyboard pins D2-D8
byte rowPins[ROWS] = {8, 7, 6, 5};
byte colPins[COLS] = {4, 3, 2};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

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
    if (led == 16) {
        Serial.println("red LED");
    }
    if (led == 15) {
        Serial.println("green LED");
    }
}

// check the entered PIN
bool check_key(char key[]) {
    bool pass_flag = true;
    for (int i = 0; i < PIN_LEN; i++) {
        if (PIN[i] != key[i]) {
            pass_flag = false;
        }
    }
    // return based on the flag
    if (pass_flag) {
        blink(acceptLed, 1);
        return true;
    }
    else {
        blink(rejectLed, 1);
        return false;
    }
}

void loop() {
    char key[10];
    char current_index = 0;
    char current_key;
    do {
        key[current_index] = keypad.getKey();
        current_key = key[current_index];
        if (current_key == NO_KEY) {
            continue;
        }
        else if (current_key == '*') {
            blink(inputLed, 2);
            return;
        }
        Serial.println(current_key);
        // blink(inputLed, 1);
        current_index++;
    } while (current_key != '#' && current_index <= 9);
    blink(inputLed, 1);
    check_key(key);
    current_index = 0;
}
