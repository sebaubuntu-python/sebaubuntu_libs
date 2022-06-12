#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#

from typing import Dict


class Account:
	def __init__(self,
	             token: str,
				 email: str,
				 tier: str,
				 root_folder: str,
				 files_count: int,
				 files_count_limit: int,
				 total_size: int,
				 total_size_limit: int,
				 total_30ddl_traffic: int,
				 total_30ddl_traffic_limit: int,
	            ):
		self.token = token
		self.email = email
		self.tier = tier
		self.root_folder = root_folder
		self.files_count = files_count
		self.files_count_limit = files_count_limit
		self.total_size = total_size
		self.total_size_limit = total_size_limit
		self.total_30ddl_traffic = total_30ddl_traffic
		self.total_30ddl_traffic_limit = total_30ddl_traffic_limit

	@staticmethod
	def from_dict(data: Dict):
		return Account(token=data["token"], email=data["email"],
		               tier=data["tier"], root_folder=data["rootFolder"],
		               files_count=data["filesCount"], files_count_limit=data["filesCountLimit"],
		               total_size=data["totalSize"], total_size_limit=data["totalSizeLimit"],
		               total_30ddl_traffic=data["total30DDLTraffic"],
		               total_30ddl_traffic_limit=data["total30DDLTrafficLimit"])
