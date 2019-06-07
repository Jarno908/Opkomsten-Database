#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

import tkinter as tk
import pygubu
import main_model
from pathlib2 import Path
import threading
from PIL import Image, ImageTk

class MyApplication:

    ui_file_path = Path(".").resolve().parent.joinpath("GUI", "Main_GUI.ui")
    home_path = Path.home()
    reggegroep_logo_200px_path = Path(".").resolve().parent.joinpath("GUI", "Reggegroep Logo Bestanden", "Reggegroep_logo_200px.png")

    timer_id = None

    def __init__(self, master):
        self.master = master
        self.model = main_model.MainModel()
        self.builder = builder = pygubu.Builder()
        builder.add_from_file(str(self.ui_file_path))
        self.mainwindow = builder.get_object("Main_Notebook", self.master)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        builder.connect_callbacks(self)
        self.master.title("Reggegroep Documenten Beheer")

        self.upload_pathchooser = builder.get_object("Pathchooser_Upload")
        self.upload_button = builder.get_object("Button_Upload")
        self.upload_logo = builder.get_object("Upload_Logo")

        self.logo_image = Image.open(str(self.reggegroep_logo_200px_path))
        self.reggegroep_logo_200px_image = ImageTk.PhotoImage(Image.open(str(self.reggegroep_logo_200px_path)))

        self.upload_logo.config(image=self.reggegroep_logo_200px_image)

        self.upload_pathchooser.config(path=self.home_path)

    def quit(self, event=None):
        self.mainwindow.quit()

    def run(self):
        self.mainwindow.mainloop()

    def on_path_changed(self, event=None):
        input_path = Path(self.upload_pathchooser.cget("path"))
        if input_path.exists() == True and input_path.is_dir() == True:
            self.upload_button.config(state="normal")
        else:
            self.upload_button.config(state="disabled")

    def upload_button_pressed(self, event=None):
        input_path = Path(self.upload_pathchooser.cget("path"))
        self.thread1 = threading.Thread(target=self.model.SortDocuments, args=[input_path])
        self.thread1.daemon = True
        self.thread1.start()
        self.loading_window = self.builder.get_object("Loading_Window", self.mainwindow)
        self.loading_window.run()
        self.loading_loop()

    def loading_loop(self):
        log.debug("still Alive")
        if self.thread1.isAlive() == True:
            self.timer_id = root.after(100, self.loading_loop)
        else:
            self.loading_window.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApplication(root)
    app.run()
