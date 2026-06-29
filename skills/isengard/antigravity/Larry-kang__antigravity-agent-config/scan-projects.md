---
description: 掃描所有專案的 Agent 設定狀態
---

# Scan Projects Agent Configuration

此工作流程用於掃描 `d:/Dev/GitHub` 下的所有專案，檢查是否已建立專案層級的 `.agent` 設定。

1.  List all directories in `d:/Dev/GitHub`
    ```bash
    Get-ChildItem -Path "d:/Dev/GitHub" -Directory | ForEach-Object {
        $agentPath = Join-Path $_.FullName ".agent"
        if (Test-Path $agentPath) {
            Write-Host "✅ [$($_.Name)] has .agent config"
        } else {
            Write-Host "⚠️ [$($_.Name)] missing .agent config"
        }
    }
    ```
