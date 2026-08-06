from __future__ import annotations

import argparse
import importlib.metadata as metadata
import shutil
from pathlib import Path

LICENSE_WORDS = ("license", "licence", "copying", "notice", "copyright", "authors")


def metadata_value(dist: metadata.Distribution, key: str) -> str:
    value = dist.metadata.get(key, "")
    return " ".join(str(value).split())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--licenses-dir", required=True, type=Path)
    args = parser.parse_args()

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.licenses_dir.mkdir(parents=True, exist_ok=True)

    rows: list[tuple[str, str, str, str]] = []
    for dist in sorted(metadata.distributions(), key=lambda item: metadata_value(item, "Name").lower()):
        name = metadata_value(dist, "Name") or "Unknown"
        version = dist.version or "Unknown"
        license_name = metadata_value(dist, "License") or metadata_value(dist, "License-Expression") or "See package files"
        url = metadata_value(dist, "Home-page")
        if not url:
            for entry in dist.metadata.get_all("Project-URL", []):
                if "," in entry:
                    _, candidate = entry.split(",", 1)
                    url = candidate.strip()
                    break
        rows.append((name, version, license_name, url))

        package_dir = args.licenses_dir / f"{name}-{version}"
        copied = False
        for file in dist.files or []:
            basename = Path(str(file)).name.lower()
            if not any(word in basename for word in LICENSE_WORDS):
                continue
            source = Path(dist.locate_file(file))
            if not source.is_file():
                continue
            package_dir.mkdir(parents=True, exist_ok=True)
            target = package_dir / Path(str(file)).name
            try:
                shutil.copy2(source, target)
                copied = True
            except OSError:
                continue
        if package_dir.exists() and not copied:
            try:
                package_dir.rmdir()
            except OSError:
                pass

    lines = [
        "# Exact Python package report for this Windows build",
        "",
        "This file is generated from the isolated build environment. It lists",
        "runtime dependencies and build tools installed for the release.",
        "Package-level license and NOTICE files are copied to `licenses/packages`.",
        "",
        "| Package | Version | License metadata | Project URL |",
        "| --- | ---: | --- | --- |",
    ]
    for name, version, license_name, url in rows:
        def esc(value: str) -> str:
            return value.replace("|", "\\|")
        lines.append(f"| {esc(name)} | {esc(version)} | {esc(license_name)} | {esc(url)} |")
    lines.append("")
    args.report.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
