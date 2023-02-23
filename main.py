from pybricksdev.connections.pybricks import PybricksHub
from pybricksdev.ble import find_device
import asyncio
import sys
import curses
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
    filename='pybricks.log',
    filemode='w'
)

log = logging.getLogger(__name__)


async def display_main(win):
    hub = PybricksHub()
    device = await find_device()
    # if there are multiple LEGO hubs around, you can force a specific hub by setting its BLE address, for example:
    # device = await find_device(service="c5f50001-8280-46da-89f4-6d8051e4aeef")
    await hub.connect(device)
    # transfer robot.py to LEGO hub
    await hub.run("robot.py", wait=False)

    win.clear()
    win.nodelay(True)
    deviceId = device.metadata["uuids"][0]
    log.info("Bluetooth Device ID: " + deviceId)
    win.addstr("Connected to Spike Prime Hub, BLE address:" + deviceId + "\n")
    win.addstr("Use arrow keys to drive; space to halt car; ESC to exit\n")

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
        if (key in robotCommandDict):
            commandStr = robotCommandDict[key] + "\0"
            # send the keyboard command to the hub
            await hub.write(commandStr.encode("UTF-8"))
        # I'd prefer the hub to stop running if the PC disconnects, but it appears we need a heartbeat
        # method to do this - instead, we'll ask it to stop, then exit
        if key == 27:
            sys.exit()


def main(win) -> None:
    return asyncio.run(display_main(win))


curses.wrapper(main)
