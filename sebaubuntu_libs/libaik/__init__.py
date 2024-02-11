#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#
"""AIK wrapper library."""

from git import Repo
from pathlib import Path
from platform import system
from sebaubuntu_libs.liblogging import LOGI
from shutil import which
from subprocess import check_output, STDOUT, CalledProcessError
from tempfile import TemporaryDirectory
from typing import Optional

AIK_REPO = "https://github.com/SebaUbuntu/AIK-Linux-mirror"

ALLOWED_OS = [
	"Linux",
	"Darwin",
]

class AIKImageInfo:
	def __init__(
		self,
		base_address: Optional[str],
		board_name: Optional[str],
		cmdline: Optional[str],
		dt: Optional[Path],
		dtb: Optional[Path],
		dtb_offset: Optional[str],
		dtbo: Optional[Path],
		header_version: Optional[str],
		image_type: Optional[str],
		kernel: Optional[Path],
		kernel_offset: Optional[str],
		origsize: Optional[str],
		os_version: Optional[str],
		pagesize: Optional[str],
		ramdisk: Optional[Path],
		ramdisk_compression: Optional[str],
		ramdisk_offset: Optional[str],
		sigtype: Optional[str],
		tags_offset: Optional[str],
	):
		self.kernel = kernel
		self.dt = dt
		self.dtb = dtb
		self.dtbo = dtbo
		self.ramdisk = ramdisk
		self.base_address = base_address
		self.board_name = board_name
		self.cmdline = cmdline
		self.dtb_offset = dtb_offset
		self.header_version = header_version
		self.image_type = image_type
		self.kernel_offset = kernel_offset
		self.origsize = origsize
		self.os_version = os_version
		self.pagesize = pagesize
		self.ramdisk_compression = ramdisk_compression
		self.ramdisk_offset = ramdisk_offset
		self.sigtype = sigtype
		self.tags_offset = tags_offset

	def __str__(self):
		return (
			f"base address: {self.base_address}\n"
			f"board name: {self.board_name}\n"
			f"cmdline: {self.cmdline}\n"
			f"dtb offset: {self.dtb_offset}\n"
			f"header version: {self.header_version}\n"
			f"image type: {self.image_type}\n"
			f"kernel offset: {self.kernel_offset}\n"
			f"original size: {self.origsize}\n"
			f"os version: {self.os_version}\n"
			f"page size: {self.pagesize}\n"
			f"ramdisk compression: {self.ramdisk_compression}\n"
			f"ramdisk offset: {self.ramdisk_offset}\n"
			f"sigtype: {self.sigtype}\n"
			f"tags offset: {self.tags_offset}\n"
		)

class AIKManager:
	"""
	This class is responsible for dealing with AIK tasks
	such as cloning, updating, and extracting recovery images.
	"""

	UNPACKING_FAILED_STRING = "Unpacking failed, try without --nosudo."

	def __init__(self):
		"""Initialize AIKManager class."""
		if system() not in ALLOWED_OS:
			raise NotImplementedError(f"{system()} is not supported")

		# Check whether cpio package is installed
		if which("cpio") is None:
			raise RuntimeError("cpio package is not installed")

		self.tempdir = TemporaryDirectory()
		self.path = Path(self.tempdir.name)

		self.images_path = self.path / "split_img"
		self.ramdisk_path = self.path / "ramdisk"

		LOGI("Cloning AIK...")
		Repo.clone_from(AIK_REPO, self.path)

	def unpackimg(self, image: Path, ignore_ramdisk_errors: bool = False):
		"""Extract recovery image."""
		image_prefix = image.name

		try:
			process = self._execute_script("unpackimg.sh", image)
		except CalledProcessError as e:
			returncode = e.returncode
			output = e.output
		else:
			returncode = 0
			output = process

		if returncode != 0:
			if self.UNPACKING_FAILED_STRING in output and ignore_ramdisk_errors:
				# Delete ramdisk folder to avoid issues
				try:
					self.ramdisk_path.rmdir()
				except Exception:
					pass
			else:
				raise RuntimeError(f"AIK extraction failed, return code {returncode}")

		return self._get_current_extracted_info(image_prefix)

	def repackimg(self):
		return self._execute_script("repack.sh")

	def cleanup(self):
		return self._execute_script("cleanup.sh")

	def _get_current_extracted_info(self, prefix: str):
		return AIKImageInfo(
			base_address=self._read_recovery_file(prefix, "base"),
			board_name=self._read_recovery_file(prefix, "board"),
			cmdline=self._read_recovery_file(prefix, "cmdline") \
				or self._read_recovery_file(prefix, "vendor_cmdline"),
			dt=self._get_extracted_info(prefix, "dt", check_size=True),
			dtb=self._get_extracted_info(prefix, "dtb", check_size=True),
			dtb_offset=self._read_recovery_file(prefix, "dtb_offset"),
			dtbo=self._get_extracted_info(prefix, "dtbo", check_size=True) \
				or self._get_extracted_info(prefix, "recovery_dtbo", check_size=True),
			header_version=self._read_recovery_file(prefix, "header_version", default="0"),
			image_type=self._read_recovery_file(prefix, "imgtype"),
			kernel=self._get_extracted_info(prefix, "kernel", check_size=True),
			kernel_offset=self._read_recovery_file(prefix, "kernel_offset"),
			origsize=self._read_recovery_file(prefix, "origsize"),
			os_version=self._read_recovery_file(prefix, "os_version"),
			pagesize=self._read_recovery_file(prefix, "pagesize"),
			ramdisk=self.ramdisk_path if self.ramdisk_path.is_dir() else None,
			ramdisk_compression=self._read_recovery_file(prefix, "ramdiskcomp") \
				or self._read_recovery_file(prefix, "vendor_ramdiskcomp"),
			ramdisk_offset=self._read_recovery_file(prefix, "ramdisk_offset"),
			sigtype=self._read_recovery_file(prefix, "sigtype"),
			tags_offset=self._read_recovery_file(prefix, "tags_offset"),
		)

	def _read_recovery_file(
		self, prefix: str, fragment: str, default: Optional[str] = None
	) -> Optional[str]:
		file = self._get_extracted_info(prefix, fragment)
		if not file:
			return default

		return file.read_text().splitlines()[0].strip()

	def _get_extracted_info(
		self, prefix: str, fragment: str, check_size: bool = False
	) -> Optional[Path]:
		path = self.images_path / f"{prefix}-{fragment}"

		if not path.is_file():
			return None

		try:
			if check_size and path.stat().st_size == 0:
				return None
		except Exception:
			return None

		return path

	def _execute_script(self, script: str, *args):
		command = [self.path / script, "--nosudo", *args]
		return check_output(command, stderr=STDOUT, universal_newlines=True, encoding="utf-8")
