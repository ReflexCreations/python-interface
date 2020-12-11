import ctypes

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

class KeyboardInput():
    def __init__(self, data, sensitivities):
        self.set_baselines(data)
        self.key_values = [30, 48, 46, 32]
        self.thresholds = [sensitivities[0], sensitivities[1], sensitivities[2], sensitivities[3]]
        self.hysteresis = [self.thresholds[0]/2, self.thresholds[1]/2, self.thresholds[2]/2, self.thresholds[3]/2]
        self.is_pressed = [ 0,  0,  0,  0]

    def set_baselines(self, data):
        self.baselines = []
        index = 0
        for panel_baseline in data:
            self.baselines.append(0)
            self.baselines[index] = panel_baseline
            index += 1

    def PressKey(self, hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
        x = Input( ctypes.c_ulong(1), ii_ )
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def ReleaseKey(self, hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
        x = Input( ctypes.c_ulong(1), ii_ )
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def poll_keys(self, data):
        index = 0
        for panel_value in data:
            if not self.is_pressed[index]:
                if panel_value > (self.baselines[index] + self.thresholds[index]):
                    self.PressKey(self.key_values[index])
                    self.is_pressed[index] = 1 
            else:
                if panel_value < (self.baselines[index] + self.thresholds[index] - self.hysteresis[index]):
                    self.ReleaseKey(self.key_values[index])
                    self.is_pressed[index] = 0
            index += 1