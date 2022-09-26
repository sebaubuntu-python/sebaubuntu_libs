#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#

from __future__ import annotations
from pathlib import Path
from typing import List

from sebaubuntu_libs.libandroid.fstab import Fstab, FstabEntry
from sebaubuntu_libs.libandroid.partitions.partition_model import PartitionModel
from sebaubuntu_libs.libandroid.props import BuildProp
from sebaubuntu_libs.libandroid.vintf.manifest import Manifest
from sebaubuntu_libs.libpath import is_relative_to
from sebaubuntu_libs.libreorder import strcoll_files_key

BUILD_PROP_LOCATION = ["build.prop", "etc/build.prop"]
DEFAULT_PROP_LOCATION = ["default.prop", "etc/default.prop"]

def get_dir(path: Path):
	dir = {}
	for i in path.iterdir():
		dir[i.name] = i if i.is_file() else get_dir(i)
	return dir

class AndroidPartition:
	def __init__(self, model: PartitionModel, real_path: Path, dump_path: Path):
		self.model = model
		self.real_path = real_path
		self.dump_path = dump_path

		self.files: List[Path] = []
		self.fstab_entry: FstabEntry = None

		self.build_prop = BuildProp()
		for possible_paths in BUILD_PROP_LOCATION + DEFAULT_PROP_LOCATION:
			build_prop_path = self.real_path / possible_paths
			if not build_prop_path.is_file():
				continue

			self.build_prop.import_props(build_prop_path)

		self.manifest = Manifest()
		for possible_paths in ["etc/vintf/manifest.xml", "manifest.xml"]:
			manifest_path = self.real_path / possible_paths
			if not manifest_path.is_file():
				continue

			self.manifest.import_file(manifest_path)

	def get_relative_path(self):
		return self.real_path.relative_to(self.dump_path)

	def fill_files(self, files: List[Path]):
		for file in files:
			if not is_relative_to(file, self.real_path):
				continue

			self.files.append(file)

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
		return self.model.proprietary_files_prefix / file.relative_to(self.real_path)

	def get_formatted_files(self):
		return [self.get_formatted_file(file) for file in self.get_files()]
