#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from pcloud import PyCloud
from pathlib2 import Path

class pCloud_shell():

    def __init__(self, credentials):
        self.credentials = credentials

    def uploadDocuments(self, file_list, replace=False):
        uploaded_files = []
        failed_files = []

        try:
            pc = PyCloud(self.credentials["storage_username"], self.credentials["storage_password"])
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
                    uploaded_files.append(file)
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
                        uploaded_files.append(file)

        finally:
            if pc != None:
                pc.logout()

            return [uploaded_files, failed_files]
