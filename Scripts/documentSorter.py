#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from pathlib import Path
import docx
import documentClass
import constants

# Sorteert de bestanden in de input folder en kopieert/verplaatst de bestanden naar de ouput folder
def sort(in_path, out_path, delete_input):
    for speltak in constants.SPELTAKKEN:
        for category in constants.CATEGORIES:
            out_path.joinpath("Opkomsten", speltak, category).mkdir(parents = True, exist_ok=True)

    for file in in_path.iterdir():
        if file.suffix == ".docx":
            log.info("Currently being sorted: {}".format(file))
            document_data = getDocumentData(str(file))

            if document_data.template_version != 0:
                log.info("Document uses {}{} format".format(document_data.document_type, document_data.template_version))

                if document_data.document_type == "Opkomst":
                    custom_path = opkomstPath(out_path, document_data)
                else:
                    raise Exception("Not a supported document-type!")

                if document_data.titel != "":
                    new_path = customPath(custom_path, document_data.titel)
                else:
                    new_path = customPath(custom_path, file.stem)

                if delete_input == True:
                    file.rename(new_path)
                    log.info("File moved to {}".format(new_path))
                else:
                    document = docx.Document(str(file))
                    document.save(str(new_path))
                    log.info("File copied to {}".format(new_path))

            else:
                log.debug("File {} does not use a valid template".format(file.stem))

# Alle informatie wordt uit het document gehaald en in een Document object gesptopt
def getDocumentData(file_path):
    try:
        doc = docx.Document(file_path)
    except ValueError:
        log.error('File provided is not a docx file!')
        return None
    except:
        log.error('Read Docx Error!!!')
        return None
    else:
        table = doc.tables[0]
        data = {}
        keys = []

        for cell in table.column_cells(0):
            keys.append(cell.paragraphs[0].text)

        for i in range(len(keys)):
            fullText = []
            for paragraph in table.column_cells(1)[i].paragraphs:
                fullText.append(paragraph.text.replace("\n", ""))

            fullText = "\n".join(fullText)

            data[keys[i]] = fullText

        data["version"] = doc.core_properties.version

        for c in constants.FORBIDDEN_CHARACTERS:
            data["Titel"] = data["Titel"].replace(c, "")

        data["Materiaal"] = data["Materiaal"].lower()
        data["Zoekwoorden"] = data["Zoekwoorden"].lower()
        data["Speltak(ken)"] = data["Speltak(ken)"].lower()
        data["Categorie"] = data["Categorie"].lower()

        return documentClass.Document(data)

# Controleert en verandert de filepath als er al een bestand met dezelfde naam aanwezig is in de folder
def customPath(file_path, name):
    already_exists = True
    while already_exists == True:
        already_exists = False
        for file in file_path.iterdir():
            if file.stem == name:
                already_exists = True
        if already_exists == True:
            name = name + "V2"

    return file_path.joinpath(name + ".docx")

def opkomstPath(start_path, document_data):
    custom_path = start_path.joinpath("Opkomsten")

    if document_data.speltakken[0] in constants.SPELTAKKEN:
        custom_path = custom_path.joinpath(document_data.speltakken[0])
    else:
        custom_path = custom_path.joinpath("Overig")

    if document_data.categorie in constants.CATEGORIES:
        custom_path = custom_path.joinpath(document_data.categorie)
    else:
        custom_path = custom_path.joinpath("Overig")

    return custom_path
