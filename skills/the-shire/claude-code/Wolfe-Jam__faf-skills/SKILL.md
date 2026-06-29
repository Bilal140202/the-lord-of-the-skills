---
name: faf-format-inspector
description: Validate both YAML frontmatter formats (SKILL.md for Claude Code) and IANA-registered project.faf formats. Use when user asks "validate my skill", "check YAML format", "is my SKILL.md correct", or needs to verify format compliance for either Claude Code skills or project.faf files.
allowed-tools: Read, Bash, Grep
---

# FAF Format Validator - Dual YAML Format Validation

## Purpose

Validate two distinct YAML formats in the FAF ecosystem:
1. **SKILL.md** - YAML frontmatter for Claude Code skills
2. **project.faf** - IANA-registered format for project DNA

**The Goal:** Ensure both tooling (Skills) and infrastructure (project.faf) maintain format integrity.

## When to Use

This skill activates when the user:
- Asks "Validate my skill format"
- Says "Check my SKILL.md"
- Asks "Is my project.faf valid?"
- Says "Verify YAML formats"
- Needs to compare SKILL.md vs project.faf format
- Creates new skills and wants validation

**Trigger Words:** validate, check format, SKILL.md, project.faf, YAML, frontmatter, format compliance

## The Two Formats

### Format 1: SKILL.md (Claude Code Skills)

**Purpose:** Configure Claude Code skill activation

**Required Structure:**
```yaml
---
name: skill-name
description: One-sentence description with trigger words
allowed-tools: Tool1, Tool2, Tool3
---

# Skill Title

## Purpose
...
```

**Required Fields:**
- `name` - Skill identifier (kebab-case)
- `description` - Comprehensive description with trigger phrases
- `allowed-tools` - List of tools the skill can use

**Optional Fields:**
- `version` - Skill version (semantic)
- `author` - Skill creator

**Validation Checks:**
1. ✅ YAML frontmatter delimited by `---`
2. ✅ `name` field present (lowercase, kebab-case)
3. ✅ `description` field present (100+ characters recommended)
4. ✅ `allowed-tools` field present
5. ✅ Markdown content follows frontmatter
6. ✅ Content has clear sections (Purpose, When to Use, etc.)

---

### Format 2: project.faf (IANA-Registered)

**Purpose:** Universal project DNA for ANY AI

**Required Structure:**
```yaml
format:
  name: FAF
  version: 3.0.0
  iana_media_type: application/vnd.faf+yaml

project:
  name: Project Name
  version: 1.0.0

architecture:
  type: web-app
  stack: []
```

**Required Fields:**
- `format.name` - Must be "FAF"
- `format.version` - Must be "3.0.0" or higher
- `format.iana_media_type` - Must be "application/vnd.faf+yaml"
- `project.name` - Project name
- `architecture.type` - Architecture type

**Validation Checks:**
1. ✅ Valid YAML syntax
2. ✅ Format version 3.0.0+
3. ✅ IANA media type present
4. ✅ Required top-level sections
5. ✅ Architecture defined
6. ✅ No SKILL.md frontmatter mixed in

---

## How It Works

### Step 1: Detect Format Type

**Auto-detection logic:**

```bash
# Check if SKILL.md (frontmatter)
if file contains "---" at line 1 AND markdown content:
  → Validate as SKILL.md format

# Check if project.faf (IANA)
if file has .faf extension OR contains "iana_media_type":
  → Validate as project.faf format

# Check if both (ERROR)
if file has both frontmatter AND iana_media_type:
  → ERROR: Mixed formats detected
```

### Step 2: Validate SKILL.md Format

**Validation workflow:**

1. **Read file**
```bash
cat skills/faf-teacher/SKILL.md
```

2. **Check YAML frontmatter**
```yaml
# Must start with ---
# Must have name, description, allowed-tools
# Must end with ---
```

3. **Validate fields**
- Name: lowercase, kebab-case, no spaces
- Description: 50+ characters, includes trigger words
- Tools: Valid Claude Code tools only

4. **Check markdown content**
- Purpose section exists
- "When to Use" section exists
- Examples provided

5. **Report results**
```
✅ SKILL.md Format Valid

Name: faf-teacher
Description: 150 characters (✅ comprehensive)
Tools: Read, WebFetch (✅ valid)
Sections: 8 found (✅ complete)
```

### Step 3: Validate project.faf Format

**Validation workflow:**

1. **Use faf-cli validation**
```bash
faf validate
```

