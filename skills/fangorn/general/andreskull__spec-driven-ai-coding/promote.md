# Promote Command

Promote a project-specific rule to the global `~/.ai_global` library. This allows sharing valuable project-specific rules across all projects.

## Purpose

When a project-specific rule proves valuable and should be shared across all projects, use this command to promote it to the global library. **IMPORTANT:** Only promote rules that contain generalizable patterns, not product-specific details.

## Workflow

1. **Identify Project-Specific Rules**
   - Scans `.cursor/rules/` or `.agent/rules/` directories
   - Identifies rules NOT in `global/` symlink
   - Lists available rules for promotion

2. **Select Rule to Promote**
   - Prompts user to select which rule to promote
   - Shows rule content for review

3. **🔒 Product-Specific Content Detection (SAFEGUARD)**
   
   **Automatically scan for product-specific content:**
   - **Project names** (e.g., "my-project", "product-name", specific product names)
   - **Specific URLs** (e.g., project-specific API endpoints, internal URLs)
   - **Resource identifiers** (e.g., database names, storage buckets, dataset names)
   - **Environment-specific configs** (e.g., staging/prod buckets, project IDs)
   - **Hardcoded paths** (e.g., `/Users/username/project-name/...`)
   - **Product-specific features** (e.g., feature names specific to one product)
   
   **If product-specific content is detected:**
   - ⚠️ **WARN** the user about detected product-specific content
   - List all detected product-specific elements
   - **REQUIRE** manual review and editing before promotion
   - Suggest extracting generalizable patterns instead
   - Offer to help create a generalized version

4. **Manual Review & Editing (REQUIRED if product-specific content found)**
   - User must review and edit the rule to remove product-specific content
   - Extract generalizable patterns, principles, or workflows
   - Replace specific examples with generic placeholders
   - Ensure rule is applicable to any project using the same framework/pattern
   - **DO NOT PROCEED** until product-specific content is removed or generalized

5. **Confirm Promotion**
   - Show cleaned/generalized rule content
   - Confirm this is appropriate for global sharing
   - User must explicitly confirm

6. **Move to Global Library**
   - Copies cleaned rule file to `~/.ai_global/rules/`
   - Ensures proper naming convention (remove project-specific prefixes)
   - Preserves generalizable content and structure
   - Adds comment noting it was promoted from a project-specific rule

7. **Update Symlinks**
   - Re-runs bootstrap linker to update symlinks
   - Ensures rule is available in all projects
   - Updates both Cursor and Antigravity symlinks

8. **Handle Local Copy**
   - Option 1: Remove local copy (rule now comes from global)
   - Option 2: Keep as override (project-specific version takes precedence)
   - User chooses based on needs

9. **Update Documentation**
   - Updates relevant documentation if needed
   - Notes rule promotion in changelog
   - Documents rule purpose and usage

## Use Cases

- A project-specific coding standard that should apply everywhere
- A useful workflow pattern discovered in one project
- A best practice rule that benefits all projects
- A framework-specific rule that's missing from global library

## ❌ Do NOT Promote

- Rules with product-specific names, URLs, or resources
- Rules with hardcoded project paths or identifiers
- Rules describing specific product features or data
- Rules that only make sense in the context of one project

## ✅ What TO Promote

- General coding standards and best practices
- Framework-specific patterns (e.g., Dagster best practices, Next.js patterns)
- Reusable workflow patterns
- Generic architectural principles
- Technology-specific guidelines (without product-specific details)

## Safety

- **Product-specific content detection** (automatic scanning)
- **Manual review required** if product-specific content found
- Shows rule content before promoting
- Asks for confirmation before moving files
- Creates backup of original rule
- Allows rollback if needed
- Prevents accidental promotion of product-specific rules

## Integration

- Works with bootstrap script for symlink updates
- Integrates with global rule system
- Maintains backward compatibility
- Updates both Cursor and Antigravity configurations
