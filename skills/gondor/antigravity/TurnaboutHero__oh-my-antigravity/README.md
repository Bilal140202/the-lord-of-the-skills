# Oh My Antigravity - VS Code Extension

This is the official VS Code extension for **Oh My Antigravity (OMA)**.

## Features

### 📦 Plugin Manager GUI
- Beautiful visual interface for managing plugins
- Install/Remove plugins with one click
- Switch between Global and Project scope
- Real-time status updates

### 🎯 Sidebar Integration
- Dedicated OMA sidebar in Activity Bar
- Quick access to:
  - **Plugins**: Browse and install skills
  - **Commands**: View available slash commands
  - **Themes**: Manage agent personas

### ⚡ Command Palette
- `OMA: Open Plugin Manager` - Launch the GUI
- `OMA: Refresh Plugins` - Update plugin list

## Installation

### From VSIX (Recommended)
1. Download `oh-my-antigravity-1.0.0.vsix`
2. Open VS Code/Antigravity
3. Go to Extensions (Ctrl+Shift+X)
4. Click `...` → `Install from VSIX...`
5. Select the downloaded file

### From Source
```bash
cd extension
npm install
code .
# Press F5 to launch Extension Development Host
```

## Usage

### Opening the Plugin Manager
1. Click the OMA icon in the Activity Bar (left sidebar)
2. Or use Command Palette: `Ctrl+Shift+P` → "OMA: Open Plugin Manager"

### Installing a Plugin
1. Open Plugin Manager
2. Browse available plugins
3. Click **Install** button
4. Choose Global or Project scope
5. Done! The plugin is now active in Antigravity

### Managing Plugins
- **Global Install**: Available across all projects (`~/.gemini/antigravity/skills/`)
- **Project Install**: Only for current workspace (`.agent/skills/`)

## Screenshots

### Plugin Manager
Beautiful card-based interface showing all available plugins with descriptions and version numbers.

### Sidebar View
Quick access tree view fo all plugins, commands, and themes.

## Requirements

- Oh My Antigravity framework installed
- VS Code 1.80.0 or higher
- (Antigravity IDE compatible)

## Extension Settings

This extension contributes the following settings:

* `oma.autoRefresh`: Automatically refresh plugin list on startup
* `oma.defaultScope`: Default installation scope ('global' or 'project')

## Known Issues

None at this time. Please report issues on GitHub.

## Release Notes

### 1.0.0
- Initial release
- Plugin Manager GUI
- Sidebar integration
- Install/Remove functionality
- Scope management

---

**Enjoy using Oh My Antigravity!** 🚀
