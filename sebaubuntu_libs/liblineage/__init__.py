#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#
"""LineageOS library."""

from sebaubuntu_libs.libandroid import AndroidVersion

GITHUB_ORG = "https://github.com/LineageOS"

LINEAGEOS_TO_ANDROID_VERSION = {
    "13.0": AndroidVersion.M,
    "14.1": AndroidVersion.N,
    "15.1": AndroidVersion.O,
	"16.0": AndroidVersion.P,
	"17.1": AndroidVersion.Q,
	"18.0": AndroidVersion.R,
	"18.1": AndroidVersion.R,
	"19.0": AndroidVersion.S,
	"19.1": AndroidVersion.Sv2,
}
