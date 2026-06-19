---
name: analyze
description: name: analyze
---
# Analyze

Comprehensive code analysis across quality, security, performance, and architecture.

## Analysis Domains

### Quality
- Code smells, duplication, complexity
- Maintainability index
- Dead code and unused imports
- Naming conventions and consistency

### Security
Load security-review skill for the full OWASP checklist.

### Performance
Load performance-optimization skill — measure before analyzing.

### Architecture
Load architecture-design skill for structural analysis.

## Usage
Specify focus: `/analyze --focus quality|security|performance|architecture`
Or run all domains for a comprehensive report.

## Output Format
For each finding:
1. **Domain** (quality/security/performance/architecture)
2. **Severity** (critical/high/medium/low/info)
3. **Location** (file:line)
4. **Issue** (what's wrong)
5. **Recommendation** (specific fix)

## After Analysis
- Critical/High: fix before proceeding
- Medium: create task to address
- Low/Info: document for future improvement
