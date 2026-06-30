# OpenClaw V3: macOS Golden Gate Ecosystem (2026) - Project Blueprint

## 🌌 Project Vision & Philosophy
**macOS Golden Gate (v26.0)** is a high-fidelity web-based OS simulation representing the "Unit 7" era of Apple computing. It is built as a React SPA that bridges the gap between legacy desktop metaphors and futuristic "Frozen Prompt" architectures.

- **Aesthetic:** "Silicon-Native Liquid Glass" (Glassmorphism + 50px blur + 190% saturation + 120fps Framer Motion physics).
- **Architecture:** Modular component architecture with a centralized `SystemContext` state machine and a persistent `FileSystemContext` virtual drive.
- **Hardware Simulation:** Real-time integration with Battery Status API, Performance Memory API (heap size), and Storage Estimation API.

---

## 🏗️ Technical Stack
- **Framework:** React 18 + Vite (TypeScript)
- **Styling:** Tailwind CSS 4 (Custom utilities for glassmorphism)
- **Animations:** Framer Motion (Transitions, Physics, True-Magnification Dock, Genie Effect)
- **Icons:** HugeIcons + Lucide React + Custom SVG paths for brand icons (Apple, Finder)
- **Persistence:** LocalStorage keys: `golden_gate_v27_state` (System) and `golden_gate_v27_fs` (Filesystem).

---

## 📂 Directory Structure (Architecture Map)
- `src/components/desktop/`: OS Shell components (MenuBar, Dock, ControlCenter, Window).
- `src/components/apps/`: Individual application modules (Finder, Safari, SystemSettings, etc.).
- `src/components/`: OS Lifecycle components (BootSequence, SetupAssistant, LoginScreen, Recovery).
- `src/contexts/`: 
    - `SystemContext.tsx`: Main OS state machine (boot state, active apps, hardware simulation).
    - `FileSystemContext.tsx`: Virtual File System (VFS) with persistent node management.
- `src/hooks/`: System-wide hooks for dynamic wallpapers, software updates, and telemetry.
- `src/utils/`: AI Engine integration and system utilities.

---

## ⚙️ Core System Logic

### 1. System Lifecycle & Routing (`App.tsx` & `BootSequence.tsx`)
- **Boot Flow:** `BootSequence` (432Hz sine chime) -> `SetupAssistant` (if `!setup_complete`) -> `LoginScreen` -> `Desktop`.
- **Recovery Mode:** Triggered via `resetSystem()` or system failure states.
- **Persistence:** State is synchronized to `localStorage` under `golden_gate_v27_state`.

### 2. Virtual File System (`FileSystemContext.tsx`)
- **Nodes:** Files and folders with unique IDs, parent relationships, metadata (tags, locked status), and optional content.
- **macOS Logic:** Deletion moves nodes to the `trash` folder; `emptyTrash` recursively purges child nodes.
- **Self-Heal:** Ensures critical system nodes (root, apps, users) are restored if missing.

### 3. Window Management (`Window.tsx`)
- **Active State:** Z-index and focus managed via `activeApp` in `SystemContext`.
- **Interactions:** Support for minimize, maximize (toggle), and close.

### 4. Hardware & Environment Integration
- **Battery & Power:** Tracks hardware battery level and adapts "Power Mode" (Low Power, Normal, High Performance).
- **Dynamic Appearance:** Supports Light, Dark, and Auto modes (system preference sync).
- **Notch:** Simulated hardware notch with active camera indicator.

---

## 🛠️ Development Workflow
- **Start Dev Server:** `npm run dev`
- **Build Project:** `npm run build` (runs `tsc` and `vite build`)
- **Linting:** `npm run lint`
- **Preview Build:** `npm run preview`

---

## 📜 Development Conventions
- **Naming:** PascalCase for components, camelCase for props and hooks.
- **Animation First:** All UI interactions must use Framer Motion for the "Liquid Glass" aesthetic.
- **Z-Index Map:**
  - Wallpaper: Background
  - Desktop Grid: 0
  - Windows: 10-50
  - Dock/MenuBar: 40
  - Spotlight/Modals: 100+
- **Persistence:** Any changes to `SystemContext` or `FileSystemContext` must be reflected in `localStorage` for state persistence across reloads.
