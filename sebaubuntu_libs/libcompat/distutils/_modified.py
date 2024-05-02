#
# Copyright (C) 2023 Python Packaging Authority
# Copyright (C) 2024 Sebastiano Barezzi
#
# SPDX-License-Identifier: MIT
#

import os.path

from .errors import DistutilsFileError

def _newer(source, target):
	return not os.path.exists(target) or (
		os.path.getmtime(source) > os.path.getmtime(target)
	)


def newer(source, target):
	"""
	Is source modified more recently than target.

	Returns True if 'source' is modified more recently than
	'target' or if 'target' does not exist.

	Raises DistutilsFileError if 'source' does not exist.
	"""
	if not os.path.exists(source):
		raise DistutilsFileError("file '%s' does not exist" % os.path.abspath(source))

	return _newer(source, target)
