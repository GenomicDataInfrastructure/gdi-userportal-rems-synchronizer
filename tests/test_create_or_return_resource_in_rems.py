# SPDX-FileCopyrightText: 2024 PNED G.I.E.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import pytest
from unittest.mock import patch
from rems import create_or_return_resource_in_rems


# Test when the resource already exists in REMS
@patch("requests.get")
def test_create_or_return_resource_in_rems_exists(mock_get):
    # Mock the GET request to return a response with an existing resource
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {
            "id": "resource-123",
            "resid": "dataset-identifier",
            "organization": {"organization/id": "test-org-id"},
        }
    ]

    # Call the function with mock parameters
    rems_base_url = "http://mock-rems-instance.com"
    headers = {"Authorization": "Bearer mock_token"}
    organization_id = "test-org-id"
    dataset_identifier = "dataset-identifier"
    resource_id = create_or_return_resource_in_rems(
        organization_id, dataset_identifier, rems_base_url, headers
    )

    # Assert the function returns the correct resource ID
    assert resource_id == "resource-123"

    # Assert the GET request was made correctly
    mock_get.assert_called_once_with(
        url=f"{rems_base_url}/api/resources?disabled=false&archived=false&resid={dataset_identifier}",
        headers=headers,
    )


# Test when the resource does not exist and needs to be created
@patch("requests.post")
@patch("requests.get")
@patch("rems.load_json")
def test_create_or_return_resource_in_rems_create(mock_load_json, mock_get, mock_post):
    # Mock the GET request to return a 200 status code with no resources
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []

    # Mock the JSON file loading to return a base resource structure
    mock_load_json.return_value = {"organization": {"organization/id": ""}, "resid": ""}

    # Mock the POST request to return a 200 status code and a resource ID
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"id": "resource-456"}

    # Call the function with mock parameters
    rems_base_url = "http://mock-rems-instance.com"
    headers = {"Authorization": "Bearer mock_token"}
    organization_id = "test-org-id"
    dataset_identifier = "dataset-identifier"
    resource_id = create_or_return_resource_in_rems(
        organization_id, dataset_identifier, rems_base_url, headers
    )

    # Assert the function returns the newly created resource ID
    assert resource_id == "resource-456"

    # Assert the POST request was made correctly
    expected_resource = {
        "organization": {"organization/id": organization_id},
        "resid": dataset_identifier,
    }
    mock_post.assert_called_once_with(
        url=f"{rems_base_url}/api/resources/create",
        json=expected_resource,
        headers=headers,
    )


# Test when resource retrieval fails with a non-200 status code
@patch("requests.get")
def test_create_or_return_resource_in_rems_retrieval_fails(mock_get):
    # Mock the GET request to return a non-200 status code
    mock_get.return_value.status_code = 500
    mock_get.return_value.text = "Internal Server Error"

    # Call the function with mock parameters and expect a RuntimeError
    rems_base_url = "http://mock-rems-instance.com"
    headers = {"Authorization": "Bearer mock_token"}
    organization_id = "test-org-id"
    dataset_identifier = "dataset-identifier"
    with pytest.raises(
        RuntimeError, match="Resource retrieval failed: Internal Server Error"
    ):
        create_or_return_resource_in_rems(
            organization_id, dataset_identifier, rems_base_url, headers
        )


# Test when resource creation fails with a non-200 status code
@patch("requests.post")
@patch("requests.get")
@patch("rems.load_json")
def test_create_or_return_resource_in_rems_creation_fails(
    mock_load_json, mock_get, mock_post
):
    # Mock the GET request to return a 200 status code with no resources
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []

    # Mock the JSON file loading to return a base resource structure
    mock_load_json.return_value = {"organization": {"organization/id": ""}, "resid": ""}

    # Mock the POST request to return a non-200 status code
    mock_post.return_value.status_code = 400
    mock_post.return_value.text = "Bad Request"

    # Call the function with mock parameters and expect a RuntimeError
    rems_base_url = "http://mock-rems-instance.com"
    headers = {"Authorization": "Bearer mock_token"}
    organization_id = "test-org-id"
    dataset_identifier = "dataset-identifier"
    with pytest.raises(RuntimeError, match="Resource creation failed: Bad Request"):
        create_or_return_resource_in_rems(
            organization_id, dataset_identifier, rems_base_url, headers
        )
