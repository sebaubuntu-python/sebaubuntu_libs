#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#
"""locale utils."""

from locale import LC_ALL, setlocale

def setup_locale():
	setlocale(LC_ALL, "C")
