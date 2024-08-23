# SPDX-FileCopyrightText: 2024 PNED G.I.E.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
import hashlib
from unittest.mock import patch, mock_open
from rems import load_json, create_or_return_organization_in_rems


# Test for load_json
@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
def test_load_json(mock_file):
    # Call the function with a mock path
    path = "mock_path.json"
    result = load_json(path)

    # Assert that the file was opened correctly and the result is as expected
    mock_file.assert_called_once_with(path, "r")
    assert result == {"key": "value"}


# Test for create_or_return_organization_in_rems when the organization already exists
@patch("requests.get")
@patch("rems.load_json")
def test_create_or_return_organization_in_rems_exists(mock_load_json, mock_get):
    # Mocking load_json to return specific content
    mock_load_json.return_value = {"organization/name": {"en": "Test Organization"}}

    # Mock the get request to return a 200 status code (organization exists)
    mock_get.return_value.status_code = 200

    # Call the function with mock parameters
    rems_base_url = "http://mock-rems-instance.com"
    headers = {"Authorization": "Bearer mock_token"}
    organization_id = create_or_return_organization_in_rems(
        rems_base_url, headers, True
    )

    # Assert that the function returns the correct organization_id
    expected_id = hashlib.md5("Test Organization".encode()).hexdigest()
    assert organization_id == expected_id

    # Assert that the GET request was made correctly
    mock_get.assert_called_once_with(
        url=f"{rems_base_url}/api/organizations/{expected_id}",
        headers=headers,
        verify=True,
    )


# Test for create_or_return_organization_in_rems when the organization does not exist and is created
@patch("requests.post")
@patch("requests.get")
@patch("rems.load_json")
def test_create_or_return_organization_in_rems_create(
    mock_load_json, mock_get, mock_post
):
    # Mocking load_json to return specific content
    mock_load_json.return_value = {"organization/name": {"en": "Test Organization"}}

    # Mock the get request to return a 404 status code (organization does not exist)
    mock_get.return_value.status_code = 404

    # Mock the post request to return a 200 status code (organization created successfully)
    mock_post.return_value.status_code = 200

    # Call the function with mock parameters
    rems_base_url = "http://mock-rems-instance.com"
    headers = {"Authorization": "Bearer mock_token"}
    organization_id = create_or_return_organization_in_rems(
        rems_base_url, headers, True
    )

    # Assert that the function returns the correct organization_id
    expected_id = hashlib.md5("Test Organization".encode()).hexdigest()
    assert organization_id == expected_id

    # Assert that the POST request was made correctly
    expected_payload = {
        "organization/name": {"en": "Test Organization"},
        "organization/id": expected_id,
    }
    mock_post.assert_called_once_with(
        url=f"{rems_base_url}/api/organizations/create",
        json=expected_payload,
        headers=headers,
        verify=True,
    )


# Test for create_or_return_organization_in_rems when retrieval fails for an unexpected reason
@patch("requests.get")
@patch("rems.load_json")
def test_create_or_return_organization_in_rems_retrieval_fails(
    mock_load_json, mock_get
):
    # Mocking load_json to return specific content
    mock_load_json.return_value = {"organization/name": {"en": "Test Organization"}}

    # Mock the get request to return a non-404 error status code (e.g., 500)
    mock_get.return_value.status_code = 500
    mock_get.return_value.text = "Internal Server Error"

    # Call the function with mock parameters and expect a RuntimeError
    rems_base_url = "http://mock-rems-instance.com"
    headers = {"Authorization": "Bearer mock_token"}
    with pytest.raises(
        RuntimeError, match="Organization retrieval failed: Internal Server Error"
    ):
        create_or_return_organization_in_rems(rems_base_url, headers, True)


# Test for create_or_return_organization_in_rems when creation fails
@patch("requests.post")
@patch("requests.get")
@patch("rems.load_json")
def test_create_or_return_organization_in_rems_creation_fails(
    mock_load_json, mock_get, mock_post
):
    # Mocking load_json to return specific content
    mock_load_json.return_value = {"organization/name": {"en": "Test Organization"}}

    # Mock the get request to return a 404 status code (organization does not exist)
    mock_get.return_value.status_code = 404

    # Mock the post request to return a non-200 status code (e.g., 400)
    mock_post.return_value.status_code = 400
    mock_post.return_value.text = "Bad Request"

    # Call the function with mock parameters and expect a RuntimeError
    rems_base_url = "http://mock-rems-instance.com"
    headers = {"Authorization": "Bearer mock_token"}
    with pytest.raises(RuntimeError, match="Organization creation failed: Bad Request"):
        create_or_return_organization_in_rems(rems_base_url, headers, True)
