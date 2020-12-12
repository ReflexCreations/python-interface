# RE:Flex Dance Python Interface

## Project Information

This tool lets you use a RE:Flex Dance Pad with any PC game by acting as a keyboard that presses keys when you press panels on the dance platform. It also lets you set pressure thresholds determining how easily a panel is "pressed", and lets you display custom images on the panel LEDs when pressed. All these settings can be saved to a profile for later quick recall.

It is built with Python, using HIDAPI (Human Interface Device, a USB standard; application programming interface to communicate with a single RE:Flex Dance Pad. The graphical user interface is implemented with PyQT5.

The tool further acts as a reference implementation for those who wish to implement a RE:Flex interface into their own codebase.

It implements the following features:
- Sensor data capture / conversion - Implements an extremely rudimentary absolute value driven sensor step detection implementation.
- Keyboard emulation - Maps the panels Left/Down/Up/Right to keyboard keys A/B/C/D. This is the easiest way to communicate with any / all programs.
- PNG file display on panels - Converts a 12x12 PNG file and displays this on panels when it is activated. Automatically rotates each image to match the panel (default being the UP arrow).
- User profiles - Can save user information to a '.rfx' file (A python dictionary stored in JSON format), making it easy to switch settings quickly.

Example user profiles and LED PNG files are provided in the `profiles` and `assets` directories.

## Building the Project

**These instructions were tested on Windows 10.**

This project was created using [VS Code](https://code.visualstudio.com/), with the Python plugin. It uses a virtual environment for dependencies, and PyInstaller to compile the single file executable. 

You can install the latest [Python](https://www.python.org/downloads/) release to get started, and [add it to your PATH environment variable](https://geek-university.com/uncategorized/add-python-to-the-windows-path/).

Within VS Code you can then use the provided terminal to setup your virtual environment and the dependencies. Start in your project root directory and enter: 

```
python -m venv env
pip install -r requirements.txt
```

You can activate your virtual environment by entering `env/Scripts/Activate.ps1` in your terminal, which is a powershell script that is automatically run by VS Code on project load. 

You can then run the program by entering `env/Scripts/python.exe main_window.py`. 

### Building the standalone program

You can build the project by running this command line script within the root directory of the project, with your virtual environment activated:

```
pyinstaller -w -F -i "assets\icon.ico" -n "reflex-config" main-window.py
```

Your program will then be in the `dist` folder.

## Project Improvements

As with everything, there's a lot that we could do to make this program better. Here's a list of fixes/improvements that I'd like to see in future updates:

### Bugs / Needs Investigation

- When more than one instance of the configuration tool is open, a single pad can still be accessed by both instances. This prevents both tools from communicating with the pad.
- Graphing reduces the sensor / LED update frequency. This isn't the end of the world as it's toggle-able, but it warrants investigation to prevent graphing data updates from causing the data to slow down.
- LED and sensor communication should run in separate threads and take the highest priority to ensure 1kHz communication to sensors and 62.5FPS communication to the LEDs.
- Currently, the paths for LED images and profiles are absolute. It would be useful if the image paths were relative to the location of the profile. This'd allow portability of these files between computers. That is, you could bring a USB stick to a friend's house and use your profile and images on their setup.
- Most of the code is portable, but a Linux / Mac OS implementation still need to be investigated and deployed. It would be best if the single code base could work on all of them, so the it would need to account for differences between these platforms.

### Quality of Life Improvements

- Automatically select a default profile upon program start-up.
- Option to select different key inputs for people who want different key mappings (instead of the currently hard-coded A/B/C/D). Save this mapping to the profile too.
- Currently, to connect to a pad, PNG files for LEDs need to be specified. This can be annoying. It could be worth having a set of default LED files. Whether that be simple arrows, or just nothing at all. A drop-down or something similar to select default LED files would also be useful here.
- Maybe make the icon actually display in the title bar and taskbar. It's kind of ugly. 
- Minimizing to system tray could also be useful. 
- The automatic PNG array rotation should be toggle-able.

### Feature Improvements

- The step detection could be much better. It should be converted to use a delta based step tracking system. It can utilize position tracking to handle foot-switching without removal of previous foot. The pad is also prone to vibration-induced hits. Anti-vibration should help. All of these options should be toggle-able / saved to profiles.
- Currently we just serve static images to the panels. This could be dramatically improved. Color-correction could be applied as the LEDs are non-linear in perceived brightness. GIFs could be interpreted to make use of the pads' animation capability. Automatic scaling to the required 12x12 size would make it easier to use; right now only PNGs that are exactly 12x12px are supported. We could even have our own data format for light 'routines';
- When firmware updates via USB / UART are made available for I/O and Panel boards, the utility should have an interface to flash a compiled executable to the platform. This however, depends on updates to the electronics and firmware.
- In the future, the pad won't just be 4-panel dependent. So a way to interpret how many panels are connected, and what configuration they're in while updating the GUI to match could dramatically improve flexibility.

## Release

The [release](https://github.com/ReflexCreations/python-interface/releases/latest) contains the compiled Windows executable of the latest RE:Flex Configuration tool.

## License

For license details, see LICENSE file