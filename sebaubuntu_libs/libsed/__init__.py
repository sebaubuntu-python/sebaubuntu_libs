#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#
"""sed (stream editor) library."""

import re

def sed(string: str, regexp: str, replacement: str, flags: str = ""):
	"""re wrapper for sed."""
	_flags = 0
	_flags |= (re.M if 'm' in flags or 'M' in flags else 0)
	_flags |= (re.I if 'i' in flags or 'I' in flags else 0)

	return re.sub(regexp, replacement, string, (0 if 'g' in flags else 1), _flags)
