#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

import tkinter as tk
from tkinter import messagebox
import pygubu
import main_model
from pathlib2 import Path
import threading
from PIL import Image, ImageTk

class MyApplication:

    ui_file_path = Path(".").resolve().parent.joinpath("Resources", "Main_GUI.ui")
    home_path = Path.home()
    reggegroep_logo_200px_path = Path(".").resolve().parent.joinpath("Resources", "Images", "Reggegroep_logo_200px.png")

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
        self.master.protocol("WM_DELETE_WINDOW", self.quit)

        windowWidth = self.mainwindow.winfo_reqwidth()
        windowHeight = self.mainwindow.winfo_reqheight()
        positionRight = int(self.mainwindow.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.mainwindow.winfo_screenheight()/3 - windowHeight/2)
        self.master.geometry("+{}+{}".format(positionRight, positionDown))

        self.load_images_init()
        self.loading_window_init()
        self.upload_tab_init()
        self.update_tab_init()
        self.settings_tab_init()

        if self.model.credentials_config_path.exists() == False:
            self.master.withdraw()
            messagebox.showerror("Error",
                                "Credentials.ini ontbreekt!\nPlaats het bestand in de folder:\n\n{}".format(str(self.model.credentials_config_path.parent)),
                                parent=self.mainwindow)
            self.quit()
        else:
            self.model.credentials_setup()

    def quit(self, event=None):
        self.master.destroy()

    def run(self):
        self.master.mainloop()

    def upload_path_changed(self, event=None):
        files = self.master.tk.splitlist(self.upload_pathchooser.cget("path"))
        log.debug(files)
        if len(files) > 0 and Path(files[0]).is_file() == True:
            self.upload_button.config(state="normal")
        else:
            self.upload_button.config(state="disabled")

    def upload_button_pressed(self, event=None):
        files = self.master.tk.splitlist(self.upload_pathchooser.cget("path"))
        files_list = []
        for file in files:
            files_list.append(Path(file))
        self.thread1 = threading.Thread(target=self.model.SortDocuments, args=[files_list])
        self.thread1.daemon = True
        self.thread1.start()
        self.loading_label.config(text="Uploading...")

        width_dif = self.mainwindow.winfo_reqwidth() - self.loading_window.toplevel.winfo_reqwidth()
        heigth_dif = self.mainwindow.winfo_reqheight() - self.loading_window.toplevel.winfo_reqheight()
        pos_x = int(self.master.winfo_x() + width_dif / 2)
        pos_y = int(self.master.winfo_y() + heigth_dif / 3)
        self.loading_window.toplevel.geometry("+{}+{}".format(pos_x, pos_y))

        self.loading_window.run()

        self.loading_loop()

    def update_path_changed(self, event=None):
        file = self.update_pathchooser.cget("path")
        log.debug(file)
        if Path(file).is_file() == True:
            self.update_button.config(state="normal")
        else:
            self.update_button.config(state="disabled")

    def update_button_pressed(self, event=None):
        file = Path(self.update_pathchooser.cget("path"))
        self.thread1 = threading.Thread(target=self.model.SortDocuments, args=[[file], True])
        self.thread1.daemon = True
        self.thread1.start()
        self.loading_label.config(text="Updating...")

        width_dif = self.mainwindow.winfo_reqwidth() - self.loading_window.toplevel.winfo_reqwidth()
        heigth_dif = self.mainwindow.winfo_reqheight() - self.loading_window.toplevel.winfo_reqheight()
        pos_x = int(self.master.winfo_x() + width_dif / 2)
        pos_y = int(self.master.winfo_y() + heigth_dif / 3)
        self.loading_window.toplevel.geometry("+{}+{}".format(pos_x, pos_y))

        self.loading_window.run()

        self.loading_loop()

    def loading_loop(self):
        if self.thread1.isAlive() == True:
            self.timer_id = root.after(100, self.loading_loop)
        else:
            self.loading_window.close()

    def update_uploader_name(self):
        new_name = self.uploader_name_text.get().replace(":", "")
        self.model.config["Preferences"]["uploader_name"] = new_name
        self.model.SaveConfig()

    def download_path_changed(self, event=None):
        new_path = self.download_pathchooser.cget("path")
        self.model.config["Preferences"]["download_directory"] = new_path
        self.model.SaveConfig()

    def upload_tab_init(self):
        self.upload_pathchooser = self.builder.get_object("Pathchooser_Upload")
        self.upload_button = self.builder.get_object("Button_Upload")
        self.upload_logo = self.builder.get_object("Upload_Logo")

        self.upload_logo.config(image=self.reggegroep_logo_200px_image)
        self.upload_pathchooser.config(start_dir=self.home_path)

    def update_tab_init(self):
        self.update_pathchooser = self.builder.get_object("Pathchooser_Update")
        self.update_button = self.builder.get_object("Button_Update")
        self.update_logo = self.builder.get_object("Update_Logo")

        self.update_logo.config(image=self.reggegroep_logo_200px_image)
        self.update_pathchooser.config(start_dir=self.home_path)

    def settings_tab_init(self):
        self.uploader_name_text = self.builder.get_variable("uploader_name_text")
        self.uploader_name_text.set(self.model.config["Preferences"]["uploader_name"])

        self.download_pathchooser = self.builder.get_object("Pathchooser_Download")
        self.download_pathchooser.config(start_dir=self.home_path, path=self.model.config["Preferences"]["download_directory"])

    def loading_window_init(self):
        self.loading_window = self.builder.get_object("Loading_Window", self.mainwindow)
        self.loading_label = self.builder.get_object("Loading_Label")

    def load_images_init(self):
        self.logo_image = Image.open(str(self.reggegroep_logo_200px_path))
        self.reggegroep_logo_200px_image = ImageTk.PhotoImage(Image.open(str(self.reggegroep_logo_200px_path)))

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApplication(root)
    app.run()
