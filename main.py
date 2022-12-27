from pybricksdev.connections.pybricks import PybricksHub
from pybricksdev.ble import find_device
import asyncio
import sys
import os

if os.name == "nt":
    import msvcrt
else:
    import termios
    import tty


def getkey():
    if os.name != "nt":
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            b = ""
            if os.name == "nt":
                if msvcrt.kbhit():
                    b = msvcrt.getch()
            else:
                b = os.read(sys.stdin.fileno(), 3).decode()

            if b != "":
                if len(b) == 3:
                    k = ord(b[2])
                else:
                    k = ord(b)
                key_mapping = {
                    127: "backspace",
                    10: "return",
                    32: "space",
                    9: "tab",
                    27: "esc",
                    65: "up",
                    66: "down",
                    67: "right",
                    68: "left",
                    72: "up",
                    80: "down",
                    77: "right",
                    75: "left",
                }
                return key_mapping.get(k, chr(k))
            else:
                return ""
    finally:
        if os.name != "nt":
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


async def main():
    hub = PybricksHub()
    device = await find_device(service="c5f50001-8280-46da-89f4-6d8051e4aeef")
    print("Connected to Spike Prime Hub, BLE address: " + device.metadata["uuids"][0])
    await hub.connect(device)
    await hub.run("robot.py", wait=False)
    print("PC Ready")
    print("Use arrow keys to drive, Esc to exit")
    while True:
        try:
            k = getkey()
            if k == "esc":
                quit()
            if k == "space":
                await hub.write((k + "\0").encode("UTF-8"))
            if k == "up" or k == "down" or k == "left" or k == "right":
                msg = k + "\0"
                # print("TX:" + msg, end="", flush=True)
                await hub.write(msg.encode("UTF-8"))
        except (KeyboardInterrupt, SystemExit):
            print("Exiting")
            await hub.write(b"exit\0")
            if os.name != "nt":
                os.system("stty sane")
            exit()


asyncio.set_event_loop(asyncio.new_event_loop())
loop = asyncio.new_event_loop()
loop.run_until_complete(main())
