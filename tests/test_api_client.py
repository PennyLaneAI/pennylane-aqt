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
"""Tests for the api_client module"""
import pytest

import requests
import json

from pennylane_aqt import api_client

SOME_URL = "http://www.corgis.org"
SOME_PAYLOAD = json.dumps({"data": 0, "stuff": "more_stuff"})
SOME_HEADER = {"Auth-token": "ABC123"}


class MockResponse:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class TestAPIClient:
    """Tests for the api_client module."""

    @pytest.mark.parametrize(
        "left_path, right_path, joined_path",
        [
            (
                "http://subdomain.domain.com",
                "api/endpoint",
                "http://subdomain.domain.com/api/endpoint",
            ),
            ("https://abc.com/", "/v1/web/app", "https://abc.com/v1/web/app"),
            ("www.youtube.com", "watch?v=oHg5SJYRHA0", "www.youtube.com/watch?v=oHg5SJYRHA0"),
        ],
    )
    def test_join_path(self, left_path, right_path, joined_path):
        """Tests that the ``join_path`` function correctly merges paths."""
        print(api_client.join_path(left_path, right_path), joined_path)
        assert api_client.join_path(left_path, right_path) == joined_path

    @pytest.mark.parametrize("status_code", [200, 201, 202])
    def test_valid_status_codes(self, status_code):
        """Tests that the function ``valid_status_codes`` returns True
        for responses with valid status codes."""
        resp = requests.Response()
        resp.status_code = status_code
        assert api_client.valid_status_code(resp)

    @pytest.mark.parametrize("status_code", [404, 123, 400])
    def test_raise_invalid_status_exception(self, status_code):
        """Tests that the function ``raise_invalid_status_exception`` raises
        HTTPError exceptions for bad status codes."""
        resp = requests.Response()
        resp.status_code = status_code
        with pytest.raises(requests.HTTPError):
            api_client.raise_invalid_status_exception(resp)

    @pytest.mark.parametrize("method", ["PUSH", "GET", "BREAD", "CHOCOLATE"])
    def test_submit_invalid_method(self, method):
        """Tests that ``submit`` raises an exception when the request type is
        invalid."""

        with pytest.raises(ValueError, match="Invalid HTTP request method provided."):
            api_client.submit(method, SOME_URL, SOME_PAYLOAD, SOME_HEADER)

    def test_submit_put_request(self, monkeypatch):
        """Tests that passing the arg "PUT" creates a response via ``requests.put``"""

        def mock_put(*args, **kwargs):
            return MockResponse(*args, **kwargs)

        monkeypatch.setattr(requests, "put", mock_put)

        response = api_client.submit("PUT", SOME_URL, SOME_PAYLOAD, SOME_HEADER)
        assert response.args == (SOME_URL, SOME_PAYLOAD)
        assert response.kwargs == ({"headers": SOME_HEADER})

    def test_submit_post_request(self, monkeypatch):
        """Tests that passing the arg "POST" creates a response via ``requests.post``"""

        def mock_put(*args, **kwargs):
            return MockResponse(*args, **kwargs)

        monkeypatch.setattr(requests, "post", mock_put)

        response = api_client.submit("POST", SOME_URL, SOME_PAYLOAD, SOME_HEADER)
        assert response.args == (SOME_URL, SOME_PAYLOAD)
        assert response.kwargs == ({"headers": SOME_HEADER})
