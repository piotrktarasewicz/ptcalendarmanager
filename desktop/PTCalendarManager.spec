# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import os

from PyInstaller.utils.hooks import collect_all

root = Path(SPECPATH).resolve()

datas = [
    (str(root / "docs"), "docs"),
    (str(root / "licenses"), "licenses"),
    (str(root / "LICENSE"), "."),
    (str(root / "LICENSE-NOTICE.md"), "."),
    (str(root / "THIRD_PARTY_NOTICES.md"), "."),
    (str(root / "SOURCE_CODE.md"), "."),
    (str(root / "AUDYT_LICENCJI_I_WYDANIA_0.16.1.md"), "."),
    (str(root / "README.md"), "."),
]
binaries = []
hiddenimports = []

for package in ("googleapiclient", "google_auth_oauthlib", "tzdata"):
    package_datas, package_binaries, package_hiddenimports = collect_all(package)
    datas += package_datas
    binaries += package_binaries
    hiddenimports += package_hiddenimports

generated_report = root / "build/generated/THIRD_PARTY_PACKAGES.md"
generated_licenses = root / "build/generated/licenses"
if generated_report.is_file():
    datas.append((str(generated_report), "."))
if generated_licenses.is_dir():
    datas.append((str(generated_licenses), "licenses/packages"))

if os.environ.get("PTCM_INCLUDE_OAUTH_CLIENT") == "1":
    oauth_file = root / "release-secrets/client_secret.json"
    if not oauth_file.is_file():
        raise SystemExit("PTCM_INCLUDE_OAUTH_CLIENT=1, but release-secrets/client_secret.json is missing")
    datas.append((str(oauth_file), "."))

a = Analysis(
    [str(root / "launcher.py")],
    pathex=[str(root / "src")],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="PT Calendar Manager",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(root / "assets/PTCalendarManager.ico"),
    version=str(root / "installer/version_info.txt"),
    manifest=str(root / "installer/app.manifest"),
    uac_admin=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="PT Calendar Manager",
)
