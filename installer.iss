#ifndef AppVersion
  #define AppVersion "0"
#endif

[Setup]
AppId={{B3F0A6C4-9D2E-4B7A-8F5C-1E6D3A9B0C2F}
AppName=Alex Videoer
AppVersion={#AppVersion}
; Per-user install: no UAC prompt, and the app can replace its own exe when self-updating
PrivilegesRequired=lowest
DefaultDirName={localappdata}\Programs\Alex Videoer
DisableDirPage=yes
DisableProgramGroupPage=yes
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\Alex Videoer.exe
OutputDir=installer
OutputBaseFilename=AlexVideoerSetup

[Languages]
Name: "norwegian"; MessagesFile: "compiler:Languages\Norwegian.isl"

[Files]
Source: "dist\Alex Videoer.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autodesktop}\Alex Videoer"; Filename: "{app}\Alex Videoer.exe"
Name: "{autoprograms}\Alex Videoer"; Filename: "{app}\Alex Videoer.exe"

[Run]
Filename: "{app}\Alex Videoer.exe"; Description: "{cm:LaunchProgram,Alex Videoer}"; Flags: nowait postinstall skipifsilent
