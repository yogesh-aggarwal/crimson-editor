import datetime
import os
import sqlite3
import tempfile
import threading
import time
from tkinter import *
from tkinter import colorchooser, filedialog, messagebox, simpledialog, ttk

import pyautogui
import winshell
from win32com.client import Dispatch


"""
--------------------------------------------------------------------------------------------------------------------------------------------
Files used-

1) "tempfile.ced" for storing file data while changing the wrap temporarily
# 2) "wrap.ced" for word wrapping
# 3) "status.ced" for status bar
# 4) "temp.ced" for storing file path temporarily
# 5) "autosave.ced" for autosaving
--------------------------------------------------------------------------------------------------------------------------------------------
Shortcut Keys-

1) F1 = About
2) F2 = Color theme decide (Opposites the current state means if theme is applied, it will deapply it or vice-versa)
3) F3 = Change word wrapping
4) F4 = Status bar decide (Opposites the current state means if status bar is applied, it will deapply it or vice-versa)
5) F5 = Insert time and date with the leading white spaces.
6) F11 = Enter full screen mode (ESC to exit)
7) Ctrl+F1 = Checkpoints (ESC to exit)
8) Ctrl+F5 = Settings
9) Ctrl+Shift+F1 = Save checkpoint
10) F6 = Converts text to speech
11) F7 = Search on Wikipedia for short paragraphs
12) F8 = Translate to other languages
13) F9 = Toggle autosave or not
14) Ctrl+Shift-F2 = Toggle apply theme or not
--------------------------------------------------------------------------------------------------------------------------------------------
"""
"""
Pending -
1) To update theme name is status bar if no theme is applied.
"""


def create_shortcut(*awargs):
    desktop = winshell.desktop()
    path = os.path.join(desktop, "Crimson Editor.lnk")
    target = r"dist\gui.exe"
    wDir = r"P:\Media\Crimson Editor"
    icon = r"assests\icon.ico"

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation = icon
    shortcut.save()


def sql(command):
    conn = sqlite3.connect(
        r"table_types.db")
    c = conn.cursor()
    c.execute(command)
    data = []
    try:
        for data_fetched in c.fetchall():
            data.append(data_fetched)
    except:
        print("SQL:SOME ERROR OCCURED")
    conn.commit()
    c.close()
    conn.close()
    return data


