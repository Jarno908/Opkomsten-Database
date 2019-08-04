#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from pcloud import PyCloud
from pathlib2 import Path
import sys

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
                try:
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
                except Exception as e:
                    log.warning(e)
                    failed_files.append(file)

        finally:
            if pc != None:
                pc.logout()

            return [uploaded_files, failed_files]


    def download_files(self, file_id_list, download_directory):

        succesfull_downloads = []
        failed_downloads = []

        try:
            pc = PyCloud(self.credentials["storage_username"], self.credentials["storage_password"])
        except:
            log.error("Could not login to pCloud!")
        else:
            for file_id, fname in file_id_list.items():
                try:
                    result = pc.file_open(flags=[0x0400], fileid=int(file_id))
                    file_path = Path(download_directory).joinpath(fname)
                    log.debug(result)
                    log.debug(file_id)
                    with open(str(file_path), "wb") as f:
                        f.write(pc.file_read(fd=result["fd"], count=sys.maxsize))
                    succesfull_downloads.append(fname)
                except Exception as e:
                    log.warning(e)
                    failed_downloads.append(fname)

        finally:
            if pc != None:
                pc.logout()
            return [succesfull_downloads, failed_downloads]
