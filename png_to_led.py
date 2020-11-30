import png



class ImageConverter():
    def __init__(self, image):
        if (image[0] % 12 != 0 or image[1] % 12 != 0) or (image[0] != image[1]):
            print("Interpolation currently unimplemented. Size x of image should equal size y, and be divisible by 12.")
            return
        led_array = [
            84, 84, 84, 84, 84,  0,  1, 84, 84, 84, 84, 84,
            84, 84, 84, 84,  2,  3,  4,  5, 84, 84, 84, 84,
            84, 84, 84,  6,  7,  8,  9, 10, 11, 84, 84, 84,
            84, 84, 12, 13, 14, 15, 16, 17, 18, 19, 84, 84,
            84, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 84,
            30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
            42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
            84, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 84,
            84, 84, 64, 65, 66, 67, 68, 69, 70, 71, 84, 84,
            84, 84, 84, 72, 73, 74, 75, 76, 77, 84, 84, 84,
            84, 84, 84, 84, 78, 79, 80, 81, 84, 84, 84, 84,
            84, 84, 84, 84, 84, 82, 83, 84, 84, 84, 84, 84
        ]
        line_index = 0
        for line in image[2]:
            pixel_index = 0
            for pixel in line:
                if pixel_index % 4 != 3:
                    if led_array[(line_index * 12) + (pixel_index // 4)] != 84:
                        print("{:4d},".format(pixel), end='')
                pixel_index += 1
            line_index += 1

if __name__ == "__main__":
    f = open("assets/gay.png", 'rb')
    r = png.Reader(f)
    image = r.read()
    print(image)
    ImageConverter(image)