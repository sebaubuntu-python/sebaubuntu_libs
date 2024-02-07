#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#

from enum import IntEnum
from pathlib import Path
from typing import List, Optional

class PartitionGroup(IntEnum):
	BOOTLOADER = 0
	SSI = 1
	TREBLE = 2
	DATA = 3

(
	BOOTLOADER,
	SSI,
	TREBLE,
	DATA,
) = PartitionGroup.__members__.values()

class _PartitionModel:
	ALL: List["_PartitionModel"] = []

	def __init__(
		self,
		name: str,
		group: PartitionGroup,
		mount_points: Optional[List[str]] = None,
		proprietary_files_prefix: Optional[Path] = None,
	):
		self.name = name
		self.group = group
		self.mount_points = mount_points or [f"/{self.name}"]
		self.proprietary_files_prefix = proprietary_files_prefix or Path(self.name)

		_PartitionModel.ALL.append(self)

	@classmethod
	def from_name(cls, name: str):
		for model in cls.ALL:
			if model.name == name:
				return model

		return None

	@classmethod
	def from_group(cls, group: PartitionGroup):
		return [model for model in cls.ALL if model.group == group]

	@classmethod
	def from_mount_point(cls, mount_point: str):
		for model in cls.ALL:
			if mount_point in model.mount_points:
				return model

		return None

class PartitionModel(_PartitionModel):
	# system/core/fastboot/fastboot.cpp

	BOOT = _PartitionModel("boot", BOOTLOADER)
	DTBO = _PartitionModel("dtbo", BOOTLOADER)
	RECOVERY = _PartitionModel("recovery", BOOTLOADER)
	MISC = _PartitionModel("misc", BOOTLOADER)
	VBMETA = _PartitionModel("vbmeta", BOOTLOADER)
	VBMETA_SYSTEM = _PartitionModel("vbmeta_system", BOOTLOADER)
	VBMETA_VENDOR = _PartitionModel("vbmeta_vendor", BOOTLOADER)
	VENDOR_BOOT = _PartitionModel("vendor_boot", BOOTLOADER)
	VENDOR_KERNEL_BOOT = _PartitionModel("vendor_kernel_boot", BOOTLOADER)
	INIT_BOOT = _PartitionModel("init_boot", BOOTLOADER)

	SYSTEM = _PartitionModel("system", SSI, ["/system", "/"], Path(""))
	PRODUCT = _PartitionModel("product", SSI)
	SYSTEM_EXT = _PartitionModel("system_ext", SSI)
	SYSTEM_DLKM = _PartitionModel("system_dlkm", SSI)

	VENDOR = _PartitionModel("vendor", TREBLE)
	ODM = _PartitionModel("odm", TREBLE)
	ODM_DLKM = _PartitionModel("odm_dlkm", TREBLE)
	VENDOR_DLKM = _PartitionModel("vendor_dlkm", TREBLE)

	USERDATA = _PartitionModel("data", DATA)
	CACHE = _PartitionModel("cache", DATA)
	METADATA = _PartitionModel("metadata", DATA)
