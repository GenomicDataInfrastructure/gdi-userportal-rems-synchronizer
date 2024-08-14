# SPDX-FileCopyrightText: 2024 PNED G.I.E.
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from unittest.mock import patch
from rems import create_or_return_workflow_in_rems


# Test when the workflow already exists in REMS
@patch("requests.get")
def test_create_or_return_workflow_in_rems_exists(mock_get):
    # Mock the GET request to return a response with an existing workflow
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"id": 123, "organization": {"organization/id": "test-org-id"}}
    ]

    # Call the function with mock parameters
    rems_base_url = "http://mock-rems-instance.com"
    headers = {"Authorization": "Bearer mock_token"}
    organization_id = "test-org-id"
    form_id = 456
    workflow_id = create_or_return_workflow_in_rems(
        organization_id, form_id, rems_base_url, headers
    )

    # Assert the function returns the correct workflow ID
    assert workflow_id == 123

    # Assert the GET request was made correctly
    mock_get.assert_called_once_with(
        url=f"{rems_base_url}/api/workflows?disabled=false&archived=false",
        headers=headers,
    )


# Test when the workflow does not exist and needs to be created
@patch("requests.post")
@patch("requests.get")
@patch("rems.load_json")
def test_create_or_return_workflow_in_rems_create(mock_load_json, mock_get, mock_post):
    # Mock the GET request to return a 200 status code with no workflows
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []

    # Mock the JSON file loading to return a base workflow structure
    mock_load_json.return_value = {
        "organization": {"organization/id": ""},
        "forms": [{"form/id": ""}],
    }

    # Mock the POST request to return a 200 status code and a workflow ID
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"id": 789}

    # Call the function with mock parameters
    rems_base_url = "http://mock-rems-instance.com"
    headers = {"Authorization": "Bearer mock_token"}
    organization_id = "test-org-id"
    form_id = 456
    workflow_id = create_or_return_workflow_in_rems(
        organization_id, form_id, rems_base_url, headers
    )

    # Assert the function returns the newly created workflow ID
    assert workflow_id == 789

    # Assert the POST request was made correctly
    expected_workflow = {
        "organization": {"organization/id": organization_id},
        "forms": [{"form/id": form_id}],
    }
    mock_post.assert_called_once_with(
        url=f"{rems_base_url}/api/workflows/create",
        json=expected_workflow,
        headers=headers,
    )


# Test when workflow retrieval fails with a non-200 status code
@patch("requests.get")
def test_create_or_return_workflow_in_rems_retrieval_fails(mock_get):
    # Mock the GET request to return a non-200 status code
    mock_get.return_value.status_code = 500
    mock_get.return_value.text = "Internal Server Error"

    # Call the function with mock parameters and expect a RuntimeError
    rems_base_url = "http://mock-rems-instance.com"
    headers = {"Authorization": "Bearer mock_token"}
    organization_id = "test-org-id"
    form_id = 456
    with pytest.raises(
        RuntimeError, match="Workflow retrieval failed: Internal Server Error"
    ):
        create_or_return_workflow_in_rems(
            organization_id, form_id, rems_base_url, headers
        )


# Test when workflow creation fails with a non-200 status code
@patch("requests.post")
@patch("requests.get")
@patch("rems.load_json")
def test_create_or_return_workflow_in_rems_creation_fails(
    mock_load_json, mock_get, mock_post
):
    # Mock the GET request to return a 200 status code with no workflows
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []

    # Mock the JSON file loading to return a base workflow structure
    mock_load_json.return_value = {
        "organization": {"organization/id": ""},
        "forms": [{"form/id": ""}],
    }

    # Mock the POST request to return a non-200 status code
    mock_post.return_value.status_code = 400
    mock_post.return_value.text = "Bad Request"

    # Call the function with mock parameters and expect a RuntimeError
    rems_base_url = "http://mock-rems-instance.com"
    headers = {"Authorization": "Bearer mock_token"}
    organization_id = "test-org-id"
    form_id = 456
    with pytest.raises(RuntimeError, match="Workflow creation failed: Bad Request"):
        create_or_return_workflow_in_rems(
            organization_id, form_id, rems_base_url, headers
        )
