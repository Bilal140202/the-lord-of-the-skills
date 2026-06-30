## 💻 PowerShell Command Rules (Windows)

> The environment is Windows PowerShell. Avoid Bashisms.

### 💀 Critical Syntax Changes
| Bash | PowerShell | Note |
|------|------------|------|
| `&&` | `;` | **CRITICAL**: No `&&` chaining support |
| `export VAR=val` | `$env:VAR = 'val'` | Setting environment variables |
| `cmd > file` | `cmd | Out-File file -Encoding UTF8` | Fixes encoding issues |
| `$(cmd)` | `(cmd)` | Sub-expression syntax |

### 🛠️ Common Equivalents
| Action | Bash | PowerShell |
|--------|------|------------|
| API Test (JSON) | `curl -X POST -d '{}' URL` | `Invoke-RestMethod -Method Post -Body '{}' -ContentType 'application/json' -Uri URL` |
| Download File | `wget URL` or `curl -O URL` | `Invoke-WebRequest -Uri URL -OutFile file` |
| Recursive Delete | `rm -rf dir` | `Remove-Item -Recurse -Force dir` |
| Create File | `touch file` | `New-Item -ItemType File -Force file` |
| Make Dir | `mkdir -p dir` | `New-Item -ItemType Directory -Force dir` |
| Search String | `grep "text" file` | `Select-String "text" file` |
| Copy | `cp -r src dest` | `Copy-Item -Recurse src dest` |
| Cat/Read | `cat file` | `Get-Content file` |
| Process Kill | `kill -9 <PID>` | `Stop-Process -Id <PID> -Force` |

### ❌ DO NOT USE
- `&&` for command chaining → Use `;` instead
- `npm run dev &` (Background) → Not supported natively, use separate terminal
- `sudo` → Use `gsudo` or run as Administrator

> [!IMPORTANT]
> PowerShell does NOT support `&&` or `||` operators for command chaining like Bash.
> Always use `;` to chain commands, or use separate command calls.

---

## File Encoding Fix Rules

> If file edit tools fail with "target content not found", likely encoding issue.

```powershell
$content = Get-Content "path/to/file.md" -Raw -Encoding UTF8
[System.IO.File]::WriteAllText("path/to/file.md", $content, [System.Text.Encoding]::UTF8)
```

> [!CAUTION]
> **NEVER use PowerShell to edit files containing emoji or special Unicode!**
> - PowerShell's `[System.IO.File]::WriteAllText()` corrupts 4-byte UTF-8 characters (emojis)
> - Result: `📊` becomes `ðŸ"Š` (mojibake)
> - **Use Node.js or file edit tools instead** for files with emoji content
> - If corruption occurs: manually Find & Replace in VSCode or restore from git

---

## Mermaid Diagram Convention

> [!IMPORTANT]
> Use PLAIN backticks for mermaid code blocks, NOT escaped backticks.
