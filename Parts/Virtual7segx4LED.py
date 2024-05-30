import Parts.Virtual7segLED as V7LED

UNIT_SITES = (
    (0, 0),
    (100, 0),
    (200, 0),
    (300, 0),
)

class Virtual7segx4LED:
    def __init__(self, x, y, unitstatus, ledstatus):
        self.Units = []
        for us in UNIT_SITES:
            self.Units.append(V7LED.Virtual7segLED(us[0] + x, us[1] + y, unitstatus))
        self.LEDStatus = [ledstatus] * len(V7LED.LED_SITES)

