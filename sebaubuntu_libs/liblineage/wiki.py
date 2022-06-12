#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#

from datetime import datetime
import requests
from sebaubuntu_libs.liblineage import GITHUB_ORG
from typing import Dict, List, Union
import yaml

class BatteryData:
	"""LineageOS battery information.

	Attributes:
	- capacity (int): The battery capacity (mAh)
	- removable (bool): Whether the battery is removable
	"""
	def __init__(self, capacity: int, removable: bool):
		"""Initialize the battery information."""
		self.capacity = capacity
		self.removable = removable

	@classmethod
	def from_dict(self, battery: Dict):
		"""Create a battery information object from a dictionary."""
		return self(battery["capacity"], battery["removable"])

	def __str__(self) -> str:
		"""Return a string representation of the battery information."""
		return (f"capacity: {self.capacity}mAh"
		        f", removable: {self.removable}")

class BluetoothData:
	"""LineageOS Bluetooth information.

	Attributes:
	- spec (str): Bluetooth specification
	"""
	def __init__(self, spec: str):
		"""Initialize the Bluetooth information."""
		self.spec = spec

	@classmethod
	def from_dict(self, bluetooth: Dict):
		"""Create a Bluetooth information object from a dictionary."""
		return self(bluetooth["spec"])

	def __str__(self) -> str:
		return f"spec: {self.spec}"

class DimensionData:
	"""LineageOS dimension information.

	Attributes:
	- height (str): The height
	- width (str): The width
	- depth (str): The depth
	"""
	def __init__(self, height: str, width: str, depth: str):
		"""Initialize the dimension information."""
		self.height = height
		self.width = width
		self.depth = depth

	@classmethod
	def from_dict(self, dimension: Dict):
		"""Create a dimension information object from a dictionary."""
		return self(dimension["height"], dimension["width"], dimension["depth"])

	def __str__(self) -> str:
		return (f"height: {self.height}"
		        f", width: {self.width}"
		        f", depth: {self.depth}")

class ScreenData:
	"""LineageOS screen information.

	Attributes:
	- size (str): The screen size (inches)
	- density (int): The screen density (dpi)
	- resolution (str): The screen resolution (e.g. 1080x1920)
	- technology (str): The screen technology (e.g. LCD)
	"""
	def __init__(self, size: str, density: int, resolution: str, technology: str):
		"""Initialize the screen information."""
		self.size = size
		self.density = density
		self.resolution = resolution
		self.technology = technology

	@classmethod
	def from_dict(self, device: Dict):
		"""Create a screen information object from a dictionary."""
		return self(device["size"], device["density"], device["resolution"], device["technology"])

	def __str__(self) -> str:
		return (f"size: {self.size}"
		        f", density: {self.density}"
		        f", resolution: {self.resolution}"
		        f", technology: {self.technology}")

