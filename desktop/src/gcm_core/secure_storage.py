# Copyright (C) 2026 Piotr Tarasewicz
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import ctypes
import os
import sys
from ctypes import wintypes
from pathlib import Path

TOKEN_FILE_MAGIC = b"PTCM-DPAPI-1\n"
CRYPTPROTECT_UI_FORBIDDEN = 0x1


class _DataBlob(ctypes.Structure):
    _fields_ = [
        ("cbData", wintypes.DWORD),
        ("pbData", ctypes.POINTER(ctypes.c_ubyte)),
    ]


def _input_blob(data: bytes) -> tuple[_DataBlob, ctypes.Array[ctypes.c_char]]:
    buffer = ctypes.create_string_buffer(data)
    pointer = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte))
    return _DataBlob(len(data), pointer), buffer


def _require_windows() -> None:
    if sys.platform != "win32":
        raise OSError("Windows DPAPI is only available on Windows.")


def protect_bytes(data: bytes, *, description: str = "PT Calendar Manager OAuth token") -> bytes:
    """Protect bytes for the current Windows user with DPAPI."""
    _require_windows()
    input_blob, _input_buffer = _input_blob(bytes(data))
    output_blob = _DataBlob()
    crypt32 = ctypes.windll.crypt32
    kernel32 = ctypes.windll.kernel32
    crypt32.CryptProtectData.argtypes = [
        ctypes.POINTER(_DataBlob),
        wintypes.LPCWSTR,
        ctypes.POINTER(_DataBlob),
        wintypes.LPVOID,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(_DataBlob),
    ]
    crypt32.CryptProtectData.restype = wintypes.BOOL
    kernel32.LocalFree.argtypes = [wintypes.HLOCAL]
    kernel32.LocalFree.restype = wintypes.HLOCAL
    success = crypt32.CryptProtectData(
        ctypes.byref(input_blob),
        description,
        None,
        None,
        None,
        CRYPTPROTECT_UI_FORBIDDEN,
        ctypes.byref(output_blob),
    )
    if not success:
        raise ctypes.WinError()
    try:
        return ctypes.string_at(output_blob.pbData, output_blob.cbData)
    finally:
        kernel32.LocalFree(ctypes.cast(output_blob.pbData, wintypes.HLOCAL))


def unprotect_bytes(data: bytes) -> bytes:
    """Unprotect DPAPI bytes for the current Windows user."""
    _require_windows()
    input_blob, _input_buffer = _input_blob(bytes(data))
    output_blob = _DataBlob()
    crypt32 = ctypes.windll.crypt32
    kernel32 = ctypes.windll.kernel32
    crypt32.CryptUnprotectData.argtypes = [
        ctypes.POINTER(_DataBlob),
        ctypes.POINTER(wintypes.LPWSTR),
        ctypes.POINTER(_DataBlob),
        wintypes.LPVOID,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(_DataBlob),
    ]
    crypt32.CryptUnprotectData.restype = wintypes.BOOL
    kernel32.LocalFree.argtypes = [wintypes.HLOCAL]
    kernel32.LocalFree.restype = wintypes.HLOCAL
    success = crypt32.CryptUnprotectData(
        ctypes.byref(input_blob),
        None,
        None,
        None,
        None,
        CRYPTPROTECT_UI_FORBIDDEN,
        ctypes.byref(output_blob),
    )
    if not success:
        raise ctypes.WinError()
    try:
        return ctypes.string_at(output_blob.pbData, output_blob.cbData)
    finally:
        kernel32.LocalFree(ctypes.cast(output_blob.pbData, wintypes.HLOCAL))


def write_protected_text(path: Path, text: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    encrypted = protect_bytes(str(text).encode("utf-8"))
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_bytes(TOKEN_FILE_MAGIC + encrypted)
    os.replace(temp, path)


def read_protected_text(path: Path) -> str:
    path = Path(path)
    payload = path.read_bytes()
    if not payload.startswith(TOKEN_FILE_MAGIC):
        raise ValueError("Unsupported encrypted token file format.")
    decrypted = unprotect_bytes(payload[len(TOKEN_FILE_MAGIC):])
    return decrypted.decode("utf-8")
