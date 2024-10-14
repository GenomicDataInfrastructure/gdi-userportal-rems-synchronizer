<!--
SPDX-FileCopyrightText: 2024 PNED G.I.E.

SPDX-License-Identifier: CC-BY-4.0
-->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

chore: move form and workflow initialization to data/*.json
chore: migrate base docker image to UBI 9
doc: update README and CONTRIBUTING.md

### Deprecated

### Removed

### Fixed

### Security

## [v1.3.0] - 2024-10-07

### Added
* feat: renovate integration by @sehaartuc in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/3

### Changed
* chore(deps): update fsfe/reuse-action action to v4 by @LNDS-Sysadmins in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/9
* chore(deps): update docker/build-push-action action to v6 by @LNDS-Sysadmins in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/8
* chore(deps): update python docker tag to v3.12 by @LNDS-Sysadmins in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/7
* chore(deps): update oss-review-toolkit/ort-ci-github-action digest to 81698a9 by @LNDS-Sysadmins in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/6
* chore(deps): update docker/metadata-action digest to a64d048 by @LNDS-Sysadmins in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/5
* chore(deps): update docker/login-action digest to 0d4c9c5 by @LNDS-Sysadmins in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/4
* chore: refactoring by @brunopacheco1 in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/32
* chore(deps): update registry.access.redhat.com/ubi9/python-312 docker tag to v1-20.1723128194 by @LNDS-Sysadmins in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/33
* chore: move json into data files by @brunopacheco1 in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/34
* chore(deps): update registry.access.redhat.com/ubi9/python-312 docker tag to v1-20.1724040322 by @LNDS-Sysadmins in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/36
* chore: add details to configure REMS-Synchronizer by @brunopacheco1 in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/37
* chore: add verify_ssl flag by @brunopacheco1 in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/38
* chore(deps): update registry.access.redhat.com/ubi9/python-312 docker tag to v1-25.1725907708 by @LNDS-Sysadmins in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/39
* chore(deps): update dependency pytest to v8.3.3 by @LNDS-Sysadmins in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/40
* chore(deps): update registry.access.redhat.com/ubi9/python-312 docker tag to v1-25.1726664318 by @LNDS-Sysadmins in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/41
* chore(deps): update aquasecurity/trivy-action action to v0.25.0 by @LNDS-Sysadmins in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/42
* chore(deps): update dependency black to v24.10.0 by @LNDS-Sysadmins in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/43

### Security
* chore(deps): upgrade requests to remove vulnerability by @brunopacheco1 in https://github.com/GenomicDataInfrastructure/gdi-userportal-rems-synchronizer/pull/45

## [v1.2.0] - 2024-06-12

### Added

* fix(ci): change trivy severity level by @brunopacheco1 
* chore: add voting to workflow creation by @brunopacheco1 
* chore: add extra fields to default form by @brunopacheco1 
* chore: add .gitignore by @brunopacheco1 
* chore: move rems-synchronizer to another repository by @brunopacheco1 

### Changed

chore: move rems-synchronizer to another repository
