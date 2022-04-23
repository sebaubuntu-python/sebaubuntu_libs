#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#
import requests

LINEAGE_BUILD_TARGETS_FILE = "https://raw.githubusercontent.com/LineageOS/hudson/master/lineage-build-targets"

class LineageBuildTarget:
    def __init__(self,
                 device: str,
                 build_type: str,
                 branch_name: str,
                 period: str,
                ):
        self.device = device
        self.build_type = build_type
        self.branch_name = branch_name
        self.period = period

    def __str__(self) -> str:
        return f"{self.device} {self.build_type} {self.branch_name} {self.period}"

    @classmethod
    def from_api(self, line: str):
        return self(*line.split())

def get_lineage_build_targets():
    response = requests.get(url=LINEAGE_BUILD_TARGETS_FILE).text.split("\n")
    return [LineageBuildTarget.from_api(line)
            for line in response
            if line and not line.startswith("#")]
