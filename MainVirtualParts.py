import Parts.BaseForm as Form
import Parts.BaseFrame as BFrame
import Parts.FrameVirtualLED as FVLED
import Parts.FrameVirtualColorLED as FVCLED
import Parts.FrameVirtual7segLED as FV7LED
import Parts.FrameVirtual7segx4LED as FV7x4LED
import Parts.FrameVirtualServo as FVServo
import Parts.FrameVirtualSensor as FVSensor

# Form
Form = Form.BaseForm("Virtual Parts", "gray95")
Form.cb_topmost(True)

# Each LED frames
FrameVLED = FVLED.VirtualLEDFrame(Form, "LED", "gray95")
FrameVCLED = FVCLED.VirtualColorLEDFrame(Form, "Color LED", "gray95")
FrameV7LED = FV7LED.Virtual7segLEDFrame(Form, "7seg LED", "gray95")
FrameV7x4LED = FV7x4LED.Virtual7segx4LEDFrame(Form, "7segx4 LED", "gray95")
FrameVServo = FVServo.VirtualServoFrame(Form, "Servo", "gray95")
FrameVSensor = FVSensor.VirtualSensorFrame(Form, "Sensor(click a sensor)", "gray95")

# Menu frame(top)
FrameMenu = BFrame.BaseFrame(Form, "gray95")
FrameMenu.label("Menu")
FrameMenu.GFButton("LED", FrameVLED)
FrameMenu.GFButton("Color LED", FrameVCLED)
FrameMenu.GFButton("7seg LED", FrameV7LED)
FrameMenu.GFButton("7segx4 LED", FrameV7x4LED)
FrameMenu.GFButton("Servo", FrameVServo)
FrameMenu.GFButton("Sensor", FrameVSensor)

# Return button for each Frames
FrameVLED.GFButton("Menu", FrameMenu)
FrameVCLED.GFButton("Menu", FrameMenu)
FrameV7LED.GFButton("Menu", FrameMenu)
FrameV7x4LED.GFButton("Menu", FrameMenu)
FrameVServo.GFButton("Menu", FrameMenu)
FrameVSensor.GFButton("Menu", FrameMenu)

Form.mainloop()
