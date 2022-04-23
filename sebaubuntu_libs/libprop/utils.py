#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#

PARTITIONS = [
	"bootimage",
	"odm",
	"odm_dlkm",
	"product",
	"system",
	"system_ext",
	"vendor",
	"vendor_dlkm",
]

def get_partition_props(format_string: str, add_empty: bool = False):
	"""
	Get a list of props given a string to format.

	If add_empty is True, you need to omit a dot at the end of the partition
	(e.g. "ro.{}.build.date" if add_empty is False, "ro.{}build.date" otherwise).
	"""
	partitions_formatted = [
		(f"{part}." if add_empty else part) for part in PARTITIONS
	]

	partition_props = [format_string.format(partition) for partition in partitions_formatted]
	if add_empty:
		partition_props.append(format_string.format(""))

	return partition_props
