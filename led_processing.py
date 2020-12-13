from PIL import Image
import numpy as np
import math

class LedProcessorError(Exception):
    pass

class LedProcessor():
    def __init__(self, image, rot):
        """
        Initializes processing of a 12x12 PNG image for reflex Dance LED data
        processing.
        The image must be 12x12. Grayscale is currently not supported, but
        RGB, RGBA at any bit depth is supported. RGB values of non-8 bit depth
        will be multiplied to be represented in 8 bit.
        Parameters:
            - png_image: a 4-tuple returned by pypng's reader.Read
        Raises:
            - LedProcessorError if the PNG image has dimensions that do not
              match 12x12
            - LedProcessorError if the PNG image is greyscale.
        """
        exp_w = self.__LED_GRID_WIDTH
        exp_h = self.__LED_GRID_HEIGHT

        if image.size[0] != self.__LED_GRID_WIDTH or image.size[1] != self.__LED_GRID_HEIGHT:

            raise LedProcessorError(
                f"Can only process {exp_w}x{exp_h} PNGs at the moment"
            )
        
        image = image.rotate(rot)

        image.load()
        bg = Image.new("RGB", image.size, (255, 255, 255))
        bg.paste(image, mask=image.split()[3])
        bitmap = np.array(bg.getdata())

        self.masked_rgb_list = self.__make_masked_rgb_array(bitmap)

        self.__ordered_rgb_list = \
                self.__order_into_segments(self.masked_rgb_list)

    def from_file(png_file_path, rot):
        r = Image.open(png_file_path)
        return LedProcessor(r, rot)

    __LED_GRID_WIDTH = 12
    __LED_GRID_HEIGHT = 12
    __LED_COUNT = 84
    __LEDS_PER_SEGMENT = 21

    # Pixel mask shows which of the pixels in a 12x12 bitmap we care about.
    # In processing the data, only the rgb data for the pixels represented by
    # a 1 in this grid is kept, the rest discarded.
    __PIXEL_MASK = [
        [0,0,0,0,0,1,1,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,0,0,0,0],
        [0,0,0,1,1,1,1,1,1,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,1,1,1,0,0,0],
        [0,0,0,0,1,1,1,1,0,0,0,0],
        [0,0,0,0,0,1,1,0,0,0,0,0]
    ]

    # Lookup table for gamme corrections, each of these 256 values corresponds
    # to an input R, G, or B value
    __GAMMA_LUT = [
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
          1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
          2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
          5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
         10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
         17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
         25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
         37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
         51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
         69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
         90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
        115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
        144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
        177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
        215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255
    ]

    # LED positioning lookup table to translate from regular left to right,
    # top to bottom, into left to right, top to bottom, in 4 segments,
    # in the order: top-left, top-right, bottom-left, bottom-right
    # The index used in this array is the original index, the value stored
    # there is where it should go in the repositioned array
    __POSITION_LUT = [
         0, 21,  2,  1, 23, 22,  5,  4,  3, 26, 25, 24,
         9,  8,  7,  6, 30, 29, 28, 27, 14, 13, 12, 11,
        10, 35, 34, 33, 32, 31, 20, 19, 18, 17, 16, 15,
        41, 40, 39, 38, 37, 36, 83, 82, 81, 80, 79, 78,
        62, 61, 60, 59, 58, 57, 77, 76, 75, 74, 73, 56,
        55, 54, 53, 52, 72, 71, 70, 69, 51, 50, 49, 48,
        68, 67, 66, 47, 46, 45, 65, 64, 44, 43, 63, 42
    ]

    def get_segment_data(self, segment_index):
        start_index = segment_index * self.__LEDS_PER_SEGMENT
        end_index = start_index + self.__LEDS_PER_SEGMENT
        segment = self.__ordered_rgb_list[start_index : end_index]

        flat_segment = []

        for led in segment:
            r, g, b = led
            # LEDs expect GRB not RGB
            flat_segment.extend([g,r,b])

        return flat_segment

    def __make_masked_rgb_array(self, bitmap):
        """
        Given the sequence of lines, each containing rgb[a] values of a given
        bit depth, applies the pixel mask to only keep the pixels we're
        interested in, discards alpha values as transparency doesn't apply,
        and returns an array of 3-value (RGB) tuples, representing each of the
        LEDs in pixel_mask where it's "1", in order of left to right, top to
        bottom. We also apply color correction here.
        """

        rgb_values_list = []
        y = 0
        values_per_pixel = 3

        bitmap = bitmap.reshape(12, 36)

        for row in bitmap:
            val_index = -1
            for val in row:
                val_index += 1
                x = val_index // values_per_pixel

                # If pixel_mask dictates current pixel is unused, skip to next
                if self.__PIXEL_MASK[y][x] == 0: continue
                rgb_values_list.append(int(val))

            y += 1

        rgb_values = []

        # Group into rgb tuples
        for i in range(0, int(len(rgb_values_list) / 3)):
            r = self.color_correct(float(rgb_values_list[i * 3 + 0])/255.0, 1.0)
            g = self.color_correct(float(rgb_values_list[i * 3 + 1])/255.0, 0.8)
            b = self.color_correct(float(rgb_values_list[i * 3 + 2])/255.0, 0.9)
            rgb_values.append((r,g,b))

        return rgb_values
    
    def color_correct(self, in_col, mul):
        out_col = math.floor(math.pow(in_col, 2) * 255.0 * mul)
        out_col = max(0, min(out_col, 255))
        out_col = int(out_col)
        return out_col

    def __order_into_segments(self, rgb_values):
        ordered_leds = [None] * self.__LED_COUNT

        for i, led in enumerate(rgb_values):
            ordered_leds[self.__POSITION_LUT[i]] = led

        return ordered_leds