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
   join_path

Code details
~~~~~~~~~~~~
"""

import urllib
import requests

SUPPORTED_HTTP_REQUESTS = ["PUT", "POST"]
VALID_STATUS_CODES = [200, 201, 202]


def join_path(base_path, path):
    """
    Joins two paths, a base path and another path, and returns a string.

    Args:
        base_path (str): the left side of the joined path
        path (str): the right side of the joined path

    Returns:
        str: the joined path
    """
    return urllib.parse.urljoin("{}/".format(base_path), path)


def valid_status_code(response):
    """
    Check a HTTP response for valid status codes.

    Returns:
        bool: whether the response has an acceptable HTTP status code
    """
    return response.status_code in VALID_STATUS_CODES


def raise_invalid_status_exception(response):
    """
    Raise appropriate errors from HTTP error codes.

    Args:
        response[requests.model.Response]: the response containing the error
    """
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
        raise ValueError("Invalid HTTP request method provided." """Options are "PUT" or "POST""")
    if request_type == "PUT":
        return requests.put(url, request, headers=headers)
    if request_type == "POST":
        return requests.post(url, request, headers=headers)
