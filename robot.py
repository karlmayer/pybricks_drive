from uselect import poll
from usys import stdin
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction

hub = PrimeHub()
leftDrive = Motor(Port.B, Direction.COUNTERCLOCKWISE)
rightDrive = Motor(Port.A, Direction.CLOCKWISE)
input_buffer = ""
loop_poll = poll()
loop_poll.register(stdin)
lDuty = 0 # duty cycle (power) of the left wheel
rDuty = 0 # duty cycle (power) of the right wheel

# Adjust motor duty to overcome breakaway force where
# static friction is greater than dynamic friction
# https://en.wikipedia.org/wiki/Duty_cycle
def correct_duty_limits(speed):
    deadZone = 30
    speed = min(max(speed, -100), 100)
    if speed != 0 and abs(speed) < deadZone:
        return int(deadZone * (speed / abs(speed)))
    else:
        return int(speed)

# Respond to commands from the PC
def input_handler(msg):
    global lDuty
    global rDuty
    d = 30 # duty cycle delta (the amount it will change up or down)
    if msg == "L":
        lDuty += -d
        rDuty += d
    elif msg == "R":
        lDuty += d
        rDuty += -d
    elif msg == "U":
        if lDuty != rDuty:
            lDuty = rDuty = max(lDuty, rDuty)
        else:
            lDuty += d
            rDuty += d
    elif msg == "D":
        if lDuty != rDuty:
            lDuty = rDuty = min(lDuty, rDuty)
        else:
            lDuty += -d
            rDuty += -d
    elif msg == " ":
        lDuty = rDuty = 0
    elif msg == "exit":
        raise SystemExit
    lDuty = correct_duty_limits(lDuty)
    rDuty = correct_duty_limits(rDuty)
    print("L: {}, R: {}".format(lDuty, rDuty))
    leftDrive.dc(lDuty)
    rightDrive.dc(rDuty)

# Assemble input from the PC into a command
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
