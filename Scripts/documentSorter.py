#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from pathlib import Path
import docx
import documentClass

def sort(in_path, out_path, categories, categories_dictionary, forbidden_chars, delete_input):
    for category in categories:
        out_path.joinpath(category).mkdir(exist_ok=True)

    for file in in_path.iterdir():
        if file.suffix == ".docx":
            log.info("Currently being sorted: {}".format(file))
            document_data = getDocumentData(str(file), forbidden_chars, categories_dictionary)

            if document_data.template_version != 0:
                log.info("Document uses {}{} format".format(document_data.document_type, document_data.template_version))

                log.debug("categorie = {}".format(document_data.categorie))
                if document_data.categorie in categories:
                    custom_path = out_path.joinpath(document_data.categorie)
                else:
                    custom_path = out_path.joinpath("Overig")

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


def getDocumentData(file_path, forbidden_chars, categories_dictionary):
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

        for c in forbidden_chars:
            data["Titel"] = data["Titel"].replace(c, "")

        data["Speltak(ken)"] = data["Speltak(ken)"].lower()
        data["Categorie"] = categories_dictionary.get(data["Categorie"].lower(), "Overig")

        return documentClass.Document(data)

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
