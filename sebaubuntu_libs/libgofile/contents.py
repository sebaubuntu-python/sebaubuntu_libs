#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#

from datetime import datetime
from typing import Dict, List

class Content:
	def __init__(self,
	             content_id: str,
				 content_type: str,
				 name: str,
				 parent_folder: str,
				 create_time: datetime,
				):
		"""Initialize a GoFile content."""
		self.content_id = content_id
		self.content_type = content_type
		self.name = name
		self.parent_folder = parent_folder
		self.create_time = create_time

	def get_kwargs(self):
		return {
			"content_id": self.content_id,
			"content_type": self.content_type,
			"name": self.name,
			"parent_folder": self.parent_folder,
			"create_time": self.create_time,
		}

	@staticmethod
	def from_dict(data: Dict):
		create_time = datetime.fromtimestamp(data["createTime"])

		return Content(content_id=data["id"], content_type=data["type"], name=data["name"],
		               parent_folder=data["parentFolder"], create_time=create_time)

class File(Content):
	"""Class representing a GoFile file."""
	def __init__(self,
	             size: int,
	             download_count: int,
				 md5: str,
				 mimetype: str,
				 server_choosen: str,
				 direct_link: str,
				 link: str,
				 *args, **kwargs,
	            ):
		"""Initialize a GoFile file."""
		super().__init__(*args, **kwargs)

		self.size = size
		self.download_count = download_count
		self.md5 = md5
		self.mimetype = mimetype
		self.server_choosen = server_choosen
		self.direct_link = direct_link
		self.link = link

	def get_kwargs(self):
		kwargs = super().get_kwargs()

		kwargs["size"] = self.size
		kwargs["download_count"] = self.download_count
		kwargs["md5"] = self.md5
		kwargs["mimetype"] = self.mimetype
		kwargs["server_choosen"] = self.server_choosen
		kwargs["direct_link"] = self.direct_link
		kwargs["link"] = self.link

		return kwargs

	@staticmethod
	def from_dict(data: Dict):
		content = Content.from_dict(data)

		return File(size=data["size"], download_count=data["downloadCount"], md5=data["md5"],
		            mimetype=data["mimetype"], server_choosen=data["serverChoosen"],
					direct_link=data["directLink"], link=data["link"],
					**content.get_kwargs())

class Folder(Content):
	"""Class representing a GoFile folder."""
	def __init__(self,
				 childs: List[str],
				 code: str,
				 public: bool,
				 *args, **kwargs,
				):
		"""Initialize a GoFile folder."""
		super().__init__(*args, **kwargs)

		self.childs = childs
		self.code = code
		self.public = public

	def get_kwargs(self):
		kwargs = super().get_kwargs()

		kwargs["childs"] = self.childs
		kwargs["code"] = self.code
		kwargs["public"] = self.public

		return kwargs

	@staticmethod
	def from_dict(data: Dict):
		content = Content.from_dict(data)

		public = data.get("public")

		return Folder(childs=data["childs"], code=data["code"], public=public,
					  **content.get_kwargs())

class ContentResponse(Folder):
	"""Class representing a GoFile content response.

	As of now all contents returned by get_content are folders."""
	def __init__(self,
				 total_download_count: int,
				 total_size: int,
				 contents: Dict[str, Dict],
				 # We may not know the owner ID if the owner isn't the one who called get_content
				 owner_id: str = None,
				 # Only for non-root folders
				 parent_folder: str = None,
				 # Only for root folders
				 is_root: bool = False,
				 *args, **kwargs,
				):
		"""Initialize a GoFile content."""
		super().__init__(*args, **kwargs)

		self.total_download_count = total_download_count
		self.total_size = total_size
		self.contents = contents
		self.owner_id = owner_id
		self.parent_folder = parent_folder
		self.is_root = is_root

	@staticmethod
	def from_dict(data: Dict):
		folder = Folder.from_dict(data)

		owner_id = data.get("ownerId")
		parent_folder = data.get("parentFolder")
		is_root = data.get("isRoot", False)

		return ContentResponse(total_download_count=data["totalDownloadCount"],
		                       total_size=data["totalSize"], contents=data["contents"],
							   owner_id=owner_id, parent_folder=parent_folder,
							   is_root=is_root,
							   **folder.get_kwargs())
