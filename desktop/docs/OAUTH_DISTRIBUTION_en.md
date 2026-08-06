# OAuth configuration in the Windows release

PT Calendar Manager uses a **Desktop app** OAuth client.

The official 0.16.3 installer and portable package include the OAuth
configuration so sign-in works on a clean computer without manual file
selection. To build the release, place the deployment file at
`release-secrets\\client_secret.json` and run:

`tools\\build_release.ps1 -IncludeOAuthClient`

The script validates the file before building and again after copying it into
the application directory. The `release-secrets` directory is excluded from
the repository and the source archive. Building without `-IncludeOAuthClient`
remains available for people who create a custom package with their own OAuth
client.

A desktop application runs on the user's device and cannot effectively keep
its OAuth client identifier or client secret confidential. These values are
not a security boundary for user data. Protection instead relies on limited
scopes, user consent, OAuth project verification and encryption of each user's
token with Windows DPAPI.

The public release must use a Desktop app client belonging to the Google
project that completes verification. A person building their own version can
use their own OAuth client.
