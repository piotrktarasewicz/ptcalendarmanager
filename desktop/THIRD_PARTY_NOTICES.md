# Komponenty zewnętrzne / Third-party components

PT Calendar Manager is licensed under `GPL-3.0-or-later`. The application is
built with and distributed alongside components under compatible open-source
licenses.

## Główne komponenty wykonawcze / Main runtime components

| Component | Version used by this source release | License |
| --- | ---: | --- |
| CPython | 3.10-3.13 supported; release build recommended with 3.13 | Python Software Foundation License Version 2 and incorporated-component licenses |
| wxPython | 4.2.5 | wxWindows Library Licence 3.1 |
| wxWidgets | bundled by wxPython | wxWindows Library Licence 3.1 |
| google-api-python-client | 2.198.0 | Apache License 2.0 |
| google-auth-oauthlib | 1.4.0 | Apache License 2.0 |
| tzdata | 2026.3 | Apache License 2.0 |

## Narzędzia budowania / Build tools

| Component | Version | License / status |
| --- | ---: | --- |
| PyInstaller | 6.21.0 | GPL-2.0-or-later with the PyInstaller Bootloader Exception; embedded bootloader distribution is permitted by that exception |
| Inno Setup | 6 or 7 | Installer builder; the compiler itself is not bundled with PT Calendar Manager |

## Zależności pośrednie / Transitive dependencies

The Windows release script creates an exact report named
`THIRD_PARTY_PACKAGES.md` from the Python environment used to build the
binary. It also copies license, copyright and NOTICE files exposed by installed
packages into the `licenses/packages` directory included with the portable
build and installer.

This generated report is authoritative for a particular binary build. It must
be distributed together with that binary because dependency versions can
change independently of this summary.

## Pełne teksty licencji / Full license texts

The `licenses` directory contains the principal license texts needed before a
Windows build. The release process adds the exact package-level notices found
in the build environment.