2. **Check IANA compliance**
```yaml
format:
  iana_media_type: application/vnd.faf+yaml  # Required
```

3. **Verify version**
```yaml
format:
  version: 3.0.0  # Must be 3.0.0+
```

4. **Check required sections**
- format (✅)
- project (✅)
- architecture (✅)

5. **Calculate score**
```bash
faf score
```

6. **Report results**
```
✅ project.faf Format Valid

Version: 3.0.0 (✅ current)
IANA Media Type: application/vnd.faf+yaml (✅ registered)
Score: 72% (🥇 Gold tier)
Required Fields: 10/10 present
```

### Step 4: Detect Format Conflicts

**Common errors:**

**ERROR 1: Mixed formats**
```yaml
---
name: my-project  # ❌ SKILL.md frontmatter
description: test
---

format:  # ❌ project.faf structure
  iana_media_type: application/vnd.faf+yaml
```

**Solution:** Choose one format - either SKILL.md OR project.faf

**ERROR 2: Wrong extension**
```
project.md  # ❌ Should be project.faf
SKILL.faf   # ❌ Should be SKILL.md
```

**Solution:** Use correct file extension

**ERROR 3: Missing IANA registration**
```yaml
# project.faf without iana_media_type
format:
  name: FAF
  version: 3.0.0
  # ❌ Missing iana_media_type
```

**Solution:** Run `faf migrate` to upgrade

---

## Validation Matrix

### SKILL.md Validation

| Check | Required | Common Issues |
|-------|----------|---------------|
| **YAML frontmatter** | ✅ Yes | Forgot closing `---` |
| **name field** | ✅ Yes | CamelCase instead of kebab-case |
| **description field** | ✅ Yes | Too short (<50 chars) |
| **allowed-tools** | ✅ Yes | Invalid tool names |
| **Markdown content** | ✅ Yes | No sections after frontmatter |
| **Purpose section** | ⚠️ Recommended | Missing purpose statement |
| **Examples** | ⚠️ Recommended | No usage examples |

### project.faf Validation

| Check | Required | Common Issues |
|-------|----------|---------------|
| **Valid YAML** | ✅ Yes | Syntax errors, tabs vs spaces |
| **format.version** | ✅ Yes | Old version (v2.x, v1.x) |
| **iana_media_type** | ✅ Yes | Missing or incorrect |
| **project section** | ✅ Yes | Empty or missing |
| **architecture** | ✅ Yes | Undefined architecture type |
| **Podium score** | ⚠️ Quality | Low score (<40%) |

---

## Examples

### Example 1: Validate SKILL.md

**User:** "Check if my faf-teacher skill is valid"

**Skill Activates:**

1. Read file: `skills/faf-teacher/SKILL.md`
2. Parse YAML frontmatter
3. Validate fields:
   ```
   ✅ name: faf-teacher (valid)
   ✅ description: 150 chars (comprehensive)
   ✅ allowed-tools: Read, WebFetch (valid)
   ```
4. Check markdown content:
   ```
   ✅ Purpose section found
   ✅ "When to Use" section found
   ✅ 5 examples provided
   ```

**Result:**
```
✅ SKILL.md Format Valid

Skill: faf-teacher
Quality: Championship grade
Sections: 8/8 required sections
Trigger words: 12 identified
```

### Example 2: Validate project.faf

**User:** "Is my project.faf valid?"

**Skill Activates:**

1. Run `faf validate`
2. Check output:
   ```bash
   ✅ Valid YAML syntax
   ✅ Format version: 3.0.0
   ✅ IANA media type: application/vnd.faf+yaml
   ✅ All required fields present
   ```
3. Run `faf score`
4. Show results:
   ```
   Score: 68% (🥈 Silver tier)

   Missing:
   - Testing documentation
   - API documentation
   ```

**Result:**
```
✅ project.faf Valid (Silver tier)

Next: Run `faf enhance` to reach Gold (70%+)
```

### Example 3: Detect Mixed Format

**User:** "Why isn't this working?"

**File content:**
```yaml
---
name: my-project
---

format:
  iana_media_type: application/vnd.faf+yaml
```

**Skill Activates:**

1. Detects YAML frontmatter (`---`)
2. Detects IANA format (`iana_media_type`)
3. **ERROR: Mixed formats**

**Result:**
```
❌ Format Conflict Detected

You're mixing two different YAML formats:
- SKILL.md (frontmatter) - For Claude Code skills
- project.faf (IANA) - For project DNA

Choose one:

Option 1 - Creating a skill?
→ Use SKILL.md format
→ File: skills/skill-name/SKILL.md

Option 2 - Describing project?
→ Use project.faf format
→ File: project.faf
→ Run: faf init
```

