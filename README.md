# PoC: keypad timing attack

This project features a PoC for a very simple timing attack. The goal is to 'guess' the correct PIN on the keypad without any prior knowledge. This type of attack is part of a group called side channel attacks, some very interesting stuff you can dig into. ;D

To get further infos on setup and the attack read the [how it works](./docs/the_attack.md).

There is also a lightweight version which takes input over the serial console and does not require a keypad. [see code here ](./code/vulnerable_serial/vulnerable_serial.ino)

## materials
**hardware**
- Arduino UNO (or other model with ATmega328)
- Logic Analyser
- breadboard
- 3x4 keypad
- 3 colored LEDs
- 220Ω resistor
- a lot of jumper wires

**software**
- Arduino IDE
- SALEAE Logic 2

## setup/wiring
Because we use a 4x4 button matrix, but don't need the row with letters we can ignore the 8. pin (blue wire) comming from the keypad.

![wireing](./docs/img/wireing.png)

Install the library, flash the [code](./code/vulnerable_keypad/vulnerable_keypad.ino) to the microcontroller and you are ready to go!

> The serial console can be used to see the I/O.

## attack
Configure Logic to wait for a trigger and capture afterwards.
- hide not needed channels and rename (optional)  

*> Device Settings > Trigger*
- select channel
- falling edge
- capture time = 100µs

After capturing a sample, measure the time from the falling edge of the trigger to the rising edge of the reject LED.  
*> Timing Makers > Measurements > add measurement*

![first_pin_correct](./docs/img/logic_first_pin_correct.png)

Now you can perform some measurements. Enter a bunch of random PINs and see what the average time without a correct digit is. Afterwards you can start testing the digits for the first number one by one, if the time delta gets larger you know the digit is correct. Loop through this process for all digits in the pin.

[my measurments](./measurements/plain_measuring.md)  

If you have a better logic analyzer your measurements might not have the noise I captured with my crappy one.

**example**  
Let's measure for the first digit.

digit | time delta
--- | ---
0000   | 9,808µs
1000   | 10,063µs
2000   | 9,846µs
3000   | 9,846µs

From the samples we can see that the first digit has to be a 1 because the time of the check increased. Next we would try the same with the next digit.  
Inputting: `1000, 1100, 1200, ...`
