param(
    [switch]$IncludeOAuthClient,
    [switch]$SkipInstaller,
    [switch]$SkipTests
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Version = "0.16.1"
$ReleaseDir = Join-Path $Root "release"
$BuildDir = Join-Path $Root "build"
$DistDir = Join-Path $Root "dist\PT Calendar Manager"
$VenvPython = Join-Path $Root ".venv-build\Scripts\python.exe"

function Find-CompatiblePython {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        foreach ($VersionCandidate in @("3.13", "3.12", "3.11", "3.10")) {
            & py "-$VersionCandidate" -c "import sys; raise SystemExit(0 if (3,10) <= sys.version_info[:2] < (3,14) and sys.maxsize > 2**32 else 1)" 2>$null
            if ($LASTEXITCODE -eq 0) {
                return @("py", "-$VersionCandidate")
            }
        }
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        & python -c "import sys; raise SystemExit(0 if (3,10) <= sys.version_info[:2] < (3,14) and sys.maxsize > 2**32 else 1)"
        if ($LASTEXITCODE -eq 0) {
            return @("python")
        }
    }
    throw "Nie znaleziono 64-bitowego Pythona 3.10-3.13. Zainstaluj Python 3.13 z python.org."
}

$PythonCommand = Find-CompatiblePython
if (-not (Test-Path $VenvPython)) {
    Write-Host "Tworzenie środowiska budowania..."
    if ($PythonCommand.Count -eq 2) {
        & $PythonCommand[0] $PythonCommand[1] -m venv .venv-build
    } else {
        & $PythonCommand[0] -m venv .venv-build
    }
    if ($LASTEXITCODE -ne 0) { throw "Nie udało się utworzyć środowiska." }
}

& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install -r requirements-build.txt
if ($LASTEXITCODE -ne 0) { throw "Instalowanie zależności nie powiodło się." }

if (-not $SkipTests) {
    $env:PYTHONPATH = Join-Path $Root "src"
    & $VenvPython -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw "Testy nie przeszły." }
}

New-Item -ItemType Directory -Force -Path (Join-Path $BuildDir "generated") | Out-Null
& $VenvPython tools\collect_licenses.py `
    --report build\generated\THIRD_PARTY_PACKAGES.md `
    --licenses-dir build\generated\licenses
if ($LASTEXITCODE -ne 0) { throw "Generowanie informacji licencyjnych nie powiodło się." }

& $VenvPython -m pip freeze | Set-Content -Encoding UTF8 build\generated\DEPENDENCIES-FROZEN.txt

Remove-Item -Recurse -Force (Join-Path $Root "dist") -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force (Join-Path $Root "build\PT Calendar Manager") -ErrorAction SilentlyContinue

if ($IncludeOAuthClient) {
    $OAuthFile = Join-Path $Root "release-secrets\client_secret.json"
    if (-not (Test-Path $OAuthFile)) {
        throw "Brak release-secrets\client_secret.json. Plik nie jest tworzony ani pobierany automatycznie."
    }
    $env:PTCM_INCLUDE_OAUTH_CLIENT = "1"
} else {
    Remove-Item Env:PTCM_INCLUDE_OAUTH_CLIENT -ErrorAction SilentlyContinue
}

& $VenvPython -m PyInstaller --noconfirm --clean PTCalendarManager.spec
if ($LASTEXITCODE -ne 0) { throw "Budowanie aplikacji PyInstaller nie powiodło się." }
if (-not (Test-Path (Join-Path $DistDir "PT Calendar Manager.exe"))) {
    throw "PyInstaller nie utworzył oczekiwanego pliku EXE."
}

# PyInstaller 6 places collected data under _internal in one-folder builds.
# Copy user-facing documents to stable public paths next to the EXE as well.
$PublicDocsDir = Join-Path $DistDir "docs"
$PublicLicensesDir = Join-Path $DistDir "licenses"
Remove-Item -Recurse -Force $PublicDocsDir -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force $PublicLicensesDir -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $PublicDocsDir | Out-Null
New-Item -ItemType Directory -Force -Path $PublicLicensesDir | Out-Null
Copy-Item (Join-Path $Root "docs\*") -Destination $PublicDocsDir -Recurse -Force
Copy-Item (Join-Path $Root "licenses\*") -Destination $PublicLicensesDir -Recurse -Force

foreach ($PublicFile in @(
    "LICENSE",
    "LICENSE-NOTICE.md",
    "THIRD_PARTY_NOTICES.md",
    "SOURCE_CODE.md",
    "AUDYT_LICENCJI_I_WYDANIA_0.16.1.md",
    "README.md"
)) {
    Copy-Item (Join-Path $Root $PublicFile) -Destination (Join-Path $DistDir $PublicFile) -Force
}