---

## Format Comparison Guide

### When to Use SKILL.md

**Use SKILL.md when:**
- Creating Claude Code skills
- Adding to `~/.config/claude-code/skills/`
- Configuring skill activation
- Writing instructions for Claude

**Structure:**
```
YAML frontmatter (metadata)
+
Markdown content (instructions)
```

**Extension:** `.md`

### When to Use project.faf

**Use project.faf when:**
- Describing project architecture
- Making project AI-readable
- Creating persistent context
- Supporting ANY AI tool

**Structure:**
```
Pure YAML (structured data)
No markdown
```

**Extension:** `.faf`

---

## Validation Commands

### For SKILL.md

```bash
# Manual validation
cat skills/faf-teacher/SKILL.md | head -10

# Check frontmatter
grep -A 5 "^---$" skills/faf-teacher/SKILL.md | head -6

# Verify tools
grep "allowed-tools:" skills/faf-teacher/SKILL.md
```

### For project.faf

```bash
# faf-cli validation (recommended)
faf validate

# Manual YAML check
cat project.faf | head -20

# Check IANA registration
grep "iana_media_type" project.faf

# Get score
faf score
```

---

## Common Mistakes

### Mistake 1: Using project.faf as SKILL.md

**Wrong:**
```
skills/faf-teacher/project.faf  # ❌ Wrong format
```

**Right:**
```
skills/faf-teacher/SKILL.md     # ✅ Correct
```

### Mistake 2: Using SKILL.md as project.faf

**Wrong:**
```yaml
# In repository root: SKILL.md
---
name: my-project  # ❌ This is not a skill
---
```

**Right:**
```yaml
# In repository root: project.faf
format:
  iana_media_type: application/vnd.faf+yaml  # ✅ Correct
```

### Mistake 3: Mixing formats

**Wrong:**
```yaml
---
format:  # ❌ Can't mix frontmatter + IANA
  iana_media_type: application/vnd.faf+yaml
---
```

**Right:** Pick one format, use it correctly

---

## Troubleshooting

### Issue: "Invalid YAML frontmatter"

**Symptom:** Skill won't load in Claude Code

**Check:**
```bash
# Must start with ---
head -1 skills/skill-name/SKILL.md

# Must have closing ---
grep -n "^---$" skills/skill-name/SKILL.md
```

**Fix:** Ensure frontmatter is properly delimited

### Issue: "project.faf not recognized"

**Symptom:** AI doesn't understand project

**Check:**
```bash
faf validate
```

**Fix:** Ensure IANA media type present:
```yaml
format:
  iana_media_type: application/vnd.faf+yaml
```

### Issue: "Mixed format error"

**Symptom:** File has both frontmatter and IANA format

**Fix:** Separate into two files:
1. SKILL.md (if creating a skill)
2. project.faf (if describing project)

---

## Related Skills

- **faf-validate** - Validates project.faf only (IANA format)
- **faf-migrate** - Upgrades old project.faf versions
- **faf-init** - Creates new project.faf files
- **faf-teacher** - Explains format differences

---

## Key Principles

### 1. Two Formats, Two Purposes

**SKILL.md:**
- Tooling (how to build FAF files)
- Claude Code specific
- Frontmatter + Markdown

**project.faf:**
- Infrastructure (the project itself)
- Universal AI compatibility
- Pure YAML

### 2. Don't Mix Them

Each format serves a distinct role:
- Skills help CREATE project.faf
- project.faf contains PROJECT data
- Never combine them

### 3. Validate Early, Validate Often

**For Skills:**
- Check before installing
- Verify after editing
- Test activation

**For project.faf:**
- Validate after creation (`faf validate`)
- Score after enhancement (`faf score`)
- Migrate when needed (`faf migrate`)

---

## Success Metrics

**SKILL.md Validation:**
- ✅ All required fields present
- ✅ Description comprehensive (100+ chars)
- ✅ Valid Claude Code tools only
- ✅ Clear markdown structure

**project.faf Validation:**
- ✅ IANA media type present
- ✅ Version 3.0.0+
- ✅ All required sections
- ✅ Score 40%+ (Bronze minimum)

---

**Generated by FAF Skill: faf-format-validator v1.0.0**
**"Two formats. Two purposes. One ecosystem. Validate both."**
