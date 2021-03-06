# encoding: utf8
from __future__ import unicode_literals

try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import filedialog
    from pathlib2 import Path
except:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog
    from pathlib2 import Path


class CustomPathChooser(ttk.Frame):
    """ Allows to choose a file, directory or multiple filenames.

    Generates <<PathChooserPathChanged>> event when the path is changed.

    """

    FILE = 'file'
    DIR = 'directory'
    FILES = "files"

    def __init__(self, master=None, **kw):
        ttk.Frame.__init__(self, master, **kw)
        self.master = master
        self._choose = self.FILE
        self.current_value = ''
        self.title_text = "Choose a File/Directory"
        self.start_dir = ""
        # subwidgets
        self.entry = o = ttk.Entry(self)
        o.grid(row=0, column=0, sticky='ew')
        o.bind('<KeyPress>', self.__on_enter_key_pressed)
        o.bind('<FocusOut>', self.__on_focus_out)
        self.folder_button = o = ttk.Button(self, text='▶', command = self.__on_folder_btn_pressed, width=4)
        o.grid(row=0, column=1, padx=2)

        #self.rowconfigure(0, weight = 0)
        self.columnconfigure(0, weight = 1)

    def configure(self, cnf=None, **kw):
        args = tk._cnfmerge((cnf, kw))
        key = 'selection type'
        if key in args:
            self._choose = args[key]
            del args[key]
        key = 'image'
        if key in args:
            self.folder_button.configure(image=args[key])
            del args[key]
        key = 'path'
        if key in args:
            self.entry.delete(0, 'end')
            self.entry.insert(0, args[key])
            self._generate_changed_event()
            del args[key]
        key = 'textvariable'
        if key in args:
            self.entry.configure(textvariable=args[key])
            self._generate_changed_event()
            del args[key]
        key = "title"
        if key in args:
            self.title_text = args[key]
            del args[key]
        key = 'start_dir'
        if key in args:
            self.start_dir = args[key]
            del args[key]
        ttk.Frame.configure(self, args)

    config = configure

    def cget(self, key):
        option = 'selection type'
        if key == option:
            return self._choose
        option = 'image'
        if key == option:
            return self.folder_button.cget(key)
        option = 'path'
        if key == option:
            return self.current_value
        option = 'textvariable'
        if key == option:
            return self.entry.cget(option)
        option = "title"
        if key == option:
            return self.title_text
        option = 'start_dir'
        if key == option:
            return self.start_dir
        return ttk.Frame.cget(self, key)

    __getitem__ = cget

    def _is_changed(self):
#        print(repr(self.current_value), ':', repr(self.entry.get()))
        if self.current_value != self.entry.get():
            return True
        return False

    def _generate_changed_event(self):
        if self._is_changed():
            self.current_value = self.entry.get()
            if self._choose == self.FILE:
                display_text = Path(self.entry.get()).name
                self.entry.delete(0, "end")
                self.entry.insert(0, display_text)
            elif self._choose == self.DIR:
                display_text = Path(self.entry.get()).stem
                self.entry.delete(0, "end")
                self.entry.insert(0, display_text)
            elif self._choose == self.FILES:
                paths = self.master.tk.splitlist(self.entry.get())
                path_list = []
                for path in paths:
                    path_list.append(str(Path(path).name))
                display_text = "; ".join(path_list)
                self.entry.delete(0, "end")
                self.entry.insert(0, display_text)
            self.event_generate('<<PathChooserPathChanged>>')

    def __on_enter_key_pressed(self, event):
        key = event.keysym
        if key in  ('Return','KP_Enter'):
            self._generate_changed_event()

    def __on_focus_out(self, event):
         self._generate_changed_event()

    def __on_folder_btn_pressed(self):
        fname = None
        if self._choose == self.FILE:
            fname = filedialog.askopenfilename(initialdir=self.cget('start_dir'), title=self.cget("title"))
        elif self._choose == self.DIR:
            fname = filedialog.askdirectory(initialdir=self.cget('start_dir'), title=self.cget("title"))
        else:
            fname = filedialog.askopenfilenames(initialdir=self.cget("start_dir"), title=self.cget("title"))
        if fname:
            self.configure(path=fname)
