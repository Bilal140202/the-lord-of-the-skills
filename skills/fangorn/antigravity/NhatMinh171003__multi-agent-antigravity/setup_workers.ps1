param(
    [string]$WorkspaceDir = (Join-Path $PSScriptRoot "..\.." | Get-Item).FullName
)

$pipelineFile = Join-Path $WorkspaceDir "AI\agent-mcp\pipeline.json"

if (-Not (Test-Path $pipelineFile)) {
    Write-Host "Loi: Khong tim thay file pipeline.json tai $pipelineFile" -ForegroundColor Red
    exit 1
}

# Doc config
Write-Host "Dang doc kien truc tu $pipelineFile..." -ForegroundColor Cyan
$jsonContent = Get-Content -Raw -Path $pipelineFile
$pipelineData = $jsonContent | ConvertFrom-Json
$roles = $pipelineData.sequence

# Tim file thuc thi Antigravity
Write-Host "Tim kiem duong dan cai dat Antigravity..." -ForegroundColor Cyan
$antigravityExe = "$env:LOCALAPPDATA\Programs\Antigravity\Antigravity.exe"

if (-Not (Test-Path $antigravityExe)) {
    Write-Host "Loi: Khong the tim thay file Antigravity.exe tai $antigravityExe." -ForegroundColor Red
    exit 1
}

Write-Host "Antigravity Exe: $antigravityExe"

# Bang mau Identity cho tung Role (khong dung emoji de tranh loi encoding)
$roleColors = @{
    "PLANNER"  = @{ border = "#00BFFF"; label = "[PLANNER]"  }
    "CODER"    = @{ border = "#00FF88"; label = "[CODER]"    }
    "TESTER"   = @{ border = "#FF8800"; label = "[TESTER]"   }
    "REVIEWER" = @{ border = "#CC44FF"; label = "[REVIEWER]" }
    "REPORTER" = @{ border = "#FFD700"; label = "[REPORTER]" }
}
$defaultColor = @{ border = "#888888"; label = "[AGENT]" }

# Tao Window Script Host doi tuong
$wshShell = New-Object -ComObject WScript.Shell
$desktopPath = [System.Environment]::GetFolderPath('Desktop')
$profilesDir = Join-Path $WorkspaceDir ".profiles"

if (-Not (Test-Path $profilesDir)) {
    New-Item -ItemType Directory -Path $profilesDir | Out-Null
}

Write-Host "Tien hanh cau hinh Profile va Shortcut..." -ForegroundColor Cyan

foreach ($role in $roles) {
    $shortcutName = "AG_$role.lnk"
    $shortcutPath = Join-Path $desktopPath $shortcutName

    # Path Antigravity se luu Memory/Auth cho tung cua so
    $targetUserDataDir = Join-Path $profilesDir $role
    $userSettingsDir = Join-Path $targetUserDataDir "User"

    # Lay mau tuong ung voi role
    $color = if ($roleColors.ContainsKey($role)) { $roleColors[$role] } else { $defaultColor }

    # Tao thu muc profile
    if (-Not (Test-Path $userSettingsDir)) {
        New-Item -ItemType Directory -Path $userSettingsDir -Force | Out-Null
    }

    # Ghi settings.json de to mau vien + tieu de cua so
    $settingsJson = "{`n  `"window.title`": `"$($color.label) Iruka Workspace`",`n  `"workbench.colorCustomizations`": {`n    `"titleBar.activeBackground`": `"$($color.border)22`",`n    `"titleBar.activeForeground`": `"#FFFFFF`",`n    `"titleBar.border`": `"$($color.border)`",`n    `"activityBar.background`": `"$($color.border)18`",`n    `"activityBar.activeBorder`": `"$($color.border)`",`n    `"statusBar.background`": `"$($color.border)`",`n    `"statusBar.foreground`": `"#000000`",`n    `"tab.activeBorderTop`": `"$($color.border)`"`n  }`n}"
    $settingsJson | Out-File -FilePath (Join-Path $userSettingsDir "settings.json") -Encoding utf8
    Write-Host "   -> Ghi Color Identity $($color.label) -> Profile: $role" -ForegroundColor DarkYellow

    # Copy mcp_config.json vao profile de Worker doc duoc iruka-hub tool
    $globalMcpConfig = "$env:USERPROFILE\.gemini\antigravity\mcp_config.json"
    if (Test-Path $globalMcpConfig) {
        Copy-Item -Path $globalMcpConfig -Destination (Join-Path $targetUserDataDir "mcp_config.json") -Force
        Write-Host "   -> Copy mcp_config.json -> Profile $role" -ForegroundColor Cyan
    } else {
        Write-Host "   -> CANH BAO: Khong tim thay $globalMcpConfig" -ForegroundColor Red
    }

    # Tao Shortcut
    $shortcut = $wshShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $antigravityExe

    # --user-data-dir: Co lap Cookie/Auth
    # --extensions-dir: Dung chung Extension goc
    $extensionDir = Join-Path $env:USERPROFILE ".antigravity\extensions"
    $workspaceArg = "`"$WorkspaceDir`""

    $shortcut.Arguments = "--user-data-dir=`"$targetUserDataDir`" --extensions-dir=`"$extensionDir`" $workspaceArg"

    $iconPath = Join-Path $WorkspaceDir "AI\agent-mcp\icon_$role`_v2.ico"
    if (Test-Path $iconPath) {
        $shortcut.IconLocation = $iconPath
    } else {
        $shortcut.IconLocation = "$antigravityExe, 0"
    }

    $shortcut.Description = "Iruka Core Agent: $role (Co lap Session)"
    $shortcut.Save()

    Write-Host " -> OK! Da tao Shortcut: $shortcutName" -ForegroundColor Green
}

Write-Host ""
Write-Host "HOAN TAT! $($roles.Count) Agent san sang!" -ForegroundColor Magenta
Write-Host "Khoi dong lai cac cua so Antigravity de nap mcp_config moi." -ForegroundColor Yellow
Start-Sleep -Seconds 2
