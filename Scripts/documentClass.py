#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from datetime import datetime, date

class Document():

    def __init__(self, doc_info, from_database = False):
        self.titel = ""
        self.auteurs = []
        self.datum = ""
        self.file_path = ""
        self.storage_id = 0
        self.uploader_name = ""
        self.document_type = ""
        self.template_version = 0

        self.titel = doc_info["Titel"].strip()

        authors = doc_info["Auteur"].split("\n")
        for author in authors:
            self.auteurs.append(author.strip())

        self.uploader_name = doc_info["Uploader_Name"]
        self.template_version = doc_info["version"]

        if (from_database == True):
            self.database_init(doc_info)
        else:
            self.sorter_init(doc_info)

    def sorter_init(self, doc_info):
        self.local_path = doc_info["local_path"]

        input_date = doc_info["Datum"].strip()
        try:
            output_date = datetime.strptime(input_date, "%d-%m-%Y").date()
        except:
            output_date = date.today()

        self.datum = str(output_date)

    def database_init(self, doc_info):
        self.file_path = doc_info["filepath"]
        self.storage_id = int(doc_info["storage_id"])

        input_date = doc_info["Datum"]
        try:
            output_date = datetime.strptime(input_date, "%Y-%m-%d").date()
        except:
            output_date = date.today()

        self.datum = str(output_date)

    def __repr__(self):
        from pprint import pformat
        return pformat(vars(self), indent=4, width=100)

    def small_info(self):
        return {
        "Titel: ":self.titel,
        "Auteur(s): ":self.auteurs,
        "Datum: ":self.datum
        }

    def all_info(self):
        return {
        "Titel: ":self.titel,
        "Auteur(s): ":self.auteurs,
        "Datum: ":self.datum,
        "Uploader: ":self.uploader_name,
        "Bestandpad: ":self.file_path
        }
