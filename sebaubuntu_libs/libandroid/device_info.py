#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#

from distutils.util import strtobool
from enum import Enum
from typing import Any, Callable, List

from sebaubuntu_libs.libandroid.props import BuildProp
from sebaubuntu_libs.libandroid.props.utils import fingerprint_to_description, get_partition_props

def get_product_props(value: str):
	return get_partition_props("ro.product.{}" + value, add_empty=True)

DEVICE_CODENAME = get_product_props("device")
DEVICE_MANUFACTURER = get_product_props("manufacturer")
DEVICE_BRAND = get_product_props("brand")
DEVICE_MODEL = get_product_props("model")

DEVICE_ARCH = ["ro.bionic.arch"]
DEVICE_CPU_ABILIST = get_partition_props("ro.{}product.cpu.abilist", add_empty=True)
DEVICE_CPU_VARIANT = ["ro.bionic.cpu_variant"]
DEVICE_SECOND_ARCH = ["ro.bionic.2nd_arch"]
DEVICE_SECOND_CPU_VARIANT = ["ro.bionic.2nd_cpu_variant"]

DEVICE_IS_AB = ["ro.build.ab_update"]
DEVICE_USES_DYNAMIC_PARTITIONS = ["ro.boot.dynamic_partitions"]
DEVICE_USES_VIRTUAL_AB = ["ro.virtual_ab.enabled"]
DEVICE_USES_SYSTEM_AS_ROOT = ["ro.build.system_root_image"]

BOOTLOADER_BOARD_NAME = ["ro.product.board"]
DEVICE_PLATFORM = ["ro.board.platform"]
DEVICE_PIXEL_FORMAT = ["ro.minui.pixel_format"]
SCREEN_DENSITY = ["ro.sf.lcd_density"]
USE_VULKAN = ["ro.hwui.use_vulkan"]

BUILD_FINGERPRINT = get_partition_props("ro.{}build.fingerprint", add_empty=True)
BUILD_DESCRIPTION = get_partition_props("ro.{}build.description", add_empty=True)

GMS_CLIENTID_BASE = ["ro.com.google.clientidbase.ms", "ro.com.google.clientidbase"]

BUILD_SECURITY_PATCH = ["ro.build.version.security_patch"]
BUILD_VENDOR_SECURITY_PATCH = ["ro.vendor.build.security_patch"]

FIRST_API_LEVEL = ["ro.product.first_api_level"]
PRODUCT_CHARACTERISTICS = ["ro.build.characteristics"]
APEX_UPDATABLE = ["ro.apex.updatable"]

class DeviceArch(Enum):
	def __new__(cls, *args, **kwargs):
		value = len(cls.__members__) + 1
		obj = object.__new__(cls)
		obj._value_ = value
		return obj

	def __init__(self,
	             arch: str,
	             arch_variant: str,
	             bitness: int,
	             cpu_abilist: List[str],
	            ):
		self.arch = arch
		self.arch_variant = arch_variant
		self.bitness = bitness
		self.cpu_abilist = cpu_abilist

		self.cpu_abi = self.cpu_abilist[0]
		self.cpu_abi2 = self.cpu_abilist[1] if len(self.cpu_abilist) > 1 else ""

	def __bool__(self):
		return self.arch != "unknown"

	def __str__(self):
		return self.arch

	@classmethod
	def from_arch(cls, arch: str):
		for arch_enum in cls:
			if arch_enum.arch != arch:
				continue

			return arch_enum

		raise ValueError(f"Unknown arch: {arch}")

	@classmethod
	def from_abi(cls, abi: str):
		for arch_enum in cls:
			if abi not in arch_enum.cpu_abilist:
				continue

			return arch_enum

		raise ValueError(f"Unknown ABI: {abi}")

	ARM = ("arm", "armv7-a-neon", 32, ["armeabi-v7a", "armeabi"])
	ARM64 = ("arm64", "armv8-a", 64, ["arm64-v8a"])
	X86 = ("x86", "generic", 32, ["x86"])
	X86_64 = ("x86_64", "generic", 64, ["x86_64"])

bool_cast = lambda x: bool(strtobool(x))

