#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

#logging.disable(logging.INFO)

from pathlib import Path
import configparser
import documentSorter

class MainModel():

    default_config_path = Path(".").resolve().joinpath("default_config.ini")
    personal_config_path = Path().home().joinpath("ScoutingOpkomstenDatabaseApp", "personal_config.ini")
    config = configparser.RawConfigParser()

    def __init__(self):
        self.innit_config()

    def innit_config(self):
        log.info("Personal configpath is {}".format(self.personal_config_path))
        if self.personal_config_path.exists() == False:
            log.warning("personal_config.ini is missing!")
            self.personal_config_path.parent.mkdir(exist_ok=True)
            if self.default_config_path.exists() == False:
                log.error("default_config.ini is missing!")
                raise Exception("config files missing!")
            else:
                self.config.read(str(self.default_config_path))
                with open(str(self.personal_config_path), "w") as configfile:
                    self.config.write(configfile)
        else:
            self.config.read(str(self.personal_config_path))
            default_config = configparser.RawConfigParser()
            default_config.read(str(self.default_config_path))
            if int(default_config["Main"]["version"]) > int(self.config["Main"]["version"]):
                with open(str(self.personal_config_path), "w") as configfile:
                    default_config.write(configfile)
                log.info("Configfile updated to newer version")
        self.ReadConfig()

    def ReadConfig(self):
        print("ReadConfig")

    def SortDocuments(self, input_path, output_path):
        categories = self.config["Sorting"]["categories"].split(";")
        forbidden_chars = self.config["Sorting"]["forbidden_characters"]
        delete_input = self.config["Sorting"].getboolean("delete_input")

        documentSorter.sort(input_path, output_path, categories, forbidden_chars, delete_input)

if __name__ == "__main__":
    model = MainModel()

    input = Path(".").resolve().parent.joinpath("Test_Input")
    output = Path(".").resolve().parent.joinpath("Test_Output")
    model.SortDocuments(input, output)
    print("Done!")
