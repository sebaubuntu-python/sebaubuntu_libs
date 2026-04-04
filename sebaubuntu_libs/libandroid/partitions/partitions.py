#
# SPDX-FileCopyrightText: Sebastiano Barezzi
# SPDX-License-Identifier: Apache-2.0
#

from pathlib import Path
from typing import Dict

from sebaubuntu_libs.libandroid.partitions.partition import AndroidPartition, BUILD_PROP_LOCATION
from sebaubuntu_libs.libandroid.partitions.partition_model import (
    PartitionGroup,
    PartitionModel,
    PartitionModels,
)


class Partitions:
    def __init__(self, dump_path: Path):
        self.dump_path = dump_path

        self.partitions: Dict[PartitionModel, AndroidPartition] = {}

        # Search for system
        for system in [self.dump_path / "system", self.dump_path / "system/system"]:
            for build_prop_location in BUILD_PROP_LOCATION:
                if not (system / build_prop_location).is_file():
                    continue

                self.partitions[PartitionModels.SYSTEM] = AndroidPartition(
                    PartitionModels.SYSTEM, system
                )

        assert PartitionModels.SYSTEM in self.partitions
        self.system = self.partitions[PartitionModels.SYSTEM]

        # Search for vendor
        for vendor in [
            self.partitions[PartitionModels.SYSTEM].path / "vendor",
            self.dump_path / "vendor",
        ]:
            for build_prop_location in BUILD_PROP_LOCATION:
                if not (vendor / build_prop_location).is_file():
                    continue

                self.partitions[PartitionModels.VENDOR] = AndroidPartition(
                    PartitionModels.VENDOR, vendor
                )

        assert PartitionModels.VENDOR in self.partitions
        self.vendor = self.partitions[PartitionModels.VENDOR]

        # Search for the other partitions
        for model in [
            model
            for model in PartitionModels.from_group(PartitionGroup.SSI)
            if model is not PartitionModels.SYSTEM
        ]:
            self._search_for_partition(model)

        for model in [
            model
            for model in PartitionModels.from_group(PartitionGroup.TREBLE)
            if model is not PartitionModels.VENDOR
        ]:
            self._search_for_partition(model)

    def get_partition(self, model: PartitionModel):
        if model in self.partitions:
            return self.partitions[model]

        return None

    def get_partition_by_name(self, name: str):
        partition_model = PartitionModels.from_name(name)
        if not partition_model:
            return None

        return self.get_partition(partition_model)

    def get_all_partitions(self):
        return self.partitions.values()

    def _search_for_partition(self, model: PartitionModel):
        possible_locations = [
            self.partitions[PartitionModels.SYSTEM].path / model.name,
            self.partitions[PartitionModels.VENDOR].path / model.name,
            self.dump_path / model.name,
        ]

        for location in possible_locations:
            for build_prop_location in BUILD_PROP_LOCATION:
                if not (location / build_prop_location).is_file():
                    continue

                self.partitions[model] = AndroidPartition(model, location)
