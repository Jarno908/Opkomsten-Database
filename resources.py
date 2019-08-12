#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from pathlib2 import Path
import sys

def ResourcePath(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr( sys, 'frozen', False ) :
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(str(sys._MEIPASS)).resolve()
    else:
        base_path = Path(".").resolve()

    log.debug("base_path= {}".format(base_path))
    return str(base_path.joinpath(relative_path))