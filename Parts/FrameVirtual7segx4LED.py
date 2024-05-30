import Parts.BaseFrame as BF
import Parts.Virtual7segx4LED as V7x4LED
import Parts.Server as Svr
import COMMON.Common as Cmn
# anode common type

#BCM(GPIO) -> PIN
BCM2UNIT = (22, 27, 17, 24)
#Numbers position
#(22)(27)(17)(24)

#BCM(GPIO) -> PIN
BCM2LED = (7, 8, 25, 23, 18, 4, 10, 11)
#segments position
#    -(11)
#|(10)    |(4)
#    -(18)
#|(7)     |(23)
#    -(8) .(25)

def getUnit(data):
    if data in BCM2UNIT:
        return BCM2UNIT.index(data)
    return -1

def getLED(data):
    if data in BCM2LED:
        return BCM2LED.index(data)
    return -1

class Virtual7segx4LEDFrame(BF.BaseFrame):
    def __init__(self, top, label, bg):
        super().__init__(top, bg)
        super().label(label)
        self.canvas = super().canvas(Cmn.BG_COLOR, 180, 410)
        self.vDisp = V7x4LED.Virtual7segx4LED(10, 10, Cmn.HIGH, Cmn.LOW)
        color = Cmn.getMonoColor(Cmn.LOW_VALUE)
        for unit in self.vDisp.Units:
            for led in unit.LEDs:
                if led.t == 2: # oval
                    led.id = self.canvas.create_oval(led.x, led.y, led.w, led.h, fill=color)
                else: # rectangle
                    led.id = self.canvas.create_rectangle(led.x, led.y, led.w, led.h, fill=color)
        # server
        self.server = None
    def off(self):
        for i in range(0, len(self.vDisp.LEDStatus)):
            self.vDisp.LEDStatus[i] = Cmn.LOW_VALUE
        for unit in self.vDisp.Units:
            unit.status = Cmn.HIGH_VALUE
            for led in unit.LEDs:
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
            # set segment
            self.vDisp.LEDStatus[bcmLed] = value
            return
        bcmUnit = getUnit(channel)
        if bcmUnit != -1:
            # show display
            self.vDisp.Units[bcmUnit].status = value
            for unit in self.vDisp.Units:
                if unit.status == Cmn.LOW_VALUE: # LOW:on, HIGH:off
                    for led in unit.LEDs:
                        self.canvas.itemconfig(led.id, fill=Cmn.getMonoColor(self.vDisp.LEDStatus[led.i]))
                else:
                    for led in unit.LEDs:
                        self.canvas.itemconfig(led.id, fill=Cmn.getMonoColor(Cmn.LOW_VALUE))