class DeviceInfo:
	"""
	This class is responsible for reading parse common build props by using BuildProp class.
	"""

	def __init__(self, build_prop: BuildProp):
		"""
		Parse common build props.
		"""
		self.build_prop = build_prop

		# Parse props
		self.codename = self.get_first_prop(DEVICE_CODENAME)
		self.manufacturer = self.get_first_prop(DEVICE_MANUFACTURER).split()[0].lower()
		self.brand = self.get_first_prop(DEVICE_BRAND, raise_exception=False)
		self.model = self.get_first_prop(DEVICE_MODEL, raise_exception=False)
		self.build_fingerprint = self.get_first_prop(BUILD_FINGERPRINT)
		self.build_description = self.get_first_prop(BUILD_DESCRIPTION, default=fingerprint_to_description(self.build_fingerprint))

		# Parse arch
		self.arch = None
		self.second_arch = None

		arch_prop = self.get_first_prop(DEVICE_ARCH, raise_exception=False)
		second_arch_prop = self.get_first_prop(DEVICE_SECOND_ARCH, raise_exception=False)
		if arch_prop:
			self.arch = DeviceArch.from_arch(arch_prop)
			if second_arch_prop:
				self.second_arch = DeviceArch.from_arch(second_arch_prop)
		else:
			# Fallback to ABI list
			abi_list = self.get_first_prop(DEVICE_CPU_ABILIST).split(",")
			assert abi_list, "No ABI list prop found"
			archs = list(set([DeviceArch.from_abi(abi) for abi in abi_list]))
			assert 0 < len(archs) <= 2, "Invalid ABI list"
			# Higher bitness architectures has priority
			archs.sort(key=lambda x: x.bitness, reverse=True)
			self.arch = archs[0]
			if len(archs) > 1:
				self.second_arch = archs[1]

		self.cpu_variant = self.get_first_prop(DEVICE_CPU_VARIANT, default="generic")
		self.second_cpu_variant = self.get_first_prop(DEVICE_SECOND_CPU_VARIANT, default="generic")

		self.bootloader_board_name = self.get_first_prop(BOOTLOADER_BOARD_NAME)
		self.platform = self.get_first_prop(DEVICE_PLATFORM, default="default")
		self.device_is_ab = self.get_first_prop(DEVICE_IS_AB, data_type=bool_cast, default=False)
		self.device_uses_dynamic_partitions = self.get_first_prop(DEVICE_USES_DYNAMIC_PARTITIONS, data_type=bool_cast, default=False)
		self.device_uses_virtual_ab = self.get_first_prop(DEVICE_USES_VIRTUAL_AB, data_type=bool_cast, default=False)
		self.device_uses_system_as_root = self.get_first_prop(DEVICE_USES_SYSTEM_AS_ROOT, data_type=bool_cast, default=False)
		self.device_uses_updatable_apex = self.get_first_prop(APEX_UPDATABLE, data_type=bool_cast, default=False)

		self.device_pixel_format = self.get_first_prop(DEVICE_PIXEL_FORMAT, raise_exception=False)
		self.screen_density = self.get_first_prop(SCREEN_DENSITY, raise_exception=False)
		self.use_vulkan = self.get_first_prop(USE_VULKAN, data_type=bool_cast, default=False)
		self.gms_clientid_base = self.get_first_prop(GMS_CLIENTID_BASE, default=f"android-{self.manufacturer}")
		self.first_api_level = self.get_first_prop(FIRST_API_LEVEL)
		self.product_characteristics = self.get_first_prop(PRODUCT_CHARACTERISTICS)

		self.build_security_patch = self.get_first_prop(BUILD_SECURITY_PATCH)
		self.vendor_build_security_patch = self.get_first_prop(BUILD_VENDOR_SECURITY_PATCH, default=self.build_security_patch)

	def get_first_prop(self, props: List[str], data_type: Callable[[str], Any] = str,
	                   default: Any = None, raise_exception: bool = True):
		for prop in props:
			prop_value = self.build_prop._get_prop(prop, data_type)
			if prop_value is None:
				continue

			return prop_value

		if default is None and raise_exception:
			raise AssertionError(f'Property {props[0]} could not be found in build.prop')
		else:
			return default
