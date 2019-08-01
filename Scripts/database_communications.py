#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

import pymysql.cursors
import constants

class database_shell():

    def __init__(self, credentials):
        self.credentials = credentials

    def insert_entries(self, files):
        connection = pymysql.connect(host=constants.HOST,
                                     port=constants.PORT,
                                     user=self.credentials["database_username"],
                                     password=self.credentials["database_password"],
                                     db=constants.DATABASE_NAME)
        connection.autocommit(True)
        failed_files = []
        for file in files:
            if (file.document_type == "Opkomst"):
                try:
                    with connection.cursor() as cursor:
                        query = "REPLACE INTO opkomst_documents(document_id, title, authors, date, file_path, template_version, uploader_name, speltakken, category, description, materials, searchwords) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(query,  (file.storage_id,
                                                file.titel,
                                                "\n".join(file.auteurs),
                                                file.datum,
                                                file.file_path,
                                                file.template_version,
                                                file.uploader_name,
                                                "\n".join(file.speltakken),
                                                file.categorie,
                                                file.omschrijving,
                                                "\n".join(file.materiaal),
                                                "\n".join(file.zoekwoorden)))
                except Exception as e:
                    log.debug(e)
                    failed_files.append(file)

        connection.close()
        return failed_files
