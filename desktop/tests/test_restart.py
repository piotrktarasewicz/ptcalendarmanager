import tempfile
import unittest
from pathlib import Path

from gcm_core.restart import build_restart_launch


class RestartLaunchTests(unittest.TestCase):
    def test_development_launch_reuses_python_and_launcher(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            launcher = root / "launcher.py"
            launcher.write_text("", encoding="utf-8")
            launch = build_restart_launch(
                executable=str(root / "python.exe"),
                arguments=[str(launcher), "--example"],
                frozen=False,
            )
            self.assertEqual(
                launch.command,
                (str((root / "python.exe").resolve()), str(launcher.resolve()), "--example"),
            )
            self.assertEqual(launch.working_directory, root.resolve())

    def test_frozen_launch_reuses_the_executable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "GCM by Piotrek.exe"
            launch = build_restart_launch(
                executable=str(executable),
                arguments=[str(executable), "--example"],
                frozen=True,
            )
            self.assertEqual(
                launch.command,
                (str(executable.resolve()), "--example"),
            )
            self.assertEqual(launch.working_directory, executable.resolve().parent)

    def test_empty_arguments_still_restart_the_interpreter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "python.exe"
            launch = build_restart_launch(
                executable=str(executable),
                arguments=[],
                frozen=False,
            )
            self.assertEqual(launch.command, (str(executable.resolve()),))


if __name__ == "__main__":
    unittest.main()
