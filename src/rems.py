# SPDX-FileCopyrightText: 2024 PNED G.I.E.
#
# SPDX-License-Identifier: Apache-2.0

import requests
import hashlib


def create_or_return_organization_in_rems(rems_base_url: str, headers: dict) -> str:
    name = "Genomic Data Institute"
    short_name = "GDI"
    organization_id = hashlib.md5(name.encode()).hexdigest()
    response = requests.get(
        url=f"{rems_base_url}/api/organizations/{organization_id}", headers=headers
    )
    if response.status_code == 200:
        return organization_id
    elif response.status_code != 404:
        raise RuntimeError(f"Organization retrieval failed: {response.text}")
    response = requests.post(
        url=f"{rems_base_url}/api/organizations/create",
        json={
            "organization/id": organization_id,
            "organization/name": {"en": name},
            "organization/short-name": {"en": short_name},
        },
        headers=headers,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Organization creation failed: {response.text}")
    return organization_id


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

    response = requests.post(
        url=f"{rems_base_url}/api/forms/create",
        json={
            "form/external-title": {"en": "GDI Default Form"},
            "form/internal-name": "GDI Default Form",
            "organization": {"organization/id": organization_id},
            "form/fields": [
                {
                    "field/type": "attachment",
                    "field/title": {"en": "Ethics Approval"},
                    "field/optional": False,
                },
                {
                    "field/type": "attachment",
                    "field/title": {"en": "Project Description"},
                    "field/optional": False,
                },
                {
                    "field/type": "attachment",
                    "field/title": {"en": "Data Analysis Plan"},
                    "field/optional": False,
                },
                {
                    "field/type": "attachment",
                    "field/title": {"en": "Funding Source"},
                    "field/optional": True,
                },
                {
                    "field/type": "attachment",
                    "field/title": {"en": "Peer Review"},
                    "field/optional": False,
                },
            ],
        },
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

    response = requests.post(
        url=f"{rems_base_url}/api/workflows/create",
        json={
            "type": "workflow/default",
            "organization": {"organization/id": organization_id},
            "title": "GDI Default Workflow",
            "forms": [{"form/id": form_id}],
            "voting": {"type": "reviewers-vote"},
        },
        headers=headers,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Workflow creation failed: {response.text}")
    return response.json()["id"]


def create_or_return_resource_in_rems(
    organization_id: str, dataset_id: str, rems_base_url: str, headers: dict
) -> str:
    response = requests.get(
        url=f"{rems_base_url}/api/resources?disabled=false&archived=false&resid={dataset_id}",
        headers=headers,
    )
    if response.status_code != 200 or len(response.json()) > 1:
        raise RuntimeError(f"Resource retrieval failed: {response.text}")
    elif len(response.json()) == 1:
        return response.json()[0]["id"]
    response = requests.post(
        url=f"{rems_base_url}/api/resources/create",
        json={
            "resid": dataset_id,
            "organization": {"organization/id": organization_id},
            "licenses": [],
        },
        headers=headers,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Resource creation failed: {response.text}")
    return response.json()["id"]


def create_or_return_catalogue_item_in_rems(
    organization_id: str,
    workflow_id: int,
    dataset_id: str,
    resource_id: int,
    title: str,
    rems_base_url: str,
    headers: dict,
) -> str:
    response = requests.get(
        url=f"{rems_base_url}/api/catalogue-items?disabled=false&archived=false&resource={dataset_id}",
        headers=headers,
    )
    if response.status_code != 200 or len(response.json()) > 1:
        raise RuntimeError(f"Catalogue Item retrieval failed: {response.text}")
    elif len(response.json()) == 1:
        return response.json()[0]["id"]
    response = requests.post(
        url=f"{rems_base_url}/api/catalogue-items/create",
        json={
            "resid": resource_id,
            "wfid": workflow_id,
            "organization": {"organization/id": organization_id},
            "localizations": {"en": {"title": title}},
            "enabled": True,
        },
        headers=headers,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Catalogue Item creation failed: {response.text}")
    return response.json()["id"]
