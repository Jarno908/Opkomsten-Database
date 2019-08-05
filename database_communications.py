#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

import pymysql.cursors
import constants
from opkomst_module import Opkomst

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

    def get_opkomsten(self, search_info):
        connection = pymysql.connect(host=constants.HOST,
                                     port=constants.PORT,
                                     user=self.credentials["database_username"],
                                     password=self.credentials["database_password"],
                                     db=constants.DATABASE_NAME)

        query = "SELECT * FROM opkomst_documents"

        search_parts = []
        search_values = []
        for key, value in search_info.items():
            if (value == "") or (value == "Alle"):
                continue
            elif key == "search_string":
                search_parts.append("(title LIKE CONCAT('%%', %s, '%%') OR description LIKE CONCAT('%%', %s, '%%') OR materials LIKE CONCAT('%%', %s, '%%') OR searchwords LIKE CONCAT('%%', %s, '%%'))")
                for i in range(4):
                    search_values.append(value)
            elif key == "speltakken":
                search_parts.append("speltakken LIKE CONCAT('%%', %s, '%%')")
                search_values.append(value)
            else:
                search_parts.append("{} = %s".format(key))
                search_values.append(value)

        if len(search_parts) > 0:
            query = query + " WHERE " + " AND ".join(search_parts)

        log.debug("Now retrieving with query: \n{}".format(query))

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, search_values)
            database_result = cursor.fetchall()

            result = []
            for item in database_result:
                item_info = {
                "storage_id":item[0],
                "Titel":item[1],
                "Auteur":item[2],
                "Datum":item[3],
                "filepath":item[4],
                "version":item[5],
                "Uploader_Name":item[6],
                "Speltak(ken)":item[7].lower(),
                "Categorie":item[8].lower(),
                "Omschrijving":item[9],
                "Materiaal":item[10],
                "Zoekwoorden":item[11]
                }
                result.append(Opkomst(item_info, True))

        except Exception as e:
            log.debug(e)

        finally:
            connection.close()

        return result
