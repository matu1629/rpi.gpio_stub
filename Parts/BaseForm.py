import tkinter as tk

def checkbuttonCheck(top, checkbuttonVar):
    top.attributes("-topmost", checkbuttonVar.get())

class BaseForm(tk.Tk):
    def __init__(self, title, bg):
        super().__init__()
        self.title(title)
        self.configure(bg=bg)
    def cb_topmost(self, topmost):
        self.attributes("-topmost", topmost)
        checkbuttonVar = tk.BooleanVar()
        checkbuttonVar.set(topmost)
        checkbutton = tk.Checkbutton(self, text="always on top", variable=checkbuttonVar, \
            command=lambda:checkbuttonCheck(self, checkbuttonVar))
        checkbutton.grid(row=0, column=0)
