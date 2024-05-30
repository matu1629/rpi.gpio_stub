import tkinter as tk

def gotoFrame(nowFrame, nextFrame):
    nowFrame.close()
    nextFrame.tkraise() # next frame is top
    nextFrame.start()

class BaseFrame(tk.Frame):
    def __init__(self, top, bg):
        super().__init__(top, background=bg)
        self.grid(row=1, column=0, sticky="nsew")
    def canvas(self, bg, height, width):
        canvas = tk.Canvas(self, background=bg, height=height, width=width)
        canvas.pack()
        return canvas
    def label(self, text):
        label = tk.Label(self, text=text)
        label.pack()
    def GFButton(self, text, frame):
        button = tk.Button(self, text=text, width=20 ,command=lambda:gotoFrame(self, frame))
        button.pack()
    def start(self): # override
        '''
        when this frame is top, this method is called
        reference gotoFrame()
        '''
        pass
    def close(self): # override
        '''
        when this frame is not top, this method is called
        reference gotoFrame()
        '''
        pass
