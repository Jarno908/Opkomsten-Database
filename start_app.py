#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from main_controller import main
from pyupdater.client import Client
from client_config import ClientConfig
from s3_uploader import S3Uploader
import sys
import constants
import threading

def log_status_info(info):
    total = info.get(u'total')
    downloaded = info.get(u'downloaded')
    status = info.get(u'status')
    log.debug(downloaded, total, status)

def update_check():
	log.debug("Start update_check:")
	client = Client(ClientConfig())
	client.refresh()
	client.add_progress_hook(log_status_info)

	app_update = client.update_check(constants.APP_NAME, constants.APP_VERSION)

	if app_update != None:
		app_update.download()

		if app_update.is_downloaded():
			app_update.extract_restart()

	return

if __name__ == '__main__':

	if getattr( sys, 'frozen', False ):
		update_thread = threading.Thread(target=update_check)
		update_thread.start()
	
	main()
