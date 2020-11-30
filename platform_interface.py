import hid
import threading
from led_processing import LedProcessor
import numpy as np
from keyboard_input import KeyboardInput

class PlatformInterface():
    def __init__(self):
        self.h = hid.device()
        #ret = hid.Device(self.USB_VID, self.USB_PID)

        #devices = [d for d in hid.enumerate(self.USB_VID, self.USB_PID)]

        ret = self.h.open(self.USB_VID, self.USB_PID)
        self.is_running = True
        self.sample_counter = 0
        data = self.h.read(64)
        self.organize_data(data)
        self.sum_panel_data(self.panel_data)
        self.timer = 0
        self.keyboard_input = KeyboardInput(self.panel_values)
        self.pressed_on_frame = list(range(4))
        self.last_frame = list(range(4))

        self.led_frame = 0
        self.led_panel = 0
        self.led_segment = 0
        self.led_frame_data = 0
        self.led_data = []
        self.frame_changed = 0
        self.led_on = 0
        rot = 270

        self.led_sources = [
                LedProcessor.from_file("assets/test.png", 90),
                LedProcessor.from_file("assets/test.png", 180),
                LedProcessor.from_file("assets/test.png", 0),
                LedProcessor.from_file("assets/test.png", 270)
            ]
        # For some reason the first byte doesn't get sent, so pad in another
        #self.led_data.append(0)
        #self.led_data.append(self.led_frame_data)
        #for i in range(2, 65):
        #    self.led_data.append(0)
        #    self.led_data.append(128 if i % 3 == 0 else 0)
        thread = threading.Thread(target=self.loop, daemon=True)
        thread.start()

    def loop(self):
        rot = 0
        while self.is_running:
            data = self.h.read(64)
            self.organize_data(data)
            self.sum_panel_data(self.panel_data)
            self.keyboard_input.poll_keys(self.panel_values)
            self.sample_counter += 1

            self.update_led_frame()
            self.h.write(bytes(self.led_data))

    def update_led_frame(self):
        self.led_frame_data = 0
        if self.led_segment < 3:
            self.led_segment += 1
        else:
            self.led_segment = 0
            if self.led_panel < 3:
                self.led_panel += 1
            else:
                self.led_panel = 0
                if self.led_frame < 15:
                    self.led_frame += 1
                else:
                    self.led_frame = 0
        if self.led_frame != self.last_frame[self.led_panel]:
            if self.keyboard_input.is_pressed[self.led_panel]:
                self.pressed_on_frame[self.led_panel] = 1
            else:
                self.pressed_on_frame[self.led_panel] = 0
        self.last_frame[self.led_panel] = self.led_frame
        
        self.led_frame_data |= self.led_panel << 6 
        self.led_frame_data |= self.led_segment << 4
        self.led_frame_data |= self.led_frame

        source = self.led_sources[self.led_panel]
        segment_data = source.get_segment_data(self.led_segment)
        if self.pressed_on_frame[self.led_panel]:
            self.led_data = [0, self.led_frame_data] + segment_data
        else:
            self.led_data = [0, self.led_frame_data] + [0 for i in range(63)]

    def polling_rate(self):
        polling_rate = self.sample_counter
        self.sample_counter = 0
        return polling_rate

    def stop_loop(self):
        self.is_running = False

    def sum_panel_data(self, panel_data):
        self.panel_values = []
        for panel in range(0, 4):
            self.panel_values.append(0)
            for sensor in range(0, 4):
                self.panel_values[panel] += self.panel_data[sensor + 4 * (panel)]

    def organize_data(self, data):
        self.panel_data = []
        for i in range(0, 32):
            self.panel_data.append(0)
        data_index = 0
        for data_point in data:
            if data_index % 2 == 0:
                self.panel_data[data_index // 2] = data_point
            if data_index % 2 == 1:
                self.panel_data[data_index // 2] |= 0x0FFF & (data_point << 8)
            data_index += 1

    def disconnect(self):
        self.stop_loop()

    USB_VID = 0x0483 # Vendor ID for I/O Microcontroller
    USB_PID = 0x5750 # Product ID for I/O Microcontroller
    panel_data = []

if __name__ == "__main__":
    pf = PlatformInterface()