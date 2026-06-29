---
description: Synchronize version numbers across the entire project
---

# Version Synchronization Workflow

This workflow updates the version number in all project files (`package.json`, `pyproject.toml`, source code, etc.) to ensure consistency.

## Prerequisites
- Python 3 installed and in PATH
- Node.js / NPM installed

## Steps

1.  **Determine New Version**
    - Decide on the new version number (e.g., `1.2.6`).

2.  **Run Sync Script**
    - Execute the synchronization script with the new version number.
    ```powershell
    python scripts/sync_version.py <NEW_VERSION>
    ```

3.  **Update Lockfiles**
    - Run npm install to synchronize `package-lock.json` with the new version in `package.json`.
    ```powershell
    npm install
    cd web
    npm install
    cd ..
    ```

4.  **Verify & Commit**
    - Check the diffs to ensure only version numbers were changed.
    - Commit the changes.
    ```powershell
    git add .
    git commit -m "chore: bump version to <NEW_VERSION>"
    ```
