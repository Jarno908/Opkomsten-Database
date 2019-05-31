#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from pathlib import Path
import docx
import documentClass
import constants

# Sorteert de bestanden in de input folder en maakt een file_path voor ieder
def sort(input_path):

    sorted_documents = []

    for file in input_path.iterdir():
        if file.suffix == ".docx":
            log.info("Currently being sorted: {}".format(file))
            document_data = getDocumentData(str(file))

            if document_data.template_version != 0:
                log.info("Document uses {}{} format".format(document_data.document_type, document_data.template_version))

                if document_data.document_type == "Opkomst":
                    custom_path = opkomstPath(document_data)
                else:
                    raise Exception("Not a supported document-type!")

                if document_data.titel != "":
                    custom_path = custom_path.joinpath(document_data.titel)
                else:
                    custom_path = custom_path.joinpath(file.stem)

                custom_path = custom_path.with_suffix(".docx")
                document_data.file_path = str(custom_path)
                sorted_documents.append(document_data)

            else:
                log.debug("File {} does not use a valid template".format(file.name))

    return sorted_documents

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
        data["local_path"] = file_path

        if "Titel" in data:
            for c in constants.FORBIDDEN_CHARACTERS:
                data["Titel"] = data["Titel"].replace(c, "")

        if "Materiaal" in data:
            data["Materiaal"] = data["Materiaal"].lower()
        if "Zoekwoorden" in data:
            data["Zoekwoorden"] = data["Zoekwoorden"].lower()
        if "Speltak(ken)" in data:
            data["Speltak(ken)"] = data["Speltak(ken)"].lower()
        if "Categorie" in data:
            data["Categorie"] = data["Categorie"].lower()

        return documentClass.Document(data)

def opkomstPath(document_data):
    custom_path = Path("/").joinpath("Opkomsten")

    if document_data.speltakken[0] in constants.SPELTAKKEN:
        custom_path = custom_path.joinpath(document_data.speltakken[0])
    else:
        custom_path = custom_path.joinpath("Overig")

    if document_data.categorie in constants.CATEGORIES:
        custom_path = custom_path.joinpath(document_data.categorie)
    else:
        custom_path = custom_path.joinpath("Overig")

    return custom_path
