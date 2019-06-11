#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

import constants

class Document():

    def __init__(self, doc_dictionary):
        self.titel = ""
        self.auteurs = []
        self.datum = ""
        self.file_path = ""
        self.storage_id = 0

        self.document_type = constants.DOCUMENT_TYPES.get(doc_dictionary["version"][0])
        self.template_version = int(doc_dictionary["version"][1:])
        self.uploader_name = doc_dictionary["Uploader_Name"]
        self.local_path = doc_dictionary["local_path"]

    def __repr__(self):
        from pprint import pformat
        return pformat(vars(self), indent=4, width=100)
