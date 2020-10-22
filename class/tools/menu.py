from tkinter import Menu, filedialog, END

def sql(query):
    print(query)
    return query

class fileMenu(Menu):
    def __init__(self, tearoff, activeforeground, activebackground, background, foreground, selectcolor, font):
        super().__init__()
        self.tearoff = tearoff
        self.activeforeground = activeforeground
        self.activebackground = activebackground
        self.background = background
        self.foreground = foreground
        self.selectcolor = selectcolor
        self.font = font

        self.menu = Menu(self, tearoff=False)

        self.createMenu()
        self.createObjects()

    def createMenu(self):
        self.add_cascade(label="File", menu=self.menu)

    def createObjects(self, textarea=""):
        self.menu.add_cascade(label="New", command=None)
        self.menu.add_cascade(label="Open", command=lambda: self.openFile(insertLocation=True))
        self.menu.add_cascade(label="Save", command=lambda: self.Save().saveDecide())
        self.menu.add_cascade(label="Save As", command=lambda: self.Save().saveFileAs(textarea=textarea))
        self.menu.add_checkbutton(label="Auto Save", variable=None,
                                  onvalue="True", offvalue="False", command=None)
        self.menu.add_cascade(label="Save Checkpoint", command=None)
        self.menu.add_separator()
        self.menu.add_cascade(label="Page setup", command=self.pageSetup)
        self.menu.add_cascade(label="Print...", command=self.printDoc)
        self.menu.add_separator()
        self.menu.add_cascade(label="Exit", command=self.exitEditor)
    
    def openFile(self, insertLocation=True):
        try:
            filename = filedialog.askopenfilename(filetypes=(("Text file", "*.txt"),
                                                             ("Log file", "*.log"),
                                                             ("All Files", "*.*")))
            file = open(filename, "r")
            readData = file.read()
            file.close()

            if insertLocation:
                # INSERT THE LOCATION OF FILE INTO SQL DATABASE.
                pass

            return readData
        except Exception as e:
            print(f"FROM MENU.PY (fileMenu class) ---> {e}")

    class Save:
        def __init__(self):
            pass
        
        def saveFile(self, textarea):
            if self.saveDecide():
                file_location = sql("SELECT value FROM TEMP_WORK WHERE work_name='file_location'")

                data = textarea.get('1.0', END+'-1c')
                
                # INSERT THE LOCATION OF FILE IN SQL DATABASE
                sql(f"UPDATE TEMP_WORK SET value='{file_location}' WHERE work_name='file_location'")
                file = open(file_location, "w")
                file.write(data)
                file.close()
                del file

                return True

            else:
                self.saveFileAs(textarea=textarea)

        def saveFileAs(self, textarea):
            try:
                file_location = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text File", "*.txt"),
                                                                                                 ("Log file", "*.log"),
                                                                                                 ("All Files", "*.*")))
                data = textarea.get('1.0', END+'-1c')
                
                # INSERT THE LOCATION OF FILE IN SQL DATABASE
                sql(f"UPDATE TEMP_WORK SET value='{file_location}' WHERE work_name='file_location'")
                file = open(file_location, "w")
                file.write(data)
                file.close()
                del file

                return True
            except Exception as e:
                print(f"FROM MENU.PY (fileMenu class) ---> {e}")

        def saveDecide(self):
            """
            Returns whether to directly save the file or not.
            >>> True ---> Save Directly\n
            >>> False ---> Save "Save As"
            """
            if sql(f"SELECT value FROM TEMP_WORK WHERE work_name='file_location'"):
                return False
            else:
                return True

        class AutoSave:
            def __init__(self):
                pass

        class Checkpoint:
            def __init__(self):
                pass
        
    def pageSetup(self):
        pass
    
    def printDoc(self):
        pass
    
    def exitEditor(self):
        exit(0)


class editMenu(Menu):
    def __init__(self, tearoff, activeforeground, activebackground, background, foreground, selectcolor, font):
        super().__init__()
        self.tearoff = tearoff
        self.activeforeground = activeforeground
        self.activebackground = activebackground
        self.background = background
        self.foreground = foreground
        self.selectcolor = selectcolor
        self.font = font

        self.menu = Menu(self, tearoff=False)

        self.createMenu()
        self.createObjects()

    def createMenu(self):
        self.add_cascade(label="Edit", menu=self.menu)

    def createObjects(self, textarea=""):
        self.menu.add_command(label="Undo", command=lambda *awargs: textarea.edit_undo)
        self.menu.add_command(label="Redo", command=lambda *awargs: textarea.edit_redo)
        self.menu.add_separator()
        self.menu.add_cascade(label="Cut", command=lambda: textarea.event_generate(("<<Cut>>")))
        self.menu.add_cascade(label="Copy", command=lambda: textarea.event_generate(("<<Copy>>")))
        self.menu.add_cascade(label="Paste", command=lambda: textarea.event_generate(("<<Paste>>")))
        # self.menu.add_cascade(label="Delete", command=lambda *awargs: pyautogui.press("delete"))
        self.menu.add_separator()
        self.menu.add_cascade(label="Find", command=lambda *awargs: None)
        self.menu.add_cascade(label="Find next")
        self.menu.add_cascade(label="Replace...")
        self.menu.add_cascade(label="Go To...")
        self.menu.add_separator()
        # self.menu.add_cascade(label="Select All", command=lambda *awargs: pyautogui.hotkey("ctrl", "a"))
        # self.menu.add_cascade(label="Time/Date", command=insert_datetime)
