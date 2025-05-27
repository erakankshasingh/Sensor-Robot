import math
from machine import Pin, RTC, I2C
#import ssd1306
from time import sleep
from buzzer import Buzzer
from stepper import Stepper
from hcsr04 import HCSR04   
from oled import I2C as OLED_I2C 
from mpu6050 import MPU6050

# ——— Setup ———
led    = Pin(12, Pin.OUT)             # LED on D12
button = Pin(27, Pin.IN, Pin.PULL_UP) # Button on D27 w/ pull-up
buzzer = Buzzer(15)                   # Buzzer on D15

# Steppers: left on D13, right on D19

# — STEP pins stay in the Stepper constructor —
left_stepper  = Stepper(13)
right_stepper = Stepper(19)

# — DIR pins as separate GPIOs —
left_dir  = Pin(26, Pin.OUT)
right_dir = Pin(17, Pin.OUT)

# set both DIR lines
left_dir.value(1 if True else 0)
right_dir.value(1 if True else 0)

# ——— Ultrasonic setup ———
ultrasonic = HCSR04(trigger_pin=5, echo_pin=18)

# ——— I²C + OLED setup ———
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
oled = OLED_I2C(128, 64, i2c)  # width=128, height=64

# ——— Accelerometer setup ———
mpu = MPU6050(i2c)

# ——— Blocking wait function ———
def wait_button_press():
    # spin here until button.value() goes from 1 → 0
    while button.value() == 1:
        sleep(0.1)
    # once pressed, simply return

# ——— steps-from-cm conversion ———
def get_steps_from_distance(distance_cm):
    steps_per_rev      = 200              # full steps per 360°
    wheel_diameter_cm  = 6                # 60 mm
    circumference_cm   = math.pi * wheel_diameter_cm
    steps_per_cm       = steps_per_rev / circumference_cm
    return int(distance_cm * steps_per_cm)

# 1) All the libraries are imported and all the instances created (LED, Button, Buzzer, Stepper motors, Ultrasonic sensor, OLED screen and Accelerometer). 
    # Additionally 2 functions, one to wait for button press and other to calculate distance to steps.

# 2) ——— while loop to Ultrasonic sensor and stepper motor with step counts ———

while True:
    #start by turning the LED off.
    led.value(0)
    step_count = 0     # ← define it here!

    # 3) Clear the OLED and print a message
    oled.fill(0)
    oled.text('Press Button to Start', 0, 0)   # acknowledge completion of SPI_FAST_FLASH_BOO
    oled.show()
    sleep(1)   # pause so you can read it

    # 4) --- wait_button_press function call ---
    wait_button_press() 
    led.value(1)
    
    # 5) --- beep the buzzer once. ---
    buzzer.beep_once()

    # 6) Read the ultrasonic sensor distance and save it into a variable
    dist = ultrasonic.distance_cm()

    # 7) Pass the read distance on step 6. Save the returned steps into a variable.
    if dist is not None:
        steps = get_steps_from_distance(dist)
        print(f"Driving {steps} steps")

    # 8) Print the distance and calculated steps into the OLED.
    oled.fill(0)  # clear
    if dist is None:
        oled.text("Out of range", 0, 2)
    else:
        oled.text(f"D={dist:.1f}cm", 0, 2)
    oled.show()

    if steps is None:
        oled.text("Out of range", 0, 3)
    else:
        oled.text(f"Steps={steps}", 0, 3)
    oled.show()
    sleep(2)   # pause so you can read it

    # 9) Create a variable called reached and set it to True
    reached = True

    # 10) Create a for loop from 0 to range number of steps from step 8
    for i in range(steps):
        # 11) move the right and left motor one step
        right_stepper.move_one_step()
        left_stepper.move_one_step()
        sleep(0.01)
    
        # 12) read accelerometer Y-axis
        values = mpu.get_values()   # Read all sensor values into a dict
        AcY = values["AcY"]         # Extract just the Y-axis acceleration
        print("AcY:", AcY)

        # 13) and 14) tilt detection threshold
        if AcY > 12000 or AcY < -12000:
            # the robot was tilted while driving and it couldn't reach the target.
            reached = False
            print("Tilt detected! Aborting drive.")
            break

    # 15) Check if the "reached" variable is True after the loop
    if reached:
        # if so, print REACHED in the OLED and beep once
        oled.fill(0)
        oled.text("REACHED", 0, 0)
        oled.show()
        # single beep
        buzzer.beep_once()
    else:
        # turn ON the LED, print TILTED in the OLED
        led.value(1)
        # Clear the display and print “TILTED”
        oled.fill(0)
        oled.text("TILTED", 0, 0)
        oled.show()
        # three beeps with small pauses
        for _ in range(3):
            buzzer.beep_once()
            sleep(0.2)

    # 16) sleep 2 or 3 seconds to leave the message on the OLED so user can read it.
    sleep(3)
