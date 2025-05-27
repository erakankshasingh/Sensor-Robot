# Sensor-Robot

Design and implementation of a simple robot in Wokwi that reads in a distance from an ultrasonic sensor, then issues commands to two stepper motors to rotate enough steps in order to move to the target distance. 
Assumption: the robot tires are 60mm diameter.

The robot contains the following elements:

    Ultrasonic sensor
    OLED display connected via I2C
    An LED connected to the microcontroller
    An Accelerometer
    A Buzzer
    Two stepper motors with their respective drivers
    A push button

The robot contains an accelerometer, if the robot detects (using the accelerometer) that it is tipped over, a warning LED should light up and a buzzer will beep 3 times, the word TILTED will be shown in the display and any stepper motion should be halted.

An example of this type of robot can be a vacuum robot. Of course this type of robot have an additional component (the vaccuum) but the principle is the same.

It has an ultrasonic sensor to detect obstacles and change vacuum direction, also it can have an accelerometer to detect if, for any reason is tilted, stop the vacuum and robot movement.

Vacuum cleaner robot
Project Summary

The robot starts on IDLE, where it doesn’t take any measurements or drive the steppers and a message is shown in the OLED "Press button to start". Once the button is pressed once, the buzzer beeps once and the robot will measure the distance from the ultrasonic sensor, show it on the OLED display and drive whatever the distance is. (i.e. if the distance is 20cm the robot will drive the stepper motors to reach 20cm) then it will beep once, show “reached” on the OLED display and stop.

Additionally, if an accelerometer reading indicates the robot is tipped over while driving, a warning LED should light up and a buzzer will beep 3 times, the word TILTED will be shown in the display and any stepper motion should be halted.
Robot images and videos

Simulation is a very good tool to test things, specially when working on online courses or designing prototypes, but its always better to see things working. This is why we built the robot and filmed some small videos showing the behaviour.
