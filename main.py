from pybricksdev.connections.pybricks import PybricksHub
from pybricksdev.ble import find_device
import asyncio
from pynput import keyboard
import sys


async def main():
    hub = PybricksHub()
    device = await find_device()
    # if there are multiple hubs around, you can force a specific hub by setting its BLE address, for example:
    # device = await find_device(service="c5f50001-8280-46da-89f4-6d8051e4aeef")
    print("Connected to Spike Prime Hub, BLE address: " +
          device.metadata["uuids"][0])
    await hub.connect(device)
    # upload to robot.py to hub
    await hub.run("robot.py", wait=False)
    print("PC Ready")
    print("Use arrow keys to drive, Esc to exit")
    while True:
        with keyboard.Events() as events:
            for event in events:
                if isinstance(event, keyboard.Events.Press):
                    if event.key == keyboard.Key.esc:
                        print("Exiting")
                        await hub.write(b"exit\0")
                        sys.exit()
                    elif event.key == keyboard.Key.left or \
                            event.key == keyboard.Key.right or \
                            event.key == keyboard.Key.up or \
                            event.key == keyboard.Key.down or \
                            event.key == keyboard.Key.space:
                        msg = event.key.name + "\0"
                        await hub.write(msg.encode("UTF-8"))
                        # print("TX:" + msg, end="", flush=True)


asyncio.set_event_loop(asyncio.new_event_loop())
loop = asyncio.new_event_loop()
loop.run_until_complete(main())
