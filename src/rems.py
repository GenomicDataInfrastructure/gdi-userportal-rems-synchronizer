# SPDX-FileCopyrightText: 2024 PNED G.I.E.
#
# SPDX-License-Identifier: Apache-2.0

import requests
import hashlib
import json
from typing import Dict
import copy


def load_json(path: str) -> Dict:
    try:
        with open(path, "r") as file:
            return json.load(file)
    except (IOError, json.JSONDecodeError) as e:
        raise ValueError(f"Error loading JSON from {path}: {str(e)}")


def create_or_return_organization_in_rems(rems_base_url: str, headers: dict) -> str:
    base_workflow_organization = load_json("./data/workflow_organization.json")
    name = base_workflow_organization["organization/name"]["en"]
    organization_id = hashlib.md5(name.encode()).hexdigest()

    workflow_organization = copy.deepcopy(base_workflow_organization)
    workflow_organization["organization/id"] = organization_id

    response = requests.get(
        url=f"{rems_base_url}/api/organizations/{organization_id}", headers=headers
    )
    if response.status_code == 200:
        return organization_id
    elif response.status_code != 404:
        raise RuntimeError(f"Organization retrieval failed: {response.text}")
    response = requests.post(
        url=f"{rems_base_url}/api/organizations/create",
        json=workflow_organization,
        headers=headers,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Organization creation failed: {response.text}")
    return workflow_organization["organization/id"]


def create_or_return_form_in_rems(
    organization_id: str, rems_base_url: str, headers: dict
) -> int:
    response = requests.get(
        url=f"{rems_base_url}/api/forms?disabled=false&archived=false",
        headers=headers,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Workflow retrieval failed: {response.text}")

    result = [
        form
        for form in response.json()
        if form["organization"]["organization/id"] == organization_id
    ]

    if len(result) > 0:
        return result[0]["form/id"]

    base_form = load_json("./data/form.json")
    base_form_str = json.dumps(base_form)
    form_checksum = hashlib.md5(base_form_str.encode()).hexdigest()
    internal_name = base_form["form/external-title"]["en"] + " - " + form_checksum

    form = copy.deepcopy(base_form)
    form["organization"]["organization/id"] = organization_id
    form["form/internal-name"] = internal_name

    response = requests.post(
        url=f"{rems_base_url}/api/forms/create",
        json=form,
        headers=headers,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Workflow creation failed: {response.text}")
    return response.json()["id"]


def create_or_return_workflow_in_rems(
    organization_id: str, form_id: int, rems_base_url: str, headers: dict
) -> int:
    response = requests.get(
        url=f"{rems_base_url}/api/workflows?disabled=false&archived=false",
        headers=headers,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Workflow retrieval failed: {response.text}")

    result = [
        workflow
        for workflow in response.json()
        if workflow["organization"]["organization/id"] == organization_id
    ]

    if len(result) > 0:
        return result[0]["id"]

    base_workflow = load_json("./data/workflow.json")

    workflow = copy.deepcopy(base_workflow)
    workflow["organization"]["organization/id"] = organization_id
    workflow["forms"][0]["form/id"] = form_id

    response = requests.post(
        url=f"{rems_base_url}/api/workflows/create",
        json=workflow,
        headers=headers,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Workflow creation failed: {response.text}")
    return response.json()["id"]


def create_or_return_resource_in_rems(
    organization_id: str, dataset_identifier: str, rems_base_url: str, headers: dict
) -> str:
    response = requests.get(
        url=f"{rems_base_url}/api/resources?disabled=false&archived=false&resid={dataset_identifier}",
        headers=headers,
    )
    if response.status_code != 200 or len(response.json()) > 1:
        raise RuntimeError(f"Resource retrieval failed: {response.text}")
    elif len(response.json()) == 1:
        return response.json()[0]["id"]

    base_resource = load_json("./data/resource.json")

    resource = copy.deepcopy(base_resource)
    resource["organization"]["organization/id"] = organization_id
    resource["resid"] = dataset_identifier

    response = requests.post(
        url=f"{rems_base_url}/api/resources/create",
        json=resource,
        headers=headers,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Resource creation failed: {response.text}")
    return response.json()["id"]


def create_or_return_catalogue_item_in_rems(
    organization_id: str,
    workflow_id: int,
    dataset_identifier: str,
    resource_id: int,
    title: str,
    rems_base_url: str,
    headers: dict,
) -> str:
    response = requests.get(
        url=f"{rems_base_url}/api/catalogue-items?disabled=false&archived=false&resource={dataset_identifier}",
        headers=headers,
    )
    if response.status_code != 200 or len(response.json()) > 1:
        raise RuntimeError(f"Catalogue Item retrieval failed: {response.text}")
    elif len(response.json()) == 1:
        return response.json()[0]["id"]

    base_catalogue_item = load_json("./data/catalogue_item.json")

    catalogue_item = copy.deepcopy(base_catalogue_item)
    catalogue_item["organization"]["organization/id"] = organization_id
    catalogue_item["resid"] = resource_id
    catalogue_item["wfid"] = workflow_id
    catalogue_item["localizations"]["en"]["title"] = title

    response = requests.post(
        url=f"{rems_base_url}/api/catalogue-items/create",
        json=catalogue_item,
        headers=headers,
    )

    if response.status_code != 200:
        raise RuntimeError(f"Catalogue Item creation failed: {response.text}")
    return response.json()["id"]
