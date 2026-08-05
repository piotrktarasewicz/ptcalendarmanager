from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True, slots=True)
class RestartLaunch:
    command: tuple[str, ...]
    working_directory: Path


def build_restart_launch(
    *,
    executable: str | None = None,
    arguments: Sequence[str] | None = None,
    frozen: bool | None = None,
) -> RestartLaunch:
    executable_path = Path(executable or sys.executable).resolve()
    argv = list(arguments if arguments is not None else sys.argv)
    is_frozen = bool(getattr(sys, "frozen", False)) if frozen is None else bool(frozen)

    if is_frozen:
        return RestartLaunch(
            command=(str(executable_path), *tuple(argv[1:])),
            working_directory=executable_path.parent,
        )

    if not argv:
        return RestartLaunch(
            command=(str(executable_path),),
            working_directory=executable_path.parent,
        )

    launcher_path = Path(argv[0])
    if not launcher_path.is_absolute():
        launcher_path = (Path.cwd() / launcher_path).resolve()
    else:
        launcher_path = launcher_path.resolve()

    return RestartLaunch(
        command=(str(executable_path), str(launcher_path), *tuple(argv[1:])),
        working_directory=launcher_path.parent,
    )


def launch_current_application() -> subprocess.Popen[bytes]:
    launch = build_restart_launch()
    kwargs: dict[str, object] = {
        "cwd": str(launch.working_directory),
        "close_fds": True,
    }
    if os.name == "nt":
        creation_flags = int(getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0))
        creation_flags |= int(getattr(subprocess, "DETACHED_PROCESS", 0))
        if creation_flags:
            kwargs["creationflags"] = creation_flags
    return subprocess.Popen(list(launch.command), **kwargs)
