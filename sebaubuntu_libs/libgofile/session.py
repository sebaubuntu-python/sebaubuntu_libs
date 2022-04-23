#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#

from sebaubuntu_libs.libgofile.utils import get_account, get_content

class Session:
	def __init__(self, token: str):
		self.token = token

		self.account = get_account(token)

	def get_root_content(self):
		return get_content(self.account.root_folder, self.token)

	def get_content(self, content_id: str):
		return get_content(content_id, self.token)
