# Markdown Standards

> **Purpose**: Ensure consistent and compatible markdown formatting across plans, walkthroughs, and documentation.

## 📸 Image Syntax

### ✅ CORRECT Format (Tauri Compatible)

When embedding images in markdown files (plans, walkthroughs, task descriptions):

**Use absolute paths with `file:///` protocol (3 slashes):**

```markdown
![Description](file:///C:/Users/username/path/to/image.png)
```

**Platform-Specific Examples:**

```markdown
# Windows (CORRECT)
![Header Layout](file:///C:/Users/andyvand/.gemini/antigravity/brain/.../screenshot.png)

# Unix/Linux (CORRECT)
![Diagram](/home/user/projects/flowcrate/docs/diagram.png)

# macOS (CORRECT)
![UI Mockup](/Users/username/Documents/mockup.png)
```

### ❌ INCORRECT Formats

```markdown
# ❌ Relative paths - breaks when viewing from different locations
![Image](../../images/screenshot.png)
![Image](./diagram.png)

# ❌ HTTP URLs without protocol
![Image](C:\Users\andyvand\image.png)

# ❌ Backslashes (Windows) - causes rendering issues
![Image](file:///C:\Users\andyvand\image.png)

# ❌ Missing file:// protocol for local files
![Image](C:/Users/andyvand/image.png)
```

## 🛠️ Technical Implementation

### How FlowCrate Renders Local Images

1. **Markdown Parser** (`MarkdownViewer.tsx`) detects `file://` protocol
2. **Path Normalizer** strips protocol and converts to platform-specific absolute path:
   - `file:///C:/path/image.png` → `C:/path/image.png` (Windows)
   - `file:///path/to/image.png` → `/path/to/image.png` (Unix)
3. **Tauri Converter** (`convertFileSrc()`) transforms to asset protocol:
   - `C:/path/image.png` → `https://asset.localhost/C:/path/image.png`
4. **Browser** loads image via Tauri's secure asset protocol

### Content Security Policy (CSP)

Images work because `tauri.conf.json` includes:

```json
{
  "app": {
    "security": {
      "csp": "img-src 'self' asset: http://asset.localhost https://asset.localhost data: blob:",
      "assetProtocol": {
        "enable": true,
        "scope": ["**"]
      }
    }
  }
}
```

## 📝 Best Practices

### When Creating Plans/Walkthroughs

1. **Use Antigravity's uploaded media paths** (auto-generated with correct format):
   ```markdown
   ![Screenshot](file:///C:/Users/username/.gemini/antigravity/brain/<conversation-id>/uploaded_media_xxx.png)
   ```

2. **For project assets**, use absolute paths:
   ```markdown
   ![Architecture](file:///C:/Users/username/Dev/flowcrate-desktop/docs/architecture.png)
   ```

3. **Add descriptive alt text** for accessibility:
   ```markdown
   ![Header layout showing Settings icon in right area, NOT as navigation tab](file:///...)
   ```

### Image Organization

```
project/
├── .flowcrate/
│   ├── plans/
│   │   └── PLAN_FEAT_XXX_NAME.md        # Contains images
│   └── walkthroughs/
│       └── WLKTH_FEAT_XXX_NAME.md       # Contains screenshots
└── docs/
    └── diagrams/                        # Reusable diagrams
        └── architecture.png
```

## 🚨 Troubleshooting

### Images Not Rendering?

1. **Check console logs** (F12 → Console):
   ```
   [MarkdownViewer] Normalizing image path: { original: "file:///...", normalized: "C:/...", isWindows: true }
   [MarkdownViewer] Converted to asset URL: "https://asset.localhost/..."
   ```

2. **Verify path format**:
   - Must start with `file:///` (3 slashes)
   - Must use forward slashes `/` (not backslashes `\`)
   - Must be absolute path (no `../../` relative paths)

3. **Check CSP configuration** in `tauri.conf.json`:
   - `assetProtocol.enable: true`
   - `img-src` includes `asset: http://asset.localhost`

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Broken image icon | Relative path | Use absolute `file:///` path |
| No image at all | Missing CSP | Add asset protocol to CSP |
| isWindows: false on Windows | Path missing drive letter | Ensure format: `file:///C:/` |
| %2F in asset URL | Wrong platform detection | Hard refresh browser (Ctrl+Shift+R) |

## 📚 Related Files

- `src-ui/components/MarkdownViewer.tsx` - Image renderer implementation
- `src-tauri/tauri.conf.json` - CSP and asset protocol config
- `bug-85e7` - Fixed markdown image rendering (commit 2cb82d4)

---

**Reference**: Based on fix for `bug-85e7` - Markdown images not rendering in plan editor preview
