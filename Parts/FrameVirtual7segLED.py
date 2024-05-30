import Parts.BaseFrame as BF
import Parts.Virtual7segLED as V7LED
import Parts.Server as Svr
import COMMON.Common as Cmn

#BCM(GPIO) -> PIN
BCM2LED = (7, 8, 25, 23, 18, 4, 10, 11)
#segments position
#    -(11)
#|(10)    |(4)
#    -(18)
#|(7)     |(23)
#    -(8) .(25)

def getLED(data):
    if data in BCM2LED:
        return BCM2LED.index(data)
    return -1

class Virtual7segLEDFrame(BF.BaseFrame):
    def __init__(self, top, label, bg):
        super().__init__(top, bg)
        super().label(label)
        self.canvas = super().canvas(Cmn.BG_COLOR, 180, 110)
        self.vDisp = V7LED.Virtual7segLED(10, 10, Cmn.LOW_VALUE)
        color = Cmn.getMonoColor(Cmn.LOW_VALUE)
        for led in self.vDisp.LEDs:
            if led.t == 2: # oval
                led.id = self.canvas.create_oval(led.x, led.y, led.w, led.h, fill=color)
            else: # rectangle
                led.id = self.canvas.create_rectangle(led.x, led.y, led.w, led.h, fill=color)
        # server
        self.server = None
    def off(self):
        for led in self.vDisp.LEDs:
            self.canvas.itemconfig(led.id, fill=Cmn.getMonoColor(Cmn.LOW_VALUE))
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
        bcmLed = getLED(channel)
        if bcmLed != -1:
            self.canvas.itemconfig(self.vDisp.LEDs[bcmLed].id, fill=Cmn.getMonoColor(value))
