# SPDX-FileCopyrightText: 2024 PNED G.I.E.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from unittest.mock import patch
from ckan import get_packages_count, get_packages

# Mock data for the API responses
mock_package_count_response = {"result": {"count": 42}}

mock_packages_response = {
    "result": {
        "results": [
            {"id": "package1", "name": "Test Package 1"},
            {"id": "package2", "name": "Test Package 2"},
        ]
    }
}


# Test for get_packages_count
@patch("requests.get")
def test_get_packages_count(mock_get):
    # Configure the mock to return a response with the JSON data
    mock_get.return_value.json.return_value = mock_package_count_response

    # Call the function with a mock CKAN base URL
    ckan_base_url = "http://mock-ckan-instance.com"
    count = get_packages_count(ckan_base_url)

    # Assert the function returns the correct count
    assert count == 42
    mock_get.assert_called_once_with(
        f"{ckan_base_url}/api/3/action/package_search?rows=0"
    )


# Test for get_packages
@patch("requests.get")
def test_get_packages(mock_get):
    # Configure the mock to return a response with the JSON data
    mock_get.return_value.json.return_value = mock_packages_response

    # Call the function with mock parameters
    start = 0
    rows = 2
    ckan_base_url = "http://mock-ckan-instance.com"
    packages = get_packages(start, rows, ckan_base_url)

    # Assert the function returns the correct packages
    assert len(packages) == 2
    assert packages[0]["id"] == "package1"
    assert packages[1]["name"] == "Test Package 2"
    mock_get.assert_called_once_with(
        f"{ckan_base_url}/api/3/action/package_search?rows={rows}&start={start}"
    )
