#
# Copyright (C) 2023 Python Packaging Authority
# Copyright (C) 2024 Sebastiano Barezzi
#
# SPDX-License-Identifier: MIT
#

class DistutilsError(Exception):
	"""The root of all Distutils evil."""

	pass

class DistutilsFileError(DistutilsError):
	"""Any problems in the filesystem: expected file not found, etc.
	Typically this is for problems that we detect before OSError
	could be raised."""

	pass

class DistutilsInternalError(DistutilsError):
	"""Internal inconsistencies or impossibilities (obviously, this
	should never be seen if the code is working!)."""

	pass
