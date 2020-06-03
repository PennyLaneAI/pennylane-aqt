# Copyright 2020 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
API Client
==========

**Module name:** :mod:`pennylane_aqt.api_client`

.. currentmodule:: pennylane_aqt.api_client

Tools to interface with online APIs.

Classes
-------

.. autosummary::
   submit
   verify_valid_status

Code details
~~~~~~~~~~~~
"""

import urllib
import requests

SUPPORTED_HTTP_REQUESTS = ["PUT", "POST"]
VALID_STATUS_CODES = [200, 201, 202]
DEFAULT_TIMEOUT = 1.0


def verify_valid_status(response):
    """
    Check a HTTP response for valid status codes, and raise an exception if
    the code is invalid

    Args:
        response[requests.model.Response]: the response containing the error

    Returns:
        bool: whether the response has an acceptable HTTP status code

    Raises:
        requests.HTTPError: if the status is not valid
    """
    if response.status_code not in VALID_STATUS_CODES:
        raise requests.HTTPError


def submit(request_type, url, request, headers):
    """Submit a request to AQT's API.

    Args:
        request_type (str): the type of HTTP request ("PUT" or "POST")
        url (str): the API's online URL
        request (str): JSON-formatted payload
        headers (dict): HTTP request header

    Returns:
        requests.models.Response: the response from the API
    """
    if request_type not in SUPPORTED_HTTP_REQUESTS:
        raise ValueError("""Invalid HTTP request method provided. Options are "PUT" or "POST".""")
    if request_type == "PUT":
        return requests.put(url, request, headers=headers, timeout=DEFAULT_TIMEOUT)
    if request_type == "POST":
        return requests.post(url, request, headers=headers, timeout=DEFAULT_TIMEOUT)
