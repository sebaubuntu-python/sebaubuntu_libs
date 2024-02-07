#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#

from __future__ import annotations
from pathlib import Path
from typing import List, Optional

from sebaubuntu_libs.libandroid.fstab import Fstab, FstabEntry
from sebaubuntu_libs.libandroid.partitions.partition_model import PartitionModel
from sebaubuntu_libs.libandroid.props import BuildProp
from sebaubuntu_libs.libandroid.vintf.manifest import Manifest
from sebaubuntu_libs.libreorder import strcoll_files_key

BUILD_PROP_LOCATION = ["build.prop", "etc/build.prop"]
DEFAULT_PROP_LOCATION = ["default.prop", "etc/default.prop"]

MANIFEST_LOCATION = ["manifest.xml", "etc/vintf/manifest.xml"]

def get_files_list(path: Path) -> List[Path]:
	files = []

	for i in path.iterdir():
		if i.is_file():
			files.append(i)
		elif i.is_dir():
			files.extend(get_files_list(i))

	return files

class AndroidPartition:
	def __init__(self, model: PartitionModel, path: Path):
		self.model = model
		self.path = path

		self.files = get_files_list(self.path)

		self.fstab_entry: Optional[FstabEntry] = None

		self.build_prop = BuildProp()
		for possible_paths in BUILD_PROP_LOCATION + DEFAULT_PROP_LOCATION:
			build_prop_path = self.path / possible_paths
			if not build_prop_path.is_file():
				continue

			self.build_prop.import_props(build_prop_path)

		self.manifest = Manifest()
		for possible_paths in MANIFEST_LOCATION:
			manifest_path = self.path / possible_paths
			if not manifest_path.is_file():
				continue

			self.manifest.import_file(manifest_path)

	def fill_fstab_entry(self, fstab: Fstab):
		for mount_point in self.model.mount_points:
			self.fstab_entry = fstab.get_partition_by_mount_point(mount_point)
			if self.fstab_entry is not None:
				return

	def get_files(self):
		"""Returns the ordered list of files."""
		self.files.sort(key=strcoll_files_key)
		return self.files

	def get_formatted_file(self, file: Path):
		return self.model.proprietary_files_prefix / file.relative_to(self.path)

	def get_formatted_files(self):
		return [self.get_formatted_file(file) for file in self.get_files()]
