#! Python3
import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from github import Github
from datetime import datetime

def check_new_version(old_version_string):

	old_version_date = datetime.strptime(old_version_string, "%Y-%m-%d %H:%M:%S")

	repo_url = "Jarno908/Opkomsten-Database"
	g = Github()

	release = g.get_repo(repo_url).get_latest_release()

	download_url = release.html_url
	for asset in release.get_assets():
		if asset.content_type == "application/x-msdownload":
			download_url = asset.browser_download_url
			break

	if release.published_at > old_version_date:
		return [True, {"title" : release.title, "date" : release.published_at, "html_url" : download_url}]
	else:
		return [False, {"title" : release.title, "date" : release.published_at, "html_url" : download_url}]
