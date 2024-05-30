import Parts.VirtualLED as VLED

# left top x, left top y, right bottom x, right bottom y, type(1:rectangle, 2:oval)
LED_SITES = (
    (0, 80, 10, 160, 1),        # left bottom vertical ver
    (10, 150, 70, 160, 1),      # center bottom vertical ver
    (80, 150, 90, 160, 2),      # dot
    (70, 80, 80, 160, 1),       # right bottom vertical ver
    (10, 75, 70, 85, 1),        # center center horizontal ver
    (70, 0, 80, 80, 1),         # right top vertiacal ver
    (0, 0, 10, 80, 1),          # left top vertical ver
    (10, 0, 70, 10, 1),         # center top horizontal ver
)

class Virtual7segLED:
    def __init__(self, x, y, status):
        self.LEDs = []
        self.status = status
        index = 0
        for ls in LED_SITES:
            self.LEDs.append(VLED.VirtualLED(ls[0] + x, ls[1] + y, ls[2] + x, ls[3] + y, ls[4], index))
            index += 1

