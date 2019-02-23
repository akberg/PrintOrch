'''
Part class, used in PrintOrch by UserGUI.pyw
Author: Andreas Klavenes Berg
Created: 10.01.2019
'''
import tkinter as tk

'''
class Part
---------------------------------------------------------
Tkinter object, combining a textbox with a spinbox to
list files and apply number of copies to be made
'''
class Part(tk.Frame):
    def __init__(self, master, path, fname, **kwargs):
        self.h = 1
        self.path = path
        self.name = tk.StringVar()
        self.num = tk.IntVar()
        self.num.set(1)
        self.name.set(fname)
        self.frame = tk.Frame(master, **kwargs)
        self.partname = tk.Label(self.frame, width=40, textvariable=self.name)
        self.partname.pack(side=tk.LEFT)
        self.btnDOWN = tk.Button(self.frame, text="-", height=self.h, width=1, command=self.actionDown)
        self.btnDOWN.pack(side=tk.RIGHT)
        self.numIn = tk.Entry(self.frame, width=3, textvariable=self.num, state=tk.DISABLED) # ???
        self.numIn.pack(side=tk.RIGHT)
        self.btnUP = tk.Button(self.frame, text="+", height=self.h, width=1, command=self.actionUp)
        self.btnUP.pack(side=tk.RIGHT)

    def actionUp(self):
        self.num.set(self.num.get() + 1)
        self.btnDOWN.config(state=tk.NORMAL)

    def actionDown(self):
        self.num.set(self.num.get() - 1)
        if self.num.get() == 0:
            self.btnDOWN.config(state=tk.DISABLED)

    def get(self):
        return self.num.get()

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)