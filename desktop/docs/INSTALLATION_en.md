# Installing and updating PT Calendar Manager

## Installer

1. Run the setup file.
2. Choose the installer language.
3. Read the license, privacy and independent-product information.
4. Change the destination folder only when needed.
5. Optionally create a desktop shortcut.
6. Choose Install.
7. The final page can open program help and keyboard shortcuts. The application starts directly in the Help view.

The installer does not require administrator privileges. The application is
installed for the current Windows user.

## Updates

A newer installer can be run without uninstalling the previous version. The
stable AppId updates the same application. The Google token and settings in
`%APPDATA%\PT Calendar Manager` are preserved.

## Uninstalling

The uninstaller asks whether local user data should be removed. The default
No answer preserves sign-in and settings for a later installation.

Choosing Yes removes the complete `%APPDATA%\PT Calendar Manager` folder,
including the token, OAuth client configuration, settings and last error report.

## Portable build

Extract the complete archive to a normal folder and run
`PT Calendar Manager.exe`. Portable means that no installer is used; user data
is still stored in `%APPDATA%\PT Calendar Manager`, and the DPAPI token remains
tied to the Windows account.
