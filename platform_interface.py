import hid
import threading
from led_processing import LedProcessor
import numpy as np
from keyboard_input import KeyboardInput

class PlatformInterface():
    def enumerate(self):
        devices = [d for d in hid.enumerate(self.USB_VID, self.USB_PID)]
        return devices

    def launch(self, serial, sensitivities, keymaps):
        if serial == None:
            serial = '0'
        self.h = hid.device()
        try:
            self.h.open(self.USB_VID, self.USB_PID, serial_number=serial)
        except Exception:
            return 0
        if self.h.get_product_string() == 'RE:Flex Dance Pad':
            self.is_running = True
            self.setup(sensitivities, keymaps)
            return 1
        else:
            self.is_running = False
            return 0

    def assign_led_files(self, led_files):
        self.led_files = led_files
        self.led_sources = [
            LedProcessor.from_file(self.led_files[0], 90),
            LedProcessor.from_file(self.led_files[1], 180),
            LedProcessor.from_file(self.led_files[2], 0),
            LedProcessor.from_file(self.led_files[3], 270)
        ]

    def setup(self, sensitivities, keymaps):
        self.sample_counter = 0

        data = self.h.read(64)
        self.organize_data(data)
        self.sum_panel_data(self.panel_data)
        self.keyboard_input = KeyboardInput(self.panel_values, sensitivities, keymaps)

        self.pressed_on_frame = list(range(4))
        self.last_frame = list(range(4))
        self.led_frame = 0
        self.led_panel = 0
        self.led_segment = 0
        self.led_frame_data = 0
        self.led_data = []
        self.lights_counter = 0

        thread = threading.Thread(target=self.loop, daemon=True)
        thread.start()

    def loop(self):
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
            self.lights_counter += 1
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

    def sensor_rate(self):
        polling_rate = self.sample_counter
        self.sample_counter = 0
        return polling_rate

    def lights_rate(self):
        polling_rate = self.lights_counter // 4
        self.lights_counter = 0
        return polling_rate

    def stop_loop(self):
        self.is_running = False

    def sum_panel_data(self, panel_data):
        self.panel_values = []
        for panel in range(0, 4):
            self.panel_values.append(0)
            for sensor in range(0, 4):
                self.panel_values[panel] += self.panel_data[sensor + 4 * panel]

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

    USB_VID = 0x0483  # Vendor ID for I/O Microcontroller
    USB_PID = 0x5750  # Product ID for I/O Microcontroller
    panel_data = []

if __name__ == "__main__":
    pf = PlatformInterface()
