#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

import constants

class Document():

    titel = ""
    auteurs = []
    datum = ""
    speltakken = []
    categorie = ""
    omschrijving = ""
    materiaal = []
    zoekwoorden = []
    document_type = ""
    template_version = 0
    file_name = ""
    storage_id = 0

    def __init__(self, doc_dictionary):
        self.titel = ""
        self.auteurs = []
        self.datum = ""
        self.speltakken = []
        self.categorie = ""
        self.omschrijving = ""
        self.materiaal = []
        self.zoekwoorden = []
        self.document_type = ""
        self.emplate_version = 0

        if len(doc_dictionary["version"]) == 4:
            self.document_type = constants.DOCUMENT_TYPES.get(doc_dictionary["version"][0])
            self.template_version = int(doc_dictionary["version"][1:])

            if self.document_type == "Opkomst":
                self.init_Opkomst(doc_dictionary)

        # Voor als het een Opkomst-document is
    def init_Opkomst(self, doc_dictionary):
        self.titel = doc_dictionary["Titel"].strip()

        authors = doc_dictionary["Auteur"].split(",")
        for author in authors:
            self.auteurs.append(author.strip())

        self.datum = doc_dictionary["Datum"].strip()

        groups = doc_dictionary["Speltak(ken)"].split(",")
        for group in groups:
            self.speltakken.append(constants.SPELTAKKEN_DICTIONARY.get(group.strip(), "Overig"))

        self.categorie = constants.CATEGORIES_DICTIONARY.get(doc_dictionary["Categorie"], "Overig")

        self.omschrijving = doc_dictionary["Omschrijving"]

        materials = doc_dictionary["Materiaal"].split(",")
        for material in materials:
            self.materiaal.append(material.strip())

        searchwords = doc_dictionary["Zoekwoorden"].split(",")
        for word in searchwords:
            self.zoekwoorden.append(word.strip())
