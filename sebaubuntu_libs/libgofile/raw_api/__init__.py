#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#

from datetime import datetime
from io import BytesIO
from sebaubuntu_libs.libgofile import DOMAIN
from sebaubuntu_libs.libgofile.raw_api.rest import GoFileRequests

__all__ = [
	'get_server',
	'upload_file',
	'get_content',
	'create_folder',
	'set_folder_option',
	'copy_content',
	'delete_content',
	'get_account_details',
]

API_URL = f"https://api.{DOMAIN}"

def get_server() -> str:
	"""Returns the best server available to receive files."""
	return GoFileRequests.get(f"{API_URL}/getServer")

def upload_file(server: str, file: BytesIO, token: str = None, folder_id: str = None,
                description: str = None, password: str = None, tags: str = None,
                expire: datetime = None):
	"""Upload one file on a specific server."""
	params = {}
	if token is not None:
		params["token"] = token
	if folder_id is not None:
		params["folderId"] = folder_id
	if description is not None:
		params["description"] = description
	if password is not None:
		params["password"] = password
	if tags is not None:
		params["tags"] = tags
	if expire is not None:
		params["expire"] = expire.timestamp()

	files = {"file": file}

	return GoFileRequests.post(f"{server}.{DOMAIN}/uploadFile", params=params, files=files)

def get_content(content_id: str, token: str):
	"""Get a specific content details."""
	params = {
		"contentId": content_id,
		"token": token,
	}

	return GoFileRequests.get(f"{API_URL}/getContent", params=params)

def create_folder(parent_folder_id: str, folder_name: str, token: str):
	"""Create a new folder."""
	data = {
		"parentFolderId": parent_folder_id,
		"folderName": folder_name,
		"token": token,
	}

	return GoFileRequests.put(f"{API_URL}/createFolder", data=data)

def set_folder_option(token: str, folder_id: str, option: str, value: str):
	"""Set an option on a folder."""
	data = {
		"token": token,
		"folderId": folder_id,
		"option": option,
		"value": value,
	}

	return GoFileRequests.put(f"{API_URL}/setFolderOption", data=data)

def copy_content(contents_id: str, folder_id_dest: str, token: str):
	"""Copy one or multiple contents to another folder."""
	data = {
		"contentsId": contents_id,
		"folderIdDest": folder_id_dest,
		"token": token,
	}

	return GoFileRequests.put(f"{API_URL}/copyContent", data=data)

def delete_content(contents_id: str, token: str):
	"""Delete one or multiple files/folders."""
	params = {
		"contentsId": contents_id,
		"token": token,
	}

	return GoFileRequests.delete(f"{API_URL}/deleteContent", params=params)

def get_account_details(token: str, all_details: bool = False):
	"""Get the account details."""
	params = {
		"token": token,
	}
	if all_details:
		params["allDetails"] = "true"

	return GoFileRequests.get(f"{API_URL}/getAccountDetails", params=params)

# Undocumented APIs

def get_geo():
    """Get the client geolocation."""
    return GoFileRequests.get(f"{API_URL}/getGeo")
