#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#

from datetime import datetime
from io import BytesIO
from pathlib import Path
from sebaubuntu_libs.libgofile import raw_api
from sebaubuntu_libs.libgofile.account import Account
from sebaubuntu_libs.libgofile.contents import ContentResponse, Folder
from sebaubuntu_libs.libtyping import is_iterable_and_not_str
from typing import Iterable, Union

def get_server() -> str:
	"""Returns the best server available to receive files."""
	return raw_api.get_server()["server"]

def upload_file(file: Union[str, Path, BytesIO], server: str = None, token: str = None,
				folder_id: str = None, description: str = None, password: str = None,
				tags: Union[str, Iterable[str]] = None, expire: datetime = None):
	"""Upload one file on a specific server."""
	if server is None:
		server = get_server()

	needs_open = not isinstance(file, BytesIO)

	if is_iterable_and_not_str(tags):
		tags = ",".join(tags)

	if needs_open:
		with open(file, "rb") as f:
			data = raw_api.upload_file(f, server, token, folder_id, description, password, tags, expire)
	else:
		data = raw_api.upload_file(file, server, token, folder_id, description, password, tags, expire)

	return data

def get_content(content_id: str, token: str):
	"""Get a specific content details."""
	data = raw_api.get_content(content_id, token)

	return ContentResponse.from_dict(data)

def create_folder(parent_folder_id: str, folder_name: str, token: str):
	"""Create a new folder."""
	data = raw_api.create_folder(parent_folder_id, folder_name, token)

	return Folder.from_dict(data)

def set_folder_option(token: str, folder_id: str, option: str, value: str):
	"""Set an option on a folder."""
	raw_api.set_folder_option(token, folder_id, option, value)

	return True

def copy_content(contents_id: Union[str, Iterable[str]], folder_id_dest: str, token: str):
	"""Copy one or multiple contents to another folder."""
	if is_iterable_and_not_str(contents_id):
		contents_id = ",".join(contents_id)

	raw_api.copy_content(contents_id, folder_id_dest, token)

	return True

def delete_content(contents_id: Union[str, Iterable[str]], token: str):
	"""Delete one or multiple files/folders."""
	if is_iterable_and_not_str(contents_id):
		contents_id = ",".join(contents_id)

	raw_api.delete_content(contents_id, token)

	return True

def get_account(token: str):
	"""Get the account details."""
	# As of now toggling all_details does nothing
	data = raw_api.get_account_details(token, True)

	return Account.from_dict(data)
