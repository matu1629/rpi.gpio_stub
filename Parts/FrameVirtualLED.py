import Parts.BaseFrame as BF
import Parts.VirtualLED as VLED
import Parts.Server as Svr
import COMMON.Common as Cmn

#BCM(GPIO) -> PIN
BCM2LED = (11,)

class VirtualLEDFrame(BF.BaseFrame):
    def __init__(self, top, label, bg):
        super().__init__(top, bg)
        super().label(label)
        self.canvas = super().canvas(Cmn.BG_COLOR, 180, 60)
        self.vLED = VLED.VirtualLED(10, 10, 50, 170, 1, 0)
        self.vLED.id = self.canvas.create_rectangle(self.vLED.x, self.vLED.y, self.vLED.w, self.vLED.h, \
            fill=Cmn.getMonoColor(Cmn.LOW_VALUE))
        # server
        self.server = None
    def off(self):
        self.canvas.itemconfig(self.vLED.id, fill=Cmn.getMonoColor(Cmn.LOW_VALUE))
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
        if channel in BCM2LED:
            self.canvas.itemconfig(self.vLED.id, fill=Cmn.getMonoColor(value))
