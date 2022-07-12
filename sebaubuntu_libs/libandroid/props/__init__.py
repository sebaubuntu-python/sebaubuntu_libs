#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#
"""Android build prop library."""

from __future__ import annotations
from distutils.util import strtobool
from pathlib import Path
from typing import Any, Callable, List, Union

class BuildProp(dict):
	"""
	A class representing a build prop.
	This class basically mimics Android props system, with both getprop and setprop commands
	"""
	@classmethod
	def from_file(cls, file: Path):
		"""Create a BuildProp object from a file."""
		build_prop = cls()
		build_prop.import_props(file)
		return build_prop

	def __str__(self):
		return self.get_readable_list()

	def get_readable_list(self, excluded_props: List[str] = []):
		ordered_props = dict(sorted(self.items()))

		for excluded_prop in excluded_props:
			ordered_props.pop(excluded_prop, None)

		return "\n".join(f"{key}={value}" for key, value in ordered_props.items()) + "\n"

	def import_props(self, file: Union[Path, BuildProp]):
		if isinstance(file, BuildProp):
			text = str(file)
		else:
			text = file.read_text(encoding="utf-8")

		for prop in text.splitlines():
			if prop.startswith("#"):
				continue
			try:
				prop_name, prop_value = prop.split("=", 1)
			except ValueError:
				continue
			else:
				self.set_prop(prop_name, prop_value)

	def _get_prop(self, key: str, data_type: Callable[[str], Any] = str, default: Any = None):
		if key in self:
			try:
				return data_type(self[key])
			except ValueError:
				return default
		else:
			return default

	def get_prop(self, key: str, default: str = None):
		return self._get_prop(key, str, default)

	def get_prop_bool(self, key: str, default: bool = False):
		return self._get_prop(key, lambda x: bool(strtobool(x)), default)

	def get_prop_int(self, key: str, default: int = 0):
		return self._get_prop(key, int, default)

	def get_prop_float(self, key: str, default: float = 0.0):
		return self._get_prop(key, float, default)

	def set_prop(self, key: str, value: str):
		assert isinstance(value, str), f"value must be a string, not {type(value)}"
		self[key] = value

	def write_to_file(self, path: Path, excluded_props: List[str] = []):
		path.write_text(self.get_readable_list(excluded_props), encoding="utf-8")