$GeneratedReport = Join-Path $BuildDir "generated\THIRD_PARTY_PACKAGES.md"
if (Test-Path $GeneratedReport) {
    Copy-Item $GeneratedReport -Destination (Join-Path $DistDir "THIRD_PARTY_PACKAGES.md") -Force
}
$GeneratedLicenseDir = Join-Path $BuildDir "generated\licenses"
if (Test-Path $GeneratedLicenseDir) {
    $PublicPackageLicenses = Join-Path $PublicLicensesDir "packages"
    New-Item -ItemType Directory -Force -Path $PublicPackageLicenses | Out-Null
    Copy-Item (Join-Path $GeneratedLicenseDir "*") -Destination $PublicPackageLicenses -Recurse -Force
}
if ($IncludeOAuthClient) {
    Copy-Item (Join-Path $Root "release-secrets\client_secret.json") -Destination (Join-Path $DistDir "client_secret.json") -Force
}

foreach ($RequiredPublicPath in @(
    "docs\SKROTY_pl.txt",
    "docs\SHORTCUTS_en.txt",
    "docs\DOKUMENTACJA_pl.md",
    "docs\DOCUMENTATION_en.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md"
)) {
    if (-not (Test-Path (Join-Path $DistDir $RequiredPublicPath))) {
        throw "Missing public release file: $RequiredPublicPath"
    }
}

New-Item -ItemType Directory -Force -Path $ReleaseDir | Out-Null
Get-ChildItem $ReleaseDir -Force | Remove-Item -Recurse -Force

$PortableZip = Join-Path $ReleaseDir "pt-calendar-manager-$Version-portable.zip"
Compress-Archive -Path $DistDir -DestinationPath $PortableZip -CompressionLevel Optimal

$SourceStageRoot = Join-Path $BuildDir "source-stage"
$SourceStage = Join-Path $SourceStageRoot "pt-calendar-manager-$Version"
Remove-Item -Recurse -Force $SourceStageRoot -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $SourceStage | Out-Null
$ExcludedNames = @(
    ".git", ".venv", ".venv-build", "build", "dist", "release",
    "release-secrets", "__pycache__"
)
Get-ChildItem $Root -Force | Where-Object { $ExcludedNames -notcontains $_.Name } | ForEach-Object {
    Copy-Item $_.FullName -Destination $SourceStage -Recurse -Force
}
Get-ChildItem $SourceStage -Recurse -Force -Directory | Where-Object { $_.Name -eq "__pycache__" } | Remove-Item -Recurse -Force
Get-ChildItem $SourceStage -Recurse -Force -File | Where-Object {
    $_.Name -in @("client_secret.json", "token.json", "token.dat", "settings.json", "last_error.txt") -or $_.Extension -eq ".pyc"
} | Remove-Item -Force
$SourceZip = Join-Path $ReleaseDir "pt-calendar-manager-$Version-source.zip"
Compress-Archive -Path $SourceStage -DestinationPath $SourceZip -CompressionLevel Optimal

if (-not $SkipInstaller) {
    $Candidates = @(
        (Join-Path $env:ProgramFiles "Inno Setup 7\ISCC.exe"),
        (Join-Path ${env:ProgramFiles(x86)} "Inno Setup 7\ISCC.exe"),
        (Join-Path $env:ProgramFiles "Inno Setup 6\ISCC.exe"),
        (Join-Path ${env:ProgramFiles(x86)} "Inno Setup 6\ISCC.exe")
    )
    $Iscc = $Candidates | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
    if (-not $Iscc) {
        throw "Nie znaleziono Inno Setup 6 ani 7. Zainstaluj Inno Setup albo użyj parametru -SkipInstaller."
    }
    & $Iscc installer\PTCalendarManager.iss
    if ($LASTEXITCODE -ne 0) { throw "Kompilacja instalatora nie powiodła się." }
}

$HashTargets = Get-ChildItem $ReleaseDir -File | Where-Object { $_.Extension -in @(".zip", ".exe") }
$HashLines = foreach ($File in $HashTargets) {
    $Hash = (Get-FileHash -Algorithm SHA256 $File.FullName).Hash.ToLowerInvariant()
    "$Hash  $($File.Name)"
}
$HashLines | Set-Content -Encoding ASCII (Join-Path $ReleaseDir "SHA256SUMS.txt")

Write-Host ""
Write-Host "Gotowe. Pliki wydania znajdują się w:"
Write-Host $ReleaseDir
