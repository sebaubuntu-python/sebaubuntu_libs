#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#
"""Strings utils."""

def removeprefix(string: str, prefix: str) -> str:
	"""Remove a prefix from a string."""
	if string.startswith(prefix):
		return string[len(prefix):]
	return string

def removesuffix(string: str, suffix: str) -> str:
	"""Remove a suffix from a string."""
	if string.endswith(suffix):
		return string[:-len(suffix)]
	return string
