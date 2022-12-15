#!/usr/bin/env python
import asyncio
from websockets import connect
import sys
import RPi.GPIO as GPIO
from time import sleep
import json

channel = [22, 5, 6, 13, 19, 26]
# pin 5 and 6 acceleration
# pin 13 and 19 wheel direction
# pin 22 and 26 are the PWM control pins
# 13 = left
# 19 = right
# for board setting
GPIO.setmode(GPIO.BCM)

# setup to pin mode
for i in channel:
    GPIO.setup(i, GPIO.OUT)

# rgb in pwm mode in a list
star = GPIO.PWM(26, 1000)
acc = GPIO.PWM(22, 1000)


async def hello(uri):
    try:
        async with connect(uri, ping_interval=None) as websocket:
            try:
                await websocket.send("Hello world!")
                while 1:
                    # cont = {"direction": "", "rospeed": 0, "acspeed": 0}
                    control = json.loads(await websocket.recv())
                    print(control)
                    if control:
                        if "direction" in control.keys():
                            if "rospeed" in control.keys():
                                star.start(control['rospeed'])
                                if control['direction'] == "right":
                                    GPIO.output(13, 0)
                                    GPIO.output(19, 1)
                                elif control['direction'] == "left":
                                    GPIO.output(13, 1)
                                    GPIO.output(19, 0)
                            if "acspeed" in control.keys():
                                acc.start(control['acspeed'])
                                if control['direction'] == "forward":
                                    GPIO.output(5, 1)
                                    GPIO.output(6, 0)
                                elif control['direction'] == "backward":
                                    GPIO.output(5, 0)
                                    GPIO.output(6, 1)

            except KeyboardInterrupt:
                GPIO.cleanup()
                # end the PWM
                print("\nExit....")
                sys.exit()
    except KeyboardInterrupt:
        GPIO.cleanup()
        # end the PWM
        print("\nExit....")
        sys.exit()
asyncio.run(hello(f"ws://{sys.argv[1]}:{sys.argv[2]}"))
