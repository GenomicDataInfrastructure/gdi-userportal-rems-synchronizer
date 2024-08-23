# SPDX-FileCopyrightText: 2024 PNED G.I.E.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import pytest
from unittest.mock import patch
from rems import create_or_return_catalogue_item_in_rems


# Test when the catalogue item already exists in REMS
@patch("requests.get")
def test_create_or_return_catalogue_item_in_rems_exists(mock_get):
    # Mock the GET request to return a response with an existing catalogue item
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {
            "id": "catalogue-item-123",
            "resid": "dataset-identifier",
            "organization": {"organization/id": "test-org-id"},
        }
    ]

    # Call the function with mock parameters
    rems_base_url = "http://mock-rems-instance.com"
    headers = {"Authorization": "Bearer mock_token"}
    organization_id = "test-org-id"
    workflow_id = 456
    dataset_identifier = "dataset-identifier"
    resource_id = 789
    title = "Test Catalogue Item"
    catalogue_item_id = create_or_return_catalogue_item_in_rems(
        organization_id,
        workflow_id,
        dataset_identifier,
        resource_id,
        title,
        rems_base_url,
        headers,
        True,
    )

    # Assert the function returns the correct catalogue item ID
    assert catalogue_item_id == "catalogue-item-123"

    # Assert the GET request was made correctly
    mock_get.assert_called_once_with(
        url=f"{rems_base_url}/api/catalogue-items?disabled=false&archived=false&resource={dataset_identifier}",
        headers=headers,
        verify=True,
    )


# Test when the catalogue item does not exist and needs to be created
@patch("requests.post")
@patch("requests.get")
@patch("rems.load_json")
def test_create_or_return_catalogue_item_in_rems_create(
    mock_load_json, mock_get, mock_post
):
    # Mock the GET request to return a 200 status code with no catalogue items
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []

    # Mock the JSON file loading to return a base catalogue item structure
    mock_load_json.return_value = {
        "organization": {"organization/id": ""},
        "resid": "",
        "wfid": "",
        "localizations": {"en": {"title": ""}},
    }

    # Mock the POST request to return a 200 status code and a catalogue item ID
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"id": "catalogue-item-456"}

    # Call the function with mock parameters
    rems_base_url = "http://mock-rems-instance.com"
    headers = {"Authorization": "Bearer mock_token"}
    organization_id = "test-org-id"
    workflow_id = 456
    dataset_identifier = "dataset-identifier"
    resource_id = 789
    title = "Test Catalogue Item"
    catalogue_item_id = create_or_return_catalogue_item_in_rems(
        organization_id,
        workflow_id,
        dataset_identifier,
        resource_id,
        title,
        rems_base_url,
        headers,
        True,
    )

    # Assert the function returns the newly created catalogue item ID
    assert catalogue_item_id == "catalogue-item-456"

    # Assert the POST request was made correctly
    expected_catalogue_item = {
        "organization": {"organization/id": organization_id},
        "resid": resource_id,
        "wfid": workflow_id,
        "localizations": {"en": {"title": title}},
    }
    mock_post.assert_called_once_with(
        url=f"{rems_base_url}/api/catalogue-items/create",
        json=expected_catalogue_item,
        headers=headers,
        verify=True,
    )


# Test when catalogue item retrieval fails with a non-200 status code
@patch("requests.get")
def test_create_or_return_catalogue_item_in_rems_retrieval_fails(mock_get):
    # Mock the GET request to return a non-200 status code
    mock_get.return_value.status_code = 500
    mock_get.return_value.text = "Internal Server Error"

    # Call the function with mock parameters and expect a RuntimeError
    rems_base_url = "http://mock-rems-instance.com"
    headers = {"Authorization": "Bearer mock_token"}
    organization_id = "test-org-id"
    workflow_id = 456
    dataset_identifier = "dataset-identifier"
    resource_id = 789
    title = "Test Catalogue Item"
    with pytest.raises(
        RuntimeError, match="Catalogue Item retrieval failed: Internal Server Error"
    ):
        create_or_return_catalogue_item_in_rems(
            organization_id,
            workflow_id,
            dataset_identifier,
            resource_id,
            title,
            rems_base_url,
            headers,
            True,
        )


# Test when catalogue item creation fails with a non-200 status code
@patch("requests.post")
@patch("requests.get")
@patch("rems.load_json")
def test_create_or_return_catalogue_item_in_rems_creation_fails(
    mock_load_json, mock_get, mock_post
):
    # Mock the GET request to return a 200 status code with no catalogue items
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []

    # Mock the JSON file loading to return a base catalogue item structure
    mock_load_json.return_value = {
        "organization": {"organization/id": ""},
        "resid": "",
        "wfid": "",
        "localizations": {"en": {"title": ""}},
    }

    # Mock the POST request to return a non-200 status code
    mock_post.return_value.status_code = 400
    mock_post.return_value.text = "Bad Request"

    # Call the function with mock parameters and expect a RuntimeError
    rems_base_url = "http://mock-rems-instance.com"
    headers = {"Authorization": "Bearer mock_token"}
    organization_id = "test-org-id"
    workflow_id = 456
    dataset_identifier = "dataset-identifier"
    resource_id = 789
    title = "Test Catalogue Item"
    with pytest.raises(
        RuntimeError, match="Catalogue Item creation failed: Bad Request"
    ):
        create_or_return_catalogue_item_in_rems(
            organization_id,
            workflow_id,
            dataset_identifier,
            resource_id,
            title,
            rems_base_url,
            headers,
            True,
        )
