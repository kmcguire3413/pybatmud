; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "PyBatMudClient"
#define MyAppVersion "1.0"
#define MyAppPublisher "Leonard Kevin McGuire Jr"
#define MyAppURL "https://github.com/kmcguire3413/pybatmud"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{3FAD2467-6542-4278-A10C-8C5643056A6D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputBaseFilename=setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
;Source: "C:\Users\kmcguire\Desktop\kmcg3413.net\pybatmud\styles\*"; DestDir: "{app}\styles"; Flags: ignoreversion recursesubdirs createallsubdirs
;Source: "C:\Users\kmcguire\Desktop\kmcg3413.net\pybatmud\plug\*"; DestDir: "{app}\plug"; Flags: ignoreversion recursesubdirs createallsubdirs
;Source: "C:\Users\kmcguire\Desktop\kmcg3413.net\pybatmud\pkg\*"; DestDir: "{app}\pkg"; Flags: ignoreversion recursesubdirs createallsubdirs
;Source: "C:\Users\kmcguire\Desktop\kmcg3413.net\pybatmud\media\*"; DestDir: "{app}\media"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\kmcguire\Desktop\kmcg3413.net\pybatmud\updater.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\kmcguire\Desktop\kmcg3413.net\pybatmud\updater.lnk"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Python34MinQt\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\Start"; Filename: "{app}\updater.lnk"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

