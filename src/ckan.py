# SPDX-FileCopyrightText: 2024 PNED G.I.E.
#
# SPDX-License-Identifier: Apache-2.0

import requests


def get_packages_count(ckan_base_url: str, verify_ssl: bool) -> int:
    response = requests.get(
        url=f"{ckan_base_url}/api/3/action/package_search?rows=0",
        verify=verify_ssl,
    ).json()
    return response["result"]["count"]


def get_packages(start, rows, ckan_base_url: str, verify_ssl: bool) -> list:
    response = requests.get(
        url=f"{ckan_base_url}/api/3/action/package_search?rows={rows}&start={start}",
        verify=verify_ssl,
    ).json()
    return response["result"]["results"]
