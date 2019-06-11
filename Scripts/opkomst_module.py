#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

import constants
from documentClass import Document

class Opkomst(Document):

    def __init__(self, doc_dictionary):
        Document.__init__(self, doc_dictionary)

        self.speltakken = []
        self.categorie = ""
        self.omschrijving = ""
        self.materiaal = []
        self.zoekwoorden = []

        method_string = "opkomstV" + str(self.template_version)
        opkomst_methods = {"opkomstV1" : self.opkomstV1}

        if method_string in opkomst_methods:
            opkomst_methods[method_string](doc_dictionary)

    def opkomstV1(self, doc_dictionary):
        self.titel = doc_dictionary["Titel"].strip()

        authors = doc_dictionary["Auteur"].split("\n")
        for author in authors:
            self.auteurs.append(author.strip())

        self.datum = doc_dictionary["Datum"].strip()

        groups = doc_dictionary["Speltak(ken)"].split("\n")
        for group in groups:
            self.speltakken.append(constants.SPELTAKKEN_DICTIONARY.get(group.strip(), "Overig"))

        self.categorie = constants.CATEGORIES_DICTIONARY.get(doc_dictionary["Categorie"], "Overig")

        self.omschrijving = doc_dictionary["Omschrijving"]

        materials = doc_dictionary["Materiaal"].split("\n")
        for material in materials:
            self.materiaal.append(material.strip())

        searchwords = doc_dictionary["Zoekwoorden"].split("\n")
        for word in searchwords:
            self.zoekwoorden.append(word.strip())
