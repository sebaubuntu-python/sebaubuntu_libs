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


class PartitionModel:
    ALL: List["PartitionModel"] = []

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

        PartitionModel.ALL.append(self)


class PartitionModels:
    # system/core/fastboot/fastboot.cpp

    BOOT = PartitionModel("boot", PartitionGroup.BOOTLOADER)
    DTBO = PartitionModel("dtbo", PartitionGroup.BOOTLOADER)
    RECOVERY = PartitionModel("recovery", PartitionGroup.BOOTLOADER)
    MISC = PartitionModel("misc", PartitionGroup.BOOTLOADER)
    VBMETA = PartitionModel("vbmeta", PartitionGroup.BOOTLOADER)
    VBMETA_SYSTEM = PartitionModel("vbmeta_system", PartitionGroup.BOOTLOADER)
    VBMETA_VENDOR = PartitionModel("vbmeta_vendor", PartitionGroup.BOOTLOADER)
    VENDOR_BOOT = PartitionModel("vendor_boot", PartitionGroup.BOOTLOADER)
    VENDOR_KERNEL_BOOT = PartitionModel("vendor_kernel_boot", PartitionGroup.BOOTLOADER)
    INIT_BOOT = PartitionModel("init_boot", PartitionGroup.BOOTLOADER)

    SYSTEM = PartitionModel("system", PartitionGroup.SSI, ["/system", "/"], Path(""))
    PRODUCT = PartitionModel("product", PartitionGroup.SSI)
    SYSTEM_EXT = PartitionModel("system_ext", PartitionGroup.SSI)
    SYSTEM_DLKM = PartitionModel("system_dlkm", PartitionGroup.SSI)

    VENDOR = PartitionModel("vendor", PartitionGroup.TREBLE)
    ODM = PartitionModel("odm", PartitionGroup.TREBLE)
    ODM_DLKM = PartitionModel("odm_dlkm", PartitionGroup.TREBLE)
    VENDOR_DLKM = PartitionModel("vendor_dlkm", PartitionGroup.TREBLE)

    USERDATA = PartitionModel("data", PartitionGroup.DATA)
    CACHE = PartitionModel("cache", PartitionGroup.DATA)
    METADATA = PartitionModel("metadata", PartitionGroup.DATA)

    @classmethod
    def from_name(cls, name: str):
        for model in PartitionModel.ALL:
            if model.name == name:
                return model

        return None

    @classmethod
    def from_group(cls, group: PartitionGroup):
        return [model for model in PartitionModel.ALL if model.group == group]

    @classmethod
    def from_mount_point(cls, mount_point: str):
        for model in PartitionModel.ALL:
            if mount_point in model.mount_points:
                return model

        return None
