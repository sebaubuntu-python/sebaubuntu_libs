#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#

from elftools.common.exceptions import ELFError
from elftools.elf.elffile import ELFFile
from pathlib import Path
from typing import Set

class ELF:
	def __init__(self, path: Path):
		self.path = path

		# Just check that this is actually an ELF file, die otherwise
		with self.path.open("rb") as f:
			ELFFile(f)

		self.needed_libraries = self.get_needed_libs(self.path)

	@classmethod
	def get_needed_libs(cls, file: Path) -> Set[str]:
		needed_libs: Set[str] = set()

		with file.open("rb") as f:
			try:
				elf = ELFFile(f)
				dynsec = elf.get_section_by_name(".dynamic")
				if dynsec:
					for dt_needed in dynsec.iter_tags("DT_NEEDED"):
						needed_libs.add(str(dt_needed.needed))
			except ELFError:
				pass

		return needed_libs
