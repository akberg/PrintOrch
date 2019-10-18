'''
PrintOrch with graphical user interface
Author: Andreas Klavenes Berg
Created: 08.01.2019
Updated: 24.02.2019
'''

from easygui    import diropenbox, msgbox, ccbox
from PyPDF2     import PdfFileMerger, PdfFileReader
from os         import listdir
from gui.Part       import Part
from tkinter    import ttk
import tkinter as tk

# TODO: List parts, find names, change num copies with up/down btns, set work as title

# -----------------------------------------------------------------
# class PrintOrch 
# -----------------------------------------------------------------
# Main class. Creates and displays main app
# -----------------------------------------------------------------
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
        self.pathVar = ""
        # ---------------------------------------------------------
        self.save_path = tk.StringVar()
        self.save_path.set("Choose save path")
        self.save_pathVar = ""
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
        # frame - canvas+scrollbar - frame
        # TODO: Create boundaries for scrollbar to prevent it from throwing
        # the content away. Make the scrollbar look enabled and enable 
        # scroll with mouse holds
        # ---------------------------------------------------------
        self.parts = []
        self.partFrame = tk.Frame(self.root, height=220, width=360)
        self.partFrame.pack()
        self.partFrame.pack_propagate(0)
        # ---------------------------------------------------------
        self.scrollable = tk.Canvas(self.partFrame, borderwidth=0, bg="#ffffff")
        # ---------------------------------------------------------
        self.listbox = tk.Frame(self.scrollable, bg="#ffffff")
        # ---------------------------------------------------------
        self.scroll = ttk.Scrollbar(self.partFrame, command=self.scrollable.yview)
        self.scroll.pack(side=tk.RIGHT, fill="y")
        # ---------------------------------------------------------
        self.scrollable.configure(yscrollcommand=self.scroll.set)
        self.scrollable.pack(side=tk.LEFT, fill="both", expand=True)
        self.scrollable.create_window((4,4), window=self.listbox, anchor="nw")
        # ---------------------------------------------------------
        @staticmethod
        def onFrameConfigure(canvas):
            '''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))
        # ---------------------------------------------------------
        self.listbox.bind("<Configure>", lambda event, canvas=self.scrollable: onFrameConfigure(self.scrollable))
        self.scrollable.bind_all('<MouseWheel>', lambda event: self.scrollable.yview_scroll(int(-1*(event.delta/120)), "units"))
        #self.listbox = tk.Listbox(self.partFrame, yscrollcommand=self.scroll.set)
        #self.listbox.pack(side=tk.LEFT, fill=tk.Y)
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
        self.goBtn = tk.Button(self.actionFrame, text="Proceed", state=tk.DISABLED, command=self.proceed)
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
            self.pathVar = p
            self.path.set(p)
            self.save_name.set(p.split("\\")[-1] + "_printready")
            if self.save_path != "":
                self.goBtn.configure(state=tk.NORMAL)
            # List files in the chosen directory
            #self.listbox.delete(0, tk.END)
            for f in listdir(p):
                if ".pdf" in f:
                    p = Part(self.listbox, p, f)
                    p.pack()
                    self.parts.append(p)

    def prompt_save_dir(self):
        '''
        Get save directory
        '''
        p = diropenbox("Velg mappen hvor du vil lagre utskriftfilen.", "Velg målmappe")
        if p != "":
            self.save_path.set(p)
            if self.path != "":
                self.goBtn.configure(state=tk.NORMAL)

    def proceed(self):
        if not ccbox("Fullføre " + self.save_pathIn.get() + self.save_name.get() + "?", choices=("Fullfør", "Avbryt"), default_choice="Fullfør", cancel_choice="Avbryt"):
            pass
        p = self.path.get()
        for part in self.parts:
            n = part.get()
            for i in range(n):
                self.out_file.append(p + part.getFile())
        self.out_file.write(self.save_path.get() + "\\" + self.save_name.get())
        pass
    
    


# ---------------------------------------------------------
# ---------------------------------------------------------
# MAIN 
# ---------------------------------------------------------
main = PrintOrch()
main.run()
# ---------------------------------------------------------
