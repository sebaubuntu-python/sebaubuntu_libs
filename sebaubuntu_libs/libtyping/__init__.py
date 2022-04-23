#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#
"""Typing utils."""

from typing import Iterable

def is_iterable_and_not_str(obj: object):
    """Check if an object is iterable and not a string."""
    return isinstance(obj, Iterable) and not isinstance(obj, str)
