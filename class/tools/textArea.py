from tkinter import Text, Scrollbar, Tk
from tkinter.constants import *

class textArea(Text):
    def __init__(self, width, height, bg, fg, font, selectbackground, selectforeground, relief=FLAT, bd=3, wrap="word", maxundo=-1):
        super().__init__()
        self.width = width
        self.height = height
        self.background = bg
        self.foreground = fg
        self.selectbackground = selectbackground
        self.selectforeground = selectforeground
        self.wrap = wrap
        self.relief = relief
        self.font = font
        self.bd = bd
        self.maxundo = maxundo

        self.createTextArea()

    def createTextArea(self):
        self.textarea = Text(win, width=self.width, height=self.height, background=self.background, foreground=self.foreground, selectbackground=self.selectbackground, selectforeground=self.selectforeground, wrap=self.wrap, relief=self.relief, font=self.font, bd=self.bd)
        self.textarea.pack()

    def toggleScrollbar(self, textarea, axis="X"):
        yview_scrollbar = Scrollbar(self)
        yview_scrollbar.config(command=textarea.yview, relief=RAISED)
        yview_scrollbar.pack(side=RIGHT, fill=Y)
        xview_scrollbar = Scrollbar(self, orient=HORIZONTAL)
        xview_scrollbar.config(command=textarea.xview)

        if self.wrap == "char":
            xview_scrollbar.pack(side=BOTTOM, fill=X, expand=1)
            textarea.configure(xscrollcommand=xview_scrollbar.set, undo=True, maxundo=-1,
                               autoseparators=True, yscrollcommand=yview_scrollbar.set)
            self.wrap="char"
        else:
            textarea.configure(yscrollcommand=yview_scrollbar.set, undo=True,
                               maxundo=-1, autoseparators=True)




if __name__ == "__main__":
    win = Tk()

    textArea(150, 200, "white", "black", ("google sans bold", 11), "black", "white", ).createTextArea()

    win.mainloop()    



