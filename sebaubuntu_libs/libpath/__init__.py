#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#
"""Paths utils."""

from pathlib import Path

def is_relative_to(path: Path, *other):
	"""Return True if the path is relative to another path or False.
	"""
	try:
		path.relative_to(*other)
		return True
	except ValueError:
		return False
