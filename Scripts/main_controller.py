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
import queue
from PIL import Image, ImageTk
from itertools import cycle
from documents_frame import DocumentsFrame
from large_info_frame import InfoFrame

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
        self.opkomsten_search_init()
        self.upload_tab_init()
        self.update_tab_init()
        self.settings_tab_init()
        self.items_window_init()
        self.info_window_init()

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

    def opkomsten_button_pressed(self, event=None):
        for child in self.items_frame.interior.winfo_children():
            child.destroy()

        search_string = self.opkomsten_search_entry.get().strip()
        search_speltak = self.opkomsten_speltaken_combobox.get()
        search_category = self.opkomsten_categories_combobox.get()

        search_info = {
        "search_string" : search_string,
        "speltakken" : search_speltak,
        "category" : search_category
        }

        self.q = queue.Queue()
        self.thread1 = threading.Thread(target=self.model.SearchDocuments, args=["opkomst", search_info, self.q])
        self.thread1.daemon = True
        self.thread1.start()

        self.loading_window_setup("Zoeken")
        self.loading_window.run()

        self.post_loading_method = self.post_document_search

        self.loading_loop()

    def post_document_search(self):
        self.current_documents = self.q.get()
        display_data = []
        for document in self.current_documents:
            display_data.append(document.small_info())
        DocumentsFrame(self.items_frame.interior, display_data, self.display_info, self.download_button_pressed)

        width_dif = self.mainwindow.winfo_reqwidth() - self.items_window.toplevel.winfo_reqwidth()
        heigth_dif = self.mainwindow.winfo_reqheight() - self.items_window.toplevel.winfo_reqheight()
        pos_x = int(self.master.winfo_x() + width_dif / 2)
        pos_y = int(self.master.winfo_y() + heigth_dif / 3)
        self.items_window.toplevel.geometry("+{}+{}".format(pos_x, pos_y))

        self.items_frame.canvas.yview_moveto(0)

        self.items_window.run()

    def display_info(self, idx):
        for child in self.info_frame.interior.winfo_children():
            child.destroy()

        InfoFrame(self.info_frame.interior, self.current_documents[idx].all_info())

        width_dif = self.mainwindow.winfo_reqwidth() - self.info_window.toplevel.winfo_reqwidth()
        heigth_dif = self.mainwindow.winfo_reqheight() - self.info_window.toplevel.winfo_reqheight()
        pos_x = int(self.master.winfo_x() + width_dif / 2)
        pos_y = int(self.master.winfo_y() + heigth_dif / 3)
        self.info_window.toplevel.geometry("+{}+{}".format(pos_x, pos_y))

        self.info_frame.canvas.yview_moveto(0)

        self.info_window.run()

    def download_button_pressed(self, idx):
        self.q = queue.Queue()
        self.thread1 = threading.Thread(target=self.model.download_files, args=[[self.current_documents[idx]], self.q])
        self.thread1.daemon = True
        self.thread1.start()

        self.loading_window_setup("Downloaden")
        self.loading_window.run()

        self.post_loading_method = self.post_downloading

        self.loading_loop()

    def post_downloading(self):
        results = self.q.get()

        if len(results[1]) > 0:
            message = "{} documenten konden niet gedownload worden.\n\nNiet gedownload:\n".format(len(results[1]))
            for url in results[1]:
                message = message + url + "\n"
            messagebox.showwarning("Downloaden svoltooid",
                                message,
                                parent=self.mainwindow)
        else:
            messagebox.showinfo("Downloaden voltooid",
                                "Alle documenten zijn succesvol gedownload.",
                                parent=self.mainwindow)

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
        self.q = queue.Queue()
        self.thread1 = threading.Thread(target=self.model.SortDocuments, args=[files_list, self.q])
        self.thread1.daemon = True
        self.thread1.start()

        self.loading_window_setup("Uploading")
        self.loading_window.run()

        self.post_loading_method = self.post_uploading

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
        self.q = queue.Queue()
        self.thread1 = threading.Thread(target=self.model.SortDocuments, args=[[file], self.q, True])
        self.thread1.daemon = True
        self.thread1.start()

        self.loading_window_setup("Updating")
        self.loading_window.run()

        self.post_loading_method = self.post_updating

        self.loading_loop()

    def loading_window_setup(self, loading_text = "Loading"):
        trail_loop = ["", ".", "..", "...", "....", "....."]
        loading_loop_text = []
        for trail in trail_loop:
            loading_loop_text.append(loading_text + trail)

        self.loading_text_loop = cycle(loading_loop_text)

        width_dif = self.mainwindow.winfo_reqwidth() - self.loading_window.toplevel.winfo_reqwidth()
        heigth_dif = self.mainwindow.winfo_reqheight() - self.loading_window.toplevel.winfo_reqheight()
        pos_x = int(self.master.winfo_x() + width_dif / 2)
        pos_y = int(self.master.winfo_y() + heigth_dif / 3)
        self.loading_window.toplevel.geometry("+{}+{}".format(pos_x, pos_y))

    def loading_loop(self):
        if self.thread1.isAlive() == True:
            self.loading_label.config(text=next(self.loading_text_loop))
            self.timer_id = root.after(100, self.loading_loop)
        else:
            self.loading_window.close()
            if self.post_loading_method != None:
                self.post_loading_method()

    def post_uploading(self):
        results = self.q.get()

        if len(results[0][1]) > 0:
            message = "{} documenten konden niet geupload worden.\nDocumenten die al online staan kunnen niet opnieuw geupload worden.\nJe kunt documenten updaten in het 'Update' tabblad.\n\nNiet geupload:\n".format(len(results[0][1]))
            for file in results[0][1]:
                message = message + str(Path(file.local_path).name) + "\n"
            messagebox.showwarning("Uploaden voltooid",
                                message,
                                parent=self.mainwindow)
        else:
            messagebox.showinfo("Uploaden voltooid",
                                "Alle documenten zijn succesvol geupload.",
                                parent=self.mainwindow)

    def post_updating(self):
        results = self.q.get()

        if len(results[0][1]) > 0:
            message = "{} kon niet geupdate worden".format(str(Path(results[0][1][0].local_path).name))
            messagebox.showwarning("Update voltooid",
                                message,
                                parent=self.mainwindow)
        else:
            messagebox.showinfo("Update voltooid",
                                "Het document is succesvol geupdate.",
                                parent=self.mainwindow)

    def update_uploader_name(self):
        new_name = self.uploader_name_text.get().replace(":", "")
        self.model.config["Preferences"]["uploader_name"] = new_name
        self.model.SaveConfig()

    def download_path_changed(self, event=None):
        new_path = self.download_pathchooser.cget("path")
        self.model.config["Preferences"]["download_directory"] = new_path
        self.model.SaveConfig()

        #All the methods for initializing the GUI

    def opkomsten_search_init(self):
        self.opkomsten_search_entry = self.builder.get_object("Opkomsten_Searchwords_Entry")
        self.opkomsten_speltaken_combobox = self.builder.get_object("Opkomsten_Speltakken_Combobox")
        self.opkomsten_categories_combobox = self.builder.get_object("Opkomsten_Categories_Combobox")

        self.opkomsten_speltaken_combobox.current(0)
        self.opkomsten_categories_combobox.current(0)

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

    def items_window_init(self):
        self.items_window = self.builder.get_object("Items_Window", self.mainwindow)
        self.items_frame = self.builder.get_object("Items_Frame", self.mainwindow)

    def info_window_init(self):
        self.info_window = self.builder.get_object("Info_Window", self.mainwindow)
        self.info_frame = self.builder.get_object("Info_Frame", self.mainwindow)


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApplication(root)
    app.run()
