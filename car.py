import RPi.GPIO as GPIO
from time import sleep


channel = [22,5,6,13,19,26]
# pin 5 and 6 acceleration
# pin 13 and 19 wheel direction
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

try:
    while 1:
        st = int(input("[1]left [2]right"))
        ac = int(input("speed:"))
        star.start(ac)
        if st==2:
            GPIO.output(13,0)
            GPIO.output(19,1)
        elif st==1:
            GPIO.output(13,1)
            GPIO.output(19,0)
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

except KeyboardInterrupt:
    GPIO.cleanup()
    # end the PWM
    print("\nExit....")
