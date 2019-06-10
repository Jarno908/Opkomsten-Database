#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from pcloud import PyCloud
import credentials
from pathlib2 import Path

def uploadDocuments(file_list, replace=False):
    failed_files = []

    try:
        pc = PyCloud(credentials.STORAGE_USERNAME, credentials.STORAGE_PASSWORD)
    except:
        log.error("Could not login to pCloud!")
    else:
        for file in file_list:
            file_path = Path(file.file_path)
            log.info("Currently trying to upload {}".format(file_path))
            file_data = open(file.local_path, "rb")

            if replace == True:
                result = pc.uploadfile(path=file_path.parent, filename=file_path.name, data=file_data)
                file.storage_id = result["fileids"][0]
            else:
                directory_list = pc.listfolder(path=file_path.parent)
                directory_names = []
                for content in directory_list["metadata"]["contents"]:
                    directory_names.append(content["name"])

                if file_path.name in directory_names:
                    log.warning("file already exist in directory!")
                    failed_files.append(file)
                else:
                    result = pc.uploadfile(path=file_path.parent, filename=file_path.name, data=file_data)
                    file.storage_id = result["fileids"][0]

    finally:
        if pc != None:
            pc.logout()

        return failed_files
