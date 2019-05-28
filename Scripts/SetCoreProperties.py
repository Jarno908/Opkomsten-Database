#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from pathlib import Path
import docx

#file = Path(".").resolve().parent.joinpath("Templates", "Opkomst Template V01.docx")

versionNumber = "01"
author = "Jarno Vos"

def changeProperties(filePath, version, name):
    try:
        doc = docx.Document(filePath)
    except ValueError:
        log.error('File provided is not a docx file!')
        return None
    except:
        log.error('Read Docx Error!!!')
        return None
    else:
        doc.core_properties.version = version
        doc.core_properties.author = name
        doc.save(filePath)

        log.info("Version = " + doc.core_properties.version)
        log.info("Author = " + doc.core_properties.author)

changeProperties(str(file), versionNumber, author)
print("Done")
