#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#

from datetime import datetime
import requests

API_VERSION = "v1"
API_URL = f"https://download.lineageos.org/api/{API_VERSION}"

class FullUpdateInfo:
	"""LineageOS full update information.

	Attributes:
	- datetime (datetime): The date and time of the update
	- filename (str): The filename of the update
	- id (str): The ID of the update
	- romtype (str): The ROM type of the update
	- size (int): The size of the update (bytes)
	- url (str): The URL of the update
	- version (str): The LineageOS version of the update (e.g. 18.1)
	"""
	def __init__(self,
		         datetime: datetime,
		         filename: str,
				 id: str,
				 romtype: str,
				 size: int,
				 url: str,
				 version: str,
		        ):
		"""Initialize the full update information."""
		self.datetime = datetime
		self.filename = filename
		self.id = id
		self.romtype = romtype
		self.size = size
		self.url = url
		self.version = version

	@classmethod
	def from_json(self, update: dict):
		"""Create a full update information object from a JSON object."""
		return self(datetime.fromtimestamp(update["datetime"]), update["filename"],
		            update["id"], update["romtype"],
		            update["size"], update["url"], update["version"])

def get_nightlies(device: str):
	"""Get the latest OTAs for a device."""
	url = f"{API_URL}/{device}/nightly/1"
	response = requests.get(url=url).json()["response"]
	updates = [FullUpdateInfo.from_json(update) for update in response]

	return updates
