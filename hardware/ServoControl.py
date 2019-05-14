#!/user/bin/env python

import sys
import time
import random
import pigpio

NUM_GPIO=4

MIN_WIDTH=1000
MAX_WIDTH=2000

pi = pigpio.pi()

if not pi.connected:
	exit()


pi.set_PWM_frequency(NUM_GPIO, 300)
pi.set_servo_pulsewidth(NUM_GPIO, 1485)
time.sleep(0.25)
pi.set_servo_pulsewidth(NUM_GPIO, 1000)
time.sleep(0.25)
pi.set_servo_pulsewidth(NUM_GPIO, 2000)
time.sleep(0.25)
pi.set_servo_pulsewidth(NUM_GPIO, 0)
pi.stop()
