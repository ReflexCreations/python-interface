# RE:Flex Dance Python Interface

## Project Information

This python interface tool uses HIDAPI to communicate with a single RE:Flex Dance Pad. The tool functions as a reference example implementation for other software developers to follow should they wish to implement a RE:Flex interface into their own codebase. It also provides an easy interface to start using your dance pad to play PC games.

It implements the following features:
- Sensor data capture / conversion - Implements an extremely rudimentary absolute value driven sensor step detection implementation.
- Keyboard emulation - Maps the panels Left/Down/Up/Right to keyboard keys A/B/C/D. This is the easiest way to communicate with any / all programs.
- PNG file display on panels - Converts a 12x12 PNG file and displays this on panels when it is activated.
- User profiles - Can save user information to a '.rfx' file (A python dictionary stored in JSON format), making it easy to switch settings quickly.

Example user profiles and LED PNG files are provided in the profiles/assets sub-directories.

## Building the Project

This project was created using [VS Code](https://code.visualstudio.com/), with the Python plugin. It uses a virtual environment for dependencies, and PyInstaller to compile the single file executable. 

You can install the latest [Python](https://www.python.org/downloads/) release to get started, and [add it to your path environment variable](https://geek-university.com/uncategorized/add-python-to-the-windows-path/).

Within VS Code you can then use the provided terminal to setup your virtual environment and the dependencies. Start in your project root directory and enter: 

```
python -m venv env
pip install PyQt5
pip install hidapi
pip install pillow
pip install numpy
pip install pyqtgraph
```

You can activate your virtual environment by entering `env/Scripts/Activate.ps1` in your terminal, which is a powershell script that is automatically run by VS Code on project load. 

You can then run the program by doing `env/Scripts/python.exe main_window.py`. 

You can build the project by running this command line script within the root directory of the project, with your virtual environment activated:

`pyinstaller -w -F -i "assets\icon.ico" -n "reflex-config" main-window.py`

Your program will then be found in the 'dist' folder.

## Project Improvements

As with everything, there's a lot that we could do to make this program better. Here's a list of fixes/improvements that I'd like to see in future utility updates:

### Bugs / Needs Investigation

- When more than one of the configuration tools are open, a single pad can still be accessed by both programs. This will prevent both tools from communicating with the pad.
- Graphing reduces the sensor / LED update frequency. This isn't the end of the world as it's toggle-able, but it warrants investigation to prevent graphing data updates from causing the data to slow down.
- Lights/Sensors should be communicated with in their own threads and take the highest priority to ensure 1kHz communication to sensors and 62.5FPS communication to the lights.
- Currently, the file directories are absolute for the lights and profiles. However, it'd be useful if these were relative, and it was standardized to have access to an assets/profiles directory in sub-directories of the RE:Flex Config executable location. This'd allow portability of these files between computers.
- Most of the code is portable. But a Linux / Mac implementation still need to be investigated and deployed.

### Quality of Life Improvements

- It'd be useful to automatically select a default profile upon program start-up.
- It would be useful if there was a drop-down to select different key inputs for people who want different key mappings, and for this to save to a user profile.
- Currently, to connect to a pad, PNG files for LEDs need to be specified. This can be annoying. It could be worth having a set of default LED files. Whether that be simple arrows, or just nothing at all. A drop-down or something similar to select default LED files would also be useful here.
- Maybe make the icon actually display in the title bar and taskbar. It's kind of ugly. 
- Minimizing to system tray could also be useful. 

### Feature Improvements

- The step detection could be far better. It should be converted to use a delta based step tracking system. It can utilize position tracking to handle foot-switching without removal of previous foot. And the pad is prone to vibration-induced hits. Anti-vibration should help. All of these options should be toggle-able / saved to profiles. 
- Currently we just serve images to the panels. This could be dramatically improved, also. Color-correction could be applied as the LEDs are non-linear in perceived brightness. GIFs could be interpreted to actually make use of the animation capability of the pad. Improvement from just 12x12 images would be useful. We could even have our own data format for light 'routines'. 
- When firmware updates via USB / UART are made available for I/O and Panel boards, the utility should have an interface to flash a compiled executable to the platform. However, this is dependent on updates to the electronics and firmware.

## Release

The release contains the compiled executable of the latest RE:Flex Configuration tool.

## License

For license details, see LICENSE file