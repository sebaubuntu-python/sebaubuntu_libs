#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: Apache-2.0
#

import requests
from requests.models import Response

class GoFileRequests:
	@classmethod
	def delete(cls, *args, **kwargs):
		response = cls._send_request(requests.delete, *args, **kwargs)
		return cls._process_response(response)

	@classmethod
	def get(cls, *args, **kwargs):
		response = cls._send_request(requests.get, *args, **kwargs)
		return cls._process_response(response)

	@classmethod
	def post(cls, *args, **kwargs):
		response = cls._send_request(requests.post, *args, **kwargs)
		return cls._process_response(response)

	@classmethod
	def put(cls, *args, **kwargs):
		response = cls._send_request(requests.put, *args, **kwargs)
		return cls._process_response(response)

	@staticmethod
	def _send_request(func, *args, **kwargs):
		for arg in ["data", "params"]:
			kwargs[arg] = kwargs.get(arg, {})
			# We do a little trolling
			kwargs[arg]["websiteToken"] = "websiteToken"

		response = func(*args, **kwargs)
		return response

	@staticmethod
	def _process_response(response: Response):
		response_json = response.json()
		if not "status" in response_json:
			raise Exception(f"Invalid response: {response_json}")

		if response_json["status"] != "ok":
			raise Exception(f"Error: {response_json['status']}")
		
		return response_json["data"]
