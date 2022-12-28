## Prereqs
* Python 3.10 https://www.python.org/downloads/
* poetry https://python-poetry.org/

## Setup
    
    poetry install

## Run
    
    poetry run python main.py

## Notes
The first version of this program redirected stdin for keyboard input. To simplify the code, I switched to _pynput_, which, for security reasons, required adding VS Code to MacOS Input Monitoring. Keyboard input is not working from my MacOS terminal, so I may ditch pynput at a later time.

## Resources
* pybricksdev: https://github.com/pybricks/pybricksdev
* PyBricks/PC communication: https://pybricks.com/projects/tutorials/wireless/hub-to-device/pc-communication/
* More PyBricks/PC communication: https://github.com/pybricks/support/issues/470
* PyBricks motor control: https://docs.pybricks.com/en/stable/pupdevices/motor.html
* PyBricks polling: https://docs.pybricks.com/en/stable/micropython/uselect.html
* PC keyboard input: https://stackoverflow.com/questions/24072790/how-to-detect-key-presses
* PC keyboard input (Windows): https://stackoverflow.com/questions/58712657/python-with-msvcrt-how-to-detect-keyboard-input-from-another-active-window
