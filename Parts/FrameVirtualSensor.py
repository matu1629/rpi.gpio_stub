import Parts.BaseFrame as BF
import Parts.Server as Svr
import COMMON.Common as Cmn

#BCM(GPIO) -> PIN
BCM2Sensor = (11,)

class VirtualSensorFrame(BF.BaseFrame):
    def __init__(self, top, label, bg):
        super().__init__(top, bg)
        super().label(label)
        self.canvas = super().canvas(Cmn.BG_COLOR, 180, 180)
        self.on = False
        self.sensor = self.canvas.create_polygon((55, 75, 65, 65, 115, 65, 125, 75, 125, 120, 55, 120), fill=self.getColor())
        self.canvas.create_rectangle(60, 120, 120, 180, fill="green")
        self.canvas.tag_bind(self.sensor, "<Button-1>", func=self.click)
        # server
        self.server = None
    def getColor(self):
        if self.on:
            return "gray64"
        return "white smoke"
    def click(self, _):
        self.on = not self.on
        self.canvas.itemconfig(self.sensor, fill=self.getColor())
    def off(self):
        if self.on:
            self.on = False
            self.canvas.itemconfig(self.sensor, fill=self.getColor())
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
        if channel in BCM2Sensor:
            if not self.on:
                return Cmn.LOW_VALUE
            return Cmn.HIGH_VALUE
