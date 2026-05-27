#define MyAppName "Professor Voice Assistant"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Professor Voice Assistant"
#define MyAppExeName "Professor.exe"

[Setup]
AppId={{8E78B9BC-20E7-46D9-87F7-2B59DBF1A401}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\Professor Voice Assistant
DefaultGroupName=Professor Voice Assistant
AllowNoIcons=yes
OutputDir=..\installer-output
OutputBaseFilename=ProfessorSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "..\dist\Professor\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Professor Voice Assistant"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Professor Voice Assistant"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch Professor Voice Assistant"; Flags: nowait postinstall skipifsilent
