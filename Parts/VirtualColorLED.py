class VirtualColorLED:
    def __init__(self, x, y, w, h, t, i, v):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.t = t # type
        self.i = i # index
        self.v = v # value[r, g, b]
        self.id = None
