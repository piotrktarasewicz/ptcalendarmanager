# OAuth configuration in the Windows release

PT Calendar Manager uses a **Desktop app** OAuth client.

The release script does not include `client_secret.json` by default. To create
an internal build containing a specific deployment configuration, place the
file at `release-secrets\\client_secret.json` and run:

`tools\\build_release.ps1 -IncludeOAuthClient`

The `release-secrets` directory is excluded from the repository and the source
archive.

A desktop application runs on the user's device and cannot effectively keep
its OAuth client identifier or client secret confidential. These values are
not a security boundary for user data. Protection instead relies on limited
scopes, user consent, OAuth project verification and encryption of each user's
token with Windows DPAPI.

The public release must use a Desktop app client belonging to the Google
project that completes verification. A person building their own version can
use their own OAuth client.
