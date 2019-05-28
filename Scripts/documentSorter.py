#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from pathlib import Path
import docx

def sort(in_path, out_path, categories, forbidden_chars, delete_input):
    for category in categories:
        out_path.joinpath(category).mkdir(exist_ok=True)

    for file in in_path.iterdir():
        if file.suffix == ".docx":
            log.info("Currently being sorted: {}".format(file))
            doc_dictionary = getText(str(file), forbidden_chars)

            version = doc_dictionary["version"]
            log.info("Document uses V{}".format(version))

            if doc_dictionary["Categorie"] in categories:
                custom_path = out_path.joinpath(doc_dictionary["Categorie"])
            else:
                custom_path = out_path.joinpath("Overig")

            if doc_dictionary["Titel"] != "":
                new_path = customPath(custom_path, doc_dictionary["Titel"])
            else:
                new_path = customPath(custom_path, file.stem)

            if delete_input == True:
                file.rename(new_path)
                log.info("File moved to {}".format(new_path))
            else:
                document = docx.Document(str(file))
                document.save(str(new_path))
                log.info("File copied to {}".format(new_path))


def getText(file_path, forbidden_chars):
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
                fullText.append(paragraph.text.replace(";", ""))

            fullText = ";".join(fullText)

            data[keys[i]] = fullText

        data["version"] = doc.core_properties.version

        for c in forbidden_chars:
            data["Titel"] = data["Titel"].replace(c, "")

        data["Auteur"] = data["Auteur"].replace(",", ";").replace(', ', ";")
        data["Speltak(ken)"] = data["Speltak(ken)"].replace(",", ";").replace(', ', ";")
        data["Zoekwoorden"] = data["Zoekwoorden"].replace(",", ";").replace(', ', ";")

        return data

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