class DeviceData:
	"""LineageOS wiki device data.

	Attributes:
	- architecture (str): The architecture of the device
	- battery (BatteryData | dict[str, BatteryData] | None): Battery info
	- bluetooth (BluetoothData): Bluetooth support info
	- codename (str): The codename of the device
	- cpu: (str): CPU name
	- cpu_cores (str): Number of CPU cores
	- cpu_freq (str): CPU frequency
	- current_branch (str): The current branch of the device
	- dimensions (DimensionData | dict[str, DimensionData] | None): Dimensions of the device
	- gpu (str): GPU name
	- image (str): The image of the device
	- install_method (str): The install method of the device
	- kernel (str): Kernel repository
	- maintainers (list[str]): The maintainers of the device
	- name (str): Commercial name of the device
	- peripherals (list[str]): Peripherals supported by the device
	- release (datetime | dict[str, datetime]): The release date of the device
	- screen (ScreenData | dict[str, ScreenData] | None): Screen info
	- tree (str): Device tree repository of the device
	- type (str): The form factor of the device
	- vendor (str): Brand name of the device vendor
	- vendor_short (str): Short name of the device vendor
	- versions (list[str]): The versions of the device
	"""
	def __init__(self,
	             architecture: str,
	             battery: Union[BatteryData, Dict, None],
	             bluetooth: BluetoothData, codename: str,
	             cpu: str,
	             cpu_cores: str,
	             cpu_freq: str,
	             current_branch: float,
	             dimensions: Union[DimensionData, Dict, None],
	             gpu: str,
	             image: str,
	             install_method: str,
	             kernel: str,
	             maintainers: List,
	             name: str,
	             peripherals: List,
	             release: Union[datetime, Dict, None],
	             screen: Union[ScreenData, Dict, None],
	             tree: str,
	             device_type: str,
	             vendor: str,
	             vendor_short: str,
	             versions: List[float]
	            ):
		"""Initialize the device information."""
		self.architecture = architecture
		self.battery = battery
		self.bluetooth = bluetooth
		self.codename = codename
		self.cpu = cpu
		self.cpu_cores = cpu_cores
		self.cpu_freq = cpu_freq
		self.current_branch = current_branch
		self.dimensions = dimensions
		self.gpu = gpu
		self.image = image
		self.install_method = install_method
		self.kernel = kernel
		self.maintainers = maintainers
		self.name = name
		self.peripherals = peripherals
		self.release = release
		self.screen = screen
		self.tree = tree
		self.device_type = device_type
		self.vendor = vendor
		self.vendor_short = vendor_short
		self.versions = versions

	@classmethod
	def from_dict(self, data: Dict):
		"""Create a device data object from a dictionary."""
		if data["battery"]:
			if isinstance(data["battery"], list):
				battery = {}
				for bat in data["battery"]:
					device, battery_data = list(bat.items())[0]
					battery[device] = BatteryData.from_dict(battery_data)
			else:
				battery = BatteryData.from_dict(data["battery"])
		else:
			battery = None

		if data["bluetooth"]:
			bluetooth = BluetoothData.from_dict(data["bluetooth"])
		else:
			bluetooth = None
		
		if data["dimensions"]:
			if isinstance(data["dimensions"], list):
				dimensions = {}
				for device, dimension_data in data["dimensions"]:
					dimensions[device] = DimensionData.from_dict(dimension_data)
			elif isinstance(data["dimensions"], dict):
				dimensions = DimensionData.from_dict(data["dimensions"])
			else:
				dimensions = None
		else:
			dimensions = None

		def convert_release_date(date: Union[int, str]):
			date = str(date)
			# YYYY-MM-DD
			try:
				return datetime.fromisoformat(date)
			except ValueError:
				# YYYY-MM
				try:
					return datetime.strptime(date, "%Y-%m")
				except ValueError:
					# YYYY
					return datetime.strptime(date, "%Y")

		if isinstance(data["release"], list):
			release = {}
			for rel in data["release"]:
				device, date = list(rel.items())[0]
				release[device] = convert_release_date(date)
		else:
			release = convert_release_date(data["release"])

		if data["screen"]:
			if isinstance(data["screen"], list):
				screen = {}
				for scr in data["screen"]:
					device, screen_data = list(scr.items())[0]
					screen[device] = ScreenData.from_dict(screen_data)
			else:
				screen = ScreenData.from_dict(data["screen"])
		else:
			screen = None

		return self(
			data["architecture"],
			battery,
			bluetooth,
			data["codename"],
			data["cpu"],
			data["cpu_cores"],
			data["cpu_freq"],
			data["current_branch"],
			dimensions,
			data["gpu"],
			data["image"],
			data["install_method"],
			data["kernel"],
			data["maintainers"],
			data["name"],
			data["peripherals"],
			release,
			screen,
			data["tree"],
			data["type"],
			data["vendor"],
			data["vendor_short"],
			data["versions"],
		)

	def __str__(self) -> str:
		"""Return a string representation of the device data."""
		return (f"Name: {self.name}\n"
		        f"Codename: {self.codename}\n"
		        f"Type: {self.device_type}\n"
				f"Vendor: {self.vendor}\n"
				f"Vendor (short): {self.vendor_short}\n"
				f"Architecture: {self.architecture}\n"
				f"CPU: {self.cpu}\n"
				f"CPU cores: {self.cpu_cores}\n"
				f"CPU frequency: {self.cpu_freq}\n"
				f"GPU: {self.gpu}\n"
				f"Install method: {self.install_method}\n"
				f"Kernel repository: {f'{GITHUB_ORG}/{self.kernel}'}\n"
				f"Maintainers: {', '.join(self.maintainers) if self.maintainers else 'None (unmaintained)'}\n"
				f"Peripherals: {', '.join(self.peripherals)}\n"
				f"Release: {str(self.release) if not isinstance(self.release, dict) else ', '.join([f'{device}: {date}' for device, date in self.release.items()])}\n"
				f"Screen: {str(self.screen) if not isinstance(self.screen, dict) else ', '.join([f'{device}: {screen_data}' for device, screen_data in self.screen.items()])}\n"
				f"Device tree repository: {f'{GITHUB_ORG}/{self.tree}'}\n"
				f"Versions: {', '.join([str(version) for version in self.versions])}\n"
				f"Battery: {str(self.battery) if not isinstance(self.battery, dict) else ', '.join([f'{device}: {battery_data}' for device, battery_data in self.battery.items()])}\n"
				f"Bluetooth: {str(self.bluetooth)}\n"
				f"Dimensions: {str(self.dimensions) if not isinstance(self.dimensions, dict) else ', '.join([f'{device}: {dimensions_data}' for device, dimensions_data in self.dimensions.items()])}")

def get_device_data(device: str):
	url = f"https://raw.githubusercontent.com/LineageOS/lineage_wiki/master/_data/devices/{device}.yml"
	response = requests.get(url=url)
	response.raise_for_status()
	return DeviceData.from_dict(yaml.safe_load(response.text))
