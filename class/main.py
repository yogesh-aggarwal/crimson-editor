from tkinter import Tk

class mainWindow(Tk):
    def __init__(self, title, width, height, icon, openX=0, openY=0):
        super().__init__()
        self.title = title
        self.width = width
        self.height = height
        self.icon = icon
        self.openX = openX
        self.openY = openY

    
    def createWindow(self):
        self.wm_title(self.title)
        self.wm_geometry(f"{self.width}x{self.height}")
    
    def addMenu(self):
        from tools import menu
        
        # FILE MENU
        fileMenu = menu.fileMenu(self, activeforeground="white", activebackground="black", background="black", foreground="black", selectcolor="white", font=("google sans regular", 13))
        editMenu = menu.editMenu(self, activeforeground="white", activebackground="black", background="black", foreground="black", selectcolor="white", font=("google sans regular", 13))
        
        self.config(menu=fileMenu)
        # self.config(menu=editMenu)
        
    def createTextArea(self):
        from tools import textArea

    def bindKey(self, key, operation):
        self.bind(key, operation)
    # def destroyWiroy()
    
    

win = mainWindow("Crimson editor", 900, 450, icon="")
win.createWindow()
win.addMenu()
win.createTextArea()
win.mainloop()