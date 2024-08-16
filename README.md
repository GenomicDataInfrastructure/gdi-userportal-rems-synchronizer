<!--
SPDX-FileCopyrightText: 2024 PNED G.I.E.

SPDX-License-Identifier: CC-BY-4.0
-->

[![REUSE status](https://api.reuse.software/badge/github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer)](https://api.reuse.software/info/github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer)
![example workflow](https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/actions/workflows/main.yml/badge.svg)
![example workflow](https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/actions/workflows/test.yml/badge.svg)
![example workflow](https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/actions/workflows/release.yml/badge.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=GenomicDataInfrastructure_gdi-userportal-rems-synchronizer&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=GenomicDataInfrastructure_gdi-userportal-rems-synchronizer)
[![GitHub contributors](https://img.shields.io/github/contributors/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer)](https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/graphs/contributors)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)

<div style="display: flex; justify-content: center; padding: 20px;">
  <img src="header-logo.svg" alt="European Genomic Data Infrastructure Logo" width="300">
</div>

# GDI User Portal - REMS Synchronizer

The GDI User Portal REMS Synchronizer serves as the data steward-friendly command line interface for REMS management, responsible to fetch datasets from a CKAN, loading them into REMS.

Here, the data steward can easily configure the workflow and form, and replicate it throughout the entire dataset, with zero headache.

## Installation

### Locally

Before using the REMS Synchronizer, you need to ensure python is available:

`pip install -r requirements.txt`

You also have to create a new `.env` file in the root directory, and copy the content of `.env.example` into the new file. Please ensure you modified the environment variables accordingly to your setup.

### Using Docker

Alternatively, you can run the compose file that provides a running instance of the application.

To start the containers:
- For Podman: `podman compose up -d`
- For Docker (new version): `docker compose up -d`
- For Docker (older version): `docker-compose up -d`

Choose the command that matches your container runtime. We recommend using `podman compose up` for most setups.

## License

- All original source code is licensed under [Apache-2.0](./LICENSES/Apache-2.0.txt).
- All documentation and images are licensed under [CC-BY-4.0](./LICENSES/CC-BY-4.0.txt).
- For more accurate information, check the individual files.
