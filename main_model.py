#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from pathlib2 import Path
import configparser
import documentSorter
import pCloud_communications
import database_communications
import base64
from resources import ResourcePath

#logging.disable(logging.DEBUG)

class MainModel():

    default_config_path = Path(ResourcePath(str(Path("Resources").joinpath("default_config.ini"))))
    personal_config_path = Path().home().joinpath("ScoutingDocumentenApp", "personal_config.ini")
    config = configparser.RawConfigParser(delimiters=(':'))

    credentials_config_path = Path().home().joinpath("ScoutingDocumentenApp", "credentials.ini")

    def __init__(self):
        self.innit_config()
        documentSorter.setup_documentSorter(self.config)

        # Voor het aanmaken en update van de config file
    def innit_config(self):
        log.info("Personal configpath is {}".format(self.personal_config_path))
        if self.personal_config_path.exists() == False:
            log.warning("personal_config.ini is missing!")
            self.personal_config_path.parent.mkdir(exist_ok=True)
            if self.default_config_path.exists() == False:
                log.error("default_config.ini is missing!")
                raise Exception("config files missing!")
            else:
                self.config.read(str(self.default_config_path))
                with open(str(self.personal_config_path), "w") as configfile:
                    self.config.write(configfile)
                self.new_config()
        else:
            self.config.read(str(self.personal_config_path))
            default_config = configparser.RawConfigParser(delimiters=(':'))
            default_config.read(str(self.default_config_path))
            if int(default_config["Main"]["version"]) > int(self.config["Main"]["version"]):
                with open(str(self.personal_config_path), "w") as configfile:
                    default_config.write(configfile)
                self.config = default_config
                log.info("Configfile updated to newer version")
                self.new_config()

    def new_config(self):
        self.config["Preferences"]["uploader_name"] = Path().home().stem
        self.config["Preferences"]["download_directory"] = str(Path().home().joinpath("Downloads"))
        self.SaveConfig()

    def SortDocuments(self, files_list, q, replace_files = False):
        sorted_documents = documentSorter.sort(files_list)
        upload_results = self.pCloud_shell.uploadDocuments(sorted_documents, replace_files)
        log.info("{} files already exist on pCloud".format(len(upload_results[1])))
        database_results = self.database_shell.insert_entries(upload_results[0])
        log.info("{} files failed to insert into database".format(len(database_results)))
        q.put([upload_results, database_results])
        return

    def SearchDocuments(self, type, search_info, q):
        result = []

        if type == "opkomst":
            result = self.database_shell.get_opkomsten(search_info)

        q.put(result)
        return

    def download_files(self, document_list, q):
        file_id_list = {}

        for document in document_list:
            fname = document.file_path.split("/")[-1]
            file_id_list[document.storage_id] = fname

        results = self.pCloud_shell.download_files(file_id_list, self.config["Preferences"]["download_directory"])
        q.put(results)
        return

    def SaveConfig(self):
        with open(str(self.personal_config_path), "w") as configfile:
            self.config.write(configfile)
        log.debug("Saved Configfile")

    def credentials_setup(self):
        self.credentials = {}
        credentials_config = configparser.RawConfigParser()
        credentials_config.read(str(self.credentials_config_path))
        for section in credentials_config.sections():
            for (key, val) in credentials_config.items(section):
                decrypted_val = base64.b64decode(val.encode('utf-8')).decode('utf-8')
                self.credentials[key] = decrypted_val

        self.pCloud_shell = pCloud_communications.pCloud_shell(self.credentials)
        self.database_shell = database_communications.database_shell(self.credentials)
