from uselect import poll
from usys import stdin

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import DCMotor
from pybricks.parameters import Port, Direction

hub = PrimeHub()
leftDrive = DCMotor(Port.B, Direction.COUNTERCLOCKWISE)
rightDrive = DCMotor(Port.A, Direction.CLOCKWISE)
input_buffer = ""
loop_poll = poll()
loop_poll.register(stdin)
lDuty = 0
rDuty = 0


def correct_duty_limits(speed):
    deadZone = 20
    speed = min(max(speed, -100), 100)
    if speed != 0 and abs(speed) < deadZone:
        return int(deadZone * (speed / abs(speed)))
    else:
        return int(speed)


def input_handler(msg):
    global lDuty
    global rDuty
    # print(" RX:" + msg)
    d = 20
    if msg == "left":
        lDuty += -d
        rDuty += d
    elif msg == "right":
        lDuty += d
        rDuty += -d
    elif msg == "up":
        if lDuty != rDuty:
            lDuty = rDuty = max(lDuty, rDuty)
        else:
            lDuty += d
            rDuty += d
    elif msg == "down":
        if lDuty != rDuty:
            lDuty = rDuty = min(lDuty, rDuty)
        else:
            lDuty += -d
            rDuty += -d
    elif msg == "space":
        lDuty = rDuty = 0
    elif msg == "exit":
        raise SystemExit("Closing program.")
    lDuty = correct_duty_limits(lDuty)
    rDuty = correct_duty_limits(rDuty)
    print("L: {}, R: {}".format(lDuty, rDuty))
    leftDrive.dc(lDuty)
    rightDrive.dc(rDuty)


def update_input(char):
    global input_buffer
    if char == "\0":
        input_handler(input_buffer)
        input_buffer = ""
    else:
        input_buffer += char


def main_loop():
    print("Robot Ready")
    while True:
        if loop_poll.poll(50):  # times out after 100ms
            char = stdin.read(1)
            if char is not None:
                update_input(char)


main_loop()
