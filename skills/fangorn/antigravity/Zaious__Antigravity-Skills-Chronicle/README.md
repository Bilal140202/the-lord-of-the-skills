<div align="center">

# 🌌 Antigravity: Skills Chronicle

**The premium management layer for AI Skills, powered by the ChronicleCore system.**

[![VS Code](https://img.shields.io/badge/VS%20Code-Extension-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=ChronicleCore.antigravity-skills-chronicle)
[![License: SEE LICENSE](https://img.shields.io/badge/License-SEE%20README-red.svg?style=for-the-badge)](LICENSE)
[![Brand](https://img.shields.io/badge/Brand-ChronicleCore-B91C1C?style=for-the-badge)](https://buymeacoffee.com/zaious)

---

*Manage your AI Skills, Workflows, and Rules with a premium visual dashboard.*

</div>

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🛠️ **Skills Dashboard** | View and manage all skills in your `.agent/skills/` directory |
| 📜 **Workflow Manager** | Organize and execute workflows from `.agent/workflows/` |
| 📋 **Rules Inspector** | View and edit agent rules |
| 💬 **Conversation Archive** | Browse and search past Claude conversations |
| 📍 **Dynamic Status Bar** | Real-time skill and workflow count in the status bar |

---

## 📊 Status Bar & Sidebar Integration

![Status Bar](https://raw.githubusercontent.com/Zaious/Antigravity-Skills-Chronicle/main/public-assets/introduce/status-bar.png)
![Sidebar Menu](https://raw.githubusercontent.com/Zaious/Antigravity-Skills-Chronicle/main/public-assets/introduce/sidebar-menu.png)

The extension provides a **real-time status bar** showing your current asset counts and a newly integrated **Activity Bar (Sidebar)**:
- **Status Bar**: Total AI skill definitions, Workflows, and Rules
- **Sidebar Commands**: Forge New Skill, Batch Export History
- **Assets Navigator**: Dynamic tree view of your `.agent/` directory

---

## 🖥️ Terminal Dashboard & Global Config

![Dashboard View](https://raw.githubusercontent.com/Zaious/Antigravity-Skills-Chronicle/main/public-assets/introduce/dashboard-full.png)
![Config View](https://raw.githubusercontent.com/Zaious/Antigravity-Skills-Chronicle/main/public-assets/introduce/config-panel.png)

The **Terminal View** is your command center for V2.0.0:

| Section | Description |
|---------|-------------|
| **Skills / Workflows / Rules** | Quick count overview at a glance |
| **LSP Status Monitor** | Connection status of your Language Server Protocol |
| **Global Path Configuration** | Dynamically switch between `.gemini/antigravity` core and local workspace |

---

## 📁 Asset Management & Discovery

![Skill Listing](https://raw.githubusercontent.com/Zaious/Antigravity-Skills-Chronicle/main/public-assets/introduce/dashboard-skills.png)
![Skill Hub](https://raw.githubusercontent.com/Zaious/Antigravity-Skills-Chronicle/main/public-assets/introduce/skill-hub.png)

Explore the internal structure of any skill or discover new ones:
- **Local Assets**: Navigate physical assets directly with markdown previews
- **Skill Hub**: Official library synced from the A1 Sentinel Framework to browse and download official templates

---

## ⚙️ Skill Detail: Configuration & Files

![Skill Config](https://raw.githubusercontent.com/Zaious/Antigravity-Skills-Chronicle/main/public-assets/introduce/skill-detail-config-2.png)
![Skill Files](https://raw.githubusercontent.com/Zaious/Antigravity-Skills-Chronicle/main/public-assets/introduce/skill-detail-files-2.png)

The updated Detail View displays the parsed Chronicle Node Schema:
- **Vibe Stats**: Endurance, Accuracy, Creativity, Aggression
- **Attributes & Identity**: Nickname, archetypes, and origin
- **File Tree Navigator**: Access embedded source codes and workflows

---

## 📝 Activity Monitor & Operations

![Activity Overview](https://raw.githubusercontent.com/Zaious/Antigravity-Skills-Chronicle/main/public-assets/introduce/dashboard-activity.png)
![Activity Monitor](https://raw.githubusercontent.com/Zaious/Antigravity-Skills-Chronicle/main/public-assets/introduce/activity-monitor.png)

Track the heartbeat of the system:
- **Conversation Logs**: Documenting visual realignments and stability
- **Activity Monitor Engine**: Engagement and context length tracking over the last 12 hours
- **Memo Engine**: Attach context, ideas, or reminders to any entity

---

## 🌌 Connectivity Map & Governance (V2.0.0)

![Connect Map](https://raw.githubusercontent.com/Zaious/Antigravity-Skills-Chronicle/main/public-assets/introduce/connect-map.png)
![Manual Overview](https://raw.githubusercontent.com/Zaious/Antigravity-Skills-Chronicle/main/public-assets/introduce/manual-overview.png)

The **Chronicle Manual** hub outlines V2.0.0 advancements:
1. **Deep Search**: Full-text indexing and incremental cache search for historical records.
2. **Star Map**: Force-directed topology for complex knowledge networks and visual analysis.
3. **Asset Governance**: Physical state persistence and batch export capabilities.

### 🌟 Golden Era Support

Become a **Golden Supporter** to fuel the evolution of the ChronicleCore ecosystem:
- Exclusive **Midnight Gold UI** theme
- **Supporter Badge** in your dashboard
- Unlock future premium features

---

## 🚀 Quick Start

1. **Install the Extension**: Search for `Antigravity: Skills Chronicle` in VS Code Extensions, or install from the Marketplace.
2. **Open the Dashboard**: Click the 📜 icon in the Activity Bar, or use the command palette (`Ctrl+Shift+P` → `Antigravity: Skills Chronicle`).
3. **Add Sample Skills**: Download official sample skills from our [Skills Repository](https://github.com/Zaious/Antigravity-Skills-Chronicle):

```bash
# English
mkdir -p .agent/skills/illustrator && curl -o .agent/skills/illustrator/Skill.md https://raw.githubusercontent.com/Zaious/Antigravity-Skills-Chronicle/main/skills/illustrator/en/Skill.md

# 繁體中文
mkdir -p .agent/skills/illustrator && curl -o .agent/skills/illustrator/Skill.md https://raw.githubusercontent.com/Zaious/Antigravity-Skills-Chronicle/main/skills/illustrator/zh-TW/Skill.md
```

## 📂 Skill Asset Customization

Each skill can display custom visual branding inside the Antigravity Dashboard:

| Asset | Recommended Size | File Path |
|-------|------------------|---------------------|
| **Avatar** | 128×128 px (1:1) | `{skill}/assets/avatar.png` |
| **Cover** | 1280×720 px (16:9) | `{skill}/assets/cover.png` |

> 💡 **Tip**: You can also upload assets directly via the Dashboard by hovering over the Avatar or Cover area in the Skill detail view.

## 🏗️ Directory Structure

The extension monitors the following directories:

```
your-project/
├── .agent/
│   ├── skills/         # Your AI skill definitions
│   ├── workflows/      # Step-by-step procedures
│   └── rules/          # Agent behavior rules
└── .gemini/
    └── conversations/  # Claude conversation archives
```

## 🌍 Global Path Configuration

You can configure global asset paths in the **Terminal Dashboard**.

**Default Global Paths:**
- Skills: `~/.gemini/antigravity/global_skills`
- Workflows: `~/.gemini/antigravity/global_workflows`
- Rules: `~/.gemini/antigravity/rules`

> **Note**: Antigravity official is continuously adjusting the global path structure. Please check the dashboard for the latest configuration options.

## 📜 License

MIT License for community skill templates.  
The core **Antigravity** engine is proprietary.

## 🙏 Acknowledgments

This project includes components from [skills-cli](https://github.com/kcchien/skills-cli) by KC Chien, used under the MIT License. See [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md) for details.

---

<p align="center">Crafted by <b>Zaious</b> · Powered by <b>ChronicleCore / 編年史記工作室</b></p>
