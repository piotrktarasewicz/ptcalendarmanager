#define MyAppName "PT Calendar Manager"
#define MyAppVersion "0.16.0"
#define MyAppPublisher "PT Projects"
#define MyAppURL "https://ptprojects.app/"
#define MyAppExeName "PT Calendar Manager.exe"

[Setup]
AppId=PTCalendarManager_A6B53B82-7D18-4D50-9A96-A451C44DB65F
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={localappdata}\Programs\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
OutputDir=..\release
OutputBaseFilename=PT-Calendar-Manager-{#MyAppVersion}-Setup
SetupIconFile=..\assets\PTCalendarManager.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
InfoBeforeFile=INFO_BEFORE.txt
UsePreviousAppDir=yes
UsePreviousGroup=yes
CreateUninstallRegKey=yes
Uninstallable=yes
CloseApplications=yes
RestartApplications=no
SetupLogging=yes
AppMutex=PTCalendarManager_A6B53B82-7D18-4D50-9A96-A451C44DB65F
VersionInfoVersion=0.16.0.0
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Accessible desktop application for Google Calendar
VersionInfoCopyright=Copyright (C) 2026 Piotr Tarasewicz
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\PT Calendar Manager\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{group}\Dokumentacja"; Filename: "{app}\docs\DOKUMENTACJA_pl.md"; Languages: polish
Name: "{group}\Documentation"; Filename: "{app}\docs\DOCUMENTATION_en.md"; Languages: english
Name: "{group}\Licencja GNU GPL"; Filename: "{app}\LICENSE"; Languages: polish
Name: "{group}\GNU GPL License"; Filename: "{app}\LICENSE"; Languages: english
Name: "{group}\Odinstaluj {#MyAppName}"; Filename: "{uninstallexe}"; Languages: polish
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"; Languages: english
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\docs\SKROTY_pl.txt"; Description: "{cm:OpenShortcuts}"; Flags: postinstall shellexec skipifsilent unchecked; Languages: polish
Filename: "{app}\docs\SHORTCUTS_en.txt"; Description: "{cm:OpenShortcuts}"; Flags: postinstall shellexec skipifsilent unchecked; Languages: english
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; WorkingDir: "{app}"; Flags: nowait postinstall skipifsilent

[CustomMessages]
polish.OpenShortcuts=Zapoznaj się ze skrótami aplikacji
english.OpenShortcuts=Read the application keyboard shortcuts
polish.DeleteUserDataPrompt=Czy usunąć token Google, ustawienia, konfigurację OAuth i raport błędu z katalogu %%APPDATA%%\PT Calendar Manager?%n%nDomyślna i zalecana odpowiedź to Nie. Wybranie Tak trwale usunie cały aktualny katalog danych aplikacji.
english.DeleteUserDataPrompt=Remove the Google token, settings, OAuth configuration and error report from %%APPDATA%%\PT Calendar Manager?%n%nThe default and recommended answer is No. Choosing Yes permanently removes the complete current application data folder.

[Code]
var
  DeleteUserData: Boolean;

function InitializeUninstall(): Boolean;
begin
  Result := True;
  DeleteUserData :=
    MsgBox(
      CustomMessage('DeleteUserDataPrompt'),
      mbConfirmation,
      MB_YESNO or MB_DEFBUTTON2
    ) = IDYES;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if (CurUninstallStep = usPostUninstall) and DeleteUserData then
    DelTree(
      ExpandConstant('{userappdata}\PT Calendar Manager'),
      True,
      True,
      True
    );
end;
