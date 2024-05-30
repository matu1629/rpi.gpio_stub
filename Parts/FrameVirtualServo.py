import math
import time
import Parts.BaseFrame as BF
import Parts.Server as Svr
import COMMON.Common as Cmn

#BCM(GPIO) -> PIN
BCM2Servo = (11,)

class VirtualServoFrame(BF.BaseFrame):
    def __init__(self, top, label, bg):
        super().__init__(top, bg)
        super().label(label)
        self.canvas = super().canvas(Cmn.BG_COLOR, 180, 180)
        self.canvas.create_rectangle(60, 60, 120, 180, fill="blue")
        self.base = (80, 15, 85, 10, 95, 10, 100, 15, 100, 95, 95, 100, 85, 100, 80, 95)
        self.baselen = len(self.base)
        self.center = (90, 90)
        self.preA = 0.0
        self.servo = self.canvas.create_polygon(self.base, fill="white smoke")
        self.canvas.create_oval(86, 86, 94, 94, fill="gray8")
        # server
        self.server = None
    def getx(self, x, y, a):
        return (x - self.center[0]) * math.cos(a) - (y - self.center[1]) * math.sin(a) + self.center[0]
    def gety(self, x, y, a):
        return (x - self.center[0]) * math.sin(a) + (y - self.center[1]) * math.cos(a) + self.center[1]
    def rotate(self, a):
        ret = []
        for i in range(0, self.baselen, 2):
            ret.append(self.getx(self.base[i], self.base[i + 1], a))
            ret.append(self.gety(self.base[i], self.base[i + 1], a))
        return ret
    def off(self):
        self.move(0.0)
    def start(self):
        self.off()
        self.server = Svr.Server()
        self.server.start(self.callback)
    def close(self):
        if self.server != None:
            self.server.close()
    def destroy(self):
        self.close()
        super().destroy()
    def move(self, a):
        temp = self.preA
        delta = Cmn.getD(a - self.preA)
        while True:
            self.canvas.coords(self.servo, self.rotate(temp))
            time.sleep(0.001)
            temp += delta
            if (temp > a and delta > 0) or (temp < a and delta < 0):
                break
        self.canvas.coords(self.servo, self.rotate(a))
        self.preA = a
    def callback(self, channel, value):
        if channel == 0 and value == 0:
            self.off()
            return
        if channel in BCM2Servo:
            self.move(Cmn.getA(value))

