# Building Google Calendar Manager

The public repository contains the add-on source code, documentation and translations. It intentionally does not contain the bundled Python dependency directory or real Google OAuth credentials.

## Requirements

- Windows
- Python 3.13 64-bit, matching the Python generation used by NVDA 2026.1
- PowerShell or another ZIP-capable shell

## 1. Prepare a build directory

Create an empty `build` directory and copy the repository contents into it, excluding `.git`, `build`, `dist` and other ignored files.

## 2. Install bundled dependencies

Install runtime dependencies directly into the add-on's `lib` directory:

```powershell
py -3.13 -m pip install --upgrade --target build\globalPlugins\googleCalendarManager\lib -r requirements.txt
```

The resulting release package must include this `lib` directory because users do not need a separate Python installation.

Native `.pyd` files must be compatible with CPython 3.13 AMD64. Do not copy native modules from a Python 3.11 build.

## 3. Add required standard-library packages

NVDA does not include every module from the full Python standard library. Copy the Python 3.13 versions of `email` and `wsgiref` into the bundled `lib` directory:

```powershell
$lib = "build\globalPlugins\googleCalendarManager\lib"
$stdlib = py -3.13 -c "import sysconfig; print(sysconfig.get_path('stdlib'))"

Copy-Item -LiteralPath (Join-Path $stdlib "email") -Destination (Join-Path $lib "email") -Recurse -Force
Copy-Item -LiteralPath (Join-Path $stdlib "wsgiref") -Destination (Join-Path $lib "wsgiref") -Recurse -Force
```

Verify the runtime imports:

```powershell
py -3.13 -B -c "import sys; sys.path.insert(0,r'build\globalPlugins\googleCalendarManager\lib'); import email,wsgiref,google_auth_oauthlib.flow,googleapiclient,google.auth; print('Runtime imports OK')"
```

## 4. Add the OAuth desktop configuration

Copy:

```text
globalPlugins/googleCalendarManager/client_secret.example.json
```

to:

```text
build/globalPlugins/googleCalendarManager/client_secret.json
```

Replace the placeholders with credentials for the Google OAuth desktop application used by the distributed add-on.

Do not commit the real `client_secret.json` file. OAuth desktop client credentials are distributed in the compiled add-on package, but they must not be stored in the public source tree.

## 5. Translations

The repository includes both `nvda.po` and the compiled `nvda.mo`. When translation text changes, rebuild the MO file with `polib` or another gettext-compatible tool.

## 6. Create the add-on package

ZIP the contents of the build directory, not the build directory itself, and give the archive the `.nvda-addon` extension.

The archive root must contain at least:

- `manifest.ini`
- `globalPlugins/`
- `locale/`
- `docs/`

## 7. Release checks

Before publishing:

1. Run syntax checks on all Python files using Python 3.13 with the `-B` option.
2. Verify imports of `email`, `wsgiref`, `google_auth_oauthlib.flow`, `googleapiclient` and `google.auth`.
3. Confirm that bundled native modules are compatible with CPython 3.13 AMD64.
4. Confirm that `token.json`, `settings.json`, diagnostic files, `__pycache__` directories and `.pyc` files are absent.
5. Confirm that the public source tree contains only `client_secret.example.json`, while the installation package contains the required `client_secret.json`.
6. Confirm that `manifest.ini` requires NVDA 2026.1 or newer.
7. Test installation, Google sign-in and the principal keyboard workflows in a clean portable copy of NVDA.
