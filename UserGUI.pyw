'''
PrintOrch with graphical user interface
Author: Andreas Klavenes Berg
Created: 08.01.2019
'''

# Imports
from easygui    import diropenbox, msgbox
from PyPDF2     import PdfFileMerger, PdfFileReader
from os         import listdir
from Part       import Part
import tkinter as tk

# TODO: List parts, find names, change num copies with up/down btns, set work as title


class PrintOrch:
    def __init__(self):
        # ---------------------------------------------------------
        #  Tk
        # ---------------------------------------------------------
        self.root = tk.Tk("PrintOrch")
        self.root.geometry("480x360")

        # ---------------------------------------------------------
        # Variables
        # ---------------------------------------------------------
        self.path = tk.StringVar() # Oppdaterer automatisk forelder
        self.path.set("Choose path")
        # ---------------------------------------------------------
        self.save_path = tk.StringVar()
        self.save_path.set("Choose save path")
        # ---------------------------------------------------------
        self.work = tk.StringVar()
        self.work.set("No work chosen")
        # ---------------------------------------------------------
        self.save_name = tk.StringVar()
        self.save_name.set("Filename")
        # ---------------------------------------------------------
        self.out_file = PdfFileMerger()
        self.alt = -1
        self.n = 0
        self.content = []
        self.nums = []

        # ---------------------------------------------------------
        # TITLE FRAME
        # --------------------------------------------------------- 
        self.title = tk.Frame(self.root)
        self.title.pack()
        # ---------------------------------------------------------
        tk.Label(self.title, textvariable=self.work).pack(side=tk.TOP)
        tk.Label(self.title, text="Save as:").pack(side=tk.LEFT)
        # ---------------------------------------------------------
        self.nameIn = tk.Entry(self.title, textvariable=self.save_name)
        self.nameIn.pack(side=tk.RIGHT)
        # ---------------------------------------------------------

        # TODO: Display files in title label, with input field to change number of copies

        # ---------------------------------------------------------
        # PATH FRAME
        # ---------------------------------------------------------
        self.pathFrame = tk.Frame(self.root)
        self.pathFrame.pack()
        # ---------------------------------------------------------
        tk.Label(self.pathFrame, text="Open directory:").grid(row=0)
        tk.Label(self.pathFrame, text="Save to directory:").grid(row=1)
        # ---------------------------------------------------------
        # Display paths
        self.pathIn = tk.Entry(self.pathFrame, textvariable=self.path)
        self.pathIn.grid(row=0, column=1)
        # ---------------------------------------------------------
        self.save_pathIn = tk.Entry(self.pathFrame, textvariable=self.save_path)
        self.save_pathIn.grid(row=1, column=1)
        # ---------------------------------------------------------
        
        # ---------------------------------------------------------
        # LIST PARTS
        # ---------------------------------------------------------
        self.parts = []
        self.partFrame = tk.Frame(self.root, height=40, width=60)
        self.partFrame.pack()
        # ---------------------------------------------------------
        self.scroll = tk.Scrollbar(self.partFrame)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox = tk.Listbox(self.partFrame, yscrollcommand=self.scroll.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        # ---------------------------------------------------------


        # ---------------------------------------------------------
        # ACTIONS FRAME
        # ---------------------------------------------------------
        # Get paths
        tk.Button(self.pathFrame, text="Browse", command=lambda: self.prompt_fetch_dir()).grid(row=0, column=2)
        tk.Button(self.pathFrame, text="Browse", command=self.prompt_save_dir).grid(row=1, column=2)
        # ---------------------------------------------------------
        self.actionFrame = tk.Frame(self.root)
        self.actionFrame.pack(fill=tk.X, side="bottom")
        # ---------------------------------------------------------
        self.quitBtn = tk.Button(self.actionFrame, text="Quit", command=exit)
        self.quitBtn.pack(side="left")
        # ---------------------------------------------------------
        self.goBtn = tk.Button(self.actionFrame, text="Proceed", command=self.proceed)
        self.goBtn.pack(side="right")

    # ---------------------------------------------------------
    # MAIN LOOP
    # ---------------------------------------------------------
    def run(self):
        self.root.mainloop()

    # ---------------------------------------------------------
    # METHODS
    # ---------------------------------------------------------
    def prompt_fetch_dir(self):
        '''
        Get source folder, and display all pdf files to be included
        '''
        p = diropenbox("Velg mappen som inneholder stykket som skal skrives ut.", "Hent notemappe")
        if p != "":
            self.path.set(p)
            # List files in the chosen directory
            self.listbox.delete(0, tk.END)
            for f in listdir(p):
                if ".pdf" in f:
                    self.listbox.insert(tk.END, Part(self.listbox, p, f).pack())

    def prompt_save_dir(self):
        '''
        Get save directory
        '''
        p = diropenbox("Velg mappen hvor du vil lagre utskriftfilen.", "Velg målmappe")
        if p != "":
            self.save_path.set(p)

    def proceed(self):
        msgbox(self.pathIn.get() + "\n" + self.save_pathIn.get())
        pass


# ---------------------------------------------------------
# ---------------------------------------------------------
# MAIN 
# ---------------------------------------------------------
main = PrintOrch()
main.run()
# ---------------------------------------------------------
