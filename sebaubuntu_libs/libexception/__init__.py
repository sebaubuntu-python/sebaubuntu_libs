#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#
"""Exceptions utils."""

import traceback

def format_exception(exception):
	"""Format an exception."""
	return ''.join(traceback.format_exception(type(exception), exception,
	                                          exception.__traceback__,
	                                          limit=None, chain=True))
