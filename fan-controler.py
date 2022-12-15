import RPi.GPIO as GPIO
from time import sleep
import socket
import sys
import json

# check the host and port argv values
if len(sys.argv) < 3:
    print("no input argument [host] [port]")
    sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])

channel = [17, 27, 22, 19]

# for board setting
GPIO.setmode(GPIO.BCM)

# setup to pin mode
for i in channel:
    GPIO.setup(i, GPIO.OUT)

GPIO.output(27, 1)
GPIO.output(22, 0)
# rgb in pwm mode in a list
fan = GPIO.PWM(channel[0], 1000)
led = GPIO.PWM(channel[3], 1000)
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("socket created...")
        s.connect((host, port))
        print("connected to the server")
        s.send(b'[CLIENT]:fan controlling started')
        while 1:
            try:
                print(s.recv(11).decode('utf-8'))
                data = int(s.recv(11).decode('utf-8'))
                if data > 100:
                    data = 100

                fan.start(data)
                led.start(data)
                # data = list(s.recv(11).decode('utf-8').strip().split(" "))
                # if data:
                #     rgb = [100, 100, 100]  # default in off condition

                #     if len(data) > 3 or len(data) < 3:
                #         rgb = precolor
                #     else:
                #         for i in range(3):
                #             for i, value in enumerate(data):
                #                 if value == "" or value == " " or len(value) > 3:
                #                     rgb[i] = int(precolor[i])
                #                 else:
                #                     if int(value) > 100:
                #                         rgb[i] = int(precolor[i])
                #                     else:
                #                         rgb[i] = int(value)

                #             precolor = rgb
                #             print(f"RGB:{rgb}::DATA:{data}")
                #             for i in range(len(channel)):
                #                 fan[i].ChangeDutyCycle(rgb[i])
                #     del data, rgb
            except ValueError as e:
                print(f"[ERROR]:{e}")
                print("try again...")
                GPIO.cleanup()
                sys.exit()

except KeyboardInterrupt:
    GPIO.cleanup()
    # end the PWM
    fan.stop()
    print("\nExit....")
    # close the socket connection
    s.close()
