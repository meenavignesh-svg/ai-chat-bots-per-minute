#define MyAppName "HelixMind Bio AI"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "HelixMind Bio AI"
#define MyAppExeName "HelixMindBioAI.exe"

[Setup]
AppId={{BB3E7873-7E6B-47D1-9B0E-C902BE7AB224}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\HelixMind Bio AI
DefaultGroupName=HelixMind Bio AI
AllowNoIcons=yes
OutputDir=..\installer-output
OutputBaseFilename=HelixMindBioAISetup
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
Source: "..\dist\HelixMindBioAI\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\HelixMind Bio AI"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\HelixMind Bio AI"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch HelixMind Bio AI"; Flags: nowait postinstall skipifsilent
