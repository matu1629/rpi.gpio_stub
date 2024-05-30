import Parts.BaseFrame as BF
import Parts.VirtualColorLED as VLED
import Parts.Server as Svr
import COMMON.Common as Cmn

#BCM(GPIO) -> PIN
BCM2COLOR = (4, 10, 11)

def getColor(data):
    if data in BCM2COLOR:
        return BCM2COLOR.index(data)
    return -1

class VirtualColorLEDFrame(BF.BaseFrame):
    def __init__(self, top, label, bg):
        super().__init__(top, bg)
        super().label(label)
        self.canvas = super().canvas(Cmn.BG_COLOR, 180, 60)
        self.vLED = VLED.VirtualColorLED(10, 10, 50, 170, 1, 0, [Cmn.LOW_VALUE, Cmn.LOW_VALUE, Cmn.LOW_VALUE])
        self.vLED.id = self.canvas.create_rectangle(self.vLED.x, self.vLED.y, self.vLED.w, self.vLED.h, \
            fill=Cmn.getFullColor(*self.vLED.v))
        # server
        self.server = None
    def off(self):
        for lv in self.vLED.v:
            lv = Cmn.LOW_VALUE
        self.canvas.itemconfig(self.vLED.id, fill=Cmn.getFullColor(*self.vLED.v))
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
    def callback(self, channel, value):
        if channel == 0 and value == 0:
            self.off()
            return
        bcmcolor = getColor(channel)
        if bcmcolor != -1:
            self.vLED.v[bcmcolor] = value
            self.canvas.itemconfig(self.vLED.id, fill=Cmn.getFullColor(*self.vLED.v))

