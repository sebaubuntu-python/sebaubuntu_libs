#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#

from __future__ import annotations
from pathlib import Path
from typing import List

(
	BOOTLOADER,
	SSI,
	TREBLE,
	DATA,
) = range(4)

class _PartitionModel:
	ALL: List[_PartitionModel] = []

	def __init__(self,
	             name: str,
	             group: int,
				 mount_points: List[str] = None,
				 proprietary_files_prefix: Path = None,
	            ):
		self.name = name
		self.group = group
		self.mount_points = mount_points
		self.proprietary_files_prefix = proprietary_files_prefix

		if self.mount_points is None:
			self.mount_points = [f"/{self.name}"]

		if self.proprietary_files_prefix is None:
			self.proprietary_files_prefix = Path(self.name)

		_PartitionModel.ALL.append(self)

	@classmethod
	def from_name(cls, name: str):
		for model in cls.ALL:
			if model.name == name:
				return model

		return None

	@classmethod
	def from_group(cls, group: int):
		return [model for model in cls.ALL if model.group == group]

	@classmethod
	def from_mount_point(cls, mount_point: str):
		for model in cls.ALL:
			if mount_point in model.mount_points:
				return model

		return None

class PartitionModel(_PartitionModel):
	BOOT = _PartitionModel("boot", BOOTLOADER)
	DTBO = _PartitionModel("dtbo", BOOTLOADER)
	RECOVERY = _PartitionModel("recovery", BOOTLOADER)
	MISC = _PartitionModel("misc", BOOTLOADER)
	VBMETA = _PartitionModel("vbmeta", BOOTLOADER)
	VBMETA_SYSTEM = _PartitionModel("vbmeta_system", BOOTLOADER)
	VBMETA_VENDOR = _PartitionModel("vbmeta_vendor", BOOTLOADER)

	SYSTEM = _PartitionModel("system", SSI, ["/system", "/"], Path(""))
	PRODUCT = _PartitionModel("product", SSI)
	SYSTEM_EXT = _PartitionModel("system_ext", SSI)

	VENDOR = _PartitionModel("vendor", TREBLE)
	ODM = _PartitionModel("odm", TREBLE)
	ODM_DLKM = _PartitionModel("odm_dlkm", TREBLE)
	VENDOR_DLKM = _PartitionModel("vendor_dlkm", TREBLE)

	USERDATA = _PartitionModel("data", DATA)
	CACHE = _PartitionModel("cache", DATA)
	METADATA = _PartitionModel("metadata", DATA)
