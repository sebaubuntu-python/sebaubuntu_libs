#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#
"""Logging utils."""

from logging import basicConfig, INFO, DEBUG
from logging import debug, info, warning, error, fatal

LOGD = debug
LOGI = info
LOGW = warning
LOGE = error
LOGF = fatal

def setup_logging(verbose: bool = False):
	if verbose:
		basicConfig(format='[%(filename)s:%(lineno)s %(levelname)s] %(funcName)s: %(message)s',
		            level=DEBUG)
	else:
		basicConfig(format='[%(levelname)s] %(message)s', level=INFO)
