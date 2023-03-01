from pybricksdev.connections.pybricks import PybricksHub
from pybricksdev.ble import find_device
from bleak import BleakScanner, BleakClient
import asyncio
import sys
import curses
import logging

# Hub name assigned when installing the Pybricks firmware
HUB_NAME = "Pybricks Hub"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
    filename='pybricks.log',
    filemode='w'
)

log = logging.getLogger(__name__)

# Add the ability to react to input from the robot
class ResponseHandlerMixin:
    _responseHandler = None

    def __init__(self, responseHandler, **kwargs):
        super().__init__(**kwargs)
        self._responseHandler = responseHandler

    def line_handler(self, line):
        input = line.decode()
        self._responseHandler(input)


class MyPybricksHub(ResponseHandlerMixin, PybricksHub):
    pass


async def display_main(win):
    def response_handler(response):
        log.info("Robot says: " + response)
        win.move(3, 0)
        win.clrtoeol()
        win.addstr(3, 0, response + "\n")

    hub = MyPybricksHub(response_handler)
    device = await find_device()
    # if there are multiple LEGO hubs around, you can force a specific hub by setting its BLE address, for example:
    # device = await find_device(service="c5f50001-8280-46da-89f4-6d8051e4aeef")
    await hub.connect(device)
    # transfer robot.py to LEGO hub
    await hub.run("robot.py", wait=False)

    win.clear()
    win.nodelay(True)
    deviceId = device.metadata["uuids"][0]
    win.addstr(1, 0, "Connected to Hub; BLE address:" + deviceId + "\n")
    win.addstr(2, 0, "Use arrow keys to drive; space to halt car; ESC to exit\n")
    log.info("Bluetooth Device ID: " + deviceId)

    robotCommandDict = {
        curses.KEY_LEFT: "L",
        curses.KEY_RIGHT: "R",
        curses.KEY_UP: "U",
        curses.KEY_DOWN: "D",
        32: " ",    # Spacebar
        27: "exit"  # ESC key
    }
    while True:
        key = win.getch()
        await asyncio.sleep(.01) # hack to give curses time to handle screen changes
        if (key in robotCommandDict):
            commandStr = robotCommandDict[key] + "\0"
            # send the command to the hub
            await hub.write(commandStr.encode("UTF-8"))
        if key == 27:
            sys.exit()


def main(win) -> None:
    return asyncio.run(display_main(win))


if __name__ == "__main__":
    curses.wrapper(main)