def start(*awargs):
    print("---> Program Started! <---")
    global main
    main = Tk()
    main.title("Crimson Editor - Untitled")
    main.geometry('900x450')
    main.iconbitmap(
        r"assests\icon.ico")
    width = 900
    height = 450
    x = (main.winfo_screenwidth() // 2) - (width // 2)
    y = (main.winfo_screenheight() // 2) - (height // 2)
    main.geometry(f'{width}x{height}+{x}+{y}')

    # Variables
    global color_theme_decide_var
    # For color theme, whether to apply or not.
    color_theme_decide_var = IntVar()
    global current_theme
    current_theme = StringVar()  # For storing the current theme value.
    global color_bg
    color_bg = StringVar()  # For background color
    global color_fg
    color_fg = StringVar()  # For foreground color
    global color_theme_var
    color_theme_var = StringVar()  # For color theme name
    global autosave_var
    autosave_var = StringVar()  # For autosave, decide whether to autosave or not
    global checkpoint_name
    checkpoint_name = StringVar()  # For storing checkpoint name
    global word_wrap_var
    word_wrap_var = StringVar()  # For word wrap, whether to wrap or not
    global status_bar_var
    status_bar_var = StringVar()  # For status bar, whether to take status bar or not
    global mode_var
    mode_var = StringVar()  # For user mode, whether Basic or Advanced
    global thread_var
    # For autosave, if autosave is ON its value is 1 and threading will start otherwise its value is 0 and threading will not performed. Helps in stoping the threading.
    thread_var = IntVar()
    global status_bar_exist
    # For status bar, checking whether status bar exists or not.
    status_bar_exist = IntVar()
    global full_screen_var
    # For checking whether to use full screen mode or not.
    full_screen_var = IntVar()
    global status_bar_status
    # For storing information to be shown on the status bar.
    status_bar_status = StringVar()
    global font_size
    font_size = IntVar()  # For defining the font size
    font_size.set(18)
    global wikipedia_query
    wikipedia_query = StringVar()  # for storing the wikipedia query
    # Variables

    def recreate_stuf(*awargs):
        """Recreates all the stuf. Means destroy all first then recreate them."""
        file = open(r"C:\Users\YOGESH~1\AppData\Local\Temp\tempfile.ced", "a+")
        file = open(r"C:\Users\YOGESH~1\AppData\Local\Temp\tempfile.ced", "w")
        file.write(textarea.get("1.0", END).rstrip())
        file.close()

        textarea.destroy()
        xview_scrollbar.destroy()
        yview_scrollbar.destroy()
        create_text_area()
        # settings_window.grab_release()
        # pyautogui.click(0,0)
        # pyautogui.hotkey("alt","f4")
        # pyautogui.hotkey("ctrl","f2")
        # pyautogui.hotkey("f2")
        # pyautogui.hotkey("ctrl","f5")
        # global status_bar
        # if status_bar_var.get()=="take_status_bar":
        #     status_bar=Label(main,text="Welcome to Crimson Editor.",relief=SUNKEN,anchor=W,bd=1,bg=color_bg.get(),fg=color_fg.get(),cursor=NONE)
        #     status_bar.pack(side=BOTTOM,fill=X)
        #     recreate_stuf()
        # else:
        #     status_bar.destroy()

        file = open(r"C:\Users\YOGESH~1\AppData\Local\Temp\tempfile.ced", "a+")
        file = open(r"C:\Users\YOGESH~1\AppData\Local\Temp\tempfile.ced", "r")
        textarea.insert("1.0", file.read())
        file.close()

    def take_opposite(value_1, value_2, variable, *awargs):
        """Updates the value to the provided variable with swapped values i.e. if variable has 'value_1' then it will replaced by 'value_2' or vice-versa."""
        if variable.get() == value_1:
            variable.set(value_2)
            try:
                awargs[0]()
            except:
                pass
        else:
            variable.set(value_1)
            try:
                awargs[0]()
            except:
                pass

    def theme_read(*awargs):
        temp = sql("SELECT * FROM ATTRIBUTES")
        theme = temp[3][1]
        temp = sql("SELECT * FROM THEME_TABLE")
        theme_list = []
        for temp_index in range(len(temp)):
            t = temp[temp_index]
            for _temp_ in range(len(t)):
                theme_list.append(t[_temp_])
        themes = tuple(theme_list)
        try:
            temp = sql(
                "SELECT value FROM ATTRIBUTES WHERE attribute_name='theme_status'")
            color_theme_decide_var.set(int(temp[0][0]))
            if color_theme_decide_var.get() != 0:
                color_bg.set(theme_list[themes.index(theme) + 1])
                color_fg.set(theme_list[themes.index(theme) + 2])
            else:
                color_bg.set("#FFFFFF")
                color_fg.set("#000000")
                current_theme.set("Default")
        except:
            pass
        temp = sql("SELECT value FROM ATTRIBUTES WHERE attribute_name='theme'")
        current_theme.set(temp[0][0])
        return themes
    theme_read()

    # THEMES
    def theme_write(color_theme):
        sql(
            f"UPDATE ATTRIBUTES SET value='{color_theme}' WHERE attribute_name='theme'")

    def create_text_area(*awargs):
        global textarea
        global xview_scrollbar
        global yview_scrollbar
        textarea = Text(main, width=100, height=80, bg=color_bg.get(), fg=color_fg.get(), font=("google sans regular", font_size.get(
        )), selectbackground=color_fg.get(), selectforeground=color_bg.get(), wrap=word_wrap_var.get(), relief=FLAT, bd=3)
        yview_scrollbar = Scrollbar(main)
        yview_scrollbar.config(command=textarea.yview, relief=RAISED)
        yview_scrollbar.pack(side=RIGHT, fill=Y)
        xview_scrollbar = Scrollbar(main, orient=HORIZONTAL)
        xview_scrollbar.config(command=textarea.xview)
        if word_wrap_var.get() == "char":
            textarea.configure(yscrollcommand=yview_scrollbar.set, undo=True,
                               maxundo=-1, autoseparators=True, insertbackground=color_fg.get())
        else:
            xview_scrollbar.pack(side=BOTTOM, fill=X, expand=1)
            textarea.configure(xscrollcommand=xview_scrollbar.set, undo=True, maxundo=-1,
                               autoseparators=True, yscrollcommand=yview_scrollbar.set, insertbackground=color_fg.get())
        textarea.focus_force()
        textarea.pack(fill=X)

    def checkpoint(*awargs):
        checkpoint_window = Toplevel()
        checkpoint_window.overrideredirect(1)
        checkpoint_window.grab_set_global()
        width = 900
        height = 500
        x = (checkpoint_window.winfo_screenwidth() // 2) - (width // 2)
        y = (checkpoint_window.winfo_screenheight() // 2) - (height // 2)
        checkpoint_window.geometry(f'{width}x{height}+{x}+{y}')
        checkpoint_window.config(bg=color_bg.get())
        close_button_image = PhotoImage(
            file=r"assests\close_icon.png")
        close_button = Button(
            checkpoint_window, bd=0, bg=color_bg.get(), command=checkpoint_window.destroy)
        close_button.config(image=close_button_image)
        close_button.pack(side=TOP, fill=X)

        listbox_frame = Frame(checkpoint_window)
        listbox_frame.pack()
        listbox_yview_scrollbar = Scrollbar(listbox_frame, orient="vertical")
        listbox_yview_scrollbar.pack(side=RIGHT, fill=Y)
        checkpoint_listbox = Listbox(listbox_frame, width=100, height=23, yscrollcommand=listbox_yview_scrollbar.set, selectbackground=color_bg.get(
        ), selectforeground=color_fg.get(), bg=color_fg.get(), fg=color_bg.get(), font=("google sans bold", 11), selectmode=SINGLE)
        listbox_yview_scrollbar.config(command=checkpoint_listbox.yview)
        checkpoint_listbox.focus_force()
        checkpoint_listbox.pack()

        checkpoints_list = []
        try:
            files = os.listdir(tempfile.gettempdir() + r"\checkpoints")
            run = 0
            j = 0
            for i in range(len(files)):
                # PENDING (is or ==)
                if ("_!@#$%^&()@checkpoint_" in files[i]) == True:
                    j = j+1
                    temp_1 = files[i].rstrip(".txt")
                    temp_2 = temp_1.find("_!@#$%^&()@checkpoint_")
                    checkpoint_name_read = ""
                    for letters in range(0, temp_2):
                        checkpoint_name_read = checkpoint_name_read + \
                            str(temp_1[letters])

                    temp_2 = temp_1.find("_!@#$%^&()@checkpoint_")
                    checkpoint_time_read = ""
                    for letters in range(temp_2 + 22, len(temp_1)-3):
                        checkpoint_time_read = checkpoint_time_read + \
                            str(temp_1[letters])
                    checkpoint_time_read = (checkpoint_time_read.replace(
                        "=", ":").replace(",", " at")).rstrip("_")

                    global checkpoint_no_list
                    checkpoint_no_list = []
                    checkpoint_no_read = ""
                    for letters in range(-1, -4, -1):
                        checkpoint_no_read = checkpoint_no_read + \
                            str(temp_1[letters])
                        checkpoint_no_read = checkpoint_no_read.lstrip(
                            "_)").rstrip("_")
                        checkpoint_no_list.append(checkpoint_no_read)
                    checkpoints_list.append(
                        f"{j}) {checkpoint_name_read}                   Taken on {checkpoint_time_read}")

                else:
                    if run == (len(files)-1):
                        raise ValueError

                run = run + 1
            for elements in range(len(checkpoints_list)):
                checkpoint_listbox.insert(elements, checkpoints_list[elements])
            sql(
                f"UPDATE ATTRIBUTES SET value='{max(checkpoint_no_list)}' WHERE attribute_name='checkpoint_nos'")
        except:
            checkpoint_listbox.insert(
                1, "No checkpoints. Save some checkpoints and try again.")

        try:
            os.mkdir(r"\AppData\Local\Temp\checkpoints")
        except:
            pass

        def save_checkpoint(*awargs):
            try:
                item = checkpoint_listbox.get(
                    checkpoint_listbox.curselection())
                a = item.replace("                   Taken on ", "_!@#$%^&()@checkpoint_").replace(
                    " at ", ", ").replace(":", "=")

                file = ""
                for i in range(a.index(" ") + 1, len(a)):
                    file = file + a[i]
                file_index = None
                for i in range(len(files)):
                    if file in files[i]:
                        file_index = i
                        break
                restore_confirm = messagebox.askyesno(
                    "Sure?", "Are you sure want to restore the selected checkpoint?")
                if restore_confirm:
                    file = open(tempfile.gettempdir() +
                                f"\\checkpoints\\{files[file_index]}", "r")
                    textarea.delete("1.0", END)
                    textarea.insert("1.0", file.read())
                    file.close()
                    checkpoint_window.destroy()

            except:
                messagebox.showwarning(
                    "Invalid selection!", "Please select a valid checkpoint!")

        restore_button_image = PhotoImage(
            file=r"assests\restore.png")
        restore_button = Button(checkpoint_window, bd=0,
                                bg=color_bg.get(), command=save_checkpoint)
        restore_button.config(image=restore_button_image)
        restore_button.pack(side=BOTTOM, fill=X)

        checkpoint_window.bind("<Escape>", checkpoint_window.destroy)
        checkpoint_window.mainloop()
        """
        Save the checkpoint with custom name (entered by the user).
        create a file with the name as the 'time' that was at the time of checkpoint creation.
        Use the checkpoint name and the file name(location) to create a query in the sqlite3 (custom name,file location)
        Create a command that create a cascade menu in the checkpoint menu option and reads the file location and restore the text from it.
        """
    main.bind("<Control-Shift-F1>", checkpoint)

    def file_menu():
        def file_dialog(*awargs):
            try:
                filename = filedialog.askopenfilename(filetypes=(
                    ("Text file", "*.txt"), ("All Files", "*.*")))
                sql(
                    f"UPDATE TEMP_WORK SET value='{filename}' WHERE work_name='file_location'")
                file = open(filename, "r")
                textarea.delete("1.0", END)
                textarea.insert("1.0", file.read())
                file.close()
                main.title(f"Crimson Editor - {filename}")
            except:
                pass

        def save_as(*awargs):
            global textarea
            try:
                file_location = (filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(
                    ("Text File", "*.txt"), ("Python File", "*.py"), ("All Files", "*.*"))))
                data = textarea.get('1.0', END+'-1c')
                sql(
                    f"UPDATE TEMP_WORK SET value='{file_location}' WHERE work_name='file_location'")
                file = open(file_location, "w")
                file.write(data)
                file.close()
                main.title(f"Crimson Editor - {file_location}")
            except:
                pass

        def save(*awargs):
            global textarea
            try:
                temp = sql("SELECT * FROM TEMP_WORK")
                file_location = temp[2][1]
                data = textarea.get('1.0', END+'-1c')
                file = open(file_location, "w")
                file.write(data)
                file.close()
            except:
                pass

        def save_decide(*awargs):
            temp = sql("SELECT * FROM TEMP_WORK")
            file_read = temp[2][1]
            if file_read == "":
                save_as()
            else:
                save()

        def exit_command(*awargs):
            answer = messagebox.askokcancel(
                "Exit?", "Do you want to exit? Your data will be lost...")
            if answer == True:
                main.destroy()
                print("---> Program Terminated! <---")
                quit()
            else:
                pass

            # AUTO_SAVE_FILE ---> TRUE

        def read_autosavefile():
            temp = sql("SELECT * FROM ATTRIBUTES")
            autosave_var.set(temp[0][1])
            if autosave_var.get() == "" or autosave_var.get() == "False":
                autosave_var.set("False")
                sql("UPDATE ATTRIBUTES SET value='False' where attribute_name='autosave'")
                thread_var.set(0)
            else:
                thread_var.set(1)

            def auto_saver(*awargs):
                save()

            def _check():
                time.sleep(4)
                if thread_var.get() == 1:
                    if autosave_var.get() == "True":
                        auto_saver()
                else:
                    pass
                _check()
            check_function_thread = threading.Thread(target=_check)
            check_function_thread.daemon = True
            check_function_thread.start()
        read_autosavefile()

        def auto_save_file():
            try:
                status_bar.destroy()
            except:
                pass
            status_bar_decide()

            def write_file():
                sql("UPDATE ATTRIBUTES SET value='{}' where attribute_name='autosave'".format(
                    autosave_var.get()))

            def read_autosavefile():
                temp = sql("SELECT * FROM ATTRIBUTES")
                autosave_var.set(temp[0][1])
                if autosave_var.get() == "" or autosave_var.get() == "False":
                    autosave_var.set("False")
                    sql("UPDATE ATTRIBUTES SET value='False' where attribute_name='autosave'")
                    thread_var.set(0)
                else:
                    thread_var.set(1)
            write_file()
            read_autosavefile()

            def auto_saver(*awargs):
                save()

            def _check():
                time.sleep(4)
                if thread_var.get() == 1:
                    if autosave_var.get() == "True":
                        auto_saver()
                    else:
                        pass
                else:
                    pass
                _check()
            check_function_thread = threading.Thread(target=_check)
            check_function_thread.start()
            if autosave_var.get() == "True":
                messagebox.showwarning(
                    "Notice!", "While using Auto Save, the file cannot be modified by any other editor.")

        def save_checkpoint(*awargs):
            def get_datetime(*awargs):
                now = datetime.datetime.now()
                current_time_tuple = str(
                    now.day)+"-"+str(now.month)+"-"+str(now.year), str(now.hour)+"=" + str(now.minute)
                current_time_list = list(current_time_tuple)
                current_time = ""
                j = 0
                for i in range(len(current_time_list)):
                    current_time += current_time_list[i]
                    j = j+1
                    if j == 1:
                        current_time += ", "
                sql(
                    f"UPDATE ATTRIBUTES SET value='{current_time}' WHERE attribute_name='date_time'")
                return current_time
            # simpledialog.askstring("Save checkpoint","Enter the checkpoint name")
            checkpoint_entry_window = Toplevel()
            checkpoint_entry_window.focus_force()
            checkpoint_entry_window.grab_set_global()
            checkpoint_entry_window.overrideredirect(1)
            checkpoint_entry_window.resizable(0, 0)
            width = 300
            height = 100
            x = (checkpoint_entry_window.winfo_screenwidth() // 2) - (width // 2)
            y = (checkpoint_entry_window.winfo_screenheight() // 2) - (height // 2)
            checkpoint_entry_window.geometry(f'{width}x{height}+{x}+{y}')
            checkpoint_entry_window.config(bg=color_fg.get())
            Label(checkpoint_entry_window, text="Enter the checkpoint name",
                  fg="red", bg="white", font=("google sans bold", 11)).pack()
            entry_save_checkpoint = Entry(
                checkpoint_entry_window, textvariable=checkpoint_name)
            entry_save_checkpoint.focus_force()
            entry_save_checkpoint.pack()

            def save_data_as_checkpoint(*awargs):
                # checkpoint_entry_window.grab_release()
                # main.destroy()
                number_of_attributes = sql(
                    f"SELECT value FROM ATTRIBUTES WHERE attribute_name='checkpoint_nos'")
                number_of_attributes = int(number_of_attributes[0][0])
                data = textarea.get("1.0", END)
                file_name = "{}_!@#$%^&()@checkpoint_{}_{}_".format(
                    checkpoint_name.get(), get_datetime(), number_of_attributes+1)
                try:
                    os.chdir(tempfile.gettempdir() + r"\checkpoints")
                except:
                    os.mkdir(tempfile.gettempdir() + r"\checkpoints")
                    os.chdir(tempfile.gettempdir() + r"\checkpoints")
                try:
                    checkpoint_entry_window.focus_force()
                    file = open(file_name, "a+")
                    file.write(data)
                    file.close()
                    checkpoint_entry_window.destroy()
                except:
                    messagebox.showerror(
                        "Invalid name", "Please choose a valid file name.")
                    checkpoint_entry_window.grab_set()
                sql(
                    f"UPDATE ATTRIBUTES SET value='{number_of_attributes + 1}' WHERE attribute_name='checkpoint_nos'")

            Button(checkpoint_entry_window, text="Save", fg="green", bg="white", bd=0, font=(
                "google sans bold", 11), command=save_data_as_checkpoint).pack()
            Button(checkpoint_entry_window, text="Cancel", fg="red", bg="white", bd=0, font=(
                "google sans bold", 11), command=checkpoint_entry_window.destroy).pack()
            checkpoint_entry_window.bind(
                "<Control-s>", save_data_as_checkpoint)
            checkpoint_entry_window.bind(
                "<Control-S>", save_data_as_checkpoint)
            checkpoint_entry_window.bind("<Insert>", save_data_as_checkpoint)
            checkpoint_entry_window.bind(
                "<Escape>", checkpoint_entry_window.destroy)
            checkpoint_entry_window.mainloop()
            try:
                main.focus_force()
            except:
                pass
        main.bind("<Control-F1>", save_checkpoint)

        def auto_save_file_by_key(*awargs):
            take_opposite("True", "False", autosave_var, auto_save_file)
            try:
                status_bar.destroy()
            except:
                pass
            status_bar_decide()
        main.bind("<F9>", auto_save_file_by_key)
        fileMenu = Menu(menu, tearoff=0, activeforeground=color_fg.get(), activebackground=color_bg.get(
        ), background=color_bg.get(), selectcolor=color_fg.get(), foreground=color_fg.get(), font=("google san bold", 11))
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_cascade(label="New", command=start)
        fileMenu.add_cascade(label="Open", command=file_dialog)
        fileMenu.add_cascade(label="Save", command=save_decide)
        fileMenu.add_cascade(label="Save As", command=save_as)
        fileMenu.add_checkbutton(label="Auto Save", variable=autosave_var,
                                 onvalue="True", offvalue="False", command=auto_save_file)
        fileMenu.add_cascade(label="Save Checkpoint", command=save_checkpoint)
        fileMenu.add_separator()
        fileMenu.add_cascade(label="Page setup")
        fileMenu.add_cascade(label="Print...")
        fileMenu.add_separator()
        fileMenu.add_cascade(label="Exit", command=exit_command)

        main.bind("<Control-n>", start)
        main.bind("<Control-o>", file_dialog)
        main.bind("<Control-s>", save_decide)
        main.bind("<Control-,>", save_checkpoint)
        main.bind("<Control-N>", start)
        main.bind("<Control-O>", file_dialog)
        main.bind("<Control-S>", save_decide)
        main.bind("<Alt-F4>", exit_command)

    def edit_menu():
        def insert_datetime(*awargs):
            now = datetime.datetime.now()
            current_time = str(now.day)+"/"+str(now.month)+"/" + \
                str(now.year), str(now.hour)+":" + str(now.minute)
            current_time_list = list(current_time)
            time = ""
            j = 0
            for i in range(len(current_time_list)):
                if i == 0:
                    time = time + current_time_list[i] + " "
                else:
                    time = time + current_time_list[i]
            time = " " + time + " "
            textarea.insert(END, time)
        editMenu = Menu(menu, tearoff=0, activeforeground=color_fg.get(), activebackground=color_bg.get(
        ), background=color_bg.get(), selectcolor=color_fg.get(), foreground=color_fg.get(), font=("google san bold", 11))
        menu.add_cascade(label="Edit", menu=editMenu)
        editMenu.add_command(
            label="Undo", command=lambda *awargs: textarea.edit_undo)
        editMenu.add_command(
            label="Redo", command=lambda *awargs: textarea.edit_redo)
        editMenu.add_separator()
        editMenu.add_cascade(
            label="Cut", command=lambda: textarea.event_generate(("<<Cut>>")))
        editMenu.add_cascade(
            label="Copy", command=lambda: textarea.event_generate(("<<Copy>>")))
        editMenu.add_cascade(
            label="Paste", command=lambda: textarea.event_generate(("<<Paste>>")))
        editMenu.add_cascade(
            label="Delete", command=lambda *awargs: pyautogui.press("delete"))
        editMenu.add_separator()
        # textarea.search("hello","1.0")
        editMenu.add_cascade(label="Find", command=lambda *awargs: None)
        editMenu.add_cascade(label="Find next")
        editMenu.add_cascade(label="Replace...")
        editMenu.add_cascade(label="Go To...")
        editMenu.add_separator()
        editMenu.add_cascade(
            label="Select All", command=lambda *awargs: pyautogui.hotkey("ctrl", "a"))
        editMenu.add_cascade(label="Time/Date", command=insert_datetime)
        main.bind("<F5>", insert_datetime)

    def format_menu():
        temp = sql("SELECT * FROM ATTRIBUTES")
        word_wrap_var.set(temp[1][1])

        def read_word_wrap_file():
            if (word_wrap_var.get() in ["char", "none"]) != True:
                word_wrap_var.set("char")
                sql("UPDATE ATTRIBUTES set value='char' WHERE attribute_name='word_wrap'")
            else:
                temp = sql("SELECT * FROM ATTRIBUTES")
                word_wrap_var.set(temp[1][1])
        read_word_wrap_file()

        def word_wrap(*awargs):
            sql("UPDATE ATTRIBUTES SET value='{}' WHERE attribute_name='word_wrap'".format(
                word_wrap_var.get()))
            read_word_wrap_file()
            file = open(
                r"C:\Users\YOGESH~1\AppData\Local\Temp\tempfile.ced", "a+")
            file = open(
                r"C:\Users\YOGESH~1\AppData\Local\Temp\tempfile.ced", "w")
            file.write(textarea.get("1.0", END).rstrip())
            file.close()

            xview_scrollbar.destroy()
            yview_scrollbar.destroy()
            textarea.destroy()
            create_text_area()

            file = open(
                r"C:\Users\YOGESH~1\AppData\Local\Temp\tempfile.ced", "a+")
            file = open(
                r"C:\Users\YOGESH~1\AppData\Local\Temp\tempfile.ced", "r")
            textarea.insert("1.0", file.read())
            file.close()
            os.remove(r"C:\Users\YOGESH~1\AppData\Local\Temp\tempfile.ced")

        def word_wrap_by_key(*awargs):
            temp = sql("SELECT * FROM ATTRIBUTES")
            word_wrap_var.set(temp[1][1])
            take_opposite("char", "none", word_wrap_var, word_wrap)
            pyautogui.press("end")

        main.bind("<F3>", word_wrap_by_key)

        formatMenu = Menu(menu, tearoff=0, activeforeground=color_fg.get(), activebackground=color_bg.get(
        ), background=color_bg.get(), selectcolor=color_fg.get(), foreground=color_fg.get(), font=("google san bold", 11))
        menu.add_cascade(label="Format", menu=formatMenu)
        formatMenu.add_checkbutton(
            label="Word Wrap", var=word_wrap_var, onvalue="char", offvalue="none", command=word_wrap)
        formatMenu.add_cascade(label="Font...")

    def status_bar_decide(*awargs):
        sql("UPDATE ATTRIBUTES SET value='{}' WHERE attribute_name='status_bar'".format(
            status_bar_var.get()))
        if status_bar_var.get() == "take_status_bar":
            global status_bar
            status_bar = Label(
                main, text=f"Welcome to Crimson Editor.      |       Current theme - {theme_read()[theme_read().index(current_theme.get())]}      |       Auto Save - {autosave_var.get()}       |       {status_bar_status.get()}", relief=SUNKEN, anchor=W, bd=1, bg=color_bg.get(), fg=color_fg.get(), cursor=NONE)
            status_bar.pack(side=BOTTOM, fill=X)
            try:
                recreate_stuf()
            except:
                pass
        else:
            try:
                status_bar.destroy()
            except:
                pass
        main.update()

    def status_bar_decide_by_key(*awargs):
        temp = sql("SELECT * FROM ATTRIBUTES")
        status_bar_var.set(temp[2][1])
        take_opposite("take_status_bar", "not_take_status_bar",
                      status_bar_var, status_bar_decide)

    def view_menu():
        temp = sql("SELECT * FROM ATTRIBUTES")
        status_bar_var.set(temp[2][1])
        global themes
        themes = theme_read()

        def color_theme_decide_by_key(*awargs):
            """Updates the color theme values to the database as well as to the window"""
            temp = sql(
                "SELECT value FROM ATTRIBUTES WHERE attribute_name='theme'")
            current_theme.set(temp[0][0])
            global themes
            themes = theme_read()
            if awargs[0] == "next_theme":
                if themes.index(current_theme.get())+4 == len(themes):
                    current_theme.set(themes[0])
                    theme_write(themes[themes.index(current_theme.get())])
                else:
                    theme_write(themes[themes.index(current_theme.get())+4])
                theme_read()
                try:
                    status_bar.destroy()
                except:
                    pass
                status_bar_decide()
            else:
                if themes.index(current_theme.get())-4 == len(themes):
                    current_theme.set(themes[0])
                    theme_write(themes[themes.index(current_theme.get())])
                else:
                    theme_write(themes[themes.index(current_theme.get())-4])
                theme_read()
                try:
                    status_bar.destroy()
                except:
                    pass
                status_bar_decide()
            recreate_stuf()

        def color_theme_decide(*awargs):
            """Updates the color theme values to the database as well as to the window"""
            try:
                if awargs[0] == "by_key":
                    take_opposite(0, 1, color_theme_decide_var)
            except:
                pass
            sql("UPDATE ATTRIBUTES SET value='{}' WHERE attribute_name='theme_status'".format(
                color_theme_decide_var.get()))
            theme_read()
            recreate_stuf()
            try:
                status_bar.destroy()
            except:
                pass
            status_bar_decide()
        status_bar_decide()
        viewMenu = Menu(menu, tearoff=0, activeforeground=color_fg.get(), activebackground=color_bg.get(
        ), background=color_bg.get(), selectcolor=color_fg.get(), foreground=color_fg.get(), font=("google san bold", 11))
        menu.add_cascade(label="View", menu=viewMenu)
        viewMenu.add_checkbutton(label="Status Bar", var=status_bar_var, onvalue="take_status_bar",
                                 offvalue="not_take_status_bar", command=status_bar_decide)
        viewMenu.add_checkbutton(label="Color theme", var=color_theme_decide_var,
                                 onvalue=1, offvalue=0, command=color_theme_decide)

        main.bind("<F2>", lambda *awargs: color_theme_decide_by_key("next_theme"))
        main.bind("<Control-F2>",
                  lambda *awargs: color_theme_decide_by_key("previous_theme"))
        main.bind("<Control-Shift-F2>",
                  lambda *awargs: color_theme_decide("by_key"))
        main.bind("<F4>", status_bar_decide_by_key)

    def about_menu():
        def open_file(*awargs):
            import webbrowser
            attribute = awargs[0]
            if attribute == "shortcut_keys":
                webbrowser.open("shortcut_keys.html", new=2)
            elif attribute == "help":
                webbrowser.open("help.html", new=2)

        def about(*awargs):
            messagebox.showinfo("About", "Made by Yogesh Aggarwal")
        aboutMenu = Menu(menu, tearoff=0, activeforeground=color_fg.get(), activebackground=color_bg.get(
        ), background=color_bg.get(), selectcolor=color_fg.get(), foreground=color_fg.get(), font=("google san bold", 11))
        menu.add_cascade(label="Help", menu=aboutMenu)
        aboutMenu.add_command(label="Shortcut keys",
                              command=lambda: open_file("shortcut_keys"))
        aboutMenu.add_separator()
        aboutMenu.add_command(label="Help", command=lambda: open_file("help"))
        aboutMenu.add_command(label="About", command=about)

    def settings_menu(*awargs):
        menu.add_command(label="Settings", command=settings)

    def tools_menu():
        def text_to_speech(*awargs):
            """Gives the output as a audio file of the fetched text from the text area."""
            from gtts import gTTS
            convert_answer = messagebox.askyesno(
                "Convert text to speech", "Do you really want to convert the text to a speech file?")

            def convert(*awargs):
                try:
                    try:
                        status_bar.destroy()
                    except:
                        pass
                    status_bar_status.set("Converting into speech...")
                    status_bar_decide()
                    tts = gTTS(text=textarea.get("1.0", END), lang='en')
                    import os
                    try:
                        os.mkdir('C:\\Users\\Public\\Documents\\Results')
                    except:
                        os.chdir('C:\\Users\\Public\\Documents\\Results')
                    os.chdir('C:\\Users\\Public\\Documents\\Results')
                    tts.save("Speech.mp3")
                    messagebox.showinfo(
                        "Speech successfully created!", r"""The speech is successfully saved at "C:\Users\Public\Documents\Results\Speech.mp3".""")
                    status_bar_decide_by_key()
                    status_bar_status.set("")
                    status_bar_decide_by_key()
                except:
                    try:
                        status_bar.destroy()
                    except:
                        pass
                    status_bar_status.set("")
                    status_bar_decide()
                    messagebox.showerror(
                        "Conversion error!", "There may be a connection problem.")
            temp_thread_function = threading.Thread(target=convert)
            temp_thread_function.daemon = True
            temp_thread_function.start()

            if convert_answer == True:
                convert()

        def search(*awargs):
            wikipedia_query_window = Toplevel()
            wikipedia_query_window.title("Save Checkpoint")
            wikipedia_query_window.focus_force()
            wikipedia_query_window.grab_set_global()
            wikipedia_query_window.overrideredirect(1)
            wikipedia_query_window.resizable(0, 0)
            width = 300
            height = 100
            x = (wikipedia_query_window.winfo_screenwidth() // 2) - (width // 2)
            y = (wikipedia_query_window.winfo_screenheight() // 2) - (height // 2)
            wikipedia_query_window.geometry(f'{width}x{height}+{x}+{y}')
            wikipedia_query_window.config(bg=color_fg.get())
            Label(wikipedia_query_window, text="Enter your query",
                  fg="red", bg="white", font=("google sans bold", 11)).pack()
            entry_wikipedia_query = Entry(
                wikipedia_query_window, textvariable=wikipedia_query)
            entry_wikipedia_query.focus_force()
            entry_wikipedia_query.pack()

            def convert(*awargs):
                wikipedia_query_window.destroy()
                query = wikipedia_query.get()

                def __convert(*awargs):
                    def status_bar_decide_by_key(*awargs):
                        temp = sql("SELECT * FROM ATTRIBUTES")
                        status_bar_var.set(temp[2][1])
                        take_opposite(
                            "take_status_bar", "not_take_status_bar", status_bar_var, status_bar_decide)
                    try:
                        try:
                            status_bar.destroy()
                        except:
                            pass
                        status_bar_status.set("Getting data from Wikipedia...")
                        status_bar_decide()
                        from wikipedia import summary
                        textarea.insert(
                            END, str("\n" + summary(query) + "\n\n"))
                        textarea.focus_force()
                        status_bar_decide_by_key()
                        status_bar_status.set("")
                        status_bar_decide_by_key()
                    except:
                        try:
                            status_bar.destroy()
                        except:
                            pass
                        status_bar_status.set("")
                        status_bar_decide()
                        if query != None:
                            messagebox.showerror(
                                "Data not found!", f"""No information found for the keyword "{query}" or it may be a connection problem.""")
                temp_thread_function = threading.Thread(target=__convert)
                temp_thread_function.daemon = True
                temp_thread_function.start()
                wikipedia_query.set("")
            Button(wikipedia_query_window, text="Search", fg="green", bg="white",
                   bd=0, font=("google sans bold", 11), command=convert).pack()
            Button(wikipedia_query_window, text="Cancel", fg="red", bg="white", bd=0, font=(
                "google sans bold", 11), command=wikipedia_query_window.destroy).pack()
            wikipedia_query_window.bind("<Insert>", convert)
            wikipedia_query_window.bind(
                "<Escape>", wikipedia_query_window.destroy)
            wikipedia_query_window.mainloop()

        def translate_text(*awargs):
            from googletrans import Translator
            global convert_language
            convert_language = simpledialog.askstring(
                "Translate text to...", "Enter the language name")
            if convert_language == None:
                convert_language = ""

            def convert(*awargs):
                def status_bar_decide_by_key(*awargs):
                    temp = sql("SELECT * FROM ATTRIBUTES")
                    status_bar_var.set(temp[2][1])
                    take_opposite(
                        "take_status_bar", "not_take_status_bar", status_bar_var, status_bar_decide)
                try:
                    try:
                        status_bar.destroy()
                    except:
                        pass
                    status_bar_status.set(status_bar_status.set(
                        f"Translating to {convert_language.capitalize()}..."))
                    status_bar_decide()
                    answer = Translator().translate(str(textarea.get("1.0", END)),
                                                    dest=str(convert_language)).text
                    textarea.insert(END, str("\n\n" + answer + "\n"))
                    textarea.focus_force()
                    try:
                        status_bar.destroy()
                    except:
                        pass
                    status_bar_status.set("")
                    status_bar_decide()
                except:
                    try:
                        status_bar.destroy()
                    except:
                        pass
                    status_bar_status.set("")
                    status_bar_decide()
                    if convert_language != "":
                        messagebox.showerror(
                            "Conversion error!", f"""Cannot convert the text to {convert_language} or it may be a connection problem.""")
            temp_thread_function = threading.Thread(target=convert)
            temp_thread_function.daemon = True
            temp_thread_function.start()

        def run_file(*awargs):
            import webbrowser
            webbrowser.open(
                sql("SELECT value FROM TEMP_WORK WHERE work_name='file_location'")[0][0], new=2)

        main.bind("<F6>", text_to_speech)
        main.bind("<F7>", search)
        main.bind("<F8>", translate_text)
        main.bind("<F12>", run_file)

        toolsMenu = Menu(menu, tearoff=0, activeforeground=color_fg.get(), activebackground=color_bg.get(
        ), background=color_bg.get(), selectcolor=color_fg.get(), foreground=color_fg.get(), font=("google san bold", 11))
        menu.add_cascade(label="Tools", menu=toolsMenu)
        toolsMenu.add_command(label="Revert to checkpoint", command=checkpoint)
        toolsMenu.add_command(label="Convert into speech",
                              command=text_to_speech)
        toolsMenu.add_command(label="Search Wikipedia", command=search)
        toolsMenu.add_command(label="Translate", command=translate_text)
        toolsMenu.add_command(label="Run/Open", command=run_file)

    def settings(*awargs):
        global settings_window
        settings_window = Toplevel()
        settings_window.focus_force()
        settings_window.grab_set()
        settings_window.title("Settings")
        settings_window.config(bg="white")
        width = 580
        height = 600

        def read_attributes():
            attributes = []
            temp = sql("SELECT * FROM ATTRIBUTES")
            for temp_index in range(len(temp)):
                t = temp[temp_index]
                for _temp_ in range(len(t)):
                    attributes.append(t[_temp_])
            print(attributes)
            status_bar_var.set(attributes[5])
            word_wrap_var.set(attributes[3])
            color_theme_var.set(attributes[7])
        read_attributes()
        print(status_bar_var.get(), word_wrap_var.get(), color_theme_var.get())

        def theme():
            theme_list = []
            temp = sql("SELECT * FROM THEME_TABLE")
            for temp_index in range(len(temp)):
                t = temp[temp_index]
                for _temp_ in range(len(t)-3):
                    theme_list.append(t[_temp_])
            return theme_list

        x = (settings_window.winfo_screenwidth() // 2) - (width // 2)
        y = (settings_window.winfo_screenheight() // 2) - (height // 2)
        settings_window.geometry(f'{width}x{height}+{x}+{y}')
        settings_window.resizable(0, 0)
        font_label = ("google sans bold", 15)

        # User Mode
        Label(settings_window, text="User mode", fg="green", bg="white",
              font=font_label).pack()  # .grid(row=0,column=0,sticky=W)

        mode_var.set("basic_mode")  # To be removed (Extra)
        Radiobutton(settings_window, text="Basic", variable=mode_var, value="basic_mode", bg="white", font=(
            "google sans regular", 12)).pack()  # .grid(row=1,column=0,sticky=W)
        Radiobutton(settings_window, text="Advanced", variable=mode_var, value="advanced_mode",
                    bg="white", font=("google sans regular", 12)).pack()  # .grid(row=1,column=1,sticky=W)

        # Appearence

        Label(settings_window, text="Appearence", fg="green", bg="white",
              font=font_label).pack()  # .grid(row=2,column=0)
        print(status_bar_var.get(), word_wrap_var.get(), color_theme_var.get())
        Checkbutton(settings_window, text="Status Bar", bg="white", font=("google sans regular", 12),
                    onvalue="take_status_bar", offvalue="not_take_status_bar", variable=status_bar_var).pack()  # .grid(row=3,column=0)
        Checkbutton(settings_window, text="Word Wrapping", bg="white", font=("google sans regular", 12),
                    onvalue="char", offvalue="none", variable=word_wrap_var).pack()  # .grid(row=3,column=1)

        Checkbutton(settings_window, text="Color Theme", bg="white", font=("google sans regular", 12), variable=color_theme_var,
                    onvalue="take_color_theme", offvalue="not_take_color_theme").pack()  # .grid(row=3,column=2)

        listbox_frame = Frame(settings_window)
        listbox_frame.pack()
        listbox_yview_scrollbar = Scrollbar(listbox_frame, orient="vertical")
        listbox_yview_scrollbar.pack(side=RIGHT, fill=Y)
        theme_listbox = Listbox(listbox_frame, width=580, yscrollcommand=listbox_yview_scrollbar.set,
                                bg="white", fg="black", font=("google sans bold", 11), selectmode=SINGLE)
        listbox_yview_scrollbar.config(command=theme_listbox.yview)
        theme_listbox.pack()

        def __theme():
            current_theme = []
            temp = sql("SELECT * FROM ATTRIBUTES")
            current_theme = temp[3][1]
            return current_theme

        Label(settings_window, text=f"Current theme : {__theme()}", bg="white", fg="green", font=(
            "google sans bold", 10)).pack()

        for i in range(len(theme())):
            theme_listbox.insert(i, theme()[i])

        def save_settings():
            usermode = mode_var.get()
            status_bar = status_bar_var.get()
            word_wrap = word_wrap_var.get()
            # color_theme_decide_var = color_theme_var.get()
            color_theme = 0
            if color_theme_decide_var.get() == 1:
                try:
                    color_theme = theme_listbox.get(
                        theme_listbox.curselection())
                except:
                    print(
                        sql("SELECT value from ATTRIBUTES WHERE attribute_name='theme'")[0][0])
                    color_theme = sql(
                        "SELECT value from ATTRIBUTES WHERE attribute_name='theme'")[0][0]
            else:
                theme_listbox.get(theme_listbox.curselection())
            sql(
                f"UPDATE ATTRIBUTES SET value='{usermode}' WHERE attribute_name='usermode'")
            sql(
                f"UPDATE ATTRIBUTES SET value='{status_bar}' WHERE attribute_name='status_bar'")
            sql(
                f"UPDATE ATTRIBUTES SET value='{word_wrap}' WHERE attribute_name='word_wrap'")
            sql(
                f"UPDATE ATTRIBUTES SET value='{color_theme}' WHERE attribute_name='theme'")
            theme_read()
            recreate_stuf()
        Button(settings_window, text="Save", bg="white", fg="red", font=(
            "google sans bold", 12), bd=1, command=save_settings).pack()

        settings_window.focus_force()
        settings_window.mainloop()

    # Bindings
    # main.bind("<Control-1")
    def imp(*awargs):
        import test

    def full_screen_F11(*awargs):
        if full_screen_var.get() == 0:
            main.attributes("-fullscreen", True)
            full_screen_var.set(1)
        else:
            main.attributes("-fullscreen", False)
            full_screen_var.set(0)

    def full_screen_ESC(*awargs):
        main.attributes("-fullscreen", False)
        full_screen_var.set(0)

    def change_font_size(event):
        if event.num == 4 or event.delta == 120:
            font_size.set(font_size.get() + 1)
            recreate_stuf()
            sql("UPDATE ATTRIBUTES SET value='{}' WHERE attribute_name='font_size'")
        else:
            font_size.set(font_size.get() - 1)
            recreate_stuf()
            sql("UPDATE ATTRIBUTES SET value='{}' WHERE attribute_name='font_size'")

    def right_click_menu(*awargs):
        def popup(event):
            try:
                popup_menu.tk_popup(event.x_root, event.y_root, 0)
            finally:
                popup_menu.grab_release()
        popup_menu = Menu(tearoff=0)
        popup_menu.add_command(label="Delete")
        popup_menu.add_command(label="Select All")

    def Interactive_console(*awargs):
        import code
        vars = globals().copy()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()

    main.bind("<Control-F5>", imp)
    main.bind("<F11>", full_screen_F11)
    main.bind("<Escape>", full_screen_ESC)
    main.bind("<Control-MouseWheel>", change_font_size)
    main.bind("<Button-3>", right_click_menu)

    menu = Menu(main, font=("google san bold", 11))
    menu.config(bg=color_fg.get())
    main.config(menu=menu)
    main.focus_get()

    file_menu()
    edit_menu()
    format_menu()
    view_menu()
    tools_menu()
    settings_menu()
    about_menu()
    create_text_area()

    main.mainloop()
    thread_var.set(0)

    try:
        sql("UPDATE TEMP_WORK SET value='' WHERE work_name='file_location'")
    except:
        pass

    print("---> Program Terminated! <---")


def run_check(*awargs):
    try:
        run = (sql("SELECT value FROM ATTRIBUTES WHERE attribute_name='runtime'"))[
            0][0]
        if run == "opened_before":
            run = "opened_before"
    except:
        run = "not_opened_before"
    if run == "not_opened_before":
        def create_database(*awargs):
            # Theme table
            themes = ('Default', 'Petal', 'Poppy', 'Stem', 'Spring green', 'Light mist', 'Stone', 'Shadow', 'Autumn foliage', 'Crevice', 'Cloud shadow', 'Desert', 'Red clay', 'Thunder cloud', 'Waterfall', 'Moss', 'Meadow', 'Deep aqua', 'Ocean', 'Wave', 'Seafoam', 'Forest green', 'Grass park', 'Lime', 'Earth', 'Blue black', 'Cadet blue', 'Rain', 'Greenery', 'Dark sky', 'Sunset', 'Sunflower', 'Grass', 'Aquamarine', 'Torquoise', 'Canary yellow', 'Pink tulip', 'Blue pine', 'New grass', 'Reflection',
                      'Mist', 'Blue sky', 'Granite', 'Pine', 'Fields', 'Sandstone', 'Burnt orange', 'Sea', 'Lagoon', 'Crimson', 'Forest', 'Rust', 'Gold', 'Overcast', 'Warm grey', 'Ice', 'Glacier blue', 'Lavender', 'Branch', 'Berry', 'Yellow feathers', 'Dark navy', 'Blueberry', 'Tangerine', 'Daffodil', 'Greenish sky', 'Sunglow', 'Mountains', 'Greenish mist', 'Orange', 'Yellow', 'Olive green', 'Leaf green', 'Deep purple', 'Indigo', 'Taupe', 'Blush', 'Hot pink', 'Bubble gum', 'Pollen', 'Chartreuse')
            color_fg = ('#000000', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#000000', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF',
                        '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#000000', '#FFFFFF', '#000000', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#000000', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#000000', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#000000', '#FFFFFF', '#000000', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF')
            color_bg = ('#FFFFFF', '#F98866', '#FF420E', '#80BD9E', '#89DA59', '#90AFC5', '#336B87', '#2A3132', '#763626', '#46211A', '#693D3D', '#BA5536', '#A43820', '#505160', '#68829E', '#AEBD38', '#598234', '#003B46', '#07575B', '#66A5AD', '#C4DFE6', '#2E4600', '#486B00', '#A2C523', '#7D4427', '#021C1E', '#004445', '#2C7873', '#6FB98F', '#375E97', '#FB6542', '#FBBB00', '#3F681C', '#98DBC6', '#5BC8AC', '#E6D72A', '#F18D9E', '#324851', '#86AC41', '#34675C',
                        '#7DA3A1', '#4CB5F5', '#4CB5F5', '#34675C', '#B3C100', '#F4CC70', '#DE7A22', '#20948B', '#6AB187', '#8D230F', '#1E434C', '#9B4F0F', '#C99E10', '#F1F1F2', '#BCBABE', '#A1D6E2', '#1995AD', '#9A9EAB', '#5D535E', '#EC96A4', '#DFE166', '#011A27', '#063852', '#F0810F', '#E6DF44', '#75B1A9', '#D9B44A', '#4F6457', '#ACD0C0', '#EB8A44', '#F9DC24', '#4B7447', '#8EBA43', '#363237', '#2d4262', '#73605B', '#D09683', '#F52549', '#FA6775', '#FFD64D', '#9BC01C')
            category = ('Defaults', 'Fresh and Bright', 'Fresh and Bright', 'Fresh and Bright', 'Fresh and Bright', 'Subdued and Professional', 'Subdued and Professional', 'Subdued and Professional', 'Subdued and Professional', 'Dark and Earthy', 'Dark and Earthy', 'Dark and Earthy', 'Dark and Earthy', 'Crisp and Dramatic', 'Crisp and Dramatic', 'Crisp and Dramatic', 'Crisp and Dramatic', 'Cool blues', 'Cool blues', 'Cool blues', 'Cool blues', 'Outdoorsy and Natural', 'Outdoorsy and Natural', 'Outdoorsy and Natural', 'Outdoorsy and Natural', 'Watery Blue Greens', 'Watery Blue Greens', 'Watery Blue Greens', 'Watery Blue Greens', 'Primary Colors With a  Vibrant Twist', 'Primary Colors With a  Vibrant Twist', 'Primary Colors With a  Vibrant Twist', 'Primary Colors With a  Vibrant Twist', 'Refreshing and Preety', 'Refreshing and Preety', 'Refreshing and Preety', 'Refreshing and Preety',
                        'Playful Greens and Blues', 'Playful Greens and Blues', 'Playful Greens and Blues', 'Playful Greens and Blues', 'Fresh & Energetic', 'Fresh & Energetic', 'Fresh & Energetic', 'Fresh & Energetic', 'Surf & Turf', 'Surf & Turf', 'Surf & Turf', 'Surf & Turf', 'Autumn in Vermont', 'Autumn in Vermont', 'Autumn in Vermont', 'Autumn in Vermont', 'Icy Blues and Grays', 'Icy Blues and Grays', 'Icy Blues and Grays', 'Icy Blues and Grays', 'Birds & Berries', 'Birds & Berries', 'Birds & Berries', 'Birds & Berries', 'Day & Night', 'Day & Night', 'Day & Night', 'Day & Night', 'Stylish & Retro', 'Stylish & Retro', 'Stylish & Retro', 'Stylish & Retro', 'Shades of Citrus', 'Shades of Citrus', 'Shades of Citrus', 'Shades of Citrus', 'Sunset to Dusk', 'Sunset to Dusk', 'Sunset to Dusk', 'Sunset to Dusk', 'Bright & Tropical', 'Bright & Tropical', 'Bright & Tropical', 'Bright & Tropical')
            sql("""CREATE TABLE IF NOT EXISTS "THEME_TABLE" ("theme_name" varchar ( 20 ), "color_bg"	varchar ( 10 ),	"color_fg" varchar ( 10 ), "category" varchar ( 50 ))""")
            for index in range(len(themes)):
                sql(
                    f"""INSERT INTO THEME_TABLE VALUES("{themes[index]}", "{color_bg[index]}", "{color_fg[index]}","{category}");""")

            try:
                # Attributes table
                sql("""CREATE TABLE "ATTRIBUTES" ("attribute_name" varchar ( 20 ),	"value"	varchar ( 20 ))""")
                attributes = ('autosave', 'word_wrap', 'status_bar', 'theme',
                              'theme_status', 'usermode', 'checkpoint_nos', 'runtime')
                values = ('False', 'none', 'not_take_status_bar',
                          'Default', '0', 'basic', '0', 'opened_before')
                for index in range(len(attributes)):
                    sql(
                        f"""INSERT INTO ATTRIBUTES VALUES ("{attributes[index]}", "{values[index]}")""")

                # Temp work table
                sql("""CREATE TABLE "TEMP_WORK" ("work_name" varchar ( 40 ), "value" TEXT)""")
                sql("""INSERT INTO TEMP_WORK VALUES ("word_wrap","")""")
                sql("""INSERT INTO TEMP_WORK VALUES ("restarted","")""")
                sql("""INSERT INTO TEMP_WORK VALUES ("file_location","")""")
                sql("""INSERT INTO TEMP_WORK VALUES ("date_time","")""")
            except:
                sql("""UPDATE ATTRIBUTES SET value='opened_before' WHERE attribute_name='runtime'""")
        create_database()
        create_shortcut()
        start()
    else:
        start()


run_check()
