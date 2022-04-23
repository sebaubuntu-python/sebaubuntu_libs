#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#

from datetime import datetime
import requests
from sebaubuntu_libs.liblineage import GITHUB_ORG
from telegram.utils.helpers import escape_markdown
from typing import Union
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
	def from_dict(self, battery: dict):
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
	def from_dict(self, bluetooth: dict):
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
	def from_dict(self, dimension: dict):
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
	def from_dict(self, device: dict):
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
	             battery: Union[BatteryData, dict, None],
	             bluetooth: BluetoothData, codename: str,
	             cpu: str,
	             cpu_cores: str,
	             cpu_freq: str,
	             current_branch: float,
	             dimensions: Union[DimensionData, dict, None],
	             gpu: str,
	             image: str,
	             install_method: str,
	             kernel: str,
	             maintainers: list,
	             name: str,
	             peripherals: list,
	             release: Union[datetime, dict, None],
	             screen: Union[ScreenData, dict, None],
	             tree: str,
	             device_type: str,
	             vendor: str,
	             vendor_short: str,
	             versions: list[float]
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
	def from_dict(self, data: dict):
		"""Create a device data object from a dictionary."""
		if data["battery"]:
			if isinstance(data["battery"], list):
				battery = {}
				for device, battery_data in data["battery"]:
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
				print(rel.items())
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
		return (f"Name: {escape_markdown(self.name, 2)}\n"
		        f"Codename: {escape_markdown(self.codename, 2)}\n"
		        f"Type: {escape_markdown(self.device_type, 2)}\n"
				f"Vendor: {escape_markdown(self.vendor, 2)}\n"
				f"Vendor \(short\): {escape_markdown(self.vendor_short, 2)}\n"
				f"Architecture: {escape_markdown(self.architecture, 2)}\n"
				f"CPU: {escape_markdown(self.cpu, 2)}\n"
				f"CPU cores: {escape_markdown(self.cpu_cores, 2)}\n"
				f"CPU frequency: {escape_markdown(self.cpu_freq, 2)}\n"
				f"GPU: {escape_markdown(self.gpu, 2)}\n"
				f"Install method: {escape_markdown(self.install_method, 2)}\n"
				f"Kernel repository: {escape_markdown(f'{GITHUB_ORG}/{self.kernel}', 2)}\n"
				f"Maintainers: {escape_markdown(', '.join(self.maintainers), 2) if self.maintainers else escape_markdown('None (unmaintained)', 2)}\n"
				f"Peripherals: {escape_markdown(', '.join(self.peripherals), 2)}\n"
				f"Release: {escape_markdown(str(self.release), 2) if not isinstance(self.release, dict) else escape_markdown(', '.join([f'{device}: {date}' for device, date in self.release.items()]), 2)}\n"
				f"Screen: {escape_markdown(str(self.screen), 2) if not isinstance(self.screen, dict) else escape_markdown(', '.join([f'{device}: {screen_data}' for device, screen_data in self.screen.items()]), 2)}\n"
				f"Device tree repository: {escape_markdown(f'{GITHUB_ORG}/{self.tree}', 2)}\n"
				f"Versions: {escape_markdown(', '.join([str(version) for version in self.versions]), 2)}\n"
				f"Battery: {escape_markdown(str(self.battery))}\n"
				f"Bluetooth: {escape_markdown(str(self.bluetooth), 2)}\n"
				f"Dimensions: {escape_markdown(str(self.dimensions), 2) if not isinstance(self.dimensions, dict) else escape_markdown(', '.join([f'{device}: {dimensions_data}' for device, dimensions_data in self.dimensions.items()]), 2)}")

def get_device_data(device: str):
	url = f"https://raw.githubusercontent.com/LineageOS/lineage_wiki/master/_data/devices/{device}.yml"
	response = requests.get(url=url)
	response.raise_for_status()
	return DeviceData.from_dict(yaml.safe_load(response.text))
