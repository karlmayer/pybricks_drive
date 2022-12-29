from pybricksdev.connections.pybricks import PybricksHub
from pybricksdev.ble import find_device
import asyncio
import sys
import curses


async def display_main(win):
    hub = PybricksHub()
    device = await find_device()
    # if there are multiple hubs around, you can force a specific hub by setting its BLE address, for example:
    # device = await find_device(service="c5f50001-8280-46da-89f4-6d8051e4aeef")
    await hub.connect(device)
    # upload robot.py to hub
    await hub.run("robot.py", wait=False)

    win.clear()
    win.nodelay(True)
    win.addstr("Connected to Spike Prime Hub, BLE address: " +
               device.metadata["uuids"][0] + "\n")
    win.addstr("Use arrow keys to drive; space to halt car; ESC to exit\n")

    while True:
        key = win.getch()
        if key == curses.KEY_LEFT:
            await hub.write("L\0".encode("UTF-8"))
        elif key == curses.KEY_RIGHT:
            await hub.write("R\0".encode("UTF-8"))
        elif key == curses.KEY_UP:
            await hub.write("U\0".encode("UTF-8"))
        elif key == curses.KEY_DOWN:
            await hub.write("D\0".encode("UTF-8"))
        elif key == 32: # SPACE
            await hub.write(" \0".encode("UTF-8"))
        elif key == 27: # ESC
            await hub.write(b"exit\0")
            sys.exit()


def main(win) -> None:
    return asyncio.run(display_main(win))


curses.wrapper(main)
