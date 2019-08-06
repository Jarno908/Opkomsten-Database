#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

import constants
from documentClass import Document

class Opkomst(Document):

    def __init__(self, doc_info, from_database = False):
        Document.__init__(self, doc_info, from_database)

        self.speltakken = []
        self.categorie = ""
        self.omschrijving = ""
        self.materiaal = []
        self.zoekwoorden = []

        self.document_type = "Opkomst"
        method_string = "opkomstV" + str(self.template_version)
        opkomst_methods = {"opkomstV1" : self.opkomstV1}

        if method_string in opkomst_methods:
            opkomst_methods[method_string](doc_info)

    def opkomstV1(self, doc_info):

        groups = doc_info["Speltak(ken)"].split("\n")
        for group in groups:
            self.speltakken.append(constants.SPELTAKKEN_DICTIONARY.get(group.strip(), "Overig"))

        self.categorie = constants.CATEGORIES_DICTIONARY.get(doc_info["Categorie"].strip(), "Overig")

        self.omschrijving = doc_info["Omschrijving"]

        materials = doc_info["Materiaal"].split("\n")
        for material in materials:
            self.materiaal.append(material.strip())

        searchwords = doc_info["Zoekwoorden"].split("\n")
        for word in searchwords:
            self.zoekwoorden.append(word.strip())

    def small_info(self):
        return {
        "Titel:":self.titel,
        "Speltak:":", ".join(self.speltakken),
        "Categorie:":self.categorie,
        "Omschrijving:":self.omschrijving
        }

    def all_info(self):
        return {
        "Titel: ":self.titel,
        "Auteur(s): ":", ".join(self.auteurs),
        "Datum: ":self.datum,
        "Speltak: ":", ".join(self.speltakken),
        "Categorie: ":self.categorie,
        "Omschrijving: ":self.omschrijving,
        "Materiaal: ":"\n".join(self.materiaal),
        "Uploader: ":self.uploader_name,
        "Bestandpad: ":self.file_path
        }
